import re
import unicodedata

def remover_acentos(texto: str) -> str:
    """
    Normaliza uma string a transformando em bytes e depois ignorando acentos
    e a convertendo para string normal.
    """

    texto = unicodedata.normalize('NFD', texto)
    textoSemAcento = texto.encode('ascii', 'ignore').decode('utf-8')
    return textoSemAcento

def normalizar_espacos(texto: str) -> str:
    """
    Substitui espaços extras por apenas um espaço 
    """

    textoSemEspaçoExtras = re.sub(r'\s+', ' ', texto).strip()
    return textoSemEspaçoExtras
