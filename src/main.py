import glob
from src.ocr.extractor import processar_imagem

def main():
    for caminho_imagem in glob.glob('./images/*.jpeg'):
        processar_imagem(caminho_imagem)

if __name__ == "__main__":
    main()