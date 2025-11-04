import os
from dotenv import load_dotenv
from login import AtualizadorPlanilhaCompras
from interacao import InteracaoSistema
from extrator import ExtratorTabela
from salvar_csv import salvar_csv
import csv

# Carregar variáveis do arquivo .env
load_dotenv()

URL = os.getenv("URL")
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

if __name__ == "__main__":
    app = AtualizadorPlanilhaCompras(headless=False)

    if app.fazer_login(URL, EMAIL, SENHA):

        # Agora passa o driver logado para a nova classe
        interacao = InteracaoSistema(app.driver)
        interacao.acessar_pagina_requisicoes()
        interacao.exemplo_interacao()

    app.fechar()
