import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navegador import Navegador


class InteracaoSistema(Navegador):
    def __init__(self, driver):
        # Reaproveita o mesmo navegador já logado
        self.driver = driver

    def acessar_pagina_requisicoes(self):
        """Abre a página de requisições de compras"""
        url_requisicoes = (
            "https://fa-euld-saasfaprod1.fa.ocs.oraclecloud.com/"
            "fscmUI/faces/FuseWelcome?_afrLoop=31542526057049838&_afrWindowMode=0&_afrWindowId=null"
            "&_adf.ctrl-state=10iu0dekos_1&_afrFS=16&_afrMT=screen&_afrMFW=1517&_afrMFH=703&_afrMFDW=1366"
            "&_afrMFDH=768&_afrMFC=8&_afrMFCI=0&_afrMFM=0&_afrMFR=86&_afrMFG=0&_afrMFS=0&_afrMFO=0"
        )
        self.driver.get(url_requisicoes)
        print("🌐 Página de requisições carregada")
        time.sleep(5)

    def exemplo_interacao(self):
        """Exemplo de como interagir com elementos depois do login"""
        try:
            elemento = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            print("✅ Página acessada com título:", elemento.text)
            time.sleep(3)
            botaoCompras = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "clusters-right-nav"))
            )
            botaoCompras.click()
            time.sleep(3)
            botaoCompras1 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "groupNode_procurement"))
            )
            botaoCompras1.click()
            time.sleep(3)

            
            
        except Exception as e:
            print("⚠️ Não consegui pegar o título da página:", e)
