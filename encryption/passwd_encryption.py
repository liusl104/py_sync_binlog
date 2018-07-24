# encoding=utf8

# 这里使用pycrypto‎库
# 按照方法:easy_install pycrypto‎

from Crypto.Cipher import AES
from binascii import b2a_hex
import sys
import uuid
import sync_conf


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac_addr = "".join([mac[e:e+2] for e in range(0, 11, 2)]) + sync_conf.encryption_strings
    return mac_addr


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, 'KfJ8Tumz%ZTjP9*&')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)


pc = prpcrypt(get_mac_address())  # 初始化密钥

if len(sys.argv) == 2:
    e = pc.encrypt(sys.argv[1])  # 加密
    print('Your encrypted string: %s ' % e)
else:
    password = input('Please enter a string that you need to encrypt: ')
    e = pc.encrypt(password)
    print('Your encrypted string: %s' % e.decode('utf-8'))

