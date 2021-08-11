from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup


produto = 'https://lista.mercadolivre.com.br/'


def busca_produtos_mercadolivre(desejado):
    global produto

    try:
        if 'https:' in desejado:
            html = urlopen(desejado)
        else:
            html = urlopen(produto + desejado)
    except HTTPError:
        print('problema no servidor 502 ou na página 404')
    except URLError:
        print('problema com a conexão ou digitou errado')
    else:
        dic = {}
        bs = BeautifulSoup(html.read(), 'html.parser')
        titulos = bs.find_all('h2', {'class': 'ui-search-item__title'})
        for titulo in titulos:
            precos = bs.find_all('div', {'class':'ui-search-price__second-line'})
            contador = 0
            for preco in precos:
                contador += 1
                if contador % 2 != 0:
                    dic.setdefault(titulo.get_text(), preco.span.span.get_text().replace('con', 'e'))
        # formatando a saída
        for item, price in dic.items():
            print(f'{item} : {price}')
        pagina = bs.find_all('div', {'class': 'ui-search-pagination'})
        link = ''
        # paginação
        for links in pagina:
            encontrar = links.find('ul').find_all('li')
            # pegando e conferindo os atributos
            for coisas in encontrar:
                for coisa in coisas:
                    try:
                        if 'title' in coisa.attrs:
                            # quando tiver página de voltar, avancar
                            if coisa.attrs['title'] == 'Anterior':
                                encontrar2 = links.find('ul').li.next_sibling.next_sibling
                                for atributos in encontrar2:
                                    if 'href' in atributos.attrs:
                                        linke = atributos.attrs['href']
                                        print(f'link de página adiante: {linke}')
                                        print()
                                        busca_produtos_mercadolivre(linke)
                        else:
                            # avançar a página
                            encontrar = links.find('ul').li.next_sibling()
                            for coisas in encontrar:
                                if 'href' in coisas.attrs:
                                    link = coisas.attrs['href']
                                    print(f'link pagina2: {link}')
                                    print()
                            busca_produtos_mercadolivre(link)
                    except TypeError:
                        print('página não encontrada ou fim da linha')
                        pass


desejado = str(input('informe o produto desejado: '))
busca_produtos_mercadolivre(desejado)
