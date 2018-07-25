# encoding=utf8


from pymysqlreplication import BinLogStreamReader
from sync_binlog.update_post import get_new_binlog_pos
from sync_binlog.batch_analysis_insert_sql import cntrast_insert_class_tab
from sync_binlog.analysis_binlog_main import *
from sync_binlog.output_log import logger as loging
from sync_binlog.safe_shutdown import safety_shutdown
from sync_binlog.Decrypt import decrypt
mysql_settings["passwd"] = decrypt(mysql_settings["passwd"])


def main_binlog(only_schemas=only_schemas, server_id=server_id, hi_table_map=None):
    stream = BinLogStreamReader(connection_settings=mysql_settings,
                                server_id=server_id,
                                blocking=blocking,
                                resume_stream=resume_stream,
                                only_events=only_events,
                                ignored_events=ignored_events,
                                auto_position=auto_position,
                                only_tables=only_tables,
                                ignored_tables=ignored_tables,
                                only_schemas=only_schemas,
                                ignored_schemas=ignored_schemas,
                                log_file=get_new_binlog_pos(binlogfile_Label_file)[0],
                                log_pos=int(get_new_binlog_pos(binlogfile_Label_file)[1]))
    #try:
    for binlogevent in stream:
            info = binlogevent.dump()
            cntrast_insert_class_tab(info, hi_table_map)
            safety_shutdown()
            if info['class'] == 'RotateEvent':
                analysis_rotate_event(info)
                init_binlog_file_name = "%s\n" % info["Next binlog file"]
            elif info['class'] == 'FormatDescriptionEvent':
                analysis_format_description_event(info)
            elif info['class'] == "GtidEvent":
                analysis_gtid_event(info, init_binlog_file_name)
            elif info['class'] == "QueryEvent":
                analysis_query_event(info, init_binlog_file_name)
            elif info['class'] == "TableMapEvent":
                table_map, hi_table_map = analysis_table_map_event(info, init_binlog_file_name)
            elif info['class'] == "UpdateRowsEvent":
                analysis_update_rows_event(info, init_binlog_file_name, table_map, hi_table_map)
            elif info['class'] == "WriteRowsEvent":
                analysis_write_rows_event(info, init_binlog_file_name, table_map, hi_table_map)
            elif info['class'] == "XidEvent":
                analysis_xid_event(info, init_binlog_file_name)
            elif info['class'] == "DeleteRowsEvent":
                analysis_delete_rows_event(info, init_binlog_file_name, hi_table_map, table_map)
            elif info['class'] == "StopEvent":
                analysis_stop_event(info, init_binlog_file_name)
            else:
                loging.warning(info)
    #except Exception as er:
    #    loging.critical("The connection source DB has an exception, "
    #                    "please check the configuration information：%s " % er)
