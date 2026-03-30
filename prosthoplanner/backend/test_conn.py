import mysql.connector
try:
    print("Connecting to MySQL...")
    conn = mysql.connector.connect(host='localhost', user='root', password='')
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS prosthoplanner")
    print("Database 'prosthoplanner' verified/created.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
