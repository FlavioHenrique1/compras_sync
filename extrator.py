import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from salvar_csv import salvar_csv

class ExtratorTabela:
    def __init__(self, driver, tempo_scroll=3):
        self.driver = driver
        self.tempo_scroll = tempo_scroll  # tempo para o sistema carregar a tabela após o scroll

    def extrair(self):
        resultados = []

        # Espera a tabela carregar pelo menos uma linha
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@id, ':cl5')]"))
        )

        # XPath do botão de voltar na página de detalhes
        voltar_btn_xpath = "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/table/tbody/tr/td/div/a"

        i = 0
        while True:
            print(i)
            time.sleep(2)
            # Reobtém todos os links visíveis de RQ
            rq_links = self.driver.find_elements(By.XPATH, "//a[contains(@id, ':cl5')]")
            time.sleep(2)
            if i >= len(rq_links):
                # Se ainda houver mais linhas no scroll, rola a tabela para baixo
                tabela_xpath = "//div[contains(@id, 'allMyReqsVCResult::_ATp')]"
                tabela = self.driver.find_element(By.XPATH, tabela_xpath)
                self.driver.execute_script("arguments[0].scrollTop += 300;", tabela)
                time.sleep(self.tempo_scroll)  # espera o sistema carregar novas linhas
                rq_links = self.driver.find_elements(By.XPATH, "//a[contains(@id, ':cl5')]")
                if i >= len(rq_links):
                    break  # não há mais linhas
            try:
                rq_link = rq_links[i]
                rq_numero = rq_link.text.strip()
                print(f"🔹 Processando RQ: {rq_numero}")

                # Clica na RQ usando JavaScript
                self.driver.execute_script("""
                    var evt = document.createEvent('MouseEvents');
                    evt.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0,
                                       false, false, false, false, 0, null);
                    arguments[0].dispatchEvent(evt);
                """, rq_link)

                # Aguarda carregar a página de detalhes
                time.sleep(self.tempo_scroll)
                # Extrai Numero da RQ
                NRQ = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div/div[1]/table/tbody/tr/td[2]/div/h1")
                    )
                ).text.strip()

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

                # Extrai UN de requisição
                UNdereq	 = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]")
                    )
                ).text.strip()

                # Extrai Local de Faturamento
                LocFat = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr/td/table/tbody/tr[9]/td[2]/span")
                    )
                ).text.strip()

                # Extrai Informado por
                InforPor =WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[1]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/span")
                    )
                ).text.strip()

                # Extrai Local para Entrega
                LocalEntrega =WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[6]/td[2]/a")
                    )
                ).text.strip()

                # Extrai centro de custo
                CentroC =WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[3]/span/span/div/table/tbody/tr/td[1]/span/span")
                    )
                ).text.strip()

                # Salva resultado
                resultados.append({
                    "RQ": rq_numero,
                    "Descricao": descricao,
                    "Comprador": comprador,
                    "valor": valorRQ,
                    "statusRQ": statusRQ,
                    "dataCriaRQ": dataCriaRQ,
                    "UNdereq": UNdereq,
                    "LocFat":LocFat,
                    "InforPor":InforPor,
                    "LocalEntrega":LocalEntrega,
                    "CentroC":CentroC,
                    "NRQ":NRQ
                })
                print(f"✅ Extraído: {rq_numero} - {descricao} - {comprador} - {valorRQ} - {statusRQ} - {dataCriaRQ} - {CentroC} - {LocalEntrega}")

                # Volta para a lista
                voltar_btn = self.driver.find_element(By.XPATH, voltar_btn_xpath)
                time.sleep(2)
                self.driver.execute_script("arguments[0].click();", voltar_btn)
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//a[contains(@id, ':cl5')]")
                    )
                )
                time.sleep(self.tempo_scroll)

                i += 1

            except Exception as e:
                print(f"⚠️ Erro ao processar {rq_numero}: {e}")
                # Tenta voltar mesmo em caso de erro
                try:
                    voltar_btn = self.driver.find_element(By.XPATH, voltar_btn_xpath)
                    self.driver.execute_script("arguments[0].click();", voltar_btn)
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//a[contains(@id, ':cl5')]")
                        )
                    )
                    time.sleep(self.tempo_scroll)
                except:
                    pass
                i += 1


        salvar_csv(resultados)  # <<< Salva o CSV
        return resultados
