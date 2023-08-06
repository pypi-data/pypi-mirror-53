import re
import logging.config

from .latin_character_encoding import LATIN_CHARACTER_ENCODINGS
from .glyphlist import GLYPH_TO_UNICODE
from .zapfdingbats import ZAPFDINGBATS
from ..config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()

STRIP_NAME = re.compile(r'uni([0-9]+)')


def glyph_name_to_unicode(name):
    if name in GLYPH_TO_UNICODE:
        return GLYPH_TO_UNICODE[name]
    if name in ZAPFDINGBATS:
        return ZAPFDINGBATS[name]

    # uni2713: '\u2713'
    m = STRIP_NAME.search(name)
    if not m:
        raise KeyError(name)
    return chr(int(m.group(1), 16))


ENCODINGS = {
    b'StandardEncoding': {},
    b'MacRomanEncoding': {},
    b'WinAnsiEncoding': {},
    b'PDFDocEncoding': {},
}

for (glyph_name, std, mac, win, pdf) in LATIN_CHARACTER_ENCODINGS:
    u = glyph_name_to_unicode(glyph_name)
    if std:
        ENCODINGS[b'StandardEncoding'][std] = u
    if mac:
        ENCODINGS[b'MacRomanEncoding'][mac] = u
    if win:
        ENCODINGS[b'WinAnsiEncoding'][win] = u
    if pdf:
        ENCODINGS[b'PDFDocEncoding'][pdf] = u


def get_encoding(name, differences=None):
    cid_to_unicode = ENCODINGS.get(name, ENCODINGS[b'StandardEncoding']).copy()
    if differences:
        cid = 0
        for d in differences:
            if isinstance(d, int):
                cid = d
            else:
                try:
                    cid_to_unicode[cid] = glyph_name_to_unicode(d.decode())
                except KeyError:
                    pass
                    # logger.warning(f'no cid name: {cid}, {d.decode()}')
                    # Type3 CharProcs
                cid += 1
    return cid_to_unicode
