from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class Navegador:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = self._setup_driver()

    def _setup_driver(self):
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def abrir_pagina(self, url):
        print(f"Abrindo: {url}")
        self.driver.get(url)

    def fechar(self):
        print("Encerrando navegador.")
        self.driver.quit()
