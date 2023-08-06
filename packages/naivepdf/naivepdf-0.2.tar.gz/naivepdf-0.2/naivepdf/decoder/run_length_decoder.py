

def run_length_decode(data):
    decoded = b''
    i = 0
    while i < len(data):
        length = data[i]
        i += 1
        if 0 <= length < 128:
            decoded += bytes(data[i: i + (length + 1)])
            i += (length + 1)
        elif 128 < length < 256:
            decoded += bytes(data[i] * (257 - length))
            i += 1
        else:
            break
    return decoded
