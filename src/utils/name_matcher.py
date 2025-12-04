from rapidfuzz import process, fuzz
from src.config import NOMES_VALIDOS
from src.utils.text_cleaning import limpar_nome

def corrigir_nome(texto_ocr: str) -> str:
    texto_limpo = limpar_nome(texto_ocr)
    if not texto_limpo:
        return ""

    scorers = [
        (fuzz.partial_ratio, 75),
        (fuzz.token_set_ratio, 70),
        (fuzz.ratio, 60),
        (fuzz.token_sort_ratio, 50)
    ]

    for scorer, limiar in scorers:
        melhor_nome, similaridade, _ = process.extractOne(
            texto_limpo, NOMES_VALIDOS, scorer=scorer
        )
        if similaridade >= limiar:
            return melhor_nome


    return texto_limpo if len(texto_limpo) > 2 else ""