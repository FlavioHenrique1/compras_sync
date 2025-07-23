from navegador import Navegador
import time

class AtualizadorPlanilhaCompras(Navegador):
    def __init__(self, headless=False):
        super().__init__(headless=headless)

    def atualizar_planilha(self, url_planilha):
        self.abrir_pagina(url_planilha)
        time.sleep(5)  # Ajuste conforme necessário
        print("Título da página:", self.driver.title)
        # Aqui você pode colocar a lógica para atualizar ou baixar a planilha
