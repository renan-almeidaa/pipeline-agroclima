import zipfile

from src.ingestion.inmet import extrair_estacoes_uf


def test_extrai_so_arquivos_da_uf(tmp_path):
    zip_path = tmp_path / "2023.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        # TODO: zf.writestr(nome, conteudo) para 2 arquivos _PR_ e 1 _SP_  
        zf.writestr("estacoes_PR.csv", "conteudo_PR")
        zf.writestr("estacoes_PR2.csv", "conteudo_PR2")
        zf.writestr("estacoes_SP.csv", "conteudo_SP")

    # TODO: chamar extrair_estacoes_uf para "PR" com destino em tmp_path / "saida"
    saida_path = tmp_path / "saida"
    extrair_estacoes_uf(zip_path, "PR", saida_path)
    # TODO: verificar que voltaram 2 caminhos e que nenhum nome tem "_SP_"
    arquivos_extraidos = list(saida_path.glob("*.csv"))
    assert len(arquivos_extraidos) == 2
    assert all("_SP_" not in arquivo.name for arquivo in arquivos_extraidos)

