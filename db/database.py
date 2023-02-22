from tools.logger import logger
from config import pool


class Database:
    def __init__(self):
        self.conn = pool.get_connection()

    def save_to_database(self, text):
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO message (text) VALUES (%s)"
                cursor.execute(sql, (text,))
            self.conn.commit()
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
                self.conn.commit()
        except Exception as e:
            logger.error("Error delete in database: %s", e, exc_info=True)

    def read_database(self):
        try:
            with self.conn.cursor() as cursor:
                # RAND() generates a random value for each row in the table
                sql = "SELECT id, text FROM message ORDER BY rand() LIMIT 10"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error("Error read 10 random message in database: %s", e, exc_info=True)
