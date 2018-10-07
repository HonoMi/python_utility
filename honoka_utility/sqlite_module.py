def table_exists(cursor, table_name):
    ret = cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'' + table_name + '\';')
    return len(ret.fetchall()) != 0


def drop_table(cursor, table_name):
    if table_exists(cursor, table_name):
        cursor.execute('DROP TABLE ' + table_name + ';')
