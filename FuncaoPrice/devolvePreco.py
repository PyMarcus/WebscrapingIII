import re

def formataPrecos(texto):
    """Funcao que me devolve o preço com desconto do produto"""
    
    regex = re.compile('\d+')  # cria listas com os números no texto
    preco = regex.findall(texto)  # me dá os números para montar o preço
    if len(preco) > 1:
        return f'R${preco[0]},{preco[1]}'
    else:
        return f'R${preco[0]}'
