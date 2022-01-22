from library.db import *

mysql = MYSQL_CONNECT('ipo')
mysql.create_table('ipo_list')
mysql.data_insert('ipo_list', result)
