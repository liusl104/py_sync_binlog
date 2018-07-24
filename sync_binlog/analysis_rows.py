# encoding=utf8

from sync_conf import encryption_column, encryption_db_column
from sync_binlog.AES_Encryption import ase_encryption


def update_before_values(values, table_map=None):
    return_values = ''
    if encryption_column is False:
        for x in values:
            if type(values[x]) == bytes:
                v = values[x].decode("utf-8")
            else:
                v = str(values[x])
            if "\\" in v:
                v = v.replace("\\", "\\" * 2)
            if "\n" in v:
                v = v.replace('\n', '\\n')
            if "'" in v:
                v = v.replace("'", "\\'")
            equal = "`%s` = '%s'" % (x, v)
            return_values += (equal + ' and ')
    else:
        table_name = str(table_map).replace('`', '').split('.')[1]
        if table_name in encryption_db_column["table_column_map"]:
            for x in values:
                if type(values[x]) == bytes:
                    v = values[x].decode("utf-8")
                else:
                    v = str(values[x])
                if "\\" in v:
                    v = v.replace("\\", "\\" * 2)
                if "\n" in v:
                    v = v.replace('\n', '\\n')
                if "'" in v:
                    v = v.replace("'", "\\'")
                if x in encryption_db_column["table_column_map"][table_name].replace(' ', '').split(','):
                    equal = "`%s` = '%s'" % (x, ase_encryption(v))
                    return_values += (equal + ' and ')
                else:
                    equal = "`%s` = '%s'" % (x, v)
                    return_values += (equal + ' and ')
        else:
            for x in values:
                if type(values[x]) == bytes:
                    v = values[x].decode("utf-8")
                else:
                    v = str(values[x])
                if "\\" in v:
                    v = v.replace("\\", "\\" * 2)
                if "\n" in v:
                    v = v.replace('\n', '\\n')
                if "'" in v:
                    v = v.replace("'", "\\'")
                equal = "`%s` = '%s'" % (x, v)
                return_values += (equal + ' and ')
    return return_values.strip('and ')


def update_after_values(values, table_map=None):
    return_values = ''
    if encryption_column is False:
        for x in values:
            if type(values[x]) == bytes:
                v = values[x].decode("utf-8")
            else:
                v = str(values[x])
            if "\\" in v:
                v = v.replace("\\", "\\" * 2)
            if "\n" in v:
                v = v.replace('\n', '\\n')
            if "'" in v:
                v = v.replace("'", "\\'")
            equal = "`%s` = '%s'" % (x, v)
            return_values += (equal + ', ')
    else:
        table_name = str(table_map).replace('`', '').split('.')[1]
        if table_name in encryption_db_column["table_column_map"]:
            for x in values:
                if type(values[x]) == bytes:
                    v = values[x].decode("utf-8")
                else:
                    v = str(values[x])
                if "\\" in v:
                    v = v.replace("\\", "\\" * 2)
                if "\n" in v:
                    v = v.replace('\n', '\\n')
                if "'" in v:
                    v = v.replace("'", "\\'")
                if x in encryption_db_column["table_column_map"][table_name].replace(' ', '').split(','):
                    equal = "`%s` = '%s'" % (x, ase_encryption(v))
                    return_values += (equal + ', ')
                else:
                    equal = "`%s` = '%s'" % (x, v)
                    return_values += (equal + ', ')
        else:
            for x in values:
                if type(values[x]) == bytes:
                    v = values[x].decode("utf-8")
                else:
                    v = str(values[x])
                if "\\" in v:
                    v = v.replace("\\", "\\" * 2)
                if "\n" in v:
                    v = v.replace('\n', '\\n')
                if "'" in v:
                    v = v.replace("'", "\\'")
                equal = "`%s` = '%s'" % (x, v)
                return_values += (equal + ', ')
    return return_values.strip(', ')


def insert_key_values(values, table_map=None):
    k_value = ''
    v_value = ''
    if encryption_column is False:
        for k in values:
            k_value += ('`%s`,' % k)
            if type(values[k]) == bytes:
                v = values[k].decode("utf-8")
            else:
                v = str(values[k])
            if "\\" in v:
                v = v.replace("\\", "\\" * 2)
            if "\n" in v:
                v = v.replace('\n', '\\n')
            if "'" in v:
                v = v.replace("'", "\\'")
            v_value += ("'%s'" % str(v)+',')
    else:
        table_name = str(table_map).replace('`', '').split('.')[1]
        if table_name in encryption_db_column["table_column_map"]:
            for k in values:  # {'id': 2, 'name': 'b'}
                if k in encryption_db_column["table_column_map"][table_name].replace(' ', '').split(','):
                    k_value += ('`%s`,' % k)
                    if type(values[k]) == bytes:
                        v = values[k].decode("utf-8")
                    else:
                        v = str(values[k])
                    if "\\" in v:
                        v = v.replace("\\", "\\" * 2)
                    if "\n" in v:
                        v = v.replace('\n', '\\n')
                    if "'" in v:
                        v = v.replace("'", "\\'")
                    v_value += ("'%s'" % ase_encryption(v)+',')
                else:
                    k_value += ('`%s`,' % k)
                    if type(values[k]) == bytes:
                        v = values[k].decode("utf-8")
                    else:
                        v = str(values[k])
                    if "\\" in v:
                        v = v.replace("\\", "\\" * 2)
                    if "\n" in v:
                        v = v.replace('\n', '\\n')
                    if "'" in v:
                        v = v.replace("'", "\\'")
                    v_value += ("'%s'" % v + ',')
        else:
            for k in values:
                k_value += ('`%s`,' % k)
                if type(values[k]) == bytes:
                    v = values[k].decode("utf-8")
                else:
                    v = str(values[k])
                if "\\" in v:
                    v = v.replace("\\", "\\" * 2)
                if "\n" in v:
                    v = v.replace('\n', '\\n')
                if "'" in v:
                    v = v.replace("'", "\\'")
                v_value += ("'%s'" % v + ',')
    return k_value.strip(','), v_value.strip(',')


def delete_rows_values(values,  table_map=None):
    k_value = ''
    if encryption_column is False:
        for k in values:
            if type(values[k]) == bytes:
                v = values[k].decode("utf-8")
            else:
                v = str(values[k])
            if "\\" in v:
                v = v.replace("\\", "\\" * 2)
            if "\n" in v:
                v = v.replace('\n', '\\n')
            if "'" in v:
                v = v.replace("'", "\\'")
            k_value += ("`%s` = '%s'" % (k, v) + ' and ')
    else:
        table_name = str(table_map).replace('`', '').split('.')[1]
        if table_name in encryption_db_column["table_column_map"]:
            for k in values:
                if type(values[k]) == bytes:
                    v = values[k].decode("utf-8")
                else:
                    v = str(values[k])
                if "\\" in v:
                    v = v.replace("\\", "\\" * 2)
                if "\n" in v:
                    v = v.replace('\n', '\\n')
                if "'" in v:
                    v = v.replace("'", "\\'")
                if k in encryption_db_column["table_column_map"][table_name].replace(' ', '').split(','):
                    k_value += ("`%s` = '%s'" % (k, ase_encryption(v)) + ' and ')
                else:
                    k_value += ("`%s` = '%s'" % (k, str(v)) + ' and ')
        else:
            for k in values:
                v = str(values[k])
                if "\\" in v:
                    v = v.replace("\\", "\\" * 2)
                if "\n" in v:
                    v = v.replace('\n', '\\n')
                if "'" in v:
                    v = v.replace("'", "\\'")
                k_value += ("`%s` = '%s'" % (k, str(v)) + ' and ')
    return k_value.strip(' and ')
