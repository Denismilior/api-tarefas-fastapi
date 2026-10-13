import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",  # Substitui pela tua senha do MySQL
        database="tarefas_bd"
    )