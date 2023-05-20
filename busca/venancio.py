import requests
from bs4 import BeautifulSoup
from validacoes.validarTextoEmArray import validarTextoEmArray

def verificar_texto_em_array(texto, array):
    for elemento in array:
        if elemento.upper() in texto.upper():
            return True
    return False

def busca(url, tipoDeClasse, classe):
    response = requests.get(url)        
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all(tipoDeClasse, {"class": classe})

def venancio(planilha, venancioURL, filtros):
    
    linha_atual = planilha.max_row + 1
    tipoDeClasse = "div"
    classe = "shelf-product"

    for indice, item in enumerate(venancioURL):
        produtos = busca(item, tipoDeClasse, classe)
        for produto in produtos:
            nome = produto.find("h4", {"class": "shelf-product__title"}).text.strip()
            if validarTextoEmArray(nome, filtros[indice]):
                preco = produto.find("strong", {"class": "shelf-product__price-best"})
                if preco is None:
                    return
                link = produto.find("a")["href"]
                planilha.cell(row=linha_atual, column=1, value=nome)
                planilha.cell(row=linha_atual, column=2, value="venancio")
                planilha.cell(row=linha_atual, column=3, value="nao possui")
                planilha.cell(row=linha_atual, column=4, value=preco.text.strip())
                planilha.cell(row=linha_atual, column=5, value=link)
            
                linha_atual += 1 

                           