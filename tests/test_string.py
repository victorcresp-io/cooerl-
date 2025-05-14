import pytest

from my_app.tratar_dados_brutos.fornecedores import remover_acentos


def test_stringSemAcento():
    resultado = remover_acentos('Fúndação')
    assert resultado == 'Fundacao'