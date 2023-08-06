import re
import struct
import logging.config
from io import BytesIO

from .pdfafm import afm_loader
from .pdfcmap import cmap_manager, PDFCmap, PDFCMapInterpreter
from .pdfparser import PDFParser
from .pdfobject import PDFKeyWord, PDFName, PDFInteger
from .exception import PDFParserDoneException, PDFCMapNotFoundException
from .encoding import glyph_name_to_unicode, get_encoding

from .config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()


class PDFFont(object):
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.default_horizon_displacement = float(descriptor.get(b'MissingWidth', 0))
        self.horizon_displacements = {}
        self.default_vertical_displacement = 0
        self.vertical_displacements = {}
        # If the font in a source document uses a bold or italic style but there is no font data for that style,
        # the host operating system synthesizes the style. In this case, a com- ma and the style name
        # (one of Bold, Italic, or BoldItalic) are appended to the font name. For example, for a TrueType font
        # that is a bold variant of the New York font, the BaseFont value is written as /NewYork,Bold
        self.font_name = None
        if b'FontName' in descriptor:
            font_name = descriptor[b'FontName']
            if isinstance(font_name, PDFName):
                font_name = font_name.value
            if isinstance(font_name, str):
                font_name = font_name.encode()
            self.font_name = self.parse_font_name(font_name)
        self.flags = int(descriptor.get(b'Flags', 0))
        self._ascent = float(descriptor.get(b'Ascent', 0))
        self._descent = float(descriptor.get(b'Descent', 0))
        self.italic_angle = float(descriptor.get(b'ItalicAngle', 0))
        self.leading = float(descriptor.get(b'Leading', 0))
        self.bbox = list(descriptor.get(b'FontBBox', (0, 0, 0, 0)))
        self.horizon_scale = 0.001
        self.vertical_scale = 0.001

    @staticmethod
    def parse_font_name(name):
        # For a font subset, the PostScript name of the font—the value of the font’s BaseFont entry
        # and the font descriptor’s FontName entry—begins with a tag followed by a plus sign (+).
        # The tag consists of exactly six uppercase letters; the choice of letters is arbitrary,
        # but different subsets in the same PDF file must have different tags.
        name = re.sub(rb'^[A-Z]{6}\+', b'', name)
        try:
            name = name.decode()
        except UnicodeDecodeError:
            name = name.decode('gbk')
        return name

    def is_vertical(self):
        return False

    def is_multi_byte(self):
        return False

    def decode(self, bytes):
        return bytearray(bytes)

    @property
    def ascent(self):
        return self._ascent * self.vertical_scale

    @property
    def descent(self):
        return self._descent * self.vertical_scale

    @property
    def width(self):
        w = self.bbox[2] - self.bbox[0]
        if w == 0:
            w = - self.default_horizon_displacement
        return w * self.horizon_scale

    @property
    def height(self):
        h = self.bbox[3] - self.bbox[1]
        if h == 0:
            h = self._ascent - self._descent
        return h * self.vertical_scale

    def char_horizon_displacement(self, cid):
        if cid in self.horizon_displacements:
            return self.horizon_displacements[cid] * self.horizon_scale
        u = self.to_unicode(cid)
        if u in self.horizon_displacements:
            return self.horizon_displacements[u] * self.horizon_scale
        return self.default_horizon_displacement * self.horizon_scale

    def char_vertical_displacement(self, cid):
        return self.vertical_displacements.get(cid, self.default_vertical_displacement) * self.vertical_scale

    def to_unicode(self, cid):
        return None


class PDFSimpleFont(PDFFont):
    def __init__(self, descriptor, spec):
        PDFFont.__init__(self, descriptor)
        # Font encoding is specified either by a name of
        # built-in encoding or a dictionary that describes
        # the differences.
        encoding = spec.get(b'Encoding')
        if isinstance(encoding, dict):
            base_encoding = encoding[b'BaseEncoding'].value if b'BaseEncoding' in encoding else b'StandardEncoding'
            differences = [i.value for i in encoding.get(b'Differences', [])]
            self.cid_unicode = get_encoding(base_encoding, differences)
        else:
            self.cid_unicode = get_encoding(encoding.value if encoding else b'StandardEncoding')

        self.cmap = None
        if b'ToUnicode' in spec:
            stream = spec[b'ToUnicode']
            interpreter = PDFCMapInterpreter(BytesIO(stream.value))
            self.cmap = interpreter.cmap

    def to_unicode(self, cid):
        if self.cmap and cid in self.cmap.cid_unicode:
            return self.cmap.cid_unicode[cid]
        if cid in self.cid_unicode:
            return self.cid_unicode[cid]
        if cid == 10:
            return '\n'
        if cid == 13:
            return '\r'
        logging.warning(f'missing cid: {cid}')
        return ''


class PDFType1Font(PDFSimpleFont):
    def __init__(self, spec):
        self.basefont = self.parse_font_name(spec[b'BaseFont'].value) if b'BaseFont' in spec else None
        # For the standard 14 fonts, the entries FirstChar, LastChar, Widths, and FontDescriptor
        # must either all be present or all be absent. Ordinarily, they are absent;
        # specifying them enables a standard font to be overridden
        if b'FontDescriptor' in spec:
            descriptor = spec[b'FontDescriptor']
            first_char = int(spec[b'FirstChar'].value) if b'FirstChar' in spec else 0
            horizon_displacements = {
                first_char + i: w for (i, w) in enumerate(spec.get(b'Widths', [0] * 256))
            }
        else:
            descriptor = afm_loader.fonts[self.basefont]['descriptor']
            horizon_displacements = {k: v['WX'] for k, v in afm_loader.fonts[self.basefont]['metrics'].items()}

        if b'FontFile3' in descriptor:
            self.parse_font_file3(descriptor[b'FontFile3'])

        super().__init__(descriptor, spec)
        self.horizon_displacements = horizon_displacements

        if b'Encoding' not in spec and b'FontFile' in descriptor:
            # try to recover the missing encoding info from the font file.
            self.parse_font_file(descriptor[b'FontFile'])

    def parse_font_file(self, stream):
        # The length in bytes of the clear-text portion of the Type 1 font program
        length1 = int(stream[b'Length1'])
        data = stream.value[:length1]

        stack = []
        parser = PDFParser(BytesIO(data))
        while True:
            try:
                o = parser.next()
            except PDFParserDoneException:
                break
            if not isinstance(o, PDFKeyWord):
                stack.append(o)
            elif o.value == b'put':
                # dup 32 /space put
                # ...
                # dup 254 /bracerightbt put
                value = stack.pop()
                key = stack.pop()
                if isinstance(key, PDFInteger) and isinstance(value, PDFName):
                    self.cid_unicode[key.value] = glyph_name_to_unicode(value.value)

    def parse_font_file3(self, stream):
        pass


class PDFTrueTypeFont(PDFType1Font):
    pass


class PDFType3Font(PDFSimpleFont):
    def __init__(self, spec):
        if b'FontDescriptor' in spec:
            descriptor = spec[b'FontDescriptor']
        else:
            descriptor = {
                b'Ascent': 0,
                b'Descent': 0,
                b'FontBBox': spec[b'FontBBox']
            }
        super().__init__(descriptor, spec)

        first_char = int(spec[b'FirstChar'].value) if b'FirstChar' in spec else 0
        self.horizon_displacements = dict((i + first_char, w) for (i, w) in enumerate(spec.get(b'Widths', [0] * 256)))

        _, self._descent, _, self._ascent = self.bbox
        a, b, c, d, e, f = spec[b'FontMatrix']
        self.horizon_scale, self.vertical_scale = a + c, b + d


class PDFCIDFont(PDFFont):
    def __init__(self, spec):
        descriptor = spec.get(b'FontDescriptor') or {}
        super().__init__(descriptor)

        self.basefont = self.parse_font_name(spec[b'BaseFont'].value) if b'BaseFont' in spec else None
        cid_system_info = spec.get(b'CIDSystemInfo', {})
        cid_coding = b'-'.join([
            cid_system_info[b'Registry'].value if b'Registry' in cid_system_info else b'',
            cid_system_info[b'Ordering'].value if b'Ordering' in cid_system_info else b'',
        ])
        encoding = spec[b'Encoding'].value if b'Encoding' in spec else None

        self.cmap = cmap_manager.get_cmap(encoding) or PDFCmap()

        self.unicode_map = PDFCmap()
        if b'ToUnicode' in spec:
            stream = spec[b'ToUnicode']
            interpreter = PDFCMapInterpreter(BytesIO(stream.value))
            self.unicode_map = interpreter.cmap
        elif cid_coding in (b'Adobe-Identity', b'Adobe-UCS'):
            if b'FontFile2' in descriptor:
                self.parse_font_file(descriptor[b'FontFile2'].value)
        else:
            self.unicode_map = cmap_manager.get_unicode_map(cid_coding, 'v' if self.cmap.is_vertical() else 'h')

        if self.is_vertical():
            widths = W2(spec.get(b'W2', []))
            vy, w = spec.get(b'DW2', [880, -1000])
            self.default_vertical_displacement = vy
            self.horizon_displacements = dict((cid, w) for (cid, (w, _)) in widths.items())
            self.default_horizon_displacement = w
            self.vertical_displacements = dict((cid, vy) for (cid, (_, (vx, vy))) in widths.items())
        else:
            self.horizon_displacements = W(spec.get(b'W', {}))
            self.default_horizon_displacement = spec.get(b'DW', 1000)

    def parse_font_file(self, font_file):
        # create unicode map
        self.unicode_map = PDFCmap()

        fp = BytesIO(font_file)
        font_type = fp.read(4)

        tables = {}
        try:
            table_number, _, _, _ = struct.unpack('>HHHH', fp.read(8))
            for _ in range(table_number):
                name, _, offset, length = struct.unpack('>4sLLL', fp.read(16))
                tables[name] = (offset, length)
        except struct.error:
            # Do not fail if there are not enough bytes to read. Even for
            # corrupted PDFs we would like to get as much information as
            # possible, so continue.
            pass

        if b'cmap' not in tables:
            return
        base_offset, length = tables[b'cmap']
        fp.seek(base_offset)
        version, sub_table_number = struct.unpack('>HH', fp.read(4))
        sub_tables = [base_offset + struct.unpack('>HHL', fp.read(8)) for _ in range(sub_table_number)]
        char2gid = {}
        # Only supports sub_tables type 0, 2 and 4.
        for _, _, sub_table_offset in sub_tables:
            fp.seek(sub_table_offset)
            fmt_type, fmt_len, fmt_lang = struct.unpack('>HHH', fp.read(6))
            if fmt_type == 0:
                char2gid.update(enumerate(struct.unpack('>256B', fp.read(256))))
            elif fmt_type == 2:
                sub_header_keys = struct.unpack('>256H', fp.read(512))
                first_bytes = [0] * 8192
                for (i, k) in enumerate(sub_header_keys):
                    first_bytes[k//8] = i
                nhdrs = max(sub_header_keys)//8 + 1
                hdrs = []
                for i in range(nhdrs):
                    (firstcode, entcount, delta, offset) = struct.unpack('>HHhH', fp.read(8))
                    hdrs.append((i, firstcode, entcount, delta, fp.tell()-2+offset))
                for (i, firstcode, entcount, delta, pos) in hdrs:
                    if not entcount:
                        continue
                    first = firstcode + (first_bytes[i] << 8)
                    fp.seek(pos)
                    for c in range(entcount):
                        gid = struct.unpack('>H', fp.read(2))
                        if gid:
                            gid += delta
                        char2gid[first+c] = gid
            elif fmt_type == 4:
                (segcount, _1, _2, _3) = struct.unpack('>HHHH', fp.read(8))
                segcount //= 2
                ecs = struct.unpack('>%dH' % segcount, fp.read(2*segcount))
                fp.read(2)
                scs = struct.unpack('>%dH' % segcount, fp.read(2*segcount))
                idds = struct.unpack('>%dh' % segcount, fp.read(2*segcount))
                pos = fp.tell()
                idrs = struct.unpack('>%dH' % segcount, fp.read(2*segcount))
                for (ec, sc, idd, idr) in zip(ecs, scs, idds, idrs):
                    if idr:
                        fp.seek(pos+idr)
                        for c in range(sc, ec+1):
                            char2gid[c] = (struct.unpack('>H', fp.read(2))[0] + idd) & 0xffff
                    else:
                        for c in range(sc, ec+1):
                            char2gid[c] = (c + idd) & 0xffff
            else:
                assert False, str(('Unhandled', fmt_type))
        for char, gid in char2gid.items():
            self.unicode_map.add_cid_unicode(gid, char)

    def is_vertical(self):
        return self.cmap.is_vertical()

    def is_multi_byte(self):
        return True

    def decode(self, bytes):
        return self.cmap.decode(bytes)

    def to_unicode(self, cid):
        return self.unicode_map.get_unicode(cid)


def W(ws):
    """
    c [w1 w2 ... wn]
    cfirst clast w
    """
    widths = {}
    while ws:
        t = ws.pop()
        if isinstance(t, list):
            c = ws.pop()
            for i, w in enumerate(t):
                widths[c + i] = w
        else:
            c2 = ws.pop()
            c1 = ws.pop()
            for c in range(c1, c2 + 1):
                widths[c] = t
    return widths


def W2(ws):
    """
    c [w11y v1x v1y w12y v2x v2y ...]
    cfirst clast w11y v1x v1y
    """
    widths = {}
    while ws:
        t = ws.pop()
        if isinstance(t, list):
            c = ws.pop()
            i = 0
            while t:
                vy = t.pop()
                vx = t.pop()
                w = t.pop()
                widths[c + i] = (w, (vx, vy))
                i += 1
        else:
            vy = t
            vx = ws.pop()
            w = ws.pop()
            c2 = ws.pop()
            c1 = ws.pop()
            for c in range(c1, c2 + 1):
                widths[c] = (w, (vx, vy))
    return widths
