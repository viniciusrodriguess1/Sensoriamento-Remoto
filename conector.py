# Dentro de main.py ou tcp_server.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='banco_de_dados'
    )
