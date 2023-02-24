import os
import pymysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    "creator": pymysql,
    "host": "127.0.0.1",
    "user": os.getenv('USER', 'root'),
    "password": os.getenv("PASS", "123456"),
    "database": os.getenv("DB", "tgdb"),
    "port": 3306,
    "charset": "utf8mb4",
    "maxconnections": 5,
    "cursorclass": DictCursor,
    "autocommit": True
}

# user_id: int
authorized = [int(os.getenv("ID"))]

token = os.getenv("TOKEN")
