import os
import pymysqlpool
from pymysql.cursors import DictCursor

pool = pymysqlpool.ConnectionPool(
    host='127.0.0.1',
    user=os.getenv('USER', 'root'),
    password=os.getenv("PASS", "123456"),
    db=os.getenv("DB", "tgdb"),
    port=3306,
    maxsize=5,
    charset='utf8mb4',
    cursorclass=DictCursor,
    autocommit=True
)

# user_id: int
authorized = [int(os.getenv("ID"))]

token = os.getenv("TOKEN")
