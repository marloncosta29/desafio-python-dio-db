import pymongo


client = pymongo.MongoClient("mongodb+srv://pymongo:pymongouser@my-cluster.qvxcdgu.mongodb.net/?retryWrites=true&w=majority&appName=my-cluster")
# client.drop_database("my_database")
db = client.my_database

clientes = [
    {
        "nome": "Marlon da costa",
        "cpf": "86945598970",
        "endereco": "rua teste de algum lugar, 122"
    },
    {
        "nome": "Janaina kempf",
        "cpf": "12121212121",
        "endereco": "rua teste lugar, 999"
    }
]

db_clientes = db.clientes
db_clientes.insert_many(clientes)

cliente_encontrado = db_clientes.find_one({"cpf": "12121212121"})

conta_correntes = [{
    "tipo": "corrente",
    "agencia": "1234-9",
    "num": 123456,
    "id_cliente": cliente_encontrado['_id']
}]

db_contas = db.contas
db_contas.insert_many(conta_correntes)

conta_corrente = db_contas.find_one({"num": 123456})
conta_id = conta_corrente["id_cliente"]
cliente_da_conta = db_clientes.find_one({"_id": conta_id})

print(f""" 
        Cliente: {cliente_da_conta['nome']}
        Conta: {conta_corrente['num']}
       """)





