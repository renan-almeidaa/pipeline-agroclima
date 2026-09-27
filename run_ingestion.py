from src import config
from src.ingestion import ibge, inmet
from src.storage import mongo


def ingerir_producao():
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


def ingerir_clima():
    for ano in config.INMET_ANOS:
        destino_ano = config.DATA_RAW_INMET / config.UF_SIGLA / str(ano)
        # TODO: se destino_ano já tiver CSVs, pular o ano (evita baixar 100+ MB à toa)
        if destino_ano.exists() and any(destino_ano.glob("*.csv")):
            print(f"-> Ano {ano} já processado. Pulando.")
            continue
        zip_path = inmet.baixar_ano(ano, config.DATA_RAW_INMET / "_zips")
        arquivos = inmet.extrair_estacoes_uf(zip_path, config.UF_SIGLA, destino_ano)
        zip_path.unlink()
        # TODO: print do ano e da quantidade de estações
        print(f"-> Ano {ano} processado. Estações: {len(arquivos)}")


def main():
    ingerir_producao()
    ingerir_clima()


if __name__ == "__main__":
    main()
