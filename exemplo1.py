from typing import Optional
from fastapi import FastAPI
from sqlmodel import (
    SQLModel,
    Field,
    create_engine,
    select,
    Session
)

#Criar engine do banco
engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)


class Pessoa(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: int

#Cria o banco de dados
SQLModel.metadata.create_all(engine)

"""
Numa aplicação rest, seriam varios endpoints (1 pra nome, outro pra idade, etc)
"""
app = FastAPI()
@app.get("/")
def get_pessoa():
    
    return {"message": "Bem vindo(a)"}

@app.get("/pessoa")
def get_pessoa():
    query = select(Pessoa)
    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    return result

@app.get("/pessoa-nome")
def get_pessoa():
    query = select(Pessoa.nome)
    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    return result
