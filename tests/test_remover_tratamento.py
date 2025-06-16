import unittest

from my_app.funcao_fornecedores import tratar_empresa
from my_app.tratar_dados_brutos.fornecedores import normalizar_espacos

class TestStringMethods(unittest.TestCase):

    def test_espaco(self):
        entrada = ' empresa    teste '
        esperado = 'EMPRESA TESTE'
        resultado = tratar_empresa(entrada)
        self.assertNotEqual(resultado, esperado)

    def test_espaco_nova_funcao(self):
        entrada = ' empresa    teste '
        esperado = 'EMPRESA TESTE'
        resultado = normalizar_espacos(entrada)
        self.assertTrue(resultado, esperado.upper())

if __name__ == '__main__':
    unittest.main()