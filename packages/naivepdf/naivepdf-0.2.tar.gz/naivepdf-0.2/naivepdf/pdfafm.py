import os
from .encoding.encoding import glyph_name_to_unicode


class AFMLoader(object):
    def __init__(self):
        self.fonts = {}
        self.load_afm()

    def load_afm(self):
        afm_path = os.path.join(os.path.dirname(__file__), 'Adobe-Core35_AFMs-314')
        for d in os.listdir(afm_path):
            if not d.endswith('.afm'):
                continue
            font = {
                'descriptor': {},
                'metrics': {},
            }
            with open(os.path.join(afm_path, d)) as f:
                for line in f:
                    line = line.strip().replace('\t', ' ')
                    if not line:
                        continue
                    row = line.split(' ')

                    k1 = {
                        'FontName': b'FontName',
                        'FamilyName': b'FontFamily',
                        'Weight': b'FontFamily'
                    }
                    k2 = {
                        'Ascender': b'Ascent',
                        'Descender': b'Descent',
                        'CapHeight': b'CapHeight',
                        'XHeight': b'XHeight',
                        'ItalicAngle': b'ItalicAngle',
                    }

                    if row[0] in k1:
                        font['descriptor'][k1[row[0]]] = row[1]
                    elif row[0] in k2:
                        font['descriptor'][k2[row[0]]] = float(row[1])
                    elif row[0] == 'IsFixedPitch' and row[1].lower() == 'true':
                        font['descriptor'][b'Flags'] = 64
                    elif row[0] == 'FontBBox':
                        font['descriptor'][b'FontBBox'] = tuple(map(float, row[1:5]))
                    elif row[0] == 'C':
                        row = line.split(';')
                        char = None
                        metrics = {}
                        for l in row:
                            r = l.strip().split(' ')
                            if r[0] == 'N':
                                char = glyph_name_to_unicode(r[1])
                            elif r[0] in {'C', 'WX'}:
                                metrics[r[0]] = int(r[1])
                            elif r[0] == 'B':
                                metrics['B'] = tuple(map(float, r[1:5]))
                        if char is not None:
                            font['metrics'][char] = metrics
            if font['descriptor'].get(b'FontName'):
                self.fonts[font['descriptor'][b'FontName']] = font


afm_loader = AFMLoader()