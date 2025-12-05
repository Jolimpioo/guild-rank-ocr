import glob
from src.ocr.extractor import processar_imagem
from src.utils.export import exportar_csv

def main():
    todos_dados = []

    imagens = glob.glob('./images/*.jpeg')
    for caminho_imagem in imagens:
        dados = processar_imagem(caminho_imagem)
        todos_dados.extend(dados)
        print()

    if todos_dados:
        todos_dados.sort(key=lambda x: int(x.get('dano', '0') or '0'), reverse=True)
        
        print("-" * 50)
        for i, registro in enumerate(todos_dados[:10], 1):
            nome = registro['nome']
            dano = int(registro.get('dano', '0') or '0')
            print(f"{i:2}. {nome:20} - {dano:,}".replace(',', '.'))

        exportar_csv(todos_dados)
    else:
        print("Nenhum dado extraído de todas as imagens")

if __name__ == "__main__":
    main()