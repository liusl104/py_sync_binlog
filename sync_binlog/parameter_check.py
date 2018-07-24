# encoding=utf8

from sync_conf import *
import sys

if skip_err_code is not None:
    if type(skip_err_code) is not list:
        sys.exit("parameter skip_err_code type is %s is not list type" % str(type(skip_err_code)))
    if type(skip_err_code) is list:
        if len(skip_err_code) == 0:
            sys.exit("parameter skip_err_code can not be empty")
