from pydantic import BaseModel
from fastapi import FastAPI
from database import get_connection

app = FastAPI()

@app.get("/")
def home():
    db = get_connection()
    if db.is_connected():
        db.close()
        return {"status": "ok"}
    return {"status": "error"}

@app.get("/tarefas")
def listar_tarefas():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    # 1. Executa o comando para buscar todas as tarefas
    cursor.execute("SELECT * FROM tarefas")




    # 2. Pega todos os resultados retornados
    tarefas = cursor.fetchall()

    # 3. Fecha o cursor e a conexão (sempre limpe a mesa!)
    cursor.close()
    db.close()

    # 4. Retorna a lista de tarefas
    return tarefas

class CriarTarefa(BaseModel):
    titulo: str
    descricao: str = None  # Descrição é opcional

@app.post("/tarefas")
def criar_tarefas(tarefa: CriarTarefa):
    db = get_connection()
    cursor = db.cursor()
    # 1. Query SQL com placeholders (%s)
    query = "INSERT INTO tarefas (titulo, descricao) VALUES (%s, %s)"
    valores = (tarefa.titulo, tarefa.descricao)
    # 2. Executa a query passando os valores
    cursor.execute(query, valores)
    # 3. Confirma a gravação no banco de dados (EFETIVA O INSERT)
    db.commit()
    #4. limpar recursos.
    cursor.close()
    db.close()
    return {"status": "ok"}


# 1. Primeiro o modelo Pydantic
class AtualizarTarefa(BaseModel):
    titulo: str
    descricao: str = None
    concluido: bool = False

# 2. Depois a rota PUT
@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, tarefa: AtualizarTarefa):
    db = get_connection()
    cursor = db.cursor()

    query = "UPDATE tarefas SET titulo = %s, descricao = %s, concluido = %s WHERE id = %s"
    valores = (tarefa.titulo, tarefa.descricao, tarefa.concluido, tarefa_id)

    cursor.execute(query, valores)
    db.commit()

    cursor.close()
    db.close()

    return {"status": "ok"}

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    db = get_connection()
    cursor = db.cursor()
    query = "DELETE FROM tarefas WHERE id = %s"
    valores = (tarefa_id,)
    cursor.execute(query, valores)
    db.commit()
    cursor.close()
    db.close()
    return {"status": "ok"}