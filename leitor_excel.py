import pandas as pd
import os

def ler_rqs_excel(caminho_excel):
    # Lê todas as RQs do Excel
    df_excel = pd.read_excel(caminho_excel, engine="openpyxl")
    rqs_excel = (
        df_excel["Requisição"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    # Caminho do CSV de resultado (mesma pasta do projeto)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(base_dir, "resultado_rq.csv")

    # Se ainda não existir CSV, tudo é pendente
    if not os.path.exists(caminho_csv):
        print("ℹ️ CSV ainda não existe. Todas as RQs serão processadas.")
        return rqs_excel

    # Lê RQs já processadas no CSV
    df_csv = pd.read_csv(caminho_csv)

    if "RQ" not in df_csv.columns:
        print("⚠️ CSV não possui coluna 'RQ'. Processando todas.")
        return rqs_excel

    rqs_processadas = (
        df_csv["RQ"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    # Filtra somente RQs pendentes
    rqs_pendentes = [rq for rq in rqs_excel if rq not in rqs_processadas]

    print(f"📊 Total no Excel: {len(rqs_excel)}")
    print(f"✅ Já processadas: {len(rqs_processadas)}")
    print(f"⏳ Pendentes: {len(rqs_pendentes)}")

    return rqs_pendentes
