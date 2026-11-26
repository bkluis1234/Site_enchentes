# Importação da API
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import mysql.connector
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

# Permitir a conexão de qualquer front-end com a API:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estrutura que o front-end precisa enviar:
class OcorrenciaSchema(BaseModel):
    tipo: str
    descricao: str
    bairro: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

# Conexão com o banco de dados usando variáveis de ambiente (seguro)
def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.post("/ocorrencias")
def criar_ocorrencia(oc: OcorrenciaSchema):
    conexao = None
    try:
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
    except mysql.connector.Error as erro:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {erro}")
    finally:
        # Garante que a conexão fecha mesmo se der erro
        if conexao and conexao.is_connected():
            conexao.close()

    return {"mensagem": "Ocorrência registrada com sucesso!", "dados": oc}

@app.get("/ocorrencias")
def listar_ocorrencias():
    conexao = None
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("select * from ocorrencia order by data_criacao desc")
        resultados = cursor.fetchall()

        cursor.close()
    except mysql.connector.Error as erro:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {erro}")
    finally:
        # Garante que a conexão fecha mesmo se der erro
        if conexao and conexao.is_connected():
            conexao.close()

    return resultados