import unittest

import pandas as pd
from models.coluna import NormalizarColuna

class TestValidarColunas(unittest.TestCase):
    def test_validar_colunas(self):
        colunas_objetivo = [
            'nome_razao_social',
            'cpf_cnpj', 'crc',
            'tipo_empresarial',
            'me_epp',
            'situacao_da_empresa',
            'data_de_cadastro',
            'cidade',
            'uf',
            'data_extracao'
            ]

        caminho_df = r"C:\Users\victor.crespo\Downloads\cooerl\my_app\data_raw\FORNECEDORES (2).CSV"

        df = pd.read_csv(caminho_df, sep = ';', encoding = 'latin-1')

        normalizador = NormalizadorTexto()

        df = normalizador.normalizar_colunas_dataframe(df)

        self.assertEqual(list(df.columns), colunas_objetivo)

if __name__ == "__main__":
    unittest.main()