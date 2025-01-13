import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',# Default user for XAMPP
            password='',         # Default password is empty
            database='college',
<<<<<<< HEAD
            port=3306# Replace with your database name
=======
            port=3307# Replace with your database name#3306
>>>>>>> otherUpdates-local
        )

        if connection.is_connected():
            print("✅ Connected to MySQL database")
            return connection

    except Error as e:
        print(f"❌ Error: {e}")
        return None

