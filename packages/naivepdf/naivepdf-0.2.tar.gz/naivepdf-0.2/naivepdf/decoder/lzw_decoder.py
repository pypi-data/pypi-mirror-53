from io import BytesIO


class CorruptDataException(Exception):
    pass


class LZWDecoder(object):
    def __init__(self, fp=None):
        self.fp = fp
        self.next_read_num = 9
        self.table = []
        self.prev = b''
        self._buffer = None
        self._buffer_remain = 0

    @property
    def buffer(self):
        if self._buffer_remain == 0:
            tmp = self.fp.read(1)
            if not tmp:
                raise EOFError()
            self._buffer = ord(tmp)
            self._buffer_remain = 8
        return self._buffer

    def read(self):
        num = self.next_read_num
        code = 0
        while num:
            buffer = self.buffer
            if self._buffer_remain < num:
                num -= self._buffer_remain
                code = (code << self._buffer_remain) | (buffer & ((1 << self._buffer_remain) - 1))
                self._buffer_remain = 0
            else:
                self._buffer_remain -= num
                code = (code << num) | ((buffer >> self._buffer_remain) & ((1 << num) - 1))
                break
        return code

    def feed(self, code):
        data = b''
        if code == 256:
            self.table = [bytes([c]) for c in range(256)]  # 0-255
            self.table.append(None)  # 256
            self.table.append(None)  # 257
            self.prev = b''
            self.next_read_num = 9
        elif code == 257:
            pass
        elif not self.prev:
            data = self.table[code]
            self.prev = data
        else:
            if code < len(self.table):
                data = self.table[code]
                self.table.append(self.prev + data[:1])
            elif code == len(self.table):
                self.table.append(self.prev + self.prev[:1])
                data = self.table[code]
            else:
                raise CorruptDataException
            table_length = len(self.table)
            if table_length == 511:
                self.next_read_num = 10
            elif table_length == 1023:
                self.next_read_num = 11
            elif table_length == 2047:
                self.next_read_num = 12
            self.prev = data
        return data

    def decode(self):
        while True:
            try:
                code = self.read()
            except EOFError:
                break
            try:
                data = self.feed(code)
            except CorruptDataException:
                break
            yield data


def lzw_decode(data):
    fp = BytesIO(data)
    decoder = LZWDecoder(fp)
    return b''.join(decoder.decode())
