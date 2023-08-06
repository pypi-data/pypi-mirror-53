import re
import logging.config

from .config import LOGGING
from .exception import PDFLexerException, PDFLexerEOLException
from .pdfcharset import (
    EOL,
    NON_EOL,
    WHITE_SPACE,
    NON_SPACE,
    REGULAR,
    NON_REGULAR,
    NUMBER,
    NON_NUMBER,
    STRING,
    NON_STRING,
    HEX_STRING,
    NON_HEX_STRING,
    NON_KEYWORD,
)

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()


class Token(object):
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __eq__(self, other):
        return self.name == other.name and self.text == other.text

    def __repr__(self):
        return f'Token("{self.name}", {self.text})'


class PDFLexer(object):

    def __init__(self, fp, buffer_size=4096):
        self.fp = fp
        self.fp.seek(0)

        self._buffer = b''
        self._buffer_size = buffer_size
        self._buffer_position = self.fp.tell()

    def tell(self):
        return self._buffer_position

    def seek(self, position, whence=0):
        self.fp.seek(position, whence)
        self._buffer = b''
        self._buffer_position = self.fp.tell()

    def reversed_lines(self):
        buffer = b''
        self.seek(0, 2)
        cur_pos = self.fp.tell()
        while cur_pos > 0:
            next_pos = max(0, cur_pos - self._buffer_size)
            self.seek(next_pos)
            s = self.fp.read(cur_pos - next_pos)
            if not s:
                break
            buffer = s + buffer

            while EOL.search(buffer):
                lines = re.split(rb'[\r\n]+', buffer)
                buffer = lines.pop(0)
                for line in reversed(lines):
                    yield line
            cur_pos = next_pos

        if buffer:
            yield buffer

    def next_line(self):
        s = self.read_until(EOL)
        self.read_until(NON_EOL)
        return s

    @property
    def buffer(self):
        if not self._buffer:
            self._buffer_position = self.fp.tell()
            self._buffer = self.fp.read(self._buffer_size)
        if not self._buffer:
            raise EOFError()
        return self._buffer

    def look_some(self, num):
        position = self.fp.tell()
        buffer = self._buffer
        buffer_position = self._buffer_position
        s = self.read_some(num)
        self.seek(position)
        self._buffer = buffer
        self._buffer_position = buffer_position
        return s

    def read_some(self, num):
        tmp = []
        while num:
            if len(self.buffer) <= num:
                num -= len(self.buffer)
                tmp.append(self.buffer)
                self._buffer = b''
            else:
                tmp.append(self.buffer[:num])
                self._buffer = self.buffer[num:]
                self._buffer_position += num
                break
        return b''.join(tmp)

    def read_until(self, stop):
        buffer = b''
        match = False
        buffer_length = 0
        while not match:
            buffer += self.buffer
            match = stop.search(buffer)
            buffer_length = len(self._buffer)
            self._buffer = b''
        rest_buffer_length = len(buffer) - match.start()
        self._buffer_position += buffer_length - rest_buffer_length
        self._buffer = buffer[match.start():]
        return buffer[:match.start()]

    def number_token(self):
        s = self.read_until(NUMBER)
        s += self.read_until(NON_NUMBER)
        if b'.' not in s and self.buffer[0:1] == b'.':
            s += self.read_some(1)
            s += self.read_until(NON_NUMBER)
        return Token('real', s) if b'.' in s else Token('integer', s)

    def literal_string_token(self):
        escapes = {
            b'n': b'\n',
            b'r': b'\r',
            b't': b'\t',
            b'b': b'\b',
            b'f': b'\f',
        }

        self.read_some(1)
        s = b''
        level = 0
        while self.buffer:
            if self.buffer[0:1] == b'\\':
                self.read_some(1)
                t = self.read_some(1)
                if t in escapes:
                    s += escapes[t]
                elif t in b'\r\n':
                    while self.buffer[0:1] in b'\r\n':
                        self.read_some(1)
                elif t in b'01234567':
                    while len(t) < 3 and self.buffer[0:1] in b'01234567':
                        t += self.read_some(1)
                    s += bytes([int(t, 8)])
                else:
                    s += t
            elif self.buffer[0:1] == b'(':
                self.read_some(1)
                level += 1
            elif self.buffer[0:1] == b')':
                if level == 0:
                    break
                self.read_some(1)
                level -= 1
            else:
                self.read_until(STRING)
                s += self.read_until(NON_STRING)
        else:
            raise PDFLexerException(f'Missing Parentheses: {s}')
        self.read_some(1)
        return Token('string', s)

    def hex_string_token(self):
        self.read_some(1)
        s = self.read_until(NON_HEX_STRING)
        s = WHITE_SPACE.sub(b'', s)

        tmp = []
        for i in range(len(s)):
            if not i % 2:
                tmp.append(bytes([int(s[i: i + 2], 16)]))
        s = b''.join(tmp)
        self.read_some(1)
        return Token('string', s)

    def array_token(self):
        tokens = []
        self.read_some(1)
        while True:
            self.read_until(NON_SPACE)
            if self.buffer[0:1] == b']':
                break
            tokens.append(self.next_token())
        self.read_some(1)
        return tokens

    def array_begin_token(self):
        s = self.read_some(1)
        return Token('array_begin', s)

    def array_end_token(self):
        s = self.read_some(1)
        return Token('array_end', s)

    def dict_begin_token(self):
        s = self.read_some(2)
        return Token('dict_begin', s)

    def dict_end_token(self):
        s = self.read_some(2)
        return Token('dict_end', s)

    def name_token(self):
        self.read_until(REGULAR)
        s = self.read_until(NON_REGULAR)
        for match in re.finditer(rb'#(?P<hex>[0-9a-f]{2})', s, flags=re.I):
            s = s.replace(match.group(), bytes([int(match.groupdict()['hex'], 16)]))
        return Token('name', s)

    def keyword_token(self):
        s = self.read_until(NON_KEYWORD)
        return Token('keyword', s)

    def next_token(self):
        try:
            self.read_until(NON_SPACE)
            c = self.look_some(1)
        except EOFError:
            raise PDFLexerEOLException()

        if c == b'%':
            self.read_until(EOL)
            token = self.next_token()
        elif c in b'-+.0123456789':
            return self.number_token()
        elif c == b'(':
            token = self.literal_string_token()
        elif c == b'<':
            if self.look_some(2) == b'<<':
                token = self.dict_begin_token()
            else:
                token = self.hex_string_token()
        elif c == b'>':
            if self.look_some(2) == b'>>':
                token = self.dict_end_token()
            else:
                raise PDFLexerException(f'Unexpected char: >')
        elif c == b'[':
            token = self.array_begin_token()
        elif c == b']':
            return self.array_end_token()
        elif c == b'/':
            token = self.name_token()
        else:
            token = self.keyword_token()
        # logger.debug(f"token: {token}")
        return token
