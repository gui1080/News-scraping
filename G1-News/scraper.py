import requests
from bs4 import BeautifulSoup
import logging
import time
from rich.console import Console
from rich.live import Live
from rich.table import Table
import emoji
import pandas as pd
from urllib.parse import urljoin
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ------------------------------------------------------------------------------------------------------------------------------------------

def get_news_g1(limit):
    logger.info('Obtendo notícias...')
    url = 'https://g1.globo.com/ultimas-noticias/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    news_list = pd.DataFrame(columns =['title','description', 'link', 'content'])

    try:
        while len(news_list) < limit:

            # Acessando a página
            # --------------------------------------------------
            response = requests.get(url, timeout=500, headers=headers)
            time.sleep(0.4)
            if response.status_code != 200:
                logger.error(f'Erro ao obter notícias. Status Code: {response.status_code}')
                return news_list

            # Segmentando e recuperando as partes da notícia
            # --------------------------------------------------
            soup = BeautifulSoup(response.content, 'html.parser')

            post_sections = soup.find_all('div', {'class': 'bastian-feed-item'})

            for section in post_sections:

                title_element = section.find('a', {'class': 'feed-post-link'})
                description_element = section.find('div', {'class': 'feed-post-body-resumo'})
                link_element = section.find('a', {'class': 'feed-post-link'})
                image_element = section.find('img', {'class': 'bstn-fd-picture-image'})

                if title_element and link_element and description_element and image_element:
                    title = title_element.text.strip()
                    link = link_element['href']
                    description = description_element.text.strip()

                    # acessar o link da pagina e recuperar o texto
                    response = requests.get(link, timeout=500, headers=headers)
                    time.sleep(1)
                    
                    if response.status_code == 200:

                        content_soup = BeautifulSoup(response.content, 'html.parser')
                        article_body = content_soup.find_all('p', {'class': 'content-text__container'})
                        
                        content_str = ""
                        for body in article_body:
                            content_str = content_str + " " + str(body.text.strip())

                    row_to_append = pd.DataFrame([{'title': title, 'description': description, 'link': link, 'content': content_str}])
                    news_list = pd.concat([news_list,row_to_append])

                    logger.info(f'Notícia {len(news_list)}: {title}')

                    if len(news_list) >= limit:
                        break

            # Acessa o próximo link
            # --------------------------------------------------
            load_more_button = soup.find('div', {'class': 'load-more gui-color-primary-bg'})
            if load_more_button and load_more_button.find('a'):
                url = load_more_button.find('a')['href']
            else:
                break

        return news_list

    except Exception as e:
        logger.exception(f'Erro ao obter notícias: {str(e)}')
        return news_list

# ------------------------------------------------------------------------------------------------------------------------------------------

def get_news_metro(limit):
    logger.info('Obtendo notícias...')

    # primeira url dummy
    url = 'https://www.metropoles.com/brasil/senado-aprova-texto-base-da-regulamentacao-da-reforma-tributaria'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }


    # lista de links para acessar
    # começa cheia para obrigar o algoritmo a visitar uma homepage que vai ter muitos links
    list_link = ["https://www.metropoles.com/", "https://www.metropoles.com/esportes", "https://www.metropoles.com/saude", 
    "https://www.metropoles.com/vida-e-estilo", "https://www.metropoles.com/entretenimento", "https://www.metropoles.com/blog-do-noblat", 
    "https://www.metropoles.com/distrito-federal", "https://www.metropoles.com/brasil", "https://www.metropoles.com/colunas/claudia-meireles", 
    "https://www.metropoles.com/colunas/paulo-cappelli", "https://www.metropoles.com/colunas/mario-sabino", "https://www.metropoles.com/materias-especiais", 
    "https://www.metropoles.com/colunas/tacio-lorran", "https://www.metropoles.com/ultimas-noticias", "https://www.metropoles.com/webstories", "https://www.metropoles.com/sao-paulo", 
    "https://www.metropoles.com/violencia-contra-a-mulher", "https://www.metropoles.com/brasil/economia-br", "https://www.metropoles.com/colunas/e-o-bicho", "https://www.metropoles.com/colunas/leo-dias"]
    
    # contador de notícias
    i = 0 

    # lista de links visitados
    history_link = []

    # dataframe final
    news_list = pd.DataFrame(columns =['title','description', 'link', 'content'])

    try:
        while len(news_list) < limit:

            logger.info("Noticia " + str(i))

            # Acessando a página
            # --------------------------------------------------

            try:
                response = requests.get(url, timeout=5000, headers=headers)
            except Exception as e:
                logger.exception("Outro except - pegando outra url")
                url = str(list_link.pop())
                response = requests.get(url, timeout=5000, headers=headers)


            time.sleep(0.4)
            if response.status_code != 200:
                logger.error(f'Erro ao obter notícias. Status Code: {response.status_code}')
                if len(list_link) > 0:
                    while response.status_code != 200:
                        url = str(list_link.pop())
                        response = requests.get(url, timeout=5000, headers=headers)

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extraíndo links
            # --------------------------------------------------
            
            links = soup.find_all('a', href=True)

            for link in links:
                found_link = str(re.search(r'href="([^"]+)"', str(link)).group(1))
                if "metropoles" in found_link:
                    if "radio" and "/author" and "/tag" not in found_link:
                        if found_link.count('/') >= 4:
                            if "https" in found_link:
                                if found_link not in history_link and found_link not in list_link:
                                    list_link.append(found_link)

            # Extraíndo título, conteúdo e descrição
            # --------------------------------------------------

            post_sections = soup.find_all('div', {'class': 'ConteudoNoticiaWrapper__Artigo-sc-19fsm27-1 iZYHrO'})

            titulo = soup.find_all('h1', {'class': 'Text__TextBase-sc-1d75gww-0 TcJvw'})
            descricao = soup.find_all('h2', {'class': 'Text__TextBase-sc-1d75gww-0 jhEviD noticiaCabecalho__subtitulo'})

            h1_content = re.search(r'<h1[^>]*>(.*?)</h1>', str(titulo))

            if h1_content:
                titulo_clean = h1_content.group(1)
            else:
                titulo_clean = ""

            if titulo_clean == "":
                logger.info("Este link não é uma notícia específica do Metropoles!")
                logger.info(url)
                logger.info("Extraíndo links e passando para o próximo link da fila...")
                logger.info("--------------------------")
            else:
                logger.info("Título - " + str(titulo_clean))
                logger.info("--------------------------")

            h2_content = re.search(r'<h2[^>]*>(.*?)</h2>', str(descricao))

            # Check if there is a match and extract the content
            if h2_content:
                descricao_clean = h2_content.group(1)
            else:
                descricao_clean = ""


            if titulo_clean != "":

                cleaned_content = ""

                # Process each section
                for section in post_sections:
                    # Option 1: Clear text inside <p> tags but keep the tags
                    for p_tag in section.find_all(['p', 'li', 'h2', 'h3', 'h4']):
                        if "Metrópoles" not in str(p_tag):
                            if "h6" not in str(p_tag):
                                cleaned_chunk = re.sub(r'<.*?>', '', str(p_tag))
                                cleaned_content = cleaned_content + " " + cleaned_chunk.strip()
                        
            # Pegando próximo link da página
            # --------------------------------------------------
            # Problema de performance em potencial aqui!
            # No scraper do G1 era só pegar um último link de "próxima notícia" na página
            # No metrópoles o site é maior com mais links e as vezes o mesmo link vai aparecer na mesma loclaidade
            # então é possível cair num loop do rodapé de uma notícia chamar a próxima e essa próxima chamar a primeira notícia
            # Solução - raspar todos os links da página, mantendo apenas os do Metrópoles, gerenciar uma fila "histórico" e uma de "próximo link"
            # Busca de links em lista de links tem complexidade de O(n), maior a lista, maior a busca, mais tempo rodando, mais demorado por conta das buscas.
            
            # Em notícia 300, já tinha 1000 links na lista, aos 1900, 1846 links (execução de dez/24)
            # Uma solução seria dropar automaticamente, ou manter a lista ordenada e aplicar um algoritmo de busca (ou algo do tipo), não pretendo implementar isso.

            prox_link = soup.find_all('h6', {'class': 'm-title'})

            for link in prox_link:

                prox_link_clean = re.search(r'href="([^"]+)"', str(prox_link[0])).group(1)
                if prox_link_clean not in list_link:
                    if link in history_link:
                        list_link.append(str(prox_link_clean))
            
            history_link.append(url)

            if len(list_link) != 0:
                
                url = str(list_link.pop())

                if url in history_link:
                    while url not in history_link:
                        url = str(list_link.pop())

                if i >= limit:

                    logger.info("Lista de links - " + str(len(list_link)))
                    logger.info("--------------------------")
                    break
                else:
                    i = i + 1
                
                if (i % 100 == 0):
                    logger.info("Tamanho da lista de links - " + str(len(list_link)))
                    logger.info("--------------------------")

            else:
                logger.info("Lista de links - " + str(len(list_link)))
                logger.info("--------------------------")
                break

            # Salvando o conteúdo da página, se era uma página de notícia (título válido)
            # --------------------------------------------------

            if titulo_clean != "":
                row_to_append = pd.DataFrame([{'title': titulo_clean, 'description': descricao_clean, 'link': url, 'content': cleaned_content.strip()}])
                news_list = pd.concat([news_list,row_to_append])
            else:
                i = i -1 
        
        logger.info("Lista de links - " + str(len(list_link)))
        logger.info("--------------------------")
        return news_list

    except Exception as e:
        logger.exception(f'Erro ao obter notícias: {str(e)}')
        logger.info("Lista de links - " + str(len(list_link)))
        logger.info("--------------------------")
        return news_list

# ------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    start = time.time()
    
    limit = 20000

    fonte = 2
    '''
    1 = G1
    2 = Metropoles
    '''

    if fonte == 1:
        news = get_news_g1(limit)
        
    if fonte == 2:
        news = get_news_metro(limit)
        
    else:
        news = []

    noticias_recuperadas = len(news)

    time.sleep(1)

    noticias_recuperadas_clean = news.drop_duplicates(subset='link')

    if fonte == 1:
        filename = "g1_noticias_" + str(int(time.time())) + "_" + str(len(noticias_recuperadas_clean)) + ".csv"
    if fonte == 2:
        filename = "metropoles_noticias_" + str(int(time.time())) + "_" + str(len(noticias_recuperadas_clean)) + ".csv"
    else:
        filename = ""

    news.to_csv(filename, sep=',', index=False, encoding='utf-8')

    end = time.time()

    execution_time = end - start

    minutes = int(execution_time // 60)
    seconds = execution_time % 60

    print("\n\n\n--------------------------------------------------------------------------------\n")

    if noticias_recuperadas == limit:
        print(f"Todas as {limit} notícias foram recuperadas!")
        
    else:
        print(f"Das {limit} noticias de meta, foram recuperadas {noticias_recuperadas}!")
    
    print(f"Depois de limpar duplicatas, acabamos com {str(len(noticias_recuperadas_clean))} notícias")
    print("\n\n--------------------------------------------------------------------------------\n")
    print(f"Tempo de execução para {limit} notícias foi de: {minutes} minutos e {seconds:.2f} segundos")
    print("\n--------------------------------------------------------------------------------\n")
        