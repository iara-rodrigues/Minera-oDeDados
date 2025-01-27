from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

caminho_chromedriver = "chromedriver" 
service = Service(caminho_chromedriver)

driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.camara.leg.br/busca-portal?contextoBusca=BuscaProposicoes&pagina=1&order=relevancia&abaEspecifica=true&tipos=PL"

driver.get(url)

time.sleep(3)

projetos = driver.find_elements(By.CLASS_NAME, "col-11")

dados = []

for projeto in projetos:
    try:
        uls = projeto.find_elements(By.XPATH, '//*[@id="lista-resultados"]/ul')

        for i, ul in enumerate(uls, start=1):  
            numero = ul.find_element(By.XPATH, f'./div/div/div/div[2]/h6/a').text
            autor = ul.find_element(By.XPATH, f'./div/div/div/div[2]/div[1]').text
            ementa = ul.find_element(By.XPATH, f'./div/div/div/div[2]/div[2]/p').text
            data = ul.find_element(By.XPATH, f'./div/div/div/div[2]/p/span').text

            dados.append({
                "Número da PL": numero,
                "Autor": autor,
                "Ementa": ementa,
                "Data": data
            })

    except Exception as e:
        print(f"Erro ao extrair dados de um projeto: {e}")

driver.quit()

df = pd.DataFrame(dados)

print(df)

df.to_csv("projetos_lei.csv", index=False)
print("Dados salvos no arquivo 'projetos_lei.csv'")