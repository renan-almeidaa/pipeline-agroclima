from datetime import datetime, timezone

from pymongo import MongoClient

from src import config


def get_db():
    """Abre conexão com o MongoDB e retorna o banco configurado."""
    client = MongoClient(config.MONGO_URI)
    return client.get_database(config.MONGO_DB) # tambem funciona client[config.MONGO_DB]



def salvar_payload(colecao: str, payload: list[dict], metadados: dict) -> str:
    """Salva o payload cru com metadados de origem e data de ingestão.

    Guardar o payload como veio permite reprocessar sem chamar a fonte de novo.
    """
    documento = {
        "ingerido_em": datetime.now(timezone.utc),
        "metadados": metadados,
        "payload": payload,
    }
    col = get_db()[colecao]
    resultado = col.insert_one(documento)
    return str(resultado.inserted_id)

if __name__ == "__main__":
    db = get_db()
    inserted_id = salvar_payload(
        "exemplo",
        [{"chave": "valor"}],
        {"fonte": "teste", "descricao": "Exemplo de payload"},
    )
    print(f"Payload salvo com sucesso! ID: {inserted_id}")
    print(f"Documento salvo: {db['exemplo'].find_one({'_id': inserted_id})}")

    # 1. Remove o documento de teste
    db["exemplo"].delete_one({"_id": inserted_id})
    print(f"Documento de teste removido.")
    
    # 2. Exclui a coleção inteira para limpar o banco
    db["exemplo"].drop()
    print(f"Coleção 'exemplo' excluída (drop).")
    
    # Agora a lista deve vir vazia [] (ou sem a coleção 'exemplo')
    print(f"DB atual: {db.list_collection_names()}")