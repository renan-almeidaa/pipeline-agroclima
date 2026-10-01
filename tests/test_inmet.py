import zipfile

from src.ingestion.inmet import extrair_estacoes_uf


def test_extrai_so_arquivos_da_uf(tmp_path):
    zip_path = tmp_path / "2023.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("INMET_S_PR_A807_CURITIBA_01-01-2023_A_31-12-2023.CSV", "conteudo_PR")
        zf.writestr("INMET_S_PR_A807_MARINGA_01-01-2023_A_31-12-2023.CSV", "conteudo_PR2")
        zf.writestr("INMET_S_SP_A807_SAOPAULO_01-01-2023_A_31-12-2023.CSV", "conteudo_SP")

    saida_path = tmp_path / "saida"
    caminhos = extrair_estacoes_uf(zip_path, "PR", saida_path)
    assert len(caminhos) == 2
    assert all("_SP_" not in caminho.name for caminho in caminhos)
