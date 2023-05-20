from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from validacoes.validarTextoEmArray import validarTextoEmArray

def busca(url, tipoDeClasse, classe):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    sleep(4)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    return soup.find_all(tipoDeClasse, {"class": classe})

def pagueMenos(planilha, pagueMenosURL, filtros): 
    
    linha_atual = planilha.max_row + 1
    tipoDeClasse = "div"
    classe = "vtex-search-result-3-x-galleryItem"

    for indice, item in enumerate(pagueMenosURL):
        produtos = busca(item, tipoDeClasse, classe)
        for produto in produtos:
            nome = produto.find("span", {"class": "vtex-product-summary-2-x-brandName"}).text.strip()
            if validarTextoEmArray(nome, filtros[indice]):
                preco = produto.find("div", {"class": "paguemenos-teaser-labels-2-x-price"})
                if preco is None:
                    return
                link = "https://www.paguemenos.com.br/" + produto.find("a")["href"]
                planilha.cell(row=linha_atual, column=1, value=nome)
                planilha.cell(row=linha_atual, column=2, value="Pague Menos")
                planilha.cell(row=linha_atual, column=3, value="nao possui")
                planilha.cell(row=linha_atual, column=4, value=preco.text.strip())
                planilha.cell(row=linha_atual, column=5, value=link)
            
                linha_atual += 1 

                           