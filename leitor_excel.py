import pandas as pd

def ler_rqs_excel(caminho_excel):
    df = pd.read_excel(caminho_excel, engine="openpyxl")

    rqs = df["Requisição"].dropna().astype(str).unique().tolist()

    return rqs