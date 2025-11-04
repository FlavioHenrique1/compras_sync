import csv
import os

def salvar_csv(dados, nome_arquivo="resultado_rq.csv"):
    # Caso não existam dados, não criar o arquivo vazio
    if not dados:
        print("⚠️ Nenhum dado para salvar no CSV.")
        return
    
    # Nome fixo + caminho na pasta do projeto
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

    # Pegamos os títulos automaticamente usando as chaves do primeiro item
    colunas = dados[0].keys()

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(dados)

    print(f"✅ CSV criado com sucesso: {caminho_arquivo}")
