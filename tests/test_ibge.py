from src.ingestion import ibge


def test_divide_em_lotes_do_tamanho_certo():
    resultado1 = ibge.dividir_em_lotes(list(range(250)), 100)
    assert [len(lote) for lote in resultado1] == [100, 100, 50]

def test_lista_menor_que_lote_vira_um_lote_so():
    resultado = ibge.dividir_em_lotes(list(range(10)), 100)
    assert [len(lote) for lote in resultado] == [10]

def test_lista_vazia_vira_lista_vazia():
    resultado = ibge.dividir_em_lotes([], 100)
    assert resultado == []

def test_juntar_lotes_devolve_lista_original():
    itens = list(range(250))
    lotes = ibge.dividir_em_lotes(itens, 100)
    assert [x for lote in lotes for x in lote] == itens