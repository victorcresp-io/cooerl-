import pytest

from my_app.tratar_dados_brutos.fornecedores import (
    remover_acentos,
    normalizar_espacos,
    normalizar_colunas
)


def test_stringSemAcento():
    resultado = remover_acentos('Fúndação')
    assert resultado == 'Fundacao'


def test_normalizarEspacos():
    resultado = normalizar_espacos(' Teste   de  espaço extras   ')
    assert resultado == 'Teste de espaço extras'


def test_colunaTratada():
    assert normalizar_colunas('Data de Cadastro') == 'data_de_cadastro'
    assert normalizar_colunas('CPF/CNPJ') == 'cpf_cnpj'
    assert normalizar_colunas('ME/EPP') == 'me_epp'