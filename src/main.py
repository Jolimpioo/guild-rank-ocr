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
    
    if not todos_dados:
        print("Nenhum dado extraído de todas as imagens")
        return
    
    # nomes duplicados
    contagem_nomes = {}
    for registro in todos_dados:
        nome = registro.get('nome', '')
        if nome:
            contagem_nomes[nome] = contagem_nomes.get(nome, 0) + 1
    
    for registro in todos_dados:
        nome = registro.get('nome', '')
        if nome and contagem_nomes.get(nome, 0) > 1:
            registro['status'] = 'revisar'
    
    # ordenar e exporta
    todos_dados.sort(key=lambda x: int(x.get('dano', '0') or '0'), reverse=True)
    
    print("-" * 70)
    exportar_csv(todos_dados)

if __name__ == "__main__":
    main()