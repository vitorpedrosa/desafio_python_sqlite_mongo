from typing import Type

from sqlalchemy import Column, create_engine, inspect, select
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

# declarative base class
Base = declarative_base()


# an example mapping using the base
class Client(Base):
    __tablename__ = "client_account"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(11))
    address = Column(String(50))

    account = relationship(
        "Account", back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, cpf={self.cpf}, address={self.address})"


class Account(Base):
    __tablename__ = "account"
    # atributos
    id = Column(Integer, primary_key=True)
    type = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_client = Column(Integer, ForeignKey("client_account.id"), nullable=False)

    client = relationship(
        "Client", back_populates="account"
    )

    def __repr__(self):
        return f"Account(id={self.id})"


print(Client.__tablename__)
print(Account.__tablename__)

# conexão com o banco de dados
engine = create_engine("sqlite://")

#cliando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)
print(inspetor_engine.get_table_names())

with Session(engine) as session:
    virna = Client(
        name="virna",
        cpf="12345678912",
        address="rua vereador pedro moura, 321",
        account=[Account(
            type="CC",
            agencia="12345",
            num=85422,
        )]
    )

    adriana = Client(
        name="adriana",
        cpf="12345678912",
        address="rua vereador pedro moura, 321",
        account=[Account(type="CP", agencia="1255345", num=855422),
                 Account(type="CC", agencia="584746", num=548)
        ]
    )

    session.add_all([virna, adriana])
    session.commit()

    stmt = select(Client).where(Client.name.in_(["adriana"]))
    for client in session.scalars(stmt):
        print(client)

    order_stmt = select(Client).order_by(Client.name.desc())
    print("\n>>>> Recuperando infor de maneira ordenada")
    for result in session.scalars(order_stmt):
        print(result)

    stmt_join = select(Client.name, Account.num).join_from(Account, Client)
    for result in session.scalars(stmt_join):
        print(result)

    connection = engine.connect()
    results = connection.execute(stmt_join).fetchall()
    print("\n>>>>>> Executando statment a partir da connection")
    for result in results:
        print(result)


