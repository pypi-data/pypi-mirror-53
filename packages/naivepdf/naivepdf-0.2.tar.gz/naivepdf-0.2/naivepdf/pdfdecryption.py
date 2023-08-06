
import struct
import hashlib as md5
from Crypto.Cipher import AES, ARC4
from Crypto.Hash import SHA256


class PDFStandardDecryption(object):
    PASSWORD_PADDING = b'(\xbfN^Nu\x8aAd\x00NV\xff\xfa\x01\x08..\x00\xb6\xd0h>\x80/\x0c\xa9\xfedSiz'

    def __init__(self, ids, param, password=''):
        self.ids = ids
        self.param = param
        self.password = password

    @property
    def key(self):
        return self.authenticate(self.password)

    @property
    def is_printable(self):
        return bool(self.param[b'P'] & 4)

    @property
    def is_modifiable(self):
        return bool(self.param[b'P'] & 8)

    @property
    def is_extractable(self):
        return bool(self.param[b'P'] & 16)

    def compute_u(self, key):
        if self.param[b'R'] == 2:
            # Algorithm 3.4
            return ARC4.new(key).encrypt(self.PASSWORD_PADDING)  # 2
        else:
            # Algorithm 3.5
            h = md5.md5(self.PASSWORD_PADDING)  # 2
            h.update(self.ids[0].value)  # 3
            result = ARC4.new(key).encrypt(h.digest())  # 4
            for i in range(1, 20):  # 5
                result = ARC4.new(bytes(c ^ i for c in key)).encrypt(result)
            result += result  # 6
            return result

    def compute_encryption_key(self, password):
        # Algorithm 3.2
        password = (password + self.PASSWORD_PADDING)[:32]  # 1
        h = md5.md5(password)  # 2
        h.update(self.param[b'O'].value)  # 3
        h.update(struct.pack('<l', self.param[b'P'].value))  # 4
        h.update(self.ids[0].value)  # 5
        if self.param[b'R'] >= 4:
            if not self.param.get(b'EncryptMetadata', True):
                h.update(b'\xff\xff\xff\xff')
        result = h.digest()
        n = 5
        if self.param[b'R'] >= 3:
            n = self.param[b'Length'] // 8
            for _ in range(50):
                result = md5.md5(result[:n]).digest()
        return result[:n]

    def authenticate(self, password):
        password = password.encode("latin1")
        key = self.authenticate_user_password(password)
        if key is None:
            key = self.authenticate_owner_password(password)
        return key

    def authenticate_user_password(self, password):
        key = self.compute_encryption_key(password)
        if self.verify_encryption_key(key):
            return key
        return b''

    def verify_encryption_key(self, key):
        # Algorithm 3.6
        u = self.compute_u(key)
        if self.param[b'R'] == 2:
            return u == self.param[b'U'].value
        return u[:16] == self.param[b'U'].value[:16]

    def authenticate_owner_password(self, password):
        # Algorithm 3.7
        password = (password + self.PASSWORD_PADDING)[:32]
        h = md5.md5(password)
        if self.param[b'R'] >= 3:
            for _ in range(50):
                h = md5.md5(h.digest())
        n = 5
        if self.param[b'R'] >= 3:
            n = self.param[b'Length'] // 8
        key = h.digest()[:n]
        if self.param[b'R'] == 2:
            user_password = ARC4.new(key).decrypt(self.param[b'O'].value)
        else:
            user_password = self.param[b'O'].value
            for i in range(19, -1, -1):
                user_password = ARC4.new(bytes(c ^ i for c in key)).decrypt(user_password)
        return self.authenticate_user_password(user_password)

    def decrypt(self, objid, genno, data, attrs=None):
        return self.decrypt_rc4(objid, genno, data)

    def decrypt_rc4(self, objid, genno, data):
        key = self.key + struct.pack('<L', objid)[:3] + struct.pack('<L', genno)[:2]
        h = md5.md5(key)
        key = h.digest()[:min(len(key), 16)]
        return ARC4.new(key).decrypt(data)


class PDFStandardDecryptionV4(PDFStandardDecryption):

    def __init__(self, ids, param, password=''):
        param[b'Length'] = 128
        super().__init__(ids, param, password)
        self.cfm = {k: self.get_cfm(v[b'CFM']) for k, v in self.param[b'CF'].items()}
        self.cfm[b'Identity'] = self.decrypt_identity

    def get_cfm(self, name):
        if name == b'V2':
            return self.decrypt_rc4
        elif name == b'AESV2':
            return self.decrypt_aes128
        return None

    def decrypt(self, objid, genno, data, attrs=None, name=None):
        if not self.param.get(b'EncryptMetadata', True) and attrs is not None:
            if attrs.get(b'Type') == b'Metadata':
                return data
        if name is None:
            name = self.param[b'StrF'].value
        return self.cfm[name](objid, genno, data)

    def decrypt_identity(self, objid, genno, data):
        return data

    def decrypt_aes128(self, objid, genno, data):
        key = self.key + struct.pack('<L', objid)[:3] + struct.pack('<L', genno)[:2] + b'sAlT'
        h = md5.md5(key)
        key = h.digest()[:min(len(key), 16)]
        return AES.new(key, mode=AES.MODE_CBC, IV=data[:16]).decrypt(data[16:])


class PDFStandardDecryptionV5(PDFStandardDecryptionV4):
    def __init__(self, ids, param, password=''):
        param[b'Length'] = 256
        super().__init__(ids, param, password)

    def get_cfm(self, name):
        if name == 'AESV3':
            return self.decrypt_aes256
        return None

    def authenticate(self, password):
        password = password.encode('utf-8')[:127]
        h = SHA256.new(password)
        h.update(self.param[b'O'].value[32:40])
        h.update(self.param[b'U'].value)
        if h.digest() == self.param[b'O'].value[:32]:
            h = SHA256.new(password)
            h.update(self.param[b'O'].value[40:])
            h.update(self.param[b'U'].value)
            return AES.new(h.digest(), mode=AES.MODE_CBC, IV=b'\x00' * 16).decrypt(self.param[b'OE'].value)
        h = SHA256.new(password)
        h.update(self.param[b'U'].value[32:40])
        if h.digest() == self.param[b'U'].value[:32]:
            h = SHA256.new(password)
            h.update(self.param[b'U'].value[40:])
            return AES.new(h.digest(), mode=AES.MODE_CBC, IV=b'\x00' * 16).decrypt(self.param[b'UE'].value)
        return None

    def decrypt_aes256(self, objid, genno, data):
        return AES.new(self.key, mode=AES.MODE_CBC, IV=data[:16]).decrypt(data[16:])


decryption = {
    1: PDFStandardDecryption,
    2: PDFStandardDecryption,
    4: PDFStandardDecryptionV4,
    5: PDFStandardDecryptionV5,
}
