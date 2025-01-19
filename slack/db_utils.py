import pymysql
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

db_config = {
    "host": 'localhost',
    "port": int(os.getenv('MARIADB_PORT')),
    "user": os.getenv('MARIADB_USER'),
    "password": os.getenv('MARIADB_PW'),
    "database": os.getenv('MARIADB_NAME'),
}

def get_message_by_reference_id(reference_id):
    """Retrieve message details by reference ID from the database."""
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, message FROM messages WHERE id=%s", (reference_id,))
            result = cursor.fetchone()
            return result  # Returns (user_id, message)
    finally:
        connection.close()
