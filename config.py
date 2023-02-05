from pymysql.cursors import DictCursor
import pymysql

db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'db': 'db',
    'charset': 'utf8',
    'cursorclass': DictCursor
}

authorized = [user_id]

token = 'token'

conn = pymysql.connect(**db_config)
