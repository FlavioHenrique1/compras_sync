import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navegador import Navegador
from extrator import ExtratorTabela


class InteracaoSistema(Navegador):
    def __init__(self, driver):
        self.driver = driver

    def acessar_pagina_requisicoes(self):
        """Abre a página de requisições de compras"""
        url_requisicoes = (
            "https://fa-euld-saasfaprod1.fa.ocs.oraclecloud.com/"
            "fscmUI/faces/FuseWelcome?_afrLoop=31542526057049838&_afrWindowMode=0&_afrWindowId=null"
            "&_adf.ctrl-state=10iu0dekos_1&_afrFS=16&_afrMT=screen&_afrMFW=1517&_afrMFH=703&_afrMFDW=1366"
            "&_afrMFDH=768&_afrMFC=8&_afrMFM=0&_afrMFR=86&_afrMFG=0&_afrMFS=0&_afrMFO=0"
        )
        self.driver.get(url_requisicoes)
        print("🌐 Página de requisições carregada")
        time.sleep(5)

    def exemplo_interacao(self):
        """Executa toda a navegação até chegar na tabela"""
        try:
            elemento = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            print("✅ Página acessada com título:", elemento.text)
            time.sleep(3)

            # Abre o menu de Compras
            botaoCompras = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "clusters-right-nav"))
            )
            botaoCompras.click()
            time.sleep(3)

            # Abre o grupo "Procurement"
            botaoCompras1 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "groupNode_procurement"))
            )
            botaoCompras1.click()
            time.sleep(3)

            # Abre "Requisições de Compra"
            botaoRequisicaoComp = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "itemNode_my_information_purchase_requisitions_0"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", botaoRequisicaoComp)
            time.sleep(1)
            botaoRequisicaoComp.click()
            print("✅ Cliquei em 'Requisições de Compra'")
            time.sleep(3)

            # Clica em "Exibir Mais"
            botaoExibirMais = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, "pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:SP4:r2:0:c12"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", botaoExibirMais)
            time.sleep(1)
            botaoExibirMais.click()
            print("✅ Cliquei em 'Exibir Mais'")
            time.sleep(10)

            # Extrai a tabela
            self.pegar_tabela()

        except Exception as e:
            print("⚠️ Erro durante interação com o sistema:", e)

    def pegar_tabela(self):
        """Chama o extrator da tabela"""
        extrator = ExtratorTabela(self.driver)
        extrator.extrair()
