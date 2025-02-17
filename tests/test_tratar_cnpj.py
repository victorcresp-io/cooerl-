import pytest
import pandas as pd
import numpy as np
from my_app.funcao_fornecedores import tratar_cnpj_df, tratar_nome_fornecedores


@pytest.fixture
def df_exemplo():
    data = {
        'empresa': ['Victor - ltda', 'Teste - ltda', 'Minha-empresa'],
        'cpf_cnpj': ['02,961.715/0001-36',' 02,961.715/  0001-36', '   02,961.715/  0001-36' ]
    }

    return pd.DataFrame(data)


def test_tratar_cnpj_df(df_exemplo):
    df_tratado = tratar_cnpj_df(df_exemplo)

    assert df_tratado['cpf_cnpj'][0] == '02.961.715/0001-36'
    assert df_tratado['cpf_cnpj'][1] == '02.961.715/0001-36'
    assert df_tratado['cpf_cnpj'][1] == '02.961.715/0001-36'



@pytest.fixture
def df_exemplo3():
    data = {
        'Nome/Razão Social': ['Rio   ','   Rio  ', 'Joao  Rio', 'Fornecedor.', 'Fornecedor ,']
    }

    return pd.DataFrame(data)

def test_tratar_nome_fornecedor(df_exemplo3):
    df_exemplo3 = tratar_nome_fornecedores(df_exemplo3)
    assert df_exemplo3['Nome/Razão Social'][0] == 'Rio'
    assert df_exemplo3['Nome/Razão Social'][1] == 'Rio'
    assert df_exemplo3['Nome/Razão Social'][2] == 'Joao Rio'
    assert df_exemplo3['Nome/Razão Social'][3] == 'Fornecedor'
    assert df_exemplo3['Nome/Razão Social'][4] == 'Fornecedor'