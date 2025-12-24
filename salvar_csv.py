import csv
import os

def salvar_csv(dados, nome_arquivo="resultado_rq.csv"):
    if not dados:
        print("⚠️ Nenhum dado para salvar no CSV.")
        return

    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

    # Colunas baseadas nas chaves do dicionário
    colunas = dados[0].keys()

    # ==============================
    # Ler RQs já existentes no CSV
    # ==============================
    rqs_existentes = set()

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, mode="r", encoding="utf-8-sig") as arquivo:
            leitor = csv.DictReader(arquivo)
            if "RQ" in leitor.fieldnames:
                for linha in leitor:
                    rqs_existentes.add(str(linha["RQ"]).strip())

    # ==============================
    # Filtrar apenas RQs novas
    # ==============================
    novos_dados = [
        d for d in dados
        if str(d.get("RQ", "")).strip() not in rqs_existentes
    ]

    if not novos_dados:
        print("ℹ️ Nenhuma RQ nova para adicionar.")
        return

    # ==============================
    # Escrever (append)
    # ==============================
    arquivo_existe = os.path.exists(caminho_arquivo)

    with open(caminho_arquivo, mode="a", newline="", encoding="utf-8-sig") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=colunas)

        # Escreve cabeçalho apenas se o arquivo for novo
        if not arquivo_existe:
            escritor.writeheader()

        escritor.writerows(novos_dados)

    print(f"✅ {len(novos_dados)} RQs adicionadas ao CSV.")
