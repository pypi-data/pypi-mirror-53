import re
import logging.config

from .config import LOGGING
from .exception import PDFParserException, PDFParserDoneException
from .pdflexer import PDFLexer
from .pdfobject import PDF_OBJECT_DICT, PDFObj, PDFIndirectRef, PDFStream, PDFXref
from .utils.struct import unpack

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()


class PDFParser(object):

    def __init__(self, fp):
        self.lexer = PDFLexer(fp)

        self._buffer = []
        self._buffer_positions = []

    @property
    def buffer(self):
        if len(self._buffer) < 3:
            for i in range(3 - len(self._buffer)):
                position = self.lexer.tell()
                try:
                    token = self.lexer.next_token()
                except:
                    break
                self._buffer_positions.append(position)
                self._buffer.append(token)

        return self._buffer

    def look_some(self, num):
        return self.buffer[:num]

    def read_some(self, num):
        tmp = []
        while num:
            if len(self.buffer) <= num:
                num -= len(self.buffer)
                tmp.extend(self.buffer)
                self._buffer = []
                self._buffer_positions = []
            else:
                tmp.extend(self.buffer[:num])
                self._buffer = self.buffer[num:]
                self._buffer_positions = self._buffer_positions[num:]
                break
        # logger.debug(f"tokens: {tmp}")
        return tmp

    def read_until(self, stop):
        if self._buffer_positions:
            self.seek(self._buffer_positions[0])
        self._buffer = []
        self._buffer_positions = []
        return self.lexer.read_until(stop)

    def next_line(self):
        if self._buffer_positions:
            self.seek(self._buffer_positions[0])
        self._buffer = []
        self._buffer_positions = []
        return self.lexer.next_line()

    def seek(self, position, whence=0):
        self._buffer = []
        self._buffer_positions = []
        self.lexer.seek(position, whence)

    def parse_object(self):
        token = self.read_some(1)[0]
        return PDF_OBJECT_DICT[token.name](token.text)

    def parse_array(self):
        self.read_some(1)
        o = []
        while True:
            token = self.look_some(1)[0]
            if token.name == 'array_end':
                self.read_some(1)
                break
            o.append(self.next())
        return o

    def parse_dict(self):
        self.read_some(1)
        o = {}
        k = None
        while True:
            token = self.look_some(1)[0]
            if token.name == 'dict_end':
                self.read_some(1)
                break
            if k is None:
                self.read_some(1)
                if token.name != 'name':
                    raise PDFParserException(f'Wrong Dict Key Type: {token}')
                k = token.text
            else:
                o[k] = self.next()
                k = None
        return o

    def parse_indirect_ref(self):
        tokens = self.read_some(3)
        return PDFIndirectRef(int(tokens[0].text), int(tokens[1].text))

    def parse_obj(self):
        tokens = self.read_some(3)
        n = self.next()
        t = self.look_some(1)[0]
        if t.name == 'keyword' and t.text == b'stream':
            n = self.parse_stream(n)
        endobj = self.read_some(1)[0]
        if endobj.name != 'keyword' or endobj.text != b'endobj':
            raise PDFParserException(f'Bad Obj: {endobj}')
        if isinstance(n, PDFStream):
            if b'Type' in n.dict and n.dict[b'Type'].value == b'XRef':
                return self.parse_xref_stream(n)
        return PDFObj(int(tokens[0].text), int(tokens[1].text), n)

    def parse_stream(self, d):
        self.read_some(1)
        stream = self.read_until(re.compile(rb'endstream'))
        endstream = self.read_some(1)[0]
        if endstream.name != 'keyword' or endstream.text != b'endstream':
            raise PDFParserException(f'Bad Stream: {endstream}')
        return PDFStream(d, stream)

    def parse_xref(self):
        self.read_some(1)
        xref = PDFXref()
        while True:
            token = self.look_some(1)[0]
            if token.text == b'trailer':
                self.read_some(1)
                xref.trailer = self.next()
                break
            line = self.next_line().strip()
            if not line:
                continue
            start, num = map(int, line.split(b' '))
            for obj_id in range(start, start + num):
                line = self.next_line().strip()
                pos, gen_no, use = line.split(b' ')
                if use != b'n':
                    continue
                xref.offsets[obj_id] = (None, int(pos), int(gen_no))
        return xref

    @staticmethod
    def parse_xref_stream(stream):
        xref = PDFXref()
        xref.trailer = stream.dict

        size = xref.trailer[b'Size']
        index = xref.trailer.get(b'Index') or [0, size]
        w = xref.trailer[b'W']
        entry_length = sum(w)

        offset = 0
        while index:
            begin, number = index[:2]
            index = index[2:]

            for i in range(number):
                entry = stream.value[offset: offset + entry_length]
                entry_type = unpack(entry[:w[0]]) if entry[:w[0]] else 1
                if entry_type == 1:
                    pos = unpack(entry[w[0]: w[0] + w[1]])
                    gen_no = unpack(entry[w[0] + w[1]:]) if entry[w[0] + w[1]:] else 0
                    xref.offsets[begin + i] = (None, int(pos), gen_no)
                elif entry_type == 2:
                    stream_object_number = unpack(entry[w[0]: w[0] + w[1]])
                    obj_pos = unpack(entry[w[0] + w[1]:]) if entry[w[0] + w[1]:] else 0
                    xref.offsets[begin + i] = (int(stream_object_number), int(obj_pos), 0)
                offset += entry_length
        return xref

    def next(self):
        tokens = self.look_some(3)
        if not tokens:
            raise PDFParserDoneException

        if len(tokens) == 3 and tokens[2].name == 'keyword':
            if tokens[2].text == b'R':
                return self.parse_indirect_ref()
            elif tokens[2].text == b'obj':
                return self.parse_obj()

        token = tokens[0]
        if token.name == 'array_begin':
            return self.parse_array()
        elif token.name == 'dict_begin':
            return self.parse_dict()
        elif token.name == 'keyword' and token.text == b'xref':
            return self.parse_xref()
        else:
            return self.parse_object()
