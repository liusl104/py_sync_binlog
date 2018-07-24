#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 这里使用pycrypto‎库
# 按照方法:easy_install pycrypto‎

from Crypto.Cipher import AES
from binascii import a2b_hex
import sys
from sync_binlog.output_log import logger as loging
import uuid
from sync_conf import encryption_strings


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac_addr = "".join([mac[e:e+2] for e in range(0, 11, 2)]) + encryption_strings
    return mac_addr


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, 'KfJ8Tumz%ZTjP9*&')
        try:
            plain_text = cryptor.decrypt(a2b_hex(text))
        except Exception as er:
            loging.critical("请检查配置文件中密码是正确的加密字符串：%s " % er)
            sys.exit()
        return str(plain_text.decode('utf-8')).rstrip('\0')


def decrypt(string):
    pc = prpcrypt(get_mac_address())
    d = pc.decrypt(string)  # 解密
    return d

