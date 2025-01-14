import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',# Default user for XAMPP
            password='',         # Default password is empty
            database='college',
            port=3307# Replace with your database name
        )

        if connection.is_connected():
            print("✅ Connected to MySQL database")
            return connection

    except Error as e:
        print(f"❌ Error: {e}")
        return None

