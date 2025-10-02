import os
from dotenv import load_dotenv
from login import AtualizadorPlanilhaCompras
from interacao import InteracaoSistema

# Carregar variáveis do arquivo .env
load_dotenv()

URL = os.getenv("URL")
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

if __name__ == "__main__":
    app = AtualizadorPlanilhaCompras(headless=False)

    if app.fazer_login(URL, EMAIL, SENHA):
        print("teste")

        # Agora passa o driver logado para a nova classe
        interacao = InteracaoSistema(app.driver)
        print("teste1")
        interacao.acessar_pagina_requisicoes()
        print("teste2")
        interacao.exemplo_interacao()

    app.fechar()
