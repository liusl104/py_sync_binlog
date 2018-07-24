# encoding=utf8

from sync_conf import merge_db_table, merge_table_rule
import sys
from sync_binlog.output_log import logger as loging


def merge_init_replicate_do_table(merge_table_rule):
    old_db = []
    new_db = []
    old_tb = []
    new_tb = []
    for db in merge_table_rule["database"]:
        for i in db:
            old_db.append(i)
            new_db.append(db[i])
    for name in merge_table_rule["table_map"]:
        for i in name:
            old_tb.append(i)
            new_tb.append(name[i])
    return {"old_db": old_db, "new_db": new_db, "old_tb": old_tb, "new_tb": new_tb}


try:
    rule = merge_init_replicate_do_table(merge_table_rule)
except Exception as e:
    loging.critical(e)
    sys.exit(e)


def merge_replicate_table(db_name, table_name=None):
    if merge_db_table is False:
        if table_name is not None:
            return db_name, table_name
        else:
            return db_name
    else:
        if table_name is not None:
            try:
                db = rule["new_db"][rule["old_db"].index(db_name)]
                tb = rule["new_tb"][rule["old_tb"].index(table_name)]
            except Exception as e:
                loging.warning("获取规则表出错，请检查配置文件。错误信息：%s " % e)
                return db_name, table_name
        else:
            try:
                db = rule["new_db"][rule["old_db"].index(db_name)]
                return db
            except Exception:
                loging.warning("获取%s库不在规则表中，将返回原始表" % db_name)
                return db_name
        return db, tb


def exclude_merge_db_table(db_name, table_name=None):
    if merge_db_table is False:
        return True
    else:
        try:
            db = rule["new_db"][rule["old_db"].index(db_name)]
            tb = rule["new_tb"][rule["old_tb"].index(table_name)]
        except Exception:
            return False
        return True

