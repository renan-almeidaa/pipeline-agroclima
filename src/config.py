import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB")

MONGO_URI = (
    f"mongodb://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASSWORD)}"
    f"@{MONGO_HOST}:{MONGO_PORT}/"
)

MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLECAO_PRODUCAO = "producao_agricola" 

IBGE_LOCALIDADES_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
IBGE_AGREGADOS_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"

UF_CODIGO = "41"                                  # Paraná
AGREGADO = "5457"                                 # Produção Agrícola Municipal
CLASSIFICACAO = "782"                             # produto das lavouras temporárias e permanentes
VARIAVEIS = ["214", "216", "112"]                 # quantidade produzida, área colhida, rendimento médio
CULTURAS = ["40124", "40122"]                     # soja em grão, milho em grão
PERIODOS = "-10"                                  # últimos 10 períodos disponíveis
TAMANHO_LOTE = 100                                # municípios por requisição