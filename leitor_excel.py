import pandas as pd
import os

def ler_rqs_excel(caminho_excel):
    # =========================
    # Lê Excel
    # =========================
    df_excel = pd.read_excel(caminho_excel, engine="openpyxl")

    df_excel["Requisição"] = (
        df_excel["Requisição"]
        .astype(str)
        .str.strip()
    )

    # =========================
    # Caminho do CSV
    # =========================
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(base_dir, "resultado_rq.csv")

    # =========================
    # Se CSV não existe → tudo pendente
    # =========================
    if not os.path.exists(caminho_csv):
        print("ℹ️ CSV ainda não existe. Todas as RQs serão processadas.")
        return df_excel["Requisição"].dropna().unique().tolist()

    # =========================
    # Lê CSV
    # =========================
    df_csv = pd.read_csv(caminho_csv, dtype=str)
    df_csv["RQ"] = df_csv["RQ"].astype(str).str.strip()

    # =========================
    # ATUALIZA Valor e Status
    # =========================
    atualizacoes = 0

    for idx_csv, row_csv in df_csv.iterrows():
        rq = row_csv["RQ"]

        match_excel = df_excel[df_excel["Requisição"] == rq]

        if match_excel.empty:
            continue

        excel_row = match_excel.iloc[0]

        valor_excel = str(excel_row.get("Valor da Aprovação", "")).strip()
        status_excel = str(excel_row.get("Status", "")).strip()

        # Atualiza Valor
        if valor_excel and valor_excel != str(row_csv.get("Valor", "")).strip():
            df_csv.at[idx_csv, "Valor"] = valor_excel
            atualizacoes += 1

        # Atualiza Status
        if status_excel and status_excel != str(row_csv.get("Status", "")).strip():
            df_csv.at[idx_csv, "Status"] = status_excel
            atualizacoes += 1

    if atualizacoes > 0:
        df_csv.to_csv(caminho_csv, index=False, encoding="utf-8-sig")
        print(f"🔄 {atualizacoes} campos atualizados no CSV.")
    else:
        print("✅ Nenhuma atualização necessária no CSV.")

    # =========================
    # Identifica pendentes
    # =========================
    rqs_excel = set(df_excel["Requisição"].dropna().unique())
    rqs_csv = set(df_csv["RQ"].dropna().unique())

    rqs_pendentes = sorted(rqs_excel - rqs_csv)

    print(f"📊 Total no Excel: {len(rqs_excel)}")
    print(f"✅ Já no CSV: {len(rqs_csv)}")
    print(f"⏳ Pendentes: {len(rqs_pendentes)}")

    return rqs_pendentes
