import struct


def ascii_85_decode(data):
    decoded = b''
    n = b = 0
    for c in data:
        if b'!' <= c <= b'u':
            n += 1
            b = b * 85 + (ord(c) - 33)
            if n == 5:
                decoded += struct.pack('>L', b)
                n = b = 0
        elif c == b'z':
            decoded += b'\0\0\0\0'
        elif c == b'~':
            if n:
                for _ in range(5-n):
                    b = b * 85 + 84
                decoded += struct.pack('>L', b)[:n-1]
            break
    return decoded
