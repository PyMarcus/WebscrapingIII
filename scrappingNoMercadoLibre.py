# pegar o nome, link e preço de vários produtos e salvá-los no banco de dados
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from devolvePreco import formataPrecos
from colorama import Fore
import re 


def parser(url):
    """Faz Parser html"""
    try:
        html = urlopen(url)
    except HTTPError:
        pass
    except URLError:
        pass
    else:
        return BeautifulSoup(html.read(), 'html.parser')


class Crawler:
    """Classe principal que ,com base nas tags, identifica os conteúdos"""
    def __init__(self, url, tagtitulo, taglink, tagpreco, tagproximaPag):
        self.url = url
        self.tagtitulo = tagtitulo
        self.taglink = taglink
        self.tagpreco = tagpreco
        self.parser = parser(self.url)
        self.urlNew = url
        self.tagproximaPag = tagproximaPag

    def crawler(self):
        global listaLinks
        global listaPrecos
        global listaTitulos


        titulos = self.parser.select(self.tagtitulo)  
        for titulo in titulos:# pega o título do produto
            listaTitulos.append(titulo.text)

        #--------------------------------------------
        links = self.parser.select(self.taglink)
        for link in links:  # links para os produtos
            if 'href' in link.attrs:
                if link.attrs['href'] in listaLinks:
                    pass
                else:
                    listaLinks.append(link.attrs['href'])

        #--------------------------------------------
        precos = self.parser.select(self.tagpreco)
        pulaPrecoParcela = 0  # se os números forem pares, pega somente os precos que estão mostrando o valor total com desconto
        for preco in precos:
            if pulaPrecoParcela % 2 == 0:
                price = formataPrecos(preco.text)  # entrega os preços dos produtos
                listaPrecos.append(price)
            pulaPrecoParcela += 1

        # ---------exibição--------------------------
        exibir = Exibir()
        exibir.echo(listaTitulos, listaLinks, listaPrecos)
        
        proxima = self.parser.select(self.tagproximaPag)
        lista = []
        for proximo in proxima:
            if proximo.attrs['title'] == 'Seguinte':
                self.urlNew = proximo.attrs['href']
                print(self.urlNew)
                if self.urlNew not in lista:
                    lista.append(self.urlNew)
                    #-------Busca raspando as páginas ------
                    print(Fore.WHITE + '')
                    if lista != 0 or lista != None:
                        print(Fore.RED + f"URL DA PRÓXIMA PÁGINA: {self.urlNew}")
                        print(Fore.WHITE + '')
                        newCrawler = Crawler(self.urlNew, self.tagtitulo, self.taglink, self.tagpreco, self.tagproximaPag)
                        newCrawler.crawler()



class Exibir:
     """Classe e função para exibição, apenas"""
     def echo(self, listaTitulos, listaLinks, listaPrecos):
        for n in range(len(listaTitulos)):
            print(f"Título: {listaTitulos[n]}.\nPreço: {listaPrecos[n]}.\nLink: {listaLinks[n]}\n")



if __name__ == '__main__':
    
    listaPrecos, listaLinks, listaTitulos = [], [], []

    urlBase = 'https://lista.mercadolivre.com.br/'  # url base para pesquisa de produtos

    # proxima página
    tag = 'div.ui-search-pagination ul li.andes-pagination__button--next a'
    #---------------
    # aqui, pode-se passar vários produtos:
    produtos = ['relogios', 'blusas', 'bonés', 'notebooks', 'chinelos']
    for produto in produtos:
        crawler = Crawler(urlBase + produto, 'h2', 'div.ui-search-result__image a', 'div.ui-search-price__second-line span.price-tag-text-sr-only', tag)
        crawler.crawler()
