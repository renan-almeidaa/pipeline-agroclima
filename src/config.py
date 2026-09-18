import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

IBGE_LOCALIDADES_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
IBGE_AGREGADOS_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"

UF_CODIGO = "41"                                  # Paraná
AGREGADO = "5457"                                 # Produção Agrícola Municipal
CLASSIFICACAO = "782"                             # produto das lavouras temporárias e permanentes
VARIAVEIS = ["214", "216", "112"]                 # quantidade produzida, área colhida, rendimento médio
CULTURAS = ["40124", "40122"]                     # soja em grão, milho em grão
PERIODOS = "-10"                                  # últimos 10 períodos disponíveis
TAMANHO_LOTE = 100                                # municípios por requisição