import pytest

from my_app.tratar_dados_brutos.fornecedores import (
    remover_acentos,
    normalizar_espacos
)


def test_stringSemAcento():
    resultado = remover_acentos('Fúndação')
    assert resultado == 'Fundacao'


def test_normalizarEspacos():
    resultado = normalizar_espacos(' Teste   de  espaço extras   ')
    assert resultado == 'Teste de espaço extras'