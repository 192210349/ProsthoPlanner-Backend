import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="prosthoplanner",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection