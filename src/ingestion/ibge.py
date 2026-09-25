import requests
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from src import config

CODIGOS_TRANSITORIOS = {429, 500, 502, 503, 504}


def _erro_transitorio(exc: BaseException) -> bool:
    """Retorna True se vale tentar de novo."""
    # Timeout e ConnectionError são erros de rede que podem ser transitórios.
    if isinstance(exc, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)):
        return True
    # HTTPError é levantado pelo raise_for_status() quando o status code indica erro.
    # Se for erro de servidor (5xx) ou limite de requisições (429), vale tentar de novo.
    elif isinstance(exc, requests.exceptions.HTTPError) and exc.response is not None:
        if exc.response.status_code in CODIGOS_TRANSITORIOS:
            return True
    return False


retry_ibge = retry(
    retry=retry_if_exception(_erro_transitorio),
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    reraise=True,
)


@retry_ibge
def buscar_municipios(uf: str) -> list[dict]:
    """Retorna os municípios de uma UF a partir da API de localidades."""

    url = f"{config.IBGE_LOCALIDADES_URL}/estados/{uf}/municipios"
    resp = requests.get(url, timeout=300)
    resp.raise_for_status()
    return resp.json()


def dividir_em_lotes(itens: list, tamanho: int) -> list[list]:
    """Divide uma lista em sublistas de no máximo `tamanho` elementos."""
    return [itens[i : i + tamanho] for i in range(0, len(itens), tamanho)]


@retry_ibge
def buscar_producao(codigos_municipio: list[str]) -> list[dict]:
    """Busca a produção agrícola de um lote de municípios.

    Usa view=flat. A primeira linha da resposta é o cabeçalho, não um
    registro de dados, e por isso é descartada.
    """
    url = (
        f"{config.IBGE_AGREGADOS_URL}/{config.AGREGADO}"
        f"/periodos/{config.PERIODOS}"
        f"/variaveis/{'|'.join(config.VARIAVEIS)}"
        f"?classificacao={config.CLASSIFICACAO}[{','.join(config.CULTURAS)}]"
        f"&localidades=N6[{','.join(codigos_municipio)}]"
        "&view=flat"
    )
    resp = requests.get(url, timeout=300)
    resp.raise_for_status()
    return resp.json()[1:]  # remove o cabeçalho, que é a primeira linha da resposta


# if __name__ == "__main__":
#     municipios = buscar_municipios(config.UF_CODIGO)
#     print(f"municípios: {len(municipios)}")

#     codigos = [str(m["id"]) for m in municipios]
#     lotes = dividir_em_lotes(codigos, config.TAMANHO_LOTE)
#     print(f"lotes: {len(lotes)} | tamanhos: {[len(l) for l in lotes]}")
