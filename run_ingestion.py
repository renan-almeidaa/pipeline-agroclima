from src import config
from src.ingestion import ibge
from src.storage import mongo


def main():
    producao = ibge.buscar_producao(config.UF_CODIGO)
    metadados = {
        "fonte": "ibge_agregados",
        "uf": config.UF_CODIGO,
        "agregado": config.AGREGADO,
        "classificacao": config.CLASSIFICACAO,
        "variaveis": config.VARIAVEIS,
        "culturas": config.CULTURAS,
        "periodos": config.PERIODOS,
        "total_registros": len(producao),
    }

    mongo.salvar_payload(config.MONGO_COLECAO_PRODUCAO, producao, metadados)
    print(f"Produção salva com sucesso! Registros: {len(producao)}")


if __name__ == "__main__":
    main()
