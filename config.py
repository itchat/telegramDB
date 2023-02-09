import os
import pymysql
from pymysql.cursors import DictCursor

db_config = {
    'host': '150.230.108.244',
    'user': os.getenv('USER', 'root'),
    'password': os.getenv("PASS", "123456"),
    'db': os.getenv("DB", "tgdb"),
    # Change the config data above
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# user_id: int
authorized = [int(os.getenv("ID"))]

token = os.getenv("TOKEN")

conn = pymysql.connect(**db_config)
