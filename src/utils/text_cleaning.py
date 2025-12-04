import re

# funcoes tratamento texto
def limpar_nome(texto: str) -> str:
    if not texto:
        return ""
    texto = re.sub(r'[\(\[\{].*?[\)\]\}]', '', texto)
    texto = re.sub(r'[^\w\u3040-\u30ff\u4e00-\u9fff]', ' ', texto)
    return re.sub(r'\s+', ' ', texto).strip()

def limpar_campo(campo: str, texto: str) -> str:
    if campo == 'frequencia':
        return re.sub(r'[^\d/]', '', texto)
    if campo == 'dano':
        texto = re.sub(r'[^\d,]', '', texto)
        return texto.replace(',', '') if texto else "0"
    return texto