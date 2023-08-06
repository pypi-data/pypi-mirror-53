import zlib


def flate_decode(data):
    try:
        data = zlib.decompress(data)
    except:
        # encrypted
        data = b''
    return data
