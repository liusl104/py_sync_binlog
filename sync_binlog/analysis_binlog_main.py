# encoding=utf8

from sync_binlog.update_post import update_binlog_pos
from sync_binlog.output_log import logger as loging
from sync_binlog.send_binlog import *
from sync_binlog.analysis_rows import *
from sync_binlog.merge_dbname_tables import *
from sync_conf import *
from sync_binlog.send_binlog import Mysql
from sync_binlog.batch_analysis_insert_sql import batch_analysis_sql
import datetime
from decimal import Decimal

mysql = Mysql("/*!40014 SET FOREIGN_KEY_CHECKS=0*/")

batch_sql = batch_analysis_sql()


def analysis_rotate_event(info):
    print("%s获取文件 %s Position id %s " % (update_datetime(), info["Next binlog file"], info["Position"]))
    loging.info("获取文件 %s Position id %s " % (info["Next binlog file"], info["Position"]))
    init_binlog_file_name = "%s\n" % info["Next binlog file"]
    update_binlog_pos(pos_id=info["Position"], binlog_file=init_binlog_file_name)


def analysis_format_description_event(info):
    print("%sbinlog日志开始写入时间: %s Position id %s " % (update_datetime(), info["Date"], str(info["Log position"])))
    loging.info("binlog日志开始写入时间: %s Position id %s " % (info["Date"], str(info["Log position"])))


def analysis_gtid_event(info, init_binlog_file_name):
    loging.info("解析日志时间 : %s Position id %s GTID_NEXT : %s " % (info["Date"], str(info["Log position"]),
                                                                eval(info["row_values"])["GTID_NEXT"]))
    update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)


def analysis_query_event(info, init_binlog_file_name):
    row_values = eval(info["row_values"])
    schema = row_values["Schema"]
    loging.debug("解析日志时间 : %s Position id %s 当前 Schema : [%s] Query : %s " % (info["Date"],
                                                                              str(info["Log position"]),
                                                                              schema, row_values["Query"]))
    if len(schema) != 0:
        loging.debug('switch database : use %s ' % schema)
        if merge_db_table is True:
            merge_db = merge_replicate_table(schema)
            loging.info("规则库变更 %s ---> %s " % (schema, merge_db))
            if write_db is True:
                if merge_db_table:
                    merge_schema = merge_replicate_table(schema)
                if schema != merge_db:
                    if merge_db_table:
                        if merge_schema in only_schemas:
                            mysql.my_sql('use %s' % merge_schema)
                        else:
                            loging.info("skip execute [use %s]" % merge_schema)
                    else:
                        mysql.my_sql('use %s' % schema)
                else:
                    if merge_db_table:
                        if schema in only_schemas:
                            mysql.my_sql('use %s' % schema)
                        else:
                            loging.info("skip execute [use %s]" % schema)
                    else:
                        mysql.my_sql('use %s' % schema)
        else:
            if write_db is True:
                if only_schemas is None:
                    if "create database" not in str(row_values["Query"]).lower():
                        mysql.my_sql('use %s' % schema)
                else:
                    if schema in only_schemas:
                        mysql.my_sql('use %s' % schema)
                    else:
                        loging.info("skip execute [use %s]" % schema)
    if row_values["Query"] == "BEGIN":
        loging.debug("skip sql begin transaction")
    else:
        if write_ddl is True:
            if merge_db_table:
                map_database = merge_table_rule["database"]
                for d in map_database:
                    for k in d:
                        if merge_schema in d[k]:
                            loging.info("同步复制DDL --> %s" % row_values["Query"])
                            mysql.my_sql("/*!40014 SET FOREIGN_KEY_CHECKS=0*/")
                            mysql.my_sql(row_values["Query"])
                        else:
                            loging.info("skip DDL sql: %s " % row_values["Query"])
                            break

            else:
                if write_ddl:
                    if only_schemas is None:
                        loging.info("同步复制DDL --> %s" % row_values["Query"])
                        mysql.my_sql("/*!40014 SET FOREIGN_KEY_CHECKS=0*/")
                        mysql.my_sql(row_values["Query"])
                    else:
                        if schema in only_schemas:
                            loging.info("同步复制DDL --> %s" % row_values["Query"])
                            mysql.my_sql("/*!40014 SET FOREIGN_KEY_CHECKS=0*/")
                            mysql.my_sql(row_values["Query"])
                        elif len(schema) == 0:
                            loging.info("同步复制DDL --> %s" % row_values["Query"])
                            mysql.my_sql("/*!40014 SET FOREIGN_KEY_CHECKS=0*/")
                            mysql.my_sql(row_values["Query"])
                        else:
                            loging.info("skip DDL sql: %s " % row_values["Query"])
        else:
            loging.warning("DDL 语句 暂不支持")
    update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)


def analysis_table_map_event(info, init_binlog_file_name):
    row_values = eval(info["row_values"])
    loging.debug("解析日志时间 : %s Position id %s Table id %d Schema [%s] Table [%s] " % (info["Date"],
                                                                                     str(info["Log position"]),
                                                                                     row_values["Table id"],
                                                                                     row_values["Schema"],
                                                                                     row_values["Table"]))
    update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
    loging.debug('switch database : use %s ' % row_values["Schema"])
    if merge_db_table is False:
        table_map = "`%s`.`%s`" % (row_values["Schema"], row_values["Table"])
        hi_table_map = "`%s`.`%s`" % (row_values["Schema"], row_values["Table"])
        loging.debug('switch database : use %s ' % row_values["Schema"])
        if write_db is True:
            mysql.my_sql('use %s' % row_values["Schema"])
    else:
        table_map = "`%s`.`%s`" % (merge_replicate_table(row_values["Schema"], row_values["Table"]))
        hi_table_map = "`%s`.`%s`" % (row_values["Schema"], row_values["Table"])
        dt = merge_replicate_table(row_values["Schema"], row_values["Table"])
        loging.info("规则库表变更 %s.%s ---> %s.%s" % (row_values["Schema"], row_values["Table"], dt[0], dt[1]))
        loging.debug('switch database : use %s ' % dt[0])
        if write_db is True:
            mysql.my_sql('use %s' % dt[0])
    return table_map, hi_table_map


def analysis_update_rows_event(info, init_binlog_file_name, table_map=None, hi_table_map=None):
    if exclude_merge_db_table(str(hi_table_map).replace('`', '').split('.')[0],
                              str(hi_table_map).replace('`', '').split('.')[1]) is False:
        loging.warning("忽略不在规则中表%s" % hi_table_map)
        return True
    values = eval(info["row_values"])["Values"]
    if len(values) > 1:
        for v in values:
            set_values = update_before_values(v["before_values"], table_map)
            where_values = update_after_values(v["after_values"], table_map)
            analysis_sql = "update %s set %s  where %s " % (table_map, where_values.replace("'None'", 'Null'),
                                                            set_values.replace("= 'None'", ' is null '))
            loging.debug("Query : %s " % analysis_sql)
            if write_db is True:
                mysql.my_sql(analysis_sql)
        update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
        loging.info("解析日志时间 : %s Position id %s" % (info["Date"], str(info["Log position"])))
    else:
        values = eval(info["row_values"])["Values"][0]
        set_values = update_before_values(values["before_values"], table_map)
        where_values = update_after_values(values["after_values"], table_map)
        analysis_sql = "update %s set %s  where %s " % (table_map, where_values.replace("'None'", 'Null'),
                                                        set_values.replace("= 'None'", ' is null '))
        loging.info("解析日志时间 : %s Position id %s " % (info["Date"], str(info["Log position"])))
        loging.debug("Query : %s " % analysis_sql)
        if write_db is True:
            mysql.my_sql(analysis_sql)
        update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)


def analysis_write_rows_event(info, init_binlog_file_name, table_map=None, hi_table_map=None):
    if exclude_merge_db_table(str(hi_table_map).replace('`', '').split('.')[0],
                              str(hi_table_map).replace('`', '').split('.')[1]) is False:
        loging.warning("忽略不在规则中表%s" % hi_table_map)
        return True
    if len(eval(info["row_values"])["Values"]) == 0:
        loging.debug("解析日志时间 : %s Position id %s Query : %s " % (info["Date"], str(info["Log position"]), None))
        update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
    else:
        batch_sql.batch_analysis_insert_binlog(info, init_binlog_file_name, table_map)


def analysis_delete_rows_event(info, init_binlog_file_name, hi_table_map=None, table_map=None):
    if exclude_merge_db_table(str(hi_table_map).replace('`', '').split('.')[0],
                              str(hi_table_map).replace('`', '').split('.')[1]) is False:
        loging.warning("忽略不在规则中表%s" % hi_table_map)
        return True
    values = eval(info["row_values"])["Values"]
    if len(values) > 1:
        for v in values:
            if merge_db_table is False:
                rows_info = eval(info["row_values"])["info"]["Table"]
            else:
                rows = eval(info["row_values"])["info"]["Table"]
                row = str(rows).split('.')
                dt = merge_replicate_table(row[0], row[1])
                loging.info("规则库表变更 %s ---> %s.%s" % (rows, dt[0], dt[1]))
                rows_info = '.'.join(dt)
            analysis_sql = "delete from %s where %s" % (rows_info,
                                                        delete_rows_values(v["values"], table_map).replace("= 'None'", ' is null '))
            loging.debug("Query : %s " % analysis_sql)
            if write_db is True:
                mysql.my_sql(analysis_sql)
            update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
        loging.info("解析日志时间 : %s Position id %s " % (info["Date"], str(info["Log position"])))
    else:
        values = eval(info["row_values"])["Values"][0]["values"]
        if merge_db_table is False:
            rows_info = eval(info["row_values"])["info"]["Table"]
        else:
            rows = eval(info["row_values"])["info"]["Table"]
            row = str(rows).split('.')
            dt = merge_replicate_table(row[0], row[1])
            loging.info("规则库表变更 %s ---> %s.%s" % (rows, dt[0], dt[1]))
            rows_info = '.'.join(dt)
        analysis_sql = "delete from %s where %s" % (rows_info, delete_rows_values(values, table_map).
                                                    replace("= 'None'", ' is null '))
        loging.info("解析日志时间 : %s Position id %s" % (info["Date"], str(info["Log position"])))
        loging.debug("Query : %s " % analysis_sql)
        if write_db is True:
            mysql.my_sql(analysis_sql)
        update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)


def analysis_xid_event(info, init_binlog_file_name):
    if 'row_values' in info.keys():
        loging.debug("解析日志时间 : %s Position id %s Transaction ID : %s " % (info["Date"], str(info["Log position"]),
                                                                          eval(info["row_values"])["Transaction ID"]))
    else:
        loging.debug("解析日志时间 : %s Position id %s" % (info["Date"], str(info["Log position"])))
    update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)


def analysis_stop_event(info, init_binlog_file_name):
    loging.info("解析日志时间 : %s 切换binlog file Position id %s" % (info["Date"], str(info["Log position"])))
    print("%s解析日志时间 : %s 切换binlog file Position id %s" % (update_datetime(), info["Date"], str(info["Log position"])))
    update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
