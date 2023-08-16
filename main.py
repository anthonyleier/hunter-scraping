import requests
from bs4 import BeautifulSoup


def buscar_pagina(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Página consultada com sucesso: {url}")
        conteudo = response.content
        pagina = BeautifulSoup(conteudo, 'html.parser')
        return pagina

    else:
        print(f"Erro na consulta: {response.status_code}")
        return False


def encontrar_corpo_noticia(url):
    pagina = buscar_pagina(url)
    conteudo_pagina = pagina.find(class_='small single')

    corpo_noticia = ''
    tags = conteudo_pagina.find_all('p')
    for tag in tags:
        conteudo = tag.text
        if 'foto: ilustrativa' not in conteudo.lower() and 'jornalismo m notícias' not in conteudo.lower():
            corpo_noticia += " " + conteudo

    return corpo_noticia.strip()


def montar_noticias(destaques):
    noticias = []
    for destaque in destaques:
        noticia = {
            'url': destaque.a['href'],
            'titulo': destaque.a.text
        }
        noticia['id'] = int(noticia['url'].replace('https://martelloonlinenoticias.com.br/?p=', ''))
        noticia['corpo'] = encontrar_corpo_noticia(noticia['url'])
        noticias.append(noticia)
    return noticias


if __name__ == "__main__":
    url = 'https://martelloonlinenoticias.com.br/'
    pagina = buscar_pagina(url)
    quantidade = 20

    destaques = pagina.find_all(class_='entry-title title')[:quantidade]
    noticias = montar_noticias(destaques)

    print(noticias)
