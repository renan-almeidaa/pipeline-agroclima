import logging

from src import config
from src.ingestion import ibge, inmet
from src.logging_config import configurar_logging
from src.storage import mongo

logger = logging.getLogger(__name__)

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
    logger.info("Produção salva com sucesso! Registros: %s", len(producao))


def ingerir_clima():
    for ano in config.INMET_ANOS:
        destino_ano = config.DATA_RAW_INMET / config.UF_SIGLA / str(ano)
        if destino_ano.exists() and any(destino_ano.glob("*.csv")):
            logger.info(" Ano %s já processado. Pulando.", ano)
            continue
        zip_path = inmet.baixar_ano(ano, config.DATA_RAW_INMET / "_zips")
        arquivos = inmet.extrair_estacoes_uf(zip_path, config.UF_SIGLA, destino_ano)
        zip_path.unlink()
        logger.info(" Ano %s processado. Estações: %s", ano, len(arquivos))


def main():
    configurar_logging()
    ingerir_producao()
    ingerir_clima()


if __name__ == "__main__":
    main()
