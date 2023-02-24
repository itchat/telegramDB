from tools.logger import logger
from config import DB_CONFIG
from dbutils.pooled_db import PooledDB


class Database:
    def __init__(self):
        self.pool = PooledDB(**DB_CONFIG)

    def _get_connection(self):
        return self.pool.connection()

    def save_to_database(self, text):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO message (text) VALUES (%s)"
                    cursor.execute(sql, (text,))
        except Exception as e:
            logger.error("Error saving to database: %s", e, exc_info=True)

    def search_in_database(self, text):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    text = "%{}%".format(text)
                    sql = "SELECT id, text FROM message WHERE TEXT LIKE %s"
                    cursor.execute(sql, (text,))
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            logger.error("Error searching in database: %s", e, exc_info=True)

    def delete_record(self, record_id):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "DELETE FROM message WHERE id = %s"
                    cursor.execute(sql, (record_id,))
        except Exception as e:
            logger.error("Error delete in database: %s", e, exc_info=True)

    def read_database(self):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # RAND() generates a random value for each row in the table
                    sql = "SELECT id, text FROM message ORDER BY rand() LIMIT 10"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            logger.error("Error read 10 random message in database: %s", e, exc_info=True)
