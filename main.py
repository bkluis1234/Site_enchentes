# Importação da API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

#Permitir a conecção de qualquuer front-end com a API:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Estrutura que o front-end precisaram enviar:
class OcorrenciaSchema(BaseModel):
    tipo: str
    descricao: str
    bairro: str
    latitude: float
    longitude: float

#Conexão com o banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tcc_enchente"
    )

@app.post("/ocorrencias")
def criar_ocorrencia(oc: OcorrenciaSchema):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO ocorrencia (tipo, descricao, bairro, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = (oc.tipo, oc.descricao, oc.bairro, oc.latitude, oc.longitude)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    return {"mensagem": "Ocorrência registrada com sucesso!", "dados": oc}

@app.get("/ocorrencias")
def listar_ocorrencias():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("select * from ocorrencia")
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados