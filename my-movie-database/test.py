import mysql.connector
from mysql.connector import Error

DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'mysecretpassword',
    'database': 'movies_db'
}

def test_connection():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        if conn.is_connected():
            print("Connection successful!")
            conn.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
