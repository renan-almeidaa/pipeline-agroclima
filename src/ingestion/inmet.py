import zipfile
from pathlib import Path

import requests

from src import config

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def baixar_ano(ano: int, destino: Path) -> Path:
    """Baixa o zip de um ano do INMET e devolve o caminho do arquivo."""

    url = config.INMET_URL.format(ano=ano)
    response = requests.get(url, headers=HEADERS, timeout=60, stream=True)
    response.raise_for_status()
    destino.mkdir(parents=True, exist_ok=True)  # Garante que a pasta destino existe
    zip_path = destino / f"{ano}.zip"

    # --- EVITA DOWNLOAD REPETIDO ---
    if zip_path.exists():
        print(f"-> Arquivo {zip_path.name} já existe. Pulando download.")
        return zip_path

    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1 MB
            if chunk:
                f.write(chunk)
    print(f"-> Baixado: {zip_path.name}")
    return zip_path


def extrair_estacoes_uf(zip_path: Path, uf: str, destino: Path) -> list[Path]:
    """Extrai do zip só os CSVs das estações da UF e devolve os caminhos."""
    extraidos = []
    destino.mkdir(parents=True, exist_ok=True)  # Garante que a pasta destino existe
    # TODO: abrir com zipfile.ZipFile
    with zipfile.ZipFile(zip_path) as zf:
        for nome_no_zip in zf.namelist():  # Itera sobre os nomes dos arquivos dentro do zip
            nome = Path(nome_no_zip).name  # Pega só o nome do arquivo, sem o caminho
            if f"_{uf}_" not in nome:  # Filtra só os arquivos da UF
                continue
            caminho = destino / nome  # Caminho completo onde o arquivo será extraído
            if not caminho.exists():  # Evita extração repetida
                print(f"   -> Extraindo: {nome_no_zip}")
                with (
                    zf.open(nome_no_zip) as origem,
                    open(caminho, "wb") as destino_arquivo,
                ):  # Abre o arquivo dentro do zip e o destino para escrita
                    destino_arquivo.write(
                        origem.read()
                    )  # Lê o conteúdo do arquivo dentro do zip e escreve no destino

            extraidos.append(caminho)
    return extraidos
