import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from salvar_csv import salvar_csv

class ExtratorTabela:
    def __init__(self, driver, tempo_scroll=2, timeout_wait=20):
        self.driver = driver
        self.tempo_scroll = tempo_scroll  # tempo para o sistema carregar a tabela após o scroll
        self.timeout_wait = timeout_wait

    def _safe_wait_presence(self, by, selector, timeout=None):
        """Wrapper para WebDriverWait presence_of_element_located com tratamento."""
        t = timeout or self.timeout_wait
        return WebDriverWait(self.driver, t).until(EC.presence_of_element_located((by, selector)))

    def _safe_wait_presence_all(self, by, selector, timeout=None):
        t = timeout or self.timeout_wait
        return WebDriverWait(self.driver, t).until(EC.presence_of_all_elements_located((by, selector)))

    def find_scrollable_table(self):
        """
        Tenta localizar a div da tabela que precisa ser scrollada.
        Retorna o elemento encontrado ou None se não achar.
        """
        # Lista de XPaths que costumam funcionar — adicione mais se souber outros padrões
        possible_xpaths = [
            "//div[contains(@id, 'allMyReqsVCResult::_ATp')]",
            "//div[contains(@id, 'allMyReqsVCResult')]",
            "//div[contains(@class, 'af_tableBody')]",   # exemplo genérico
            "//div[contains(@id, 'results')]"           # fallback genérico
        ]
        for xp in possible_xpaths:
            try:
                el = self.driver.find_element(By.XPATH, xp)
                print(f"✔️ Encontrada tabela pelo XPath: {xp}")
                return el
            except Exception:
                continue
        print("⚠️ Não encontrou div específica para scroll. Usarei scroll da janela como fallback.")
        return None

    def extrair(self):
        resultados = []

        # Espera a tabela carregar pelo menos uma linha de RQ (se existir)
        try:
            WebDriverWait(self.driver, self.timeout_wait).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@id, ':cl5')]"))
            )
            print("✔️ Linha(s) de RQ detectada(s).")
        except Exception as e:
            print(f"⚠️ Timeout esperando por links de RQ: {e}. Vou continuar e tentar recuperar.")

        # XPath do botão de voltar na página de detalhes (se precisar ajuste conforme o seu sistema)
        voltar_btn_xpath = "/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/table/tbody/tr/td/div/a"

        i = 0
        consecutive_failures = 0
        MAX_CONSECUTIVE_FAILS = 5

        while True:
            print(f"\n🔁 Loop principal - index {i}")
            time.sleep(1)  # pequeno descanso para estabilidade

            # Reobtém todos os links visíveis de RQ
            try:
                rq_links = self.driver.find_elements(By.XPATH, "//a[contains(@id, ':cl5')]")
            except Exception as e:
                print(f"⚠️ Falha ao obter lista de links de RQ: {e}")
                rq_links = []

            time.sleep(0.8)

            # Se chegamos ao fim dos links visíveis, tenta scroll na tabela (ou na janela)
            if i >= len(rq_links):
                tabela = self.find_scrollable_table()
                if tabela is not None:
                    try:
                        # scroll dentro da div (mais seguro em apps SPA)
                        self.driver.execute_script("arguments[0].scrollTop += 400;", tabela)
                        print("↧ Rolando a div da tabela para carregar mais linhas...")
                    except Exception as e:
                        print(f"⚠️ Erro ao rolar a div da tabela: {e}. Tentarei scroll da janela.")
                        self.driver.execute_script("window.scrollBy(0, 600);")
                        print("↧ Rolando a janela como fallback.")
                        
                else:
                    # fallback: rola a janela inteira
                    try:
                        self.driver.execute_script("window.scrollBy(0, 600);")
                        print("↧ Rolando a janela para carregar mais linhas...")
                    except Exception as e:
                        print(f"⚠️ Erro ao rolar a janela: {e}")

                time.sleep(self.tempo_scroll)  # espera o sistema carregar novas linhas
                time.sleep(2)
                try:
                    rq_links = self.driver.find_elements(By.XPATH, "//a[contains(@id, ':cl5')]")
                except Exception:
                    rq_links = []

                # Se não apareceram novas linhas, finaliza
                if i >= len(rq_links):
                    print("✅ Não há mais linhas depois do scroll — finalizando.")
                    break

            # Define rq_numero sempre (None se ainda não atribuído) para evitar NameError no except
            rq_numero = None

            try:
                rq_link = rq_links[i]
            except IndexError:
                print(f"⚠️ Índice {i} fora do range dos links ({len(rq_links)}). Tentando continuar.")
                consecutive_failures += 1
                if consecutive_failures >= MAX_CONSECUTIVE_FAILS:
                    print("❌ Muitas falhas consecutivas ao acessar links. Finalizando.")
                    break
                time.sleep(1)
                continue
            except Exception as e:
                print(f"⚠️ Erro inesperado obtendo rq_link: {e}")
                # tenta salvar parcial e interrompe
                try:
                    salvar_csv(resultados)
                    print("💾 CSV salvo (parcial) após erro inesperado ao obter rq_link.")
                except Exception as err_csv:
                    print(f"❌ Falha ao salvar CSV: {err_csv}")
                break

            # Obtém o texto da RQ com proteção
            try:
                rq_numero = rq_link.text.strip()
            except Exception:
                rq_numero = None

            print(f"🔹 Processando RQ (index {i}): {rq_numero or 'Desconhecido'}")

            try:
                # Clica na RQ usando JavaScript (às vezes o click padrão falha)
                try:
                    self.driver.execute_script("""
                        var evt = document.createEvent('MouseEvents');
                        evt.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0,
                                           false, false, false, false, 0, null);
                        arguments[0].dispatchEvent(evt);
                    """, rq_link)
                except Exception:
                    # fallback para click padrão
                    rq_link.click()

                # Aguarda carregar a página de detalhes (ou elemento que indique a página de detalhe)
                time.sleep(0.5)
                WebDriverWait(self.driver, self.timeout_wait).until(
                    EC.presence_of_element_located((By.XPATH,
                        "//h1 | //div[contains(@class,'detail') or contains(@id,'detail')]"
                    ))
                )

                # ---------- EXTRAÇÃO DOS DADOS ----------
                # Para cada campo, tentamos localizar com wait; se falhar, definimos valor vazio e seguimos
                def safe_text(xpath, friendly_name="campo"):
                    try:
                        el = WebDriverWait(self.driver, 6).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        return el.text.strip()
                    except Exception:
                        print(f"⚠️ Não encontrou {friendly_name} com XPath: {xpath}")
                        return ""

                NRQ = safe_text("/html/body/div[2]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div/div[1]/table/tbody/tr/td[2]/div/h1", "NRQ")
                descricao = safe_text("/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[1]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]", "descricao")
                comprador = safe_text("/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[10]/td[2]/span", "comprador").replace("\n", "").replace("Mais...", "").strip()
                valorRQ = safe_text("/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]", "valorRQ")
                statusRQ = safe_text("/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]", "statusRQ")
                dataCriaRQ = safe_text("/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]", "dataCriaRQ")
                UNdereq = safe_text("/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]", "UNdereq")
                LocFat = safe_text("/html/body/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[3]/div/table/tbody/tr/td/table/tbody/tr[9]/td[2]/span", "LocFat")
                InforPor = safe_text("/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/table/tbody/tr/td[1]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/span", "InforPor")
                LocalEntrega = safe_text("/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[6]/td[2]/a", "LocalEntrega")
                CentroC = safe_text("/html/body/div[1]/form/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/table/tbody/tr/td[1]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div[7]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[3]/span/span/div/table/tbody/tr/td[1]/span/span", "CentroC")

                # Salva resultado no buffer
                resultados.append({
                    "RQ": rq_numero,
                    "Descricao": descricao,
                    "Comprador": comprador,
                    "valor": valorRQ,
                    "statusRQ": statusRQ,
                    "dataCriaRQ": dataCriaRQ,
                    "UNdereq": UNdereq,
                    "LocFat": LocFat,
                    "InforPor": InforPor,
                    "LocalEntrega": LocalEntrega,
                    "CentroC": CentroC,
                    "NRQ": NRQ
                })

                print(f"✅ Extraído: {rq_numero or 'Desconhecido'} - {descricao[:40]}...")

                # Volta para a lista de RQs
                try:
                    voltar_btn = self.driver.find_element(By.XPATH, voltar_btn_xpath)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", voltar_btn)
                except Exception:
                    # fallback: tenta voltar pelo histórico do navegador
                    try:
                        self.driver.back()
                        print("↩️ Usando driver.back() como fallback para voltar à lista.")
                    except Exception:
                        print("⚠️ Não foi possível voltar para a lista via botão nem via history. Prosseguirei com cautela.")

                # Aguarda lista reaparecer
                try:
                    WebDriverWait(self.driver, self.timeout_wait).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id, ':cl5')]"))
                    )
                except Exception:
                    print("⚠️ Lista de RQs não reapareceu dentro do timeout. Vou tentar continuar, mas pode falhar.")
                    # não aborta aqui — vamos permitir que o loop tente novos scrolls

                time.sleep(self.tempo_scroll)
                consecutive_failures = 0
                i += 1

            except Exception as e:
                # Tratamento robusto de exceções: sempre tenta salvar resultados já coletados
                print(f"⚠️ Erro ao processar {rq_numero or 'Desconhecido'}: {e}")

                try:
                    salvar_csv(resultados)
                    print("💾 CSV salvo (parcial) após erro.")
                except Exception as err_csv:
                    print(f"❌ Falha ao salvar CSV após erro: {err_csv}")

                # tenta voltar para a lista para evitar travamento
                try:
                    voltar_btn = self.driver.find_element(By.XPATH, voltar_btn_xpath)
                    self.driver.execute_script("arguments[0].click();", voltar_btn)
                    WebDriverWait(self.driver, 6).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id, ':cl5')]"))
                    )
                    time.sleep(self.tempo_scroll)
                    print("↩️ Voltou para a lista após erro (tentativa).")
                except Exception:
                    print("⚠️ Não conseguiu voltar para a lista após erro. Encerrando extração.")
                    break  # encerra o loop principal

        # Ao final, sempre tenta salvar o que foi coletado
        try:
            salvar_csv(resultados)
            print("💾 CSV final salvo com sucesso.")
        except Exception as err_csv:
            print(f"❌ Falha ao salvar CSV final: {err_csv}")

        return resultados
