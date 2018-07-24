# encoding=utf8

import os
import uuid
from sync_binlog.output_log import logger as loging


def get_auto_uuid_cnf():
    # 判断auto.cnf文件是否存在
    auto_cnf_file_path = "%s/auto_cnf/auto.cnf" % os.path.abspath('.')
    if os.path.exists(auto_cnf_file_path):
        auto = open(auto_cnf_file_path, 'r', encoding='utf-8')
        server_uuid = auto.readline()
        auto.close()
        if len(server_uuid) != 36:
            server_uuid = uuid.uuid1()
            auto = open(auto_cnf_file_path, 'w', encoding='utf-8')
            auto.write(str(server_uuid))
            auto.close()
        return server_uuid
    else:
        server_uuid = uuid.uuid1()
        auto = open(auto_cnf_file_path, 'w', encoding='utf-8')
        auto.write(str(server_uuid))
        auto.close()
        loging.warning("未能发现UUID存储文件，自动创建UUID:%s" % server_uuid)
        return server_uuid


