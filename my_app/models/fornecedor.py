import re
import unicodedata

import pandas as pd

class NormalizarColuna:
    def __init__(self, separador: str = '_'):
        self.separador = separador

    def remover_acentos(self, texto: str) -> str:
        texto = unicodedata.normalize('NFD', texto)
        return texto.encode('ascii', 'ignore').decode('utf-8')

    def remover_acentos(self, texto: str) -> str:
        texto = unicodedata.normalize('NFD', texto)
        return texto.encode('ascii', 'ignore').decode('utf-8')

    def normalizar_espacos(self, texto: str) -> str:
        return re.sub(r'\s+', ' ', texto).strip()

    def normalizar_coluna(self, texto: str) -> str:
        texto = self.remover_acentos(texto).lower()
        texto = self.normalizar_espacos(texto)
        texto = re.sub(r'[ /]', self.separador, texto)
        return texto
    
    def normalizar_colunas_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        colunas_normalizadas = [self.normalizar_coluna(col) for col in df.columns]
        df.columns = colunas_normalizadas 
        return df
    
