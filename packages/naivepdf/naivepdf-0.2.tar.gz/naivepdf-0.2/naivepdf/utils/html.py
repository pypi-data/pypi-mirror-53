

def html(f, data):
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
    f.write('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">')
    _html(f, data)


def _html(f, data):
    for d in data:
        if 'text' in d:
            for t in d['text'].split('\n'):
                f.write(f"<p style='text-indent:2em'>{t}</p>")
        elif 'cells' in d:
            f.write('<table border="1" cellspacing="0">')
            for i in range(d['height']):
                f.write('<tr>')
                for j in range(d['width']):
                    if d['cells'][i, j]['left_merged'] or d['cells'][i, j]['up_merged']:
                        continue
                    colspan = 1
                    while colspan < d['width'] - j and d['cells'][i, j + colspan]['left_merged']:
                        colspan += 1
                    rowspan = 1
                    while rowspan < d['height'] - i and d['cells'][i + rowspan, j]['up_merged']:
                        rowspan += 1
                    f.write(f"<td colspan='{colspan}' rowspan='{rowspan}'>{d['cells'][i, j]['text']}</td>")
                f.write('</tr>')
            f.write('</table>')

