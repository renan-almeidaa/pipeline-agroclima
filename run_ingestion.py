from src.ingestion import ibge
from src.storage import mongo
from src import config


def main():
    municipios = ibge.buscar_municipios(config.UF_CODIGO)
    print(f"municípios encontrados: {len(municipios)}")

    codigos = [str(m["id"]) for m in municipios]
    lotes = ibge.dividir_em_lotes(codigos, config.TAMANHO_LOTE)

    for i, lote in enumerate(lotes, start=1):
        producao = ibge.buscar_producao(lote)
        metadados = {
            "lote": i,
            "total_lotes": len(lotes),
            "uf": config.UF_CODIGO,
            "agregado": config.AGREGADO,
            "classificacao": config.CLASSIFICACAO,
            "variaveis": config.VARIAVEIS,
            "culturas": config.CULTURAS,
            "periodos": config.PERIODOS,
            "total_registros": len(producao),
            "municipios": lote
            }
        
        mongo.salvar_payload(config.MONGO_COLECAO_PRODUCAO, producao, metadados)
        print(f"Lote {i}/{len(lotes)} salvo com sucesso! Registros: {len(producao)}")


if __name__ == "__main__":
    main()