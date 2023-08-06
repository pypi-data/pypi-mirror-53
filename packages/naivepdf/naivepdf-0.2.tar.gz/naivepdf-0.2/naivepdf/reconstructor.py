

class PageReconstructor(object):
    THRESHOLD = 3

    def __init__(self, page):
        self.page = page
        self.horizontal_lines = {}
        self.vertical_lines = {}
        self.vertical_lines_groups = {}

        self.chars_box = [None, None, None, None]
        self.chars_ids = {}
        self.chars = {}
        self.ys = []
        self.strings = {}

        self.vertical_borders = {}
        self.horizontal_borders = {}
        self.tables = []

    def near_enough(self, a, b):
        return abs(a - b) < self.THRESHOLD

    def reconstruct(self):
        self.read_lines()
        self.horizontal_lines = self.join_lines(self.merge_lines(self.horizontal_lines))
        self.vertical_lines_groups = {
            k: self.join_lines(self.merge_lines(v)) for k, v in self.group_lines(self.vertical_lines).items()
        }
        self.vertical_lines = {}
        for k, vertical_lines in self.vertical_lines_groups.items():
            for x, lines in vertical_lines.items():
                if x not in self.vertical_lines:
                    self.vertical_lines[x] = []
                self.vertical_lines[x].extend(lines)
        self.read_chars()
        self.read_vertical_borders()
        self.read_tables()
        return sorted(list(self.strings.values()) + self.tables, key=lambda x: x['bounds'][1], reverse=True)

    def read_lines(self):
        for item in self.page['data']:
            if 'rectangle' in item or 'line' in item:
                x0, y0, x1, y1 = item.get('rectangle') or item.get('line')
                x0, x1 = min(x0, x1), max(x0, x1)
                y0, y1 = min(y0, y1), max(y0, y1)
                # 竖线
                if self.near_enough(x0, x1):
                    if x0 not in self.vertical_lines:
                        self.vertical_lines[x0] = []
                    self.vertical_lines[x0].append((y0, y1))
                # 横线
                elif self.near_enough(y0, y1):
                    if y0 not in self.horizontal_lines:
                        self.horizontal_lines[y0] = []
                    self.horizontal_lines[y0].append((x0, x1))

    def merge_lines(self, lines):
        merged_lines = {}
        ps = []
        for p in sorted(lines.keys()):
            if not ps or not self.near_enough(ps[-1], p):
                ps.append(p)
                merged_lines[p] = lines[p]
            else:
                if isinstance(lines[p], list):
                    merged_lines[ps[-1]].extend(lines[p])
                elif isinstance(lines[p], dict):
                    merged_lines[ps[-1]].update(lines[p])
        return merged_lines

    def join_lines(self, lines):
        joint_lines = {}
        for p in lines.keys():
            tmp_lines = []
            begin, end = None, None
            for b, e in sorted(lines[p]):
                if begin is None:
                    begin, end = b, e
                else:
                    if b <= end or self.near_enough(b, end):
                        end = max(e, end)
                    else:
                        tmp_lines.append((begin, end))
                        begin, end = b, e
            if begin is not None:
                tmp_lines.append((begin, end))
            joint_lines[p] = tmp_lines
        return joint_lines

    def group_lines(self, lines):
        lines_group = {}
        lines_groups = {}
        begin, end = None, None
        for p, b, e in sorted([(p, b, e) for p, v in lines.items() for b, e in v], key=lambda x: x[1]):
            if end is None:
                begin, end = b, e
            if b <= end or self.near_enough(b, end):
                end = max(e, end)
                if p not in lines_group:
                    lines_group[p] = []
                lines_group[p].append((b, e))
            else:
                lines_groups[(begin, end)] = lines_group
                begin, end = b, e
                lines_group = {}
        if lines_group:
            lines_groups[(begin, end)] = lines_group
        return lines_groups

    def read_chars(self):
        chars = {}
        heights = {}
        widths = {}
        for i, item in enumerate(self.page['data']):
            if 'char' not in item:
                continue
            self.chars_ids[i] = item
            if self.chars_box[0] is None or item['x0'] < self.chars_box[0]:
                self.chars_box[0] = item['x0']
            if self.chars_box[1] is None or item['y0'] < self.chars_box[1]:
                self.chars_box[1] = item['y0']
            if self.chars_box[2] is None or item['x1'] > self.chars_box[2]:
                self.chars_box[2] = item['x1']
            if self.chars_box[3] is None or item['y1'] > self.chars_box[3]:
                self.chars_box[3] = item['y1']
            x, y = (item['x0'] + item['x1']) / 2, (item['y0'] + item['y1']) / 2
            if y not in chars:
                chars[y] = {}
                heights[y] = {'y0': item['y0'], 'y1': item['y1']}
                widths[y] = {'x0': item['x0'], 'x1': item['x1']}
            else:
                heights[y]['y0'] = min(heights[y]['y0'], item['y0'])
                heights[y]['y1'] = max(heights[y]['y1'], item['y1'])
                widths[y]['x0'] = min(widths[y]['x0'], item['x0'])
                widths[y]['x1'] = max(widths[y]['x1'], item['x1'])

            if x not in chars[y]:
                chars[y][x] = i

        for y in sorted(chars, reverse=True):
            if not self.ys:
                self.ys.append(y)
                self.chars[y] = chars[y]
                continue

            y_ = self.ys[-1]
            min_range = min(
                heights[y_]['y1'] - heights[y_]['y0'],
                heights[y]['y1'] - heights[y]['y0']
            )
            if heights[y_]['y1'] - heights[y]['y0'] < min_range / 2 \
                    or heights[y]['y1'] - heights[y_]['y0'] < min_range / 2:
                self.ys.append(y)
                self.chars[y] = chars[y]
            else:
                self.chars[y_].update(chars[y])
                heights[y_]['y0'] = min(heights[y]['y0'], heights[y_]['y0'])
                heights[y_]['y1'] = max(heights[y]['y1'], heights[y_]['y1'])
                widths[y_]['x0'] = min(widths[y]['x0'], widths[y_]['x0'])
                widths[y_]['x1'] = max(widths[y]['x1'], widths[y_]['x1'])
        for y in reversed(self.ys):
            self.strings[y] = {
                'text': ''.join(self.chars_ids[self.chars[y][x]]['char'] for x in sorted(self.chars[y])),
                'bounds': [widths[y]['x0'], heights[y]['y0'], widths[y]['x1'], heights[y]['y1']]
            }

    def read_vertical_borders(self):
        for (y0, y1), vertical_lines in self.vertical_lines_groups.items():
            ys = []
            for y in reversed(self.ys):
                if y < y0:
                    continue
                if y > y1:
                    break
                ys.append(y)

            if ys:
                for y in ys:
                    del self.strings[y]
                self.add_vertical_borders(vertical_lines)
                horizontal_lines = self.read_horizontal_borders(vertical_lines)
                self.add_horizontal_borders(horizontal_lines)

    def read_horizontal_borders(self, vertical_lines):
        horizontal_lines = {}

        y0s, y1s = [], []
        for x, lines in vertical_lines.items():
            for y0, y1 in lines:
                y0s.append(y0)
                y1s.append(y1)
        if not y0s:
            return horizontal_lines

        y0, y1 = min(y0s), max(y1s)
        for y in self.horizontal_lines:
            if y0 <= y <= y1 or self.near_enough(y, y0) or self.near_enough(y, y1):
                horizontal_lines[y] = self.horizontal_lines[y]

        return horizontal_lines

    def add_vertical_borders(self, vertical_lines):
        vertical_borders = {}
        y0, y1 = None, None
        for x, lines in vertical_lines.items():
            if not lines:
                continue
            y0_ = min(ly0 for ly0, ly1 in lines)
            y1_ = max(ly1 for ly0, ly1 in lines)
            if y0 is None or y0 > y0_:
                y0 = y0_
            if y1 is None or y1 < y1_:
                y1 = y1_
            if x not in self.vertical_borders:
                vertical_borders[x] = lines
            else:
                vertical_borders[x].extend(lines)
        self.vertical_borders[y0, y1] = vertical_borders

    def add_horizontal_borders(self, horizontal_lines):
        for y, lines in horizontal_lines.items():
            if y not in self.horizontal_borders:
                self.horizontal_borders[y] = lines
            else:
                self.horizontal_borders[y].extend(lines)

    def read_tables(self):
        horizontal_border_ys = sorted(self.horizontal_borders.keys())
        for (b, e), vertical_borders in self.vertical_borders.items():
            table = {
                'bounds': [None, b, None, e],
                'horizontal_borders': {},
                'vertical_borders': vertical_borders,
                'cells': {},
                'width': 0,
                'height': 0,
            }
            for i, y in enumerate(horizontal_border_ys):
                if b > y and not self.near_enough(b, y):
                    continue
                if b <= y <= e or self.near_enough(b, y) or self.near_enough(e, y):
                    table['horizontal_borders'][y] = self.horizontal_borders[y]
                    for x0, x1 in self.horizontal_borders[y]:
                        if table['bounds'][0] is None or x0 < table['bounds'][0]:
                            table['bounds'][0] = x0
                        if table['bounds'][2] is None or x1 > table['bounds'][2]:
                            table['bounds'][2] = x1
                else:
                    horizontal_border_ys = horizontal_border_ys[i:]
                    break

            if not table['vertical_borders'] or not table['horizontal_borders']:
                continue

            text_ids = self.crop([table['bounds'][0], table['bounds'][1], min(table['vertical_borders']), table['bounds'][3]])
            if any(self.chars_ids[i]['char'].strip() for i in text_ids):
                table['vertical_borders'][table['bounds'][0]] = [(table['bounds'][1], table['bounds'][3])]
            else:
                table['vertical_borders'][min(table['vertical_borders'])] = [(table['bounds'][1], table['bounds'][3])]

            text_ids = self.crop([max(table['vertical_borders']), table['bounds'][1], table['bounds'][2], table['bounds'][3]])
            if any(self.chars_ids[i]['char'].strip() for i in text_ids):
                table['vertical_borders'][table['bounds'][2]] = [(table['bounds'][1], table['bounds'][3])]
            else:
                table['vertical_borders'][max(table['vertical_borders'])] = [(table['bounds'][1], table['bounds'][3])]

            text_ids = self.crop([table['bounds'][0], table['bounds'][1], table['bounds'][2], min(table['horizontal_borders'])])
            if any(self.chars_ids[i]['char'].strip() for i in text_ids):
                table['horizontal_borders'][table['bounds'][1]] = [(table['bounds'][0], table['bounds'][2])]
            else:
                table['horizontal_borders'][min(table['horizontal_borders'])] = [(table['bounds'][0], table['bounds'][2])]

            text_ids = self.crop([table['bounds'][0], max(table['horizontal_borders']), table['bounds'][2], table['bounds'][3]])
            if any(self.chars_ids[i]['char'].strip() for i in text_ids):
                table['horizontal_borders'][table['bounds'][3]] = [(table['bounds'][0], table['bounds'][2])]
            else:
                table['horizontal_borders'][max(table['horizontal_borders'])] = [(table['bounds'][0], table['bounds'][2])]

            self.read_cells(table)
            if not table['cells']:
                continue
            table['width'] = max(i[1] for i in table['cells']) + 1
            table['height'] = max(i[0] for i in table['cells']) + 1
            self.tables.append(table)

    def read_cells(self, table):
        cells = table['cells']
        horizontal_borders = table['horizontal_borders']
        vertical_borders = table['vertical_borders']
        x0, y1 = None, None
        for i, y in enumerate(sorted(horizontal_borders.keys(), reverse=True)):
            if i == 0:
                y1 = y
                continue
            for j, x in enumerate(sorted(vertical_borders.keys())):
                if j == 0:
                    x0 = x
                    continue

                left_merged = self.is_merged((y1 + y) / 2, vertical_borders[x0])
                up_merged = self.is_merged((x0 + x) / 2, horizontal_borders[y1])

                current_cell_i = i - 1
                current_cell_j = j - 1
                cells[(current_cell_i, current_cell_j)] = {
                    'bounds': [x0, y, x, y1],
                    'text': '',
                    'left_merged': left_merged,
                    'up_merged': up_merged,
                }
                while left_merged or up_merged:
                    if left_merged:
                        if not current_cell_j:
                            break
                        current_cell_j -= 1
                        cells[(current_cell_i, current_cell_j)]['bounds'][2] = x
                        cells[(current_cell_i, current_cell_j)]['bounds'][3] = y
                    elif up_merged:
                        if not current_cell_i:
                            break
                        current_cell_i -= 1
                        cells[(current_cell_i, current_cell_j)]['bounds'][2] = x
                        cells[(current_cell_i, current_cell_j)]['bounds'][3] = y
                    left_merged = cells[(current_cell_i, current_cell_j)]['left_merged']
                    up_merged = cells[(current_cell_i, current_cell_j)]['up_merged']

                x0 = x
            y1 = y

        for cell in table['cells'].values():
            cell['text'] = ''
            for text in [self.chars_ids[i] for i in self.crop(cell['bounds'])]:
                cell['text'] += text['char']

    def is_merged(self, p, lines):
        for b, e in lines:
            if b <= p <= e or self.near_enough(p, b) or self.near_enough(e, p):
                return False
        return True

    def crop(self, bounds):
        text_ids = []
        x0, y0, x1, y1 = bounds
        for y in self.ys:
            if y + self.THRESHOLD < y0:
                continue
            if y > y1 + self.THRESHOLD:
                continue
            for x in sorted(self.chars[y]):
                text = self.chars_ids[self.chars[y][x]]
                x0_, y0_, x1_, y1_ = text['x0'], text['y0'], text['x1'], text['y1']
                tx, ty = (x0_ + x1_) / 2, (y0_ + y1_) / 2
                if y0 < ty < y1 and x0 < tx < x1:
                    text_ids.append(self.chars[y][x])
        return text_ids
