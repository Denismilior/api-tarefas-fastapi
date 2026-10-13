import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sua_senha_aqui",  # Substitui pela tua senha do MySQL
        database="tarefas_bd"
    )
