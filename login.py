import time
from navegador import Navegador
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AtualizadorPlanilhaCompras(Navegador):
    def __init__(self, headless=False):
        super().__init__(headless=headless)

    def fazer_login(self, url, email_usuario, senha_usuario):
        """Realiza apenas o login"""
        try:
            self.abrir_pagina(url)

            # === 1. Clicar no botão SSO ===
            botao = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ssoBtn"))
            )
            botao.click()
            time.sleep(4)

            # === 2. Preencher e-mail ===
            campo_email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "loginfmt"))
            )
            campo_email.clear()
            campo_email.send_keys(email_usuario)
            time.sleep(3)

            botao_avancar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "idSIButton9"))
            )
            botao_avancar.click()
            time.sleep(3)

            # === 3. Preencher senha ===
            campo_senha = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "passwd"))
            )
            campo_senha.clear()
            campo_senha.send_keys(senha_usuario)
            time.sleep(3)

            botao_entrar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "idSIButton9"))
            )
            botao_entrar.click()
            time.sleep(3)

            # Tela extra "Manter conectado"
            try:
                botao_entrar1 = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "idSIButton9"))
                )
                botao_entrar1.click()
                time.sleep(3)
            except:
                pass

            print("✅ Login realizado com sucesso!")
            return True

        except Exception as e:
            print("⚠️ Erro durante login:", e)
            return False

    def navegar_para_requisicoes(self):
        """Acessa Procurement > Purchase Requisitions"""
        try:
            menu_procurement = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, "groupNode_procurement"))
            )
            menu_procurement.click()
            time.sleep(3)

            menu_requisitions = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, "itemNode_my_information_purchase_requisitions_0"))
            )
            menu_requisitions.click()
            time.sleep(3)

            print("✅ Página de Purchase Requisitions aberta!")
            return True
        except Exception as e:
            print("⚠️ Erro na navegação:", e)
            return False
