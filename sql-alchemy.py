import sqlalchemy as sqlA
import sqlalchemy.orm as orm

Base = orm.declarative_base()


class Cliente(Base):
    __tablename__ = "customer"

    id = sqlA.Column(sqlA.Integer, autoincrement=True, primary_key=True)
    nome = sqlA.Column(sqlA.String)
    cpf = sqlA.Column(sqlA.String)
    endereco = sqlA.Column(sqlA.String)

    conta = orm.relationship("Conta", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Customner [id:{self.id} - nome:{self.nome} - cpf:{self.cpf} - endereco:{self.endereco}"


class Conta(Base):
    __tablename__ = "account"
    id = sqlA.Column(sqlA.Integer, autoincrement=True, primary_key=True)
    tipo = sqlA.Column(sqlA.String)
    agencia = sqlA.Column(sqlA.String)
    num = sqlA.Column(sqlA.Integer)
    id_cliente = sqlA.Column(sqlA.Integer, sqlA.ForeignKey("customer.id"), nullable=False)

    cliente = orm.relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Customner [id:{self.id} - tipo:{self.tipo} - agencia:{self.agencia} - numero:{self.num}"


engine = sqlA.create_engine("sqlite://")
Base.metadata.create_all(engine)

with orm.Session(engine) as session:
    cliente_um = Cliente(
        nome="Marlon da costa",
        cpf="88888888888",
        endereco="rua teste, num 123, casa",
        conta=[Conta(
            tipo="corrente",
            agencia="123",
            num=123456
        )]
    )
    cliente_dois = Cliente(
        nome="Janaina Ruiz",
        cpf="99999999999",
        endereco="rua teste, num 123, casa",
        conta=[Conta(
            tipo="poupanca",
            agencia="123",
            num=123457
        )]
    )
    session.add_all([cliente_um, cliente_dois])
    session.commit()

cliente_com_contas = sqlA.select(Cliente.nome, Conta.tipo,  Conta.agencia, Conta.num).join_from(Conta, Cliente)
conexao = engine.connect()
resultados = conexao.execute(cliente_com_contas).fetchall()
for resultado in resultados:
    print(f"Cliente: {resultado[0]}, conta do tipo {resultado[1]} ag: {resultado[2]} conta: {resultado[3]}")
