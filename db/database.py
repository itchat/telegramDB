from tools.logger import logger
from config import conn


# Connect to database
class Database:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.conn = conn
        return cls.instance

    def save_to_database(self, text):
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO message (text) VALUES (%s)"
                cursor.execute(sql, (text,))
            conn.commit()
        except Exception as e:
            logger.error("Error saving to database: %s", e, exc_info=True)

    def search_in_database(self, text):
        try:
            with self.conn.cursor() as cursor:
                text = "%{}%".format(text)
                sql = "SELECT id, text FROM message WHERE TEXT LIKE %s"
                cursor.execute(sql, (text,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error("Error searching in database: %s", e, exc_info=True)

    def delete_record(self, record_id):
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM message WHERE id = %s"
                cursor.execute(sql, (record_id,))
                conn.commit()
        except Exception as e:
            logger.error("Error delete in database: %s", e, exc_info=True)

