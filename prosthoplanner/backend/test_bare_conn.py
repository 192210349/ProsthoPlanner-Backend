import mysql.connector
print("Attempting bare connection...")
conn = mysql.connector.connect(host='localhost', user='root', password='')
print("Success!")
conn.close()
