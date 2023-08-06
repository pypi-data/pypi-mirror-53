
import regex as re

PATTERN = re.compile(
    br'('
    br'(?P<pair>[0-9a-f]{2})'
    br'|\s'
    br')*'
    br'(?P<single>[0-9a-f])?',
    re.IGNORECASE
)


def ascii_hex_decode(data):
    decoded = b''
    match = PATTERN.fullmatch(data)
    if match:
        d = match.capturesdict()
        if d.get('pair'):
            decoded += bytes(int(pair, 16) for pair in d['pair'])
        if d.get('single'):
            decoded += bytes(int(single + b'0', 16) for single in d['single'])
    return decoded
