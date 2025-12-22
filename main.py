import os
from dotenv import load_dotenv
from login import AtualizadorPlanilhaCompras
from interacao import InteracaoSistema
from extrator import ExtratorTabela

# Carregar variáveis do .env
load_dotenv()

URL = os.getenv("URL")
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

if __name__ == "__main__":
    app = AtualizadorPlanilhaCompras(headless=False)

    try:
        if app.fazer_login(URL, EMAIL, SENHA):

            interacao = InteracaoSistema(app.driver)
            interacao.acessar_pagina_requisicoes()
            interacao.exemplo_interacao()
            extrator = ExtratorTabela(app.driver)
            print("terminou a execução")
    finally:
        app.fechar()
