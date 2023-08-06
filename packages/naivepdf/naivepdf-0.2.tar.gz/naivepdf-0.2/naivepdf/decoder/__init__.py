
from .ascii_85_decoder import ascii_85_decode
from .ascii_hex_decoder import ascii_hex_decode
from .flate_decoder import flate_decode
from .lzw_decoder import lzw_decode
from .run_length_decoder import run_length_decode


DECODER_MAP = {
    b'FlateDecode': flate_decode,
    b'Fl': flate_decode,

    b'LZWDecode': lzw_decode,
    b'LZW': lzw_decode,

    b'ASCII85Decode': ascii_85_decode,
    b'A85': ascii_85_decode,

    b'ASCIIHexDecode': ascii_hex_decode,
    b'AHx': ascii_hex_decode,

    b'RunLengthDecode': run_length_decode,
    b'RL': run_length_decode,

    b'CCITTFaxDecode': None,
    b'CCF': None,

    b'DCTDecode': None,
    b'DCT': None,

    b'JBIG2Decode': None,
    b'JBIG2': None,
}


__all__ = [
    'DECODER_MAP',

    'ascii_85_decode',
    'ascii_hex_decode',
    'flate_decode',
    'lzw_decode',
    'run_length_decode',
]
