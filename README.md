# G1 News Scraping

Este é um projeto simples de web scraping desenvolvido em Python para extrair as últimas notícias do site G1 (globo.com). Ele utiliza as bibliotecas requests e BeautifulSoup para coletar informações das páginas web.

## Objetivo

O objetivo principal deste projeto é fornecer uma ferramenta de scraping para coletar notícias do G1 de maneira automatizada. Esse código pode ser usado como base para projetos mais avançados ou para entender os conceitos básicos de scraping.

## Como Usar

Para utilizar este projeto, siga os passos abaixo:

### Crie e acesse um ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate
```

### Instalação das Dependências:

Certifique-se de ter o Python instalado em seu ambiente. Este projeto foi desenvolvido usando Python 3.x.

Utilize o comando abaixo para instalar as dependências necessárias:

```bash
pip3 install -r requirements.txt
```

### Execução do Scraping:

Após a instalação das dependências, você pode executar o arquivo `scrapper.py` para iniciar o scraping das notícias.

```bash
python G1-News/scraper.py
```

### Resultado:

O código irá coletar as últimas notícias do G1, exibindo os títulos das notícias obtidas no console.

## Estrutura de Pasta

A estrutura de pastas do projeto está organizada da seguinte maneira:

```bash
G1_News_Scraper/
│
├── src/
│ ├── main.py # Arquivo principal onde você inicia o web scraping
│ └── scraper.py # Arquivo onde a função de scraping (get_news) está definida
│
├── requirements.txt # Arquivo que lista todas as dependências do projeto
└── README.md # Este arquivo, contendo informações sobre o projeto e instruções de uso
```

-   `src/`: Pasta que contém o código fonte do projeto.
-   `requirements.txt`: Lista todas as dependências do projeto para facilitar a instalação.
-   `README.md`: Documentação explicando o projeto, instruções de uso e informações gerais.

## Avisos Importantes

-   **Uso Responsável:** Este projeto foi desenvolvido para fins educacionais e de aprendizado. Sempre respeite os termos de serviço dos sites ao realizar web scraping.

-   **Limitações e Restrições:** O scraping de sites pode ser contra os termos de serviço de alguns sites. Verifique as políticas de uso e os limites de solicitação do site alvo antes de executar o código.

## Esse fork

Esse código é um fork desse [repositório](https://github.com/leviobrabo/G1-news-scraping). Eu alterei esse código para, ao invés de mostrar na tela as notícias, elas são salvas em um dataframe do pandas.

Fiz essas alterações aplicando a metodologia *Go Horse* de deploy rápido e sujo, realizando processos da forma menos otimizada possível. A cada título e manchete, eu faço outro request para acessar a url parseando o documento com outro argumento, me permitindo acessar o conteúdo escrito ao invés de só o título e a descrição da notícia. Isso pode com certeza pode ser melhorado. Não pretendo correr atrás disso no momento pois não estava com tempo para isso, mas sinta-se a vontade para arrumar isso. Se precisar de ajuda, não me procure. Sugestão: recuperar o título e a descrição da notícia direto do segundo texto parseado na segunda chamada do BeautifulSoup.

Com um arquivo salvo em formanto *.csv*, é possível usar esse corpo de texto para análises de processamento de linguagem natural e como corpus para treinamento de LLMs. Não se esquecer do uso responsável e dos direitos e condições de uso dos sites sendo processados.