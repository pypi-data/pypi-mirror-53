import re
import logging.config

from .exception import PDFObjectTypeException, PDFObjNotFoundException, PDFStreamException
from .decoder import DECODER_MAP

from .config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()


class PDFObject(object):
    def __init__(self, string):
        self.text = string
        self.value = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        return f'{self.__class__.__name__}({self.value})'


class PDFBoolean(PDFObject):
    def __init__(self, string):
        super().__init__(string)
        if re.search(rb'true', string, flags=re.I):
            self.value = True
        elif re.search(rb'false', string, flags=re.I):
            self.value = False
        else:
            raise PDFObjectTypeException(f'Unexpected PDFBoolean: {string}')

    def __bool__(self):
        return self.value


class PDFNumeric(PDFObject):
    pass


class PDFInteger(PDFNumeric, int):
    def __init__(self, string):
        super().__init__(string)
        try:
            self.value = int(string)
        except:
            raise PDFObjectTypeException(f'Unexpected PDFInteger: {string}')


class PDFReal(PDFNumeric, float):
    def __init__(self, string):
        super().__init__(string)
        try:
            self.value = float(string)
        except:
            raise PDFObjectTypeException(f'Unexpected PDFReal: {string}')


class PDFString(PDFObject, str):
    def __init__(self, string):
        super().__init__(string)
        self.value = string

    def __eq__(self, other):
        return self.value == other


class PDFName(PDFObject, str):
    def __init__(self, string):
        super().__init__(string)
        self.value = string

    def __eq__(self, other):
        return self.value == other


class PDFKeyWord(PDFObject, str):
    def __init__(self, string):
        if not string:
            raise PDFObjectTypeException(f'Unexpected PDFKeyWord: {string}')
        super().__init__(string)
        self.value = string

    def __eq__(self, other):
        return self.value == other


PDF_OBJECT_DICT = {
    'boolean': PDFBoolean,
    'integer': PDFInteger,
    'real': PDFReal,
    'string': PDFString,
    'name': PDFName,
    'keyword': PDFKeyWord,
}


class PDFIndirectRef(object):
    def __init__(self, number, generation):
        self.number = number
        self.generation = generation

    def __repr__(self):
        return f"PDFIndirectRef({self.number}, {self.generation})"


class PDFObj(object):
    def __init__(self, number, generation, value=None):
        self.number = number
        self.generation = generation
        self.value = value

    def __repr__(self):
        return f"PDFObj({self.number}, {self.generation}, {self.value})"


class PDFStream(object):
    def __init__(self, d, v):
        self.dict = d
        # The keyword stream that follows the stream dictionary should be followed by an end-of-line marker
        # consisting of either a carriage return and a line feed or just a line feed, and not by a carriage
        # return alone.
        # Note: Without the restriction against following the keyword stream by a carriage return alone,
        # it would be impossible to differentiate a stream that uses carriage return as its end-of-line marker
        # and has a line feed as its first byte of data from one that uses a carriage return–line feed sequence
        # to denote end-of-line.
        if v.startswith(b'\r\n'):
            v = v[2:]
        elif v.startswith(b'\n'):
            v = v[1:]

        length = d[b'Length'] if b'Length' in d else d.get(b'L')
        if length and length <= len(v):
            v = v[:length]
        else:
            if v.endswith(b'\r\n'):
                v = v[2:]
            elif v.endswith(b'\r') or v.endswith(b'\n'):
                v = v[1:]
        self.v = v
        self._value = None

    @property
    def value(self):
        if self._value is None:
            self._value = self.decode(self.v)
        return self._value

    def filters(self):
        filters = []
        for k in [b'F', b'Filter']:
            if k in self.dict:
                if isinstance(self.dict[k], list):
                    filters.extend(self.dict[k])
                else:
                    filters.append(self.dict[k])
        params = []
        for k in [b'DP', b'DecodeParms', b'FDecodeParms']:
            if k in self.dict:
                if isinstance(self.dict[k], list):
                    params.extend(self.dict[k])
                else:
                    params.append(self.dict[k])
        if len(params) == 0:
            params = [{}]
        if len(params) == 1:
            params = params * len(filters)
        if len(filters) != len(params):
            logger.warning(f'filters and params not equal: {filters}, {params}')

        return zip(filters, params)

    def decode(self, value):
        for f, p in self.filters():
            if DECODER_MAP.get(f.value) is None:
                break
            if f.value in (b'CCITTFaxDecode', b'CCF'):
                value = DECODER_MAP[f.value](value, p)
            else:
                value = DECODER_MAP[f.value](value)

            if isinstance(p, dict) and b'Predictor' in p:
                predictor = int(p[b'Predictor'])
                if predictor >= 10:
                    # PNG predictor
                    colors = int(p.get(b'Colors', 1))
                    columns = int(p.get(b'Columns', 1))
                    bits_per_component = int(p.get(b'BitsPerComponent', 8))
                    value = self.apply_png_predictor(colors, columns, bits_per_component, value)
                elif predictor != 1:
                    raise PDFStreamException(f'Unsupported Predictor: {predictor}')
        return value

    @staticmethod
    def apply_png_predictor(colors, columns, bits_per_component, data):
        if bits_per_component != 8:
            raise PDFStreamException(f"Unsupported bits_per_component: {bits_per_component}")
        nbytes = colors * columns * bits_per_component // 8
        buf = b''
        line0 = b'\x00' * columns
        for i in range(0, len(data), nbytes + 1):
            ft = data[i]
            i += 1
            line1 = data[i:i + nbytes]
            line2 = b''
            if ft == 0:
                # PNG none
                line2 += line1
            elif ft == 1:
                # PNG sub (UNTESTED)
                c = 0
                for b in line1:
                    c = (c + b) & 255
                    line2 += bytes([c])
            elif ft == 2:
                # PNG up
                for (a, b) in zip(line0, line1):
                    c = (a + b) & 255
                    line2 += bytes([c])
            elif ft == 3:
                # PNG average (UNTESTED)
                c = 0
                for (a, b) in zip(line0, line1):
                    c = ((c + a + b) // 2) & 255
                    line2 += bytes([c])
            else:
                raise ValueError("Unsupported predictor value: %d" % ft)
            buf += line2
            line0 = line2
        return buf

    def __repr__(self):
        return f"PDFStream({self.dict}, {self.v})"


class PDFXref(object):
    def __init__(self):
        self.offsets = {}
        self.trailer = {}

    def obj_position(self, obj_id):
        try:
            obj_position = self.offsets[obj_id]
        except KeyError:
            raise PDFObjNotFoundException(f"Obj Id Not Found: {obj_id}")
        return obj_position

    def __repr__(self):
        return f"PDFXref({self.offsets}, {self.trailer})"
