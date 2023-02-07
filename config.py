from pymysql.cursors import DictCursor
import pymysql

db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'db': 'db',
    # Change the config data above
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# user_id: int
authorized = [123456]

token = 'bot_token'

conn = pymysql.connect(**db_config)
