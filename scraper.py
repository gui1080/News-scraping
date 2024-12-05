import requests
from bs4 import BeautifulSoup
import logging
import time
from rich.console import Console
from rich.live import Live
from rich.table import Table
import emoji
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_news(limit):
    logger.info('Obtendo notícias...')
    url = 'https://g1.globo.com/ultimas-noticias/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    #news_list = []
    news_list = pd.DataFrame(columns =['title','description', 'link', 'content'])

    try:
        while len(news_list) < limit:
            response = requests.get(url, timeout=500, headers=headers)
            if response.status_code != 200:
                logger.error(f'Erro ao obter notícias. Status Code: {response.status_code}')
                return news_list

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
                            if "Participe do canal do g1" not in str(body.text) and "Veja os vídeos mais assistidos no g1" not in str(body.text) and (emoji.emoji_count(str(body.text)) != 0): 
                                content_str = content_str + " " + str(body.text.strip())

                    row_to_append = pd.DataFrame([{'title': title, 'description': description, 'link': link, 'content': content_str}])
                    news_list = pd.concat([news_list,row_to_append])

                    logger.info(f'Notícia {len(news_list)}: {title}')

                    if len(news_list) >= limit:
                        break

            load_more_button = soup.find('div', {'class': 'load-more gui-color-primary-bg'})
            if load_more_button and load_more_button.find('a'):
                url = load_more_button.find('a')['href']
            else:
                break

        return news_list

    except Exception as e:
        logger.exception(f'Erro ao obter notícias: {str(e)}')
        return news_list


if __name__ == "__main__":

    start = time.time()
    
    limit = 4000
    
    news = get_news(limit)
    noticias_recuperadas = len(news)

    time.sleep(1)

    filename = "g1_noticias_" + str(int(time.time())) + "_" + str(limit) + ".csv"

    news.to_csv(filename, sep=',', index=False, encoding='utf-8')

    end = time.time()

    execution_time = end - start

    minutes = int(execution_time // 60)
    seconds = execution_time % 60

    if noticias_recuperadas == limit:
        print(f"Todas as {limit} notícias foram recuperadas!")
    else:
        print(f"Das {limit} noticias de meta, foram recuperadas {noticias_recuperadas}!")

    print(f"Tempo de execução para {limit} notícias foi de: {minutes} minutes and {seconds:.2f} seconds")
        