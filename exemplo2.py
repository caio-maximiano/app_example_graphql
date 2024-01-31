"""     ************* GRAPHQL *************

Existem 4 conceitos fundamentais no Graphql
 1 - SDL (Schemma Definition Language)
        - A formatação dos dados que vamos aceitar e responder
        - Seus respectivos tipos
 2 - Queries
        - Como buscar esses dados no banco e devolver para API
 3 - Mutations
        - Como alterar os dados
        - Como criar novos dados
 4 - Subscription
        - Ouvir os eventos que acontecem no servidor
        - websocket
"""
import strawberry
from typing import Optional
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


class Person(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: int


def create_app(nome:str, idade:int):
    person = Person(nome=nome, idade=idade)
    
    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)
    
    return person


@strawberry.type
class Pessoa:
    id: Optional[int]
    nome: str
    idade: int

@strawberry.type
class Query:
    
    @strawberry.field
    def all_pessoa(self) -> list[Pessoa]:
        query = select(Person)
        with Session(engine) as session:
            result = session.execute(query).scalars().all()
        return result

@strawberry.type
class Mutation:
    create_pessoa: Pessoa = strawberry.field(resolver = create_app)


schema = strawberry.Schema(
    query = Query,
    mutation = Mutation
    )