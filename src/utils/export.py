import csv
from datetime import datetime
from pathlib import Path

def exportar_csv(dados: list[dict], nome_arquivo: str = None):
    if not dados:
        print('Nenhum dado para exportar')
        return

    if not nome_arquivo:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"ocr_dados_{timestamp}.csv"

    # cria pasta de saida se nao existir
    Path("output").mkdir(exist_ok=True)
    caminho_completo = Path("output") / nome_arquivo

    colunas = list(dados[0].keys())

    # escreve dados no arquivo csv
    with open(caminho_completo, 'w', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(dados)

    print(f"Dados exportados para {caminho_completo}")
    print(f"Total de registros exportados: {len(dados)}")
