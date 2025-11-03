import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExtratorTabela:
    def __init__(self, driver):
        self.driver = driver

    def extrair(self):
        resultados = []
        processados = set()  # RQs já processadas

        # XPath do botão de voltar da página de detalhes
        voltar_btn_xpath = "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/table/tbody/tr/td/div/a"

        while True:
            # Reobtém todos os links visíveis de RQ
            rq_links = self.driver.find_elements(By.XPATH, "//a[contains(@id, ':cl5')]")
            # Filtra apenas os que ainda não foram processados
            rq_links = [link for link in rq_links if link.text.strip() not in processados]

            if not rq_links:
                break  # Não há mais RQs para processar

            rq_link = rq_links[0]  # Pega o primeiro não processado
            rq_numero = rq_link.text.strip()
            print(f"🔹 Processando RQ: {rq_numero}")

            try:
                # Clica na RQ usando JavaScript (necessário para ADF)
                self.driver.execute_script("""
                    var evt = document.createEvent('MouseEvents');
                    evt.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0,
                                       false, false, false, false, 0, null);
                    arguments[0].dispatchEvent(evt);
                """, rq_link)

                time.sleep(3)  # Espera a página de detalhes carregar

                # Extrai descrição
                descricao = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[1]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]")
                    )
                ).text.strip()

                # Extrai nome do comprador
                comprador = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[10]/td[2]/span")
                    )
                ).text.strip().replace("\n", "").replace("Mais...", "").strip()

                # Extrai valor
                valorRQ = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]")
                    )
                ).text.strip()

                # Extrai status
                statusRQ = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]")
                    )
                ).text.strip()

                # Extrai data de criação
                dataCriaRQ = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]")
                    )
                ).text.strip()

                # Salva resultado
                resultados.append({
                    "RQ": rq_numero,
                    "Descricao": descricao,
                    "Comprador": comprador,
                    "valor": valorRQ,
                    "statusRQ": statusRQ,
                    "dataCriaRQ": dataCriaRQ
                })
                print(f"✅ Extraído: {rq_numero} - {descricao} - {comprador} - {valorRQ} - {statusRQ} - {dataCriaRQ}")

                processados.add(rq_numero)  # Marca como processado

                # Volta para a página da lista
                voltar_btn = self.driver.find_element(By.XPATH, voltar_btn_xpath)
                self.driver.execute_script("arguments[0].click();", voltar_btn)
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id, ':cl5')]"))
                )
                time.sleep(2)

            except Exception as e:
                print(f"⚠️ Erro ao processar {rq_numero}: {e}")
                try:
                    voltar_btn = self.driver.find_element(By.XPATH, voltar_btn_xpath)
                    self.driver.execute_script("arguments[0].click();", voltar_btn)
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id, ':cl5')]"))
                    )
                    time.sleep(2)
                except:
                    pass
                processados.add(rq_numero)  # Evita tentar processar de novo

        return resultados
