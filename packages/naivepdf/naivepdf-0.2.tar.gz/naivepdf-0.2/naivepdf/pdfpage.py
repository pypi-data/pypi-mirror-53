from io import BytesIO
import re

from .pdfparser import PDFParser
from .pdfobject import PDFNumeric, PDFKeyWord, PDFStream, PDFIndirectRef
from .exception import PDFParserDoneException, PDFInterpreterException
from .pdffont import PDFType1Font, PDFType3Font, PDFTrueTypeFont, PDFCIDFont

COLOR_SPACES = {
    b'DeviceGray': {'name': b'DeviceGray', 'value': 1},
    b'CalRGB': {'name': b'CalRGB', 'value': 3},
    b'CalGray': {'name': b'CalGray', 'value': 1},
    b'Lab': {'name': b'Lab', 'value': 3},
    b'DeviceRGB': {'name': b'DeviceRGB', 'value': 3},
    b'DeviceCMYK': {'name': b'DeviceCMYK', 'value': 4},
    b'Separation': {'name': b'Separation', 'value': 1},
    b'Indexed': {'name': b'Indexed', 'value': 1},
    b'Pattern': {'name': b'Pattern', 'value': 1},
}


class PDFPage(object):
    def __init__(self, document, attrs):
        self.document = document
        self.attrs = attrs

        # The media box defines the boundaries of the physical medium on which the page is to be printed
        # The crop box determines how the page’s contents are to be positioned on the output medium.
        # Conceptually, user space is an infinite plane. Only a small portion of this plane
        # corresponds to the imageable area of the output device: a rectangular region defined
        # by the CropBox entry in the page dictionary.

        self.media_box = self.document.resolve_indirect_ref(self.attrs[b'MediaBox'])
        self.crop_box = self.document.resolve_indirect_ref(self.attrs.get(b'CropBox')) or self.media_box
        self.box_color_info = self.document.resolve_indirect_ref(self.attrs.get(b'BoxColorInfo') or {})
        self.rotate = (int(self.attrs.get(b'Rotate') or 0) + 360) % 360
        self.annotations = self.attrs.get(b'Annots')
        self.beads = self.attrs.get(b'B')

        contents = self.document.resolve_indirect_ref(self.attrs.get(b'Contents') or [])
        if not isinstance(contents, list):
            contents = [contents]
        self.contents = [self.document.resolve_indirect_ref(content) for content in contents]

        self.resources = self.document.resolve_indirect_ref(self.attrs.get(b'Resources') or {})

        self._fonts = None
        self._color_spaces = None
        self._x_objects = None
        self._properties = None

    @property
    def fonts(self):
        if self._fonts is None:
            self._fonts = {}
            for k, v in (self.document.resolve_indirect_ref(self.resources.get(b'Font')) or {}).items():
                if isinstance(v, PDFIndirectRef) and (v.number, v.generation) in self.document.fonts:
                    self._fonts[k] = self.document.fonts[v.number, v.generation]
                else:
                    self._fonts[k] = self.font(self.document.deep_resolve_indirect_ref(v))
                    if isinstance(v, PDFIndirectRef):
                        self.document.fonts[v.number, v.generation] = self._fonts[k]
        return self._fonts

    def font(self, font):
        subtype = font[b'Subtype'].value if b'Subtype' in font else b'Type1'
        if subtype in {b'Type1', b'MMType1'}:
            # Type1
            return PDFType1Font(font)
        elif subtype == b'TrueType':
            # TrueType
            return PDFTrueTypeFont(font)
        elif subtype == b'Type3':
            # Type3
            return PDFType3Font(font)
        elif subtype in {b'CIDFontType0', b'CIDFontType2'}:
            # CID
            return PDFCIDFont(font)
        elif subtype == b'Type0':
            sub_font = font[b'DescendantFonts'][0].copy()
            for k in (b'Encoding', b'ToUnicode'):
                if k in font:
                    sub_font[k] = font[k]
            return self.font(sub_font)

    @property
    def color_spaces(self):
        if self._color_spaces is None:
            self._color_spaces = {}
            for k, v in (self.document.resolve_indirect_ref(self.resources.get(b'ColorSpace')) or {}).items():
                if isinstance(v, PDFIndirectRef) and (v.number, v.generation) in self.document.color_spaces:
                    self._color_spaces[k] = self.document.color_spaces[v.number, v.generation]
                else:
                    self._color_spaces[k] = self.color_space(self.document.deep_resolve_indirect_ref(v))
                    if isinstance(v, PDFIndirectRef):
                        self.document.color_spaces[v.number, v.generation] = self._color_spaces[k]
        return self._color_spaces

    def color_space(self, color_space):
        if isinstance(color_space, list):
            name = color_space[0]
            if name == b'ICCBased':
                return {
                    'name': name.value,
                    'value': color_space[1].dict[b'N'].value
                }
            elif name == b'DeviceN':
                return {
                    'name': name.value,
                    'value': len(color_space[1])
                }
            # A Separation color space is defined as follows:
            # [ /Separation name alternateSpace tintTransform ]
            # In other words, it is a four-element array whose first element is the color space family name Separation.
            # The alternateSpace parameter must be an array or name object that identifies the alternate color space,
            # which can be any device or CIE-based color space but not another special color space.
            elif name == b'Separation':
                return self.color_space(color_space[2])
            else:
                return {
                    'name': name.value,
                    'value': None
                }
        else:
            return COLOR_SPACES[color_space.value]

    @property
    def x_objects(self):
        if self._x_objects is None:
            self._x_objects = {}
            for k, v in (self.document.resolve_indirect_ref(self.resources.get(b'XObject')) or {}).items():
                if isinstance(v, PDFIndirectRef) and (v.number, v.generation) in self.document.x_objects:
                    self._x_objects[k] = self.document.x_objects[v.number, v.generation]
                else:
                    self._x_objects[k] = self.document.deep_resolve_indirect_ref(v)
                    if isinstance(v, PDFIndirectRef):
                        self.document.x_objects[v.number, v.generation] = self._x_objects[k]
        return self._x_objects

    @property
    def properties(self):
        if self._properties is None:
            self._properties = {}
            for k, v in (self.document.resolve_indirect_ref(self.resources.get(b'Properties')) or {}).items():
                if isinstance(v, PDFIndirectRef) and (v.number, v.generation) in self.document.properties:
                    self._properties[k] = self.document.properties[v.number, v.generation]
                else:
                    self._properties[k] = self.document.deep_resolve_indirect_ref(v)
                    if isinstance(v, PDFIndirectRef):
                        self.document.properties[v.number, v.generation] = self._properties[k]
        return self._properties

    def __repr__(self):
        return f"PDFPage({self.attrs})"


class PDFPageInterpreter(object):
    PDF_PAGE_OPERATORS = {
        'general_graphics_state': {'w', 'J', 'j', 'M', 'd', 'ri', 'i', 'gs'},
        'special_graphics_state': {'q', 'Q', 'cm'},
        'path_construction': {'m', 'l', 'c', 'v', 'y', 'h', 're'},
        'path_painting': {'S', 's', 'f', 'F', 'f*', 'B', 'B*', 'b', 'b*', 'n'},
        'clipping_paths': {'W', 'W*'},
        'text_objects': {'BT', 'ET'},
        'text_state': {'Tc', 'Tw', 'Tz', 'TL', 'Tf', 'Tr', 'Ts'},
        'text_positioning': {'Td', 'TD', 'Tm', 'T*'},
        'text_showing': {'Tj', 'TJ', "'", '"'},
        'type_3_fonts': {'d0', 'd1'},
        'color': {'CS', 'cs', 'SC', 'SCN', 'sc', 'scn', 'G', 'g', 'RG', 'rg', 'K', 'k'},
        'shading_patterns': {'sh'},
        'inline_images': {'BI', 'ID', 'EI'},
        'x_objects': {'Do'},
        'marked_content': {'MP', 'DP', 'BMC', 'BDC', 'EMC'},
        'compatibility': {'BX', 'EX'},
    }

    PDF_PAGE_OPERATOR_TYPES = {
        k_: k for k, v in PDF_PAGE_OPERATORS.items() for k_ in v
    }

    def __init__(self, page):
        self.page = page
        self.current_path = []
        x0, y0, x1, y1 = page.media_box
        # current transformation matrix
        # • Translations are specified as [1 0 0 1 tx ty], where tx and ty are the distances to translate
        #   the origin of the coordinate system in the horizontal and vertical dimensions, respectively.
        # • Scaling is obtained by [sx 0 0 sy 0 0]. This scales the coordinates so that 1 unit in the
        #   horizontal and vertical dimensions of the new coordinate system is the same size as sx and sy units,
        #   respectively, in the previous coordinate system.
        # • Rotations are produced by [cosθ sinθ −sinθ cosθ 0 0 ], which has the effect of rotating
        #   the coordinate system axes by an angle θ counterclockwise.
        # • Skew is specified by [1 tanα tanβ 1 0 0], which skews the x axis by an angle α and the y axis by an angle β.
        if page.rotate == 90:
            self.ctm = [0, -1, 1, 0, -y0, x1]
        elif page.rotate == 180:
            self.ctm = [-1, 0, 0, -1, x1, y1]
        elif page.rotate == 270:
            self.ctm = [0, 1, -1, 0, y1, -x0]
        else:
            self.ctm = [1, 0, 0, 1, x0, y0]
        self.graphics_states = {
            'line_width': 0,
            'linecap': None,
            'miterlimit': None,
            'dash': None,
            'intent': None,
            'flatness': None,
            'stroking_color': None,
            'stroking_color_space': None,
            'non_stroking_color': None,
            'non_stroking_color_space': None
        }
        self.text_states = {
            'font': None,
            'fontsize': 0,
            'char_spacing': 0,
            'word_spacing': 0,
            'scaling': 100,
            'leading': 0,
            'rendering_mode': 0,
            'rise': 0,
            'text_matrix': self.identity_matrix,
            'line_matrix': self.identity_matrix,
        }
        self.tag_states = {'tag': None, 'properties': {}}
        self.states_stack = []
        self.parameter_stack = []
        self.inline_image_parameters = {}
        self.data = []

    def interpret(self):
        parser = PDFParser(BytesIO(b''.join(content.value for content in self.page.contents)))
        while True:
            try:
                o = parser.next()
            except PDFParserDoneException:
                break

            if isinstance(o, PDFKeyWord):
                operator = o.value.decode()
                if operator not in self.PDF_PAGE_OPERATOR_TYPES:
                    raise PDFInterpreterException(f'Unknown Operator: {o}')

                operator = operator.replace('*', '_s').replace('"', '_dq').replace("'", '_q')
                if hasattr(self, operator):
                    getattr(self, operator)()

                if operator == 'ID':
                    inline_data = parser.read_until(re.compile(rb'[\x00\t\n\f\r ]EI'))
                    self.parameter_stack.append(inline_data)
            else:
                self.parameter_stack.append(o)

    @staticmethod
    def initial_color(color_space):
        if color_space['name'] in {b'DeviceGray', b'DeviceRGB', b'CalGray', b'CalRGB'}:
            initial_color = 0.0
        elif color_space['name'] == b'DeviceCMYK':
            initial_color = [0.0, 0.0, 0.0, 1.0]
        elif color_space['name'] in {b'Lab', b'ICCBased'}:
            initial_color = [0.0] * color_space['value']
        elif color_space['name'] == b'Indexed':
            initial_color = 0
        elif color_space['name'] in {b'Separation', b'DeviceN'}:
            initial_color = 1.0
        elif color_space['name'] == b'Pattern':
            initial_color = None
        else:
            raise PDFInterpreterException('Unknown Color Space')
        return initial_color

    @property
    def identity_matrix(self):
        return [1, 0, 0, 1, 0, 0]

    @staticmethod
    def transform_coordinates(transformation_matrix, x, y):
        # PDF transformation matrices specify the conversion from the transformed coordinate system
        # to the original (untransformed) coordinate system
        a, b, c, d, e, f = transformation_matrix
        x = a * x + c * y + e
        y = b * x + d * y + f
        return x, y

    @staticmethod
    def transform_matrix(m1, m2):
        a1, b1, c1, d1, e1, f1 = m1
        a2, b2, c2, d2, e2, f2 = m2
        a = a1 * a2 + b1 * c2
        b = a1 * b2 + b1 * d2
        c = c1 * a2 + d1 * c2
        d = c1 * b2 + d1 * d2
        e = e1 * a2 + f1 * c2 + e2
        f = e1 * b2 + f1 * d2 + f2
        return [a, b, c, d, e, f]

    # special_graphics_state
    def q(self):
        self.states_stack.append((
            self.ctm,
            self.graphics_states.copy(),
            self.text_states.copy(),
        ))

    def Q(self):
        if self.states_stack:
            self.ctm, self.graphics_states, self.text_states = self.states_stack.pop()

    def cm(self):
        self.ctm = self.transform_matrix(self.parameter_stack[-6:], self.ctm)
        self.parameter_stack = self.parameter_stack[:-6]

    # general_graphics_state
    def w(self):
        self.graphics_states['line_width'] = self.parameter_stack.pop()

    def J(self):
        self.graphics_states['linecap'] = self.parameter_stack.pop()

    def j(self):
        self.graphics_states['linejoin'] = self.parameter_stack.pop()

    def M(self):
        self.graphics_states['miterlimit'] = self.parameter_stack.pop()

    def d(self):
        self.graphics_states['dash'] = self.parameter_stack[-2:]
        self.parameter_stack = self.parameter_stack[:-2]

    def ri(self):
        self.graphics_states['intent'] = self.parameter_stack.pop()

    def i(self):
        self.graphics_states['flatness'] = self.parameter_stack.pop()

    def gs(self):
        return

    # color
    def CS(self):
        p = self.parameter_stack.pop()
        color_space = COLOR_SPACES.get(p.value) or self.page.color_spaces[p.value]
        self.graphics_states['stroking_color_space'] = color_space
        self.graphics_states['stroking_color'] = self.initial_color(color_space)

    def cs(self):
        p = self.parameter_stack.pop()
        color_space = COLOR_SPACES.get(p.value) or self.page.color_spaces[p.value]
        self.graphics_states['non_stroking_color_space'] = color_space
        self.graphics_states['non_stroking_color'] = self.initial_color(color_space)

    def SC(self):
        n = self.graphics_states['stroking_color_space'].get('value') or 1
        self.graphics_states['stroking_color'] = [i.value for i in self.parameter_stack[-n:]]
        self.parameter_stack = self.parameter_stack[:-n]

    def SCN(self):
        color_space_name = self.graphics_states['stroking_color_space'].get('name')
        if color_space_name == b'Pattern':
            name = self.parameter_stack.pop()
        n = self.graphics_states['stroking_color_space'].get('value') or 1
        self.graphics_states['stroking_color'] = [i.value for i in self.parameter_stack[-n:]]
        self.parameter_stack = self.parameter_stack[:-n]

    def sc(self):
        n = self.graphics_states['non_stroking_color_space'].get('value') or 1
        self.graphics_states['non_stroking_color'] = [i.value for i in self.parameter_stack[-n:]]
        self.parameter_stack = self.parameter_stack[:-n]

    def scn(self):
        color_space_name = self.graphics_states['non_stroking_color_space'].get('name')
        if color_space_name == b'Pattern':
            name = self.parameter_stack.pop()
        n = self.graphics_states['non_stroking_color_space'].get('value') or 1
        self.graphics_states['non_stroking_color'] = [i.value for i in self.parameter_stack[-n:]]
        self.parameter_stack = self.parameter_stack[:-n]

    def G(self):
        self.graphics_states['stroking_color_space'] = COLOR_SPACES[b'DeviceGray']
        self.graphics_states['stroking_color'] = self.parameter_stack.pop().value

    def g(self):
        self.graphics_states['non_stroking_color_space'] = COLOR_SPACES[b'DeviceGray']
        self.graphics_states['non_stroking_color'] = self.parameter_stack.pop().value

    def RG(self):
        r, g, b = self.parameter_stack[-3:]
        self.parameter_stack = self.parameter_stack[:-3]
        self.graphics_states['stroking_color_space'] = COLOR_SPACES[b'DeviceRGB']
        self.graphics_states['stroking_color'] = (r.value, g.value, b.value)

    def rg(self):
        r, g, b = self.parameter_stack[-3:]
        self.parameter_stack = self.parameter_stack[:-3]
        self.graphics_states['non_stroking_color_space'] = COLOR_SPACES[b'DeviceRGB']
        self.graphics_states['non_stroking_color'] = (r.value, g.value, b.value)

    def K(self):
        c, m, y, k = self.parameter_stack[-4:]
        self.parameter_stack = self.parameter_stack[:-4]
        self.graphics_states['stroking_color_space'] = COLOR_SPACES[b'DeviceCMYK']
        self.graphics_states['stroking_color'] = (c.value, m.value, y.value, k.value)

    def k(self):
        c, m, y, k = self.parameter_stack[-4:]
        self.parameter_stack = self.parameter_stack[:-4]
        self.graphics_states['non_stroking_color_space'] = COLOR_SPACES[b'DeviceCMYK']
        self.graphics_states['non_stroking_color'] = (c.value, m.value, y.value, k.value)

    # path_construction
    def m(self):
        x, y = self.parameter_stack[-2:]
        self.parameter_stack = self.parameter_stack[:-2]
        self.current_path.append(('m', x.value, y.value))

    def l(self):
        x, y = self.parameter_stack[-2:]
        self.parameter_stack = self.parameter_stack[:-2]
        self.current_path.append(('l', x.value, y.value))

    def c(self):
        x1, y1, x2, y2, x3, y3 = self.parameter_stack[-6:]
        self.parameter_stack = self.parameter_stack[:-6]
        self.current_path.append(('c', x1.value, y1.value, x2.value, y2.value, x3.value, y3.value))

    def v(self):
        x2, y2, x3, y3 = self.parameter_stack[-4:]
        self.parameter_stack = self.parameter_stack[:-4]
        self.current_path.append(('v', x2.value, y2.value, x3.value, y3.value))

    def y(self):
        x1, y1, x3, y3 = self.parameter_stack[-4:]
        self.parameter_stack = self.parameter_stack[:-4]
        self.current_path.append(('y', x1.value, y1.value, x3.value, y3.value))

    def h(self):
        # rectangle
        if len(self.current_path) >= 4 and self.current_path[-4][0] == 'm':
            path = self.current_path[-4:]
            self.current_path = self.current_path[:-4]
            self.current_path.append(('r', path[0][1], path[0][2], path[2][1], path[2][2]))
        else:
            self.current_path.append(('h',))

    def re(self):
        x, y, w, h = self.parameter_stack[-4:]
        self.parameter_stack = self.parameter_stack[:-4]
        self.current_path.append(('m', x.value, y.value))
        self.current_path.append(('l', x.value + w.value, y.value))
        self.current_path.append(('l', x.value + w.value, y.value + h.value))
        self.current_path.append(('l', x.value, y.value + h.value))
        self.h()

    # path_painting
    def S(self):
        begin_point = None
        current_point = None
        for i, *p in self.current_path:
            if i == 'm':
                begin_point = p
                current_point = p
            elif i == 'l' or i == 'h' and current_point != begin_point:
                if i == 'h':
                    p = begin_point
                x0, y0 = self.transform_coordinates(self.ctm, *begin_point)
                x1, y1 = self.transform_coordinates(self.ctm, *p)
                self.data.append({
                    'line': (x0, y0, x1, y1),
                    'line_width': self.graphics_states['line_width'],
                    'stroking_color': self.graphics_states['stroking_color'],
                    'non_stroking_color': self.graphics_states['non_stroking_color']
                })
                current_point = p

        self.current_path = []

    def s(self):
        self.h()
        self.S()

    def f(self):
        for i, *p in self.current_path:
            if i == 'r':
                x0, y0, x1, y1 = p
                x0, y0 = self.transform_coordinates(self.ctm, x0, y0)
                x1, y1 = self.transform_coordinates(self.ctm, x1, y1)
                self.data.append({
                    'rectangle': (x0, y0, x1, y1),
                    'stroking_color': self.graphics_states['stroking_color'],
                    'non_stroking_color': self.graphics_states['non_stroking_color']
                })
        self.current_path = []

    def F(self):
        self.f()

    def f_s(self):
        self.f()
        # self.current_path = []

    def B(self):
        current_path = self.current_path
        self.f()
        self.current_path = current_path
        self.S()
        self.current_path = []

    def B_s(self):
        current_path = self.current_path
        self.f_s()
        self.current_path = current_path
        self.S()
        self.current_path = []

    def b(self):
        self.h()
        self.B()

    def b_s(self):
        self.h()
        self.B_s()

    def n(self):
        self.current_path = []

    def W(self):
        return

    def W_s(self):
        return

    # text_objects
    def BT(self):
        self.text_states['text_matrix'] = self.identity_matrix
        self.text_states['line_matrix'] = self.identity_matrix

    # text_state
    def Tf(self):
        self.text_states['fontsize'] = self.parameter_stack.pop()
        self.text_states['font'] = self.parameter_stack.pop()

    def Tc(self):
        self.text_states['char_spacing'] = self.parameter_stack.pop()

    def Tw(self):
        self.text_states['word_spacing'] = self.parameter_stack.pop()

    def Tz(self):
        self.text_states['scaling'] = self.parameter_stack.pop()

    def TL(self):
        self.text_states['leading'] = self.parameter_stack.pop()

    def Tr(self):
        self.text_states['rendering_mode'] = self.parameter_stack.pop()

    def Ts(self):
        self.text_states['rise'] = self.parameter_stack.pop()

    # text_positioning
    def Td(self):
        ty = self.parameter_stack.pop()
        tx = self.parameter_stack.pop()
        self.text_states['text_matrix'] = self.transform_matrix([1, 0, 0, 1, tx, ty], self.text_states['line_matrix'])
        self.text_states['line_matrix'] = self.text_states['text_matrix'].copy()

    def TD(self):
        self.parameter_stack.append(-self.parameter_stack[-1])
        self.TL()
        self.Td()

    def Tm(self):
        self.text_states['text_matrix'] = self.parameter_stack[-6:]
        self.text_states['line_matrix'] = self.text_states['text_matrix'].copy()
        self.parameter_stack = self.parameter_stack[:-6]

    def T_s(self):
        self.parameter_stack.extend([0, -self.text_states['leading']])
        self.Td()

    # text_showing
    def TJ(self):
        seq = self.parameter_stack.pop()
        # Artifacts are graphics objects that are typically not part of the author’s original content
        # but rather are generated by the PDF producer application in the course of pagination, layout,
        # or other strictly mechanical processes. Artifacts may also be used to describe areas of the document
        # where the author uses a graphical background, with the goal of enhancing the visual experience.
        # In such a case, the background is not required for understanding the content.

        # Note that the identification of what constitutes a word is unrelated to how the text
        # happens to be grouped into show strings. The division into show strings has no semantic significance.
        # In particular, a space or other word-breaking character is still needed
        # even if a word break happens to fall at the end of a show string.

        tag = self.tag_states['tag']
        if self.text_states['font'] is not None:
            font = self.page.fonts[self.text_states['font'].value]
            fontsize = self.text_states['fontsize'].value
            rise = self.text_states['rise']
            rendering_mode = self.text_states['rendering_mode']
            scaling = self.text_states['scaling'] / 100
            char_spacing = self.text_states['char_spacing']
            word_spacing = self.text_states['word_spacing']
            if font.is_multi_byte():
                word_spacing = 0

            tx, ty = 0, 0
            for item in seq:
                if isinstance(item, PDFNumeric):
                    if font.is_vertical():
                        ty = -item.value / 1000 * fontsize
                    else:
                        tx = -item.value / 1000 * fontsize * scaling
                    self.text_states['text_matrix'] = self.transform_matrix(
                        [1, 0, 0, 1, tx, ty],
                        self.text_states['text_matrix']
                    )
                    continue
                for cid in font.decode(item.value):
                    self.data.append({
                        'font_name': font.font_name,
                        'font_size': fontsize,
                        'char': font.to_unicode(cid),
                    })

                    render_matrix = self.transform_matrix(
                        self.transform_matrix(
                            [fontsize * scaling, 0, 0, fontsize, 0, rise + font.descent * fontsize],
                            self.text_states['text_matrix']
                        ),
                        self.ctm
                    )
                    w0 = font.char_horizon_displacement(cid)
                    w1 = font.char_vertical_displacement(cid)
                    x0, y0 = self.transform_coordinates(render_matrix, 0, 0)
                    x1, y1 = self.transform_coordinates(render_matrix, w0, font.height)

                    self.data[-1]['x0'] = x0
                    self.data[-1]['x1'] = x1
                    self.data[-1]['y0'] = y0
                    self.data[-1]['y1'] = y1

                    # Word spacing works the same way as character spacing
                    # but applies only to the space character, code 32.
                    cur_word_spacing = word_spacing if self.data[-1]['char'] == ' ' else 0
                    if font.is_vertical():
                        self.data[-1]['size'] = x1 - x0
                        ty = (w1 * fontsize + char_spacing + cur_word_spacing)
                    else:
                        self.data[-1]['size'] = y1 - y0
                        tx = (w0 * fontsize + char_spacing + cur_word_spacing) * scaling
                    self.text_states['text_matrix'] = self.transform_matrix(
                        [1, 0, 0, 1, tx, ty],
                        self.text_states['text_matrix']
                    )

    def Tj(self):
        s = self.parameter_stack.pop()
        self.parameter_stack.append([s])
        self.TJ()

    def _q(self):
        self.T_s()
        s = self.parameter_stack.pop()
        self.parameter_stack.append([s])
        self.TJ()

    def _dq(self):
        aw, ac, s = self.parameter_stack[-3:]
        self.parameter_stack = self.parameter_stack[:-3]
        self.parameter_stack.extend([s], ac, aw)
        self.Tw()
        self.Tc()
        self.TJ()

    # text_objects
    def ET(self):
        return

    # shading_patterns
    def sh(self):
        return

    # inline_images
    def BI(self):
        self.parameter_stack.append('BI')

    def ID(self):
        tmp = []
        while True:
            p = self.parameter_stack.pop()
            if p == 'BI':
                break
            tmp.append(p)
        tmp.reverse()

        k = None
        for p in tmp:
            if k is None:
                k = p.value
            else:
                self.inline_image_parameters[k] = p
                k = None

    def EI(self):
        o = self.parameter_stack.pop()
        h = self.inline_image_parameters[b'Height'] if b'Height' in self.inline_image_parameters \
            else self.inline_image_parameters.get(b'H')
        w = self.inline_image_parameters[b'Width'] if b'Width' in self.inline_image_parameters \
            else self.inline_image_parameters.get(b'W')

        stream = PDFStream(self.inline_image_parameters, o)

        ctm = self.transform_matrix(stream.dict.get(b'Matrix', [1 / w, 0, 0, 1 / h, 0, 0]), self.ctm)
        x0, y0 = self.transform_coordinates(ctm, 0, 0)
        x1, y1 = self.transform_coordinates(ctm, w, h)
        self.data.append({
            'image': stream.value,
            'x0': x0,
            'y0': y0,
            'x1': x1,
            'y1': y1,
        })
        self.inline_image_parameters = {}

    # x_objects
    def Do(self):
        x_object_name = self.parameter_stack.pop()
        x_object = self.page.x_objects[x_object_name.value]
        subtype = x_object.dict.get(b'Subtype')
        if subtype.value == b'Form' and b'BBox' in x_object.dict:
            x_object.dict[b'MediaBox'] = self.page.media_box
            page = PDFPage(self.page.document, x_object.dict)
            page.contents = [x_object]

            interpreter = PDFPageInterpreter(page)
            interpreter.ctm = self.transform_matrix(x_object.dict.get(b'Matrix', self.identity_matrix), self.ctm)
            interpreter.interpret()
            self.data.extend(interpreter.data)
        elif subtype.value == b'Image':
            h = x_object.dict[b'Height'] if b'Height' in x_object.dict else x_object.dict.get(b'H')
            w = x_object.dict[b'Width'] if b'Width' in x_object.dict else x_object.dict.get(b'W')
            ctm = self.transform_matrix(x_object.dict.get(b'Matrix', [1 / w, 0, 0, 1 / h, 0, 0]), self.ctm)
            x0, y0 = self.transform_coordinates(ctm, 0, 0)
            x1, y1 = self.transform_coordinates(ctm, w, h)
            self.data.append({
                'image': x_object.value,
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
            })

    # marked_content
    def MP(self):
        tag = self.parameter_stack.pop()

    def DP(self):
        properties = self.parameter_stack.pop()
        tag = self.parameter_stack.pop()
        if not isinstance(properties, dict):
            properties = self.page.properties[properties.value]

    def BMC(self):
        tag = self.parameter_stack.pop()
        self.tag_states['tag'] = tag.value
        self.tag_states['properties'] = {}

    def BDC(self):
        properties = self.parameter_stack.pop()
        tag = self.parameter_stack.pop()
        if not isinstance(properties, dict):
            properties = self.page.properties[properties.value]
        self.tag_states['tag'] = tag.value
        self.tag_states['properties'] = properties

    def EMC(self):
        self.tag_states['tag'] = None
        self.tag_states['properties'] = {}
