import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from salvar_csv import salvar_csv
from leitor_excel import ler_rqs_excel
import os


class ExtratorTabela:
    def __init__(self, driver, tempo_scroll=2, timeout_wait=20):
        self.driver = driver
        self.tempo_scroll = tempo_scroll
        self.timeout_wait = timeout_wait

        # IDs fixos informados por você
        self.CAMPO_PESQUISA_RQ = "pt1:_FOr1:1:_FONSr2:0:MAnt2:1:pt1:r1:0:ap1:r1:0:q1:value20"
        self.BOTAO_PESQUISAR = "pt1:_FOr1:1:_FONSr2:0:MAnt2:1:pt1:r1:0:ap1:r1:0:q1::search"
        self.LINK_RQ_FILTRADA = "//a[contains(@id, ':cl5')]"

        # XPath do botão Voltar (o mesmo que você já usava)
        self.voltar_btn_xpath = "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/table/tbody/tr/td/div/a"

    # ======================================================
    # 🔎 Pesquisa a RQ no campo e abre o resultado filtrado
    # ======================================================
    def pesquisar_e_abrir_rq(self, numero_rq):
        print(f"🔍 Pesquisando RQ: {numero_rq}")

        # Campo de pesquisa
        campo = WebDriverWait(self.driver, self.timeout_wait).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'value20')]"))
        )

        # Setar valor via JS (ADF safe)
        self.driver.execute_script(
            """
            arguments[0].focus();
            arguments[0].value = '';
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            campo,
            str(numero_rq)
        )

        # Clicar no botão pesquisar
        botao = WebDriverWait(self.driver, self.timeout_wait).until(
            EC.element_to_be_clickable((By.ID, self.BOTAO_PESQUISAR))
        )
        self.driver.execute_script("arguments[0].click();", botao)

        # 🔴 ADF precisa de tempo para renderizar a linha
        time.sleep(2)

        # Localiza o link EXATO da RQ pelo texto
        rq_link = WebDriverWait(self.driver, self.timeout_wait).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//a[normalize-space()='{numero_rq}']"
            ))
        )

        # Scroll até o link (ESSENCIAL)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            rq_link
        )
        time.sleep(0.5)

        # Clique via JS (ADF safe)
        self.driver.execute_script("arguments[0].click();", rq_link)

        print(f"➡️ Entrou na RQ {numero_rq}")



    # ======================================================
    # 📥 EXTRAÇÃO PRINCIPAL (via Excel)
    # ======================================================
    def extrair(self):
        resultados = []

        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_excel = os.path.join(base_dir, "RQ.xlsx")

        lista_rqs = ler_rqs_excel(caminho_excel)

        print(f"📊 Total de RQs no Excel: {len(lista_rqs)}")

        for rq_numero in lista_rqs:
            try:
                self.pesquisar_e_abrir_rq(rq_numero)

                # Aguarda tela de detalhe
                WebDriverWait(self.driver, self.timeout_wait).until(
                    EC.presence_of_element_located((By.XPATH, "//h1"))
                )

                # =============================
                # Função segura de texto
                # =============================
                def safe_text(xpath, nome="campo"):
                    try:
                        el = WebDriverWait(self.driver, 6).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        return el.text.strip()
                    except Exception:
                        print(f"⚠️ Não encontrou {nome}")
                        return ""

                # =============================
                # EXTRAÇÃO (XPATHS ORIGINAIS)
                # =============================
                
                TipoRQ = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span",
                    "TTipoRQ"
                )

                Justificativa = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]",
                    "Justificativa"
                )

                LocalEntrega = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[6]/td[2]/a",
                    "LocalEntrega"
                )

                CC = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[3]/span/span/div/table/tbody/tr/td[1]/span/span",
                    "CC"
                )

                descricao = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[1]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]",
                    "descricao"
                )

                comprador = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[10]/td[2]/span",
                    "comprador"
                ).replace("\n", "").replace("Mais...", "").strip()

                valorRQ = safe_text(
                    "/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]",
                    "valorRQ"
                )

                statusRQ = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]",
                    "statusRQ"
                )

                dataCriaRQ = safe_text(
                    "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]",
                    "dataCriaRQ"
                )

                resultados.append({
                    "RQ": rq_numero,
                    "Descricao": descricao,
                    "Comprador": comprador,
                    "Valor": valorRQ,
                    "Status": statusRQ,
                    "DataCriacao": dataCriaRQ,
                    "TipoRQ": TipoRQ,
                    "Justificativa": Justificativa,
                    "LocalEntrega": LocalEntrega,
                    "CC": CC
                })

                print(f"✅ Extraído com sucesso: {rq_numero}")

                # =============================
                # 🔙 VOLTAR PARA LISTA
                # =============================
                try:
                    voltar = self.driver.find_element(By.XPATH, self.voltar_btn_xpath)
                    self.driver.execute_script("arguments[0].click();", voltar)
                except Exception:
                    self.driver.back()

                WebDriverWait(self.driver, self.timeout_wait).until(
                    EC.presence_of_element_located((By.ID, self.CAMPO_PESQUISA_RQ))
                )

                time.sleep(self.tempo_scroll)

            except Exception as e:
                print(f"❌ Erro ao processar RQ {rq_numero}: {e}")
                salvar_csv(resultados)
                continue

        salvar_csv(resultados)
        print("💾 CSV final salvo com sucesso")

        return resultados
