import os
import codecs
import struct
from collections import defaultdict
from copy import deepcopy
import logging.config

from .utils.struct import pack, unpack
from .pdfparser import PDFParser
from .exception import PDFParserDoneException, PDFCMapNotFoundException
from .pdfobject import PDFKeyWord, PDFName
from .encoding import glyph_name_to_unicode


from .config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()


class PDFCmap(object):
    def __init__(self, attrs=None):
        self.attrs = attrs or {}
        self.code_cid = {}
        self.cid_unicode = {}

    def is_vertical(self):
        return self.attrs.get(b'WMode', 0) != 0

    def set_attr(self, k, v):
        self.attrs[k] = v
        if k == b'CMapName':
            cmap_manager.set_cmap(v.value, self)

    def use_cmap(self, cmap_name):
        cmap = cmap_manager.get_cmap(cmap_name)
        if cmap:
            code_cid = deepcopy(cmap.code_cid)
            self.code_cid.update(code_cid)

    def add_code_cid(self, code, cid, force=True):
        d = self.code_cid
        for c in code[:-1]:
            if c in d:
                d = d[c]
            else:
                t = {}
                d[c] = t
                d = t
        c = code[-1]
        if force or c not in d:
            d[c] = cid

    def add_cid_unicode(self, cid, code):
        if isinstance(code, PDFName):
            # Interpret as an Adobe glyph name.
            self.cid_unicode[cid] = glyph_name_to_unicode(code.value)
        elif isinstance(code, bytes):
            # Interpret as UTF-16BE.
            self.cid_unicode[cid] = code.decode('UTF-16BE', 'ignore')
        elif isinstance(code, int):
            self.cid_unicode[cid] = chr(code)
        else:
            self.cid_unicode[cid] = code

    def get_unicode(self, cid):
        if cid in self.cid_unicode:
            return self.cid_unicode[cid]
        return ''

    def decode(self, code):
        d = self.code_cid
        for c in code:
            if c in d:
                d = d[c]
                if isinstance(d, int):
                    yield d
                    d = self.code_cid
            else:
                d = self.code_cid


class PDFIdentityCmap(PDFCmap):
    def decode(self, code):
        n = len(code) // 2
        return struct.unpack(f'>{n}H', code) if n else ()


class PDFCMapInterpreter(object):

    def __init__(self, fp):
        self.parser = PDFParser(fp)
        self.cmap = PDFCmap()
        self.stack = []
        self.interpret()

    def interpret(self):
        while True:
            try:
                o = self.parser.next()
            except PDFParserDoneException:
                break
            if not isinstance(o, PDFKeyWord):
                self.stack.append(o)
            elif o.value == b'begincmap':
                self.stack = []
            elif o.value == b'endcmap':
                pass
            elif o.value == b'def':
                v = self.stack.pop()
                k = self.stack.pop().value
                self.cmap.set_attr(k, v)
            elif o.value == b'usecmap':
                cmap_name = self.stack.pop()
                self.cmap.use_cmap(cmap_name)
            elif o.value == b'begincodespacerange':
                self.stack = []
            elif o.value == b'endcodespacerange':
                self.stack = []
            elif o.value == b'begincidrange':
                self.stack = []
            elif o.value == b'endcidrange':
                while self.stack:
                    cid = self.stack.pop().value
                    end = self.stack.pop().value
                    begin = self.stack.pop().value

                    length = len(begin[-4:])
                    b1, b2 = begin[:-4], unpack(begin[-4:])
                    e1, e2 = end[:-4], unpack(end[-4:])
                    for i in range(e2 - b2 + 1):
                        x = b1 + pack(b2 + i, length)
                        self.cmap.add_code_cid(x, cid + i)
            elif o.value == b'begincidchar':
                self.stack = []
            elif o.value == b'endcidchar':
                while self.stack:
                    cid = self.stack.pop().value
                    code = unpack(self.stack.pop().value)
                    self.cmap.add_code_cid(code, cid)
            elif o.value == b'beginbfrange':
                self.stack = []
            elif o.value == b'endbfrange':
                while self.stack:
                    code = self.stack.pop()
                    end = unpack(self.stack.pop().value)
                    begin = unpack(self.stack.pop().value)
                    if isinstance(code, list):
                        for i in range(end - begin + 1):
                            self.cmap.add_cid_unicode(begin + i, code[i].value)
                    else:
                        code = code.value
                        length = len(code[-4:])
                        c1, c2 = code[:-4], unpack(code[-4:])
                        for i in range(end - begin + 1):
                            x = c1 + pack(c2 + i, length)
                            self.cmap.add_cid_unicode(begin + i, x)
            elif o.value == b'beginbfchar':
                self.stack = []
            elif o.value == b'endbfchar':
                while self.stack:
                    code = self.stack.pop().value
                    cid = unpack(self.stack.pop().value)
                    self.cmap.add_cid_unicode(cid, code)
            elif o.value == b'beginnotdefrange':
                self.stack = []
            elif o.value == b'endnotdefrange':
                self.stack = []


class CmapLoader(object):
    CODEC_DICT = {
        'B5': 'cp950',
        'GBK-EUC': 'cp936',
        'RKSJ': 'cp932',
        'EUC': 'euc-jp',
        'KSC-EUC': 'euc-kr',
        'KSC-Johab': 'johab',
        'KSCms-UHC': 'cp949',
        'UniCNS-UTF8': 'utf-8',
        'UniGB-UTF8': 'utf-8',
        'UniJIS-UTF8': 'utf-8',
        'UniKS-UTF8': 'utf-8',
    }

    def __init__(self):
        self.cmap_dict = {}
        self.unicode_map_dict = {}

    def load_cmap(self):
        cmap_path = os.path.join(os.path.dirname(__file__), 'cmap')
        for d in os.listdir(cmap_path):
            cid2code = os.path.join(cmap_path, d, 'cid2code.txt')
            if not os.path.isfile(cid2code):
                continue
            unicode_map_name = '-'.join(d.split('-')[:-1]).encode()
            self.unicode_map_dict[unicode_map_name] = {'v': PDFCmap(attrs={b'WMode': 1}), 'h': PDFCmap()}
            headers = []
            with open(cid2code) as f:
                for line in f:
                    line, _, _ = line.strip().partition('#')
                    if not line:
                        continue
                    row = line.split('\t')
                    if row[0] == 'CID':
                        headers = row
                        continue
                    if not headers:
                        continue
                    cid = int(row[0])
                    unicode_counter_h = defaultdict(int)
                    unicode_counter_v = defaultdict(int)
                    for header, value in zip(headers[1:], row[1:]):
                        if value == '*':
                            continue
                        code_h = []
                        code_v = []
                        for code in value.split(','):
                            vertical = code.endswith('v')
                            if vertical:
                                code = code[:-1]
                            try:
                                code = codecs.decode(code, 'hex_codec')
                            except:
                                code = chr(int(code, 16))
                            try:
                                u = code.decode(self.CODEC_DICT[header], 'strict')
                            except:
                                u = ''
                            if vertical:
                                code_v.append(code)
                                if len(u) == 1:
                                    unicode_counter_v[u] += 1
                            else:
                                code_h.append(code)
                                if len(u) == 1:
                                    unicode_counter_h[u] += 1

                        cmap_h, cmap_v = self.get_cmap(header)
                        if code_v:
                            for code in code_v:
                                cmap_v.add_code_cid(code, cid)
                            for code in code_h:
                                cmap_h.add_code_cid(code, cid)
                        else:
                            for code in code_h:
                                cmap_v.add_code_cid(code, cid, force=False)
                                cmap_h.add_code_cid(code, cid)
                    if unicode_counter_h:
                        self.unicode_map_dict[unicode_map_name]['h'].add_cid_unicode(
                            cid,
                            self.pick_unicode(unicode_counter_h)
                        )
                    if unicode_counter_v or unicode_counter_h:
                        self.unicode_map_dict[unicode_map_name]['v'].add_cid_unicode(
                            cid,
                            self.pick_unicode(unicode_counter_v or unicode_counter_h)
                        )

    @staticmethod
    def pick_unicode(counter):
        chars = sorted(counter.items(), key=(lambda x: (x[1], -ord(x[0]))), reverse=True)
        return chars[0][0]

    def get_cmap(self, name):
        name = name.encode()
        if name.endswith(b'-H'):
            name_h, name_v = name, None
        elif name == b'H':
            name_h, name_v = name, b'V'
        else:
            name_h, name_v = name + b'-H', name + b'-V'

        if name_h not in self.cmap_dict:
            self.cmap_dict[name_h] = PDFCmap()
        if name_v:
            if name_v not in self.cmap_dict:
                self.cmap_dict[name_v] = PDFCmap(attrs={b'WMode': 1})
        return self.cmap_dict[name_h], self.cmap_dict.get(name_v)


class CmapManager(object):
    CMAP_DICT = {}

    def __init__(self):
        self.cmap_loader = CmapLoader()
        self.cmap_dict = {}
        self.init()

    def init(self):
        self.cmap_dict = deepcopy(self.CMAP_DICT)
        self.cmap_loader.load_cmap()

    def set_cmap(self, cmap_name, cmap):
        self.cmap_dict[cmap_name] = cmap

    def get_cmap(self, cmap_name):
        if cmap_name == b'Identity-H':
            return PDFIdentityCmap(attrs={b'WMode': 0})
        if cmap_name == b'Identity-V':
            return PDFIdentityCmap(attrs={b'WMode': 1})
        if cmap_name in self.cmap_dict:
            return self.cmap_dict[cmap_name]
        if cmap_name in self.cmap_loader.cmap_dict:
            return self.cmap_loader.cmap_dict[cmap_name]

        raise PDFCMapNotFoundException(f'cmap not found: {cmap_name}')

    def get_unicode_map(self, unicode_map_name, wmode='h'):
        if unicode_map_name in self.cmap_loader.unicode_map_dict:
            return self.cmap_loader.unicode_map_dict[unicode_map_name][wmode]

        raise PDFCMapNotFoundException(f'unicode_map not found: {unicode_map_name}')


cmap_manager = CmapManager()
