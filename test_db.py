import sqlite3

def get_db_connection():
    # Replace 'example.db' with your database file or connection string
    try:
        conn = sqlite3.connect('example.db')
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

conn = get_db_connection()
if conn:
    print("Connection successful!")
    conn.close()
else:
    print("Connection failed!")
