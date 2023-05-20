from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from validacoes.validarTextoEmArray import validarTextoEmArray

def verificar_texto_em_array(texto, array):
    for elemento in array:
        if elemento.upper() in texto.upper():
            return True
    return False

def busca(url, tipoDeClasse, classe):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # Faz a requisição HTTP para a página de teclados do Kabum
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    while(not driver.find_elements_by_class_name("eUTaSA") and not driver.find_elements_by_class_name("cyQKTT")):
        try:
            WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, "hJbuz"))
            )
            ver_mais_button = driver.find_element(By.CLASS_NAME, "hJbuz")
            print(ver_mais_button)
            ver_mais_button.click()
        except:
            print('caiu no except')
            
    
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Encontra todos os produtos da página que são teclados
    return soup.find_all(tipoDeClasse, {"class": classe})


def cliqueFarma(planilha, cliqueFormaURL, filtros):    
    
    linha_atual = planilha.max_row + 1
    tipoDeClasse = "div"
    classe = "ProductWrapperstyles__Paper-sc-1b94yc5-0 UZZjD"
    # classe = "__next"

    for indice, item in enumerate(cliqueFormaURL):
        produtos = busca(item, tipoDeClasse, classe)
        for produto in produtos:
            nome = produto.find("h2", {"class": ""}).text.strip()
            if validarTextoEmArray(nome, filtros[indice]):
                fabricante = produto.find("b", string="FABRICANTE:")
                if fabricante is not None: 
                    fabricante = fabricante.find_next("mark").text.strip()

                if produto.find("div", {"class": "swiper-wrapper"}):
                    lojas = produto.find_all("div", {"class": "swiper-wrapper"})
                    for l in lojas:
                        card = l.find_all("div", {"class": "swiper-slide"})
                        for loja in card:
                            preco = loja.find("p", {"class": "OyUCD"})
                            if preco is not None:
                                preco = preco.text.strip()
                            link = "https://www.cliquefarma.com.br/" + loja.find("a")["href"]
                            nomeLoja = loja.find("p", {"class": "bjRtsq"})
                            if preco is not None:
                                nomeLoja = nomeLoja.text.strip()
                            # Insere os valores na planilha
                            planilha.cell(row=linha_atual, column=1, value=nome)
                            planilha.cell(row=linha_atual, column=2, value=nomeLoja)
                            planilha.cell(row=linha_atual, column=3, value=fabricante)
                            planilha.cell(row=linha_atual, column=4, value=preco)
                            planilha.cell(row=linha_atual, column=5, value=link)
                        
                            linha_atual += 1    