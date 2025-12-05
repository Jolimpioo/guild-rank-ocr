import cv2
import pytesseract
from pathlib import Path
from src.utils.text_cleaning import limpar_campo
from src.utils.name_matcher import corrigir_nome
from src.config import REGIOES_BASE, INCREMENTO_Y, NUMERO_LINHAS

# funcao OCR
def ocr_recorte(recorte, campo: str) -> str:
    recorte_cinza = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    
    _, recorte_bin = cv2.threshold(recorte_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    recorte_blur = cv2.GaussianBlur(recorte_cinza, (3, 3), 0)
    _, recorte_bin_blur = cv2.threshold(recorte_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # config tesseract
    config = '--psm 7 -c tessedit_char_whitelist=0123456789/'
    if campo == 'nome':
        config = '--psm 8'

    # OCR principal
    texto = pytesseract.image_to_string(recorte_bin, config=config, lang='eng+por+jpn').strip()

    # segunda tentativa campo nome caso vazio ou muito curto
    if campo == 'nome' and (not texto or len(texto) < 2):
        texto = pytesseract.image_to_string(recorte_bin_blur, config='--psm 8', lang='eng+por+jpn').strip()

    return texto

# processamento imagem 
def processar_imagem(caminho_imagem: str) -> list[dict]:
    # executa OCR e extrai dados da imagem
    img = cv2.imread(caminho_imagem)
    if img is None:
        return []
    
    dados_extraidos = []
    nome_imagem = Path(caminho_imagem).name

    for i in range(NUMERO_LINHAS):
        linha_dados = {'imagem_origem': nome_imagem}

        for campo, (x, y, w, h) in REGIOES_BASE.items():
            y_atual = y + (INCREMENTO_Y * i)
            recorte = img[y_atual:y_atual+h, x:x+w]
            texto = ocr_recorte(recorte, campo)

            # correcoes pos OCR
            if campo == 'nome' and texto:
                nome_corrigido, status = corrigir_nome(texto)
                linha_dados['nome'] = nome_corrigido
                linha_dados['status'] = status 
            else:
                texto = limpar_campo(campo, texto)
                linha_dados[campo] = texto if texto else ""

        if 'status' not in linha_dados:
            linha_dados['status'] = ""

        dados_extraidos.append(linha_dados)


        status_display = f" [{linha_dados['status']}]" if linha_dados['status'] else ""
        print(f"{linha_dados.get('nome', 'VAZIO'):10} | {linha_dados.get('frequencia', 'N/A'):3} | {linha_dados.get('dano', '0'):10}{status_display}")
    
    
    return dados_extraidos