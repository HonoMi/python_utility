# -*- coding: utf-8 -*-

# https://qiita.com/mas9612/items/a881e9f14d20ee1c0703

import sqlite3

from utility import sqlite_module

# Connect to db.
db_name = 'database.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create table.
table_name = 'users'
if not sqlite_module.table_exists(cursor, table_name):
    # executeメソッドでSQL文を実行する
    create_table = 'CREATE TABLE ' + table_name + ' (id INT, name VARCHAR(64), age INT, gender VARCHAR(32));'
    cursor.execute(create_table)

# SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
# セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
# タプルで渡す．
sql = 'INSERT INTO ' + table_name + ' (id, name, age, gender) VALUES (?,?,?,?);'
user = (1, 'Taro', 20, 'male')
cursor.execute(sql, user)

# 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
# executemanyメソッドを実行する
insert_sql = 'INSERT INTO ' + table_name + ' (id, name, age, gender) VALUES (?,?,?,?);'
users = [
    (2, 'Shota', 54, 'male'),
    (3, 'Nana', 40, 'female'),
    (4, 'Tooru', 78, 'male'),
    (5, 'Saki', 31, 'female')
]
cursor.executemany(insert_sql, users)
conn.commit()

select_sql = 'SELECT * FROM ' + table_name + ';'
ret = cursor.execute(select_sql).fetchall()
for row in ret:
    print(row)

sqlite_module.drop_table(cursor, table_name)

conn.close()
