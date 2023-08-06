import struct


def pack(code, length):
    return struct.pack('>L', code)[-length:]


def unpack(s):
    length = len(s)
    if length == 1:
        return ord(s)
    elif length == 2:
        return struct.unpack('>H', s)[0]
    elif length == 3:
        return struct.unpack('>L', b'\x00'+s)[0]
    elif length == 4:
        return struct.unpack('>L', s)[0]
    elif length == 8:
        return struct.unpack('>Q', s)[0]
