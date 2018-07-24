# coding: utf-8

from Crypto.Cipher import AES
import base64
from sync_conf import *
from sync_binlog.Decrypt import decrypt

# 不足16位补位
PADDING = '\0'
pad_it = lambda s: s+(16 - len(s) % 16)*PADDING

# 加密密钥和偏移值


key_values = decrypt(key)
iv_valyes = decrypt(iv)


def ase_encryption(datastr, key_values=key_values, iv_valyes=iv_valyes, pad_it=pad_it):
    """
    :param datastr:
    :param key_values:
    :param iv_valyes:
    :param pad_it:
    :return:
    """
    # 将加密字符串转成base64再转义为bytes
    source_value = base64.b64encode(datastr.encode('utf-8')).decode('utf-8')
    # 加密初始化
    generator = AES.new(key_values, AES.MODE_CBC, iv_valyes)
    crypt = generator.encrypt(pad_it(source_value))
    cryptedStr = base64.b64encode(crypt)
    data = cryptedStr.decode('utf-8')
    return data


def aes_decrypt(datastr, key_values=key_values, iv_valyes=iv_valyes):
    """
    :param datastr:
    :param key_values:
    :param iv_valyes:
    :return:
    """
    endata = datastr.encode('utf-8')
    crdStr = base64.b64decode(endata)
    generator = AES.new(key_values, AES.MODE_CBC, iv_valyes)
    recovery = generator.decrypt(crdStr)
    data = base64.b64decode(recovery.decode('utf-8')).decode('utf-8')
    return data




