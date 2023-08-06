from io import BytesIO
from .pdfpage import PDFPage, PDFPageInterpreter
from .pdfparser import PDFParser
from .pdfobject import PDFObj, PDFIndirectRef, PDFStream
from .pdfdecryption import decryption
from .exception import PDFObjNotFoundException, PDFDocumentException, PDFSyntaxException, PDFParserException, PDFParserDoneException


class PDFDocument(object):
    PAGE_INHERITABLE_ATTRS = {b'Resources', b'MediaBox', b'CropBox', b'Rotate'}

    def __init__(self, fp, password=''):
        self.parser = PDFParser(fp)
        self.password = password
        self.decipher = None
        self._startxref = None
        self._xrefs = None
        self._root = None
        self._info = []
        self._obj_cache = {}
        self._obj_stream_cache = {}
        self._indirect_ref_cache = {}

        self.fonts = {}
        self.color_spaces = {}
        self.x_objects = {}
        self.properties = {}

    @property
    def startxref(self):
        if self._startxref is None:
            startxref = None
            for line in self.parser.lexer.reversed_lines():
                line = line.strip()
                if line == b'startxref':
                    break
                startxref = line
            else:
                raise PDFDocumentException('Startxref Not Found')
            try:
                self._startxref = int(startxref)
            except:
                raise PDFDocumentException('Startxref Not Found')
        return self._startxref

    @property
    def xrefs(self):
        if self._xrefs is None:
            self._xrefs = []
            self.xref(self.startxref)
        return self._xrefs

    def xref(self, startxref):
        self.parser.seek(startxref)
        xref = self.parser.next()
        self._xrefs.append(xref)

        if b'Encrypt' in xref.trailer:
            ids = self.resolve_indirect_ref(xref.trailer[b'ID'])
            encrypt = self.resolve_indirect_ref(xref.trailer[b'Encrypt'])
            self.decipher = decryption[encrypt[b'V'].value](ids, encrypt, self.password)
        if b'Root' in xref.trailer:
            self._root = xref.trailer[b'Root']
        if b'Info' in xref.trailer:
            self._info.append(xref.trailer[b'Info'])

        if b'XRefStm' in xref.trailer:
            self.xref(int(xref.trailer[b'XRefStm']))
        if b'Prev' in xref.trailer:
            self.xref(int(xref.trailer[b'Prev']))

    @property
    def catalog(self):
        if self._root is None:
            _ = self.xrefs
            self._root = self.resolve_indirect_ref(self._root)
            self._root[b'Pages'] = self.resolve_indirect_ref(self._root[b'Pages'])
        return self._root

    @property
    def pages(self):
        for page in self._pages(self.catalog[b'Pages']):
            i = PDFPageInterpreter(page)
            i.interpret()
            yield {
                'box': [i.value for i in page.crop_box],
                'rotate': page.rotate,
                'data': i.data,
            }

    def _pages(self, page_tree):
        for kid in self.resolve_indirect_ref(page_tree[b'Kids']):
            kid = self.resolve_indirect_ref(kid)
            for k in self.PAGE_INHERITABLE_ATTRS:
                if k not in kid:
                    kid[k] = page_tree.get(k)
            if kid[b'Type'] == b'Page':
                yield PDFPage(self, kid)
            elif kid[b'Type'] == b'Pages':
                yield from self._pages(kid)

    def resolve_indirect_ref(self, o):
        while isinstance(o, PDFIndirectRef):
            key = (o.number, o.generation)
            if key not in self._indirect_ref_cache:
                o = self.get_obj(o.number)
                if isinstance(o, PDFObj):
                    o = o.value
                self._indirect_ref_cache[key] = o
            o = self._indirect_ref_cache[key]
        return o

    def deep_resolve_indirect_ref(self, o):
        o = self.resolve_indirect_ref(o)
        if isinstance(o, list):
            return [self.deep_resolve_indirect_ref(i) for i in o]
        if isinstance(o, dict):
            return {k: self.deep_resolve_indirect_ref(v) for k, v in o.items()}
        return self.resolve_indirect_ref(o)

    def decrypt(self, number, generation, value):
        if isinstance(value, list):
            value = [self.decrypt(number, generation, v) for v in value]
        elif isinstance(value, dict):
            value = {k: self.decrypt(number, generation, v) for k, v in value.items()}
        elif isinstance(value, bytes):
            value = self.decipher.decrypt(number, generation, value)
        elif isinstance(value, PDFStream):
            value.v = self.decipher.decrypt(number, generation, value.v, value.dict)
        return value

    def get_obj(self, obj_number):
        if obj_number not in self._obj_cache:
            for xref in self.xrefs:
                try:
                    stream_obj_number, position, gen_no = xref.obj_position(obj_number)
                except PDFObjNotFoundException:
                    continue
                try:
                    if stream_obj_number is None:
                        obj = self.obj(position, obj_number)
                        if self.decipher:
                            obj.value = self.decrypt(obj.number, obj.generation, obj.value)
                    else:
                        obj = self.obj_in_stream(position, stream_obj_number)
                    break
                except (PDFParserException, PDFSyntaxException):
                    continue
            else:
                raise PDFObjNotFoundException(obj_number)
            self._obj_cache[obj_number] = (obj, gen_no)
        obj, gen_no = self._obj_cache[obj_number]
        return obj

    def obj(self, position, obj_number):
        self.parser.seek(position)
        obj = self.parser.next()
        if not isinstance(obj, PDFObj):
            raise PDFSyntaxException(f'Not A PDFObj: {obj}')
        if obj.number != obj_number:
            raise PDFSyntaxException(f'Obj Mismatch: {obj.number} != {obj_number}')
        if isinstance(obj.value, PDFStream):
            obj.value.dict = self.deep_resolve_indirect_ref(obj.value.dict)
        return obj

    def obj_in_stream(self, position, stream_obj_number):
        stream_obj = self.get_obj(stream_obj_number)
        if stream_obj_number not in self._obj_stream_cache:
            stream = stream_obj.value
            parser = PDFParser(BytesIO(stream.value))
            objs = []
            while True:
                try:
                    o = parser.next()
                except PDFParserDoneException:
                    break
                objs.append(o)
            n = stream.dict[b'N'].value if b'N' in stream.dict else 0
            self._obj_stream_cache[stream_obj_number] = (n, objs)
        n, objs = self._obj_stream_cache[stream_obj_number]
        obj = objs[n * 2 + position]
        return obj
