from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import io
import os
import re

path = os.path.abspath('Seu caminho do chromeDriver');
replacement = "akl_roepstdltklproslPOweos".encode()

with io.open(path, "r+b") as fh:
    for line in iter(lambda: fh.readline(), b""):
        if b"cdc_" in line:
            fh.seek(-len(line), 1);
            newline = re.sub(b"cdc_.{22}", replacement, line);
            fh.write(newline);
            print("\033[93m[*]\033[0m Linha encontrada e alterada com sucesso: ", line, "to", newline);

site = "https://www.estadao.com.br/noticias-ultimas/"

opcoes = Options()
opcoes.headless = True

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=opcoes)
driver.get(site)

containers = driver.find_elements(By.XPATH, '//div[@class="noticias-mais-recenter--item"]')

titulos = []
descricoes = []
datas = []
links = []

for noticias in containers:

    titulo = noticias.find_element(By.XPATH, './div/a/h3').text
    descricao = noticias.find_element(By.XPATH, './div/a/p').text
    data = noticias.find_element(By.XPATH, './div/div[@class="info"]/span[@class="date"]').text
    link = noticias.find_element(By.XPATH, './div/a').get_attribute("href")

    titulos.append(titulo)
    descricoes.append(descricao)
    datas.append(data)
    links.append(link)

dicionario = {
    'Titulo': titulos,
    'Descricao': descricoes,
    'Link': links,
    'Data': datas
    }

manchetes = pd.DataFrame(dicionario)
manchetes.to_csv('Manchetes.csv')

driver.quit()