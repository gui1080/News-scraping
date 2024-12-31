import pandas as pd
import re

# G1 - junta tudo e limpa
# ---------------------------------------------------

print("\n---------------------------------------------------------")

# pega os dataframes
df_g1_noticias_1733440362_1000 = pd.read_csv("../g1_dados/g1_noticias_1733440362_1000.csv")
df_g1_noticias_1733448595_4000 = pd.read_csv("../g1_dados/g1_noticias_1733448595_4000.csv")
df_g1_noticias_1733846320_6799 = pd.read_csv("../g1_dados/g1_noticias_1733846320_6799.csv")
df_g1_noticias_1733861514_1882 = pd.read_csv("../g1_dados/g1_noticias_1733861514_1882.csv")

# append todos os dataframes
df_g1_fim = df_g1_noticias_1733440362_1000._append(df_g1_noticias_1733448595_4000)
df_g1_fim = df_g1_fim._append(df_g1_noticias_1733846320_6799)
df_g1_fim = df_g1_fim._append(df_g1_noticias_1733861514_1882)

df_g1_fim = df_g1_fim.drop_duplicates(subset='link')

total_words_metro_content = df_g1_fim['content'].str.split().str.len().sum()
total_words_metro_title = df_g1_fim['title'].str.split().str.len().sum()
total_words_metro_description = df_g1_fim['description'].str.split().str.len().sum()

print("\n")
print("Quantidade de notícias recuperadas do G1 no total")
print(len(df_g1_fim))
print("Quantidade de palavras no total - corpo da notícia")
print(total_words_metro_content)
print("Quantidade de palavras no total - título da notícia")
print(total_words_metro_title)
print("Quantidade de palavras no total - descrição da notícia")
print(total_words_metro_description)
print("Média do tamanho da notícia - corpo da notícia")
print(total_words_metro_content/len(df_g1_fim))
print("Média do tamanho da notícia - título da notícia")
print(total_words_metro_title/len(df_g1_fim))
print("Média do tamanho da notícia - descrição da notícia")
print(total_words_metro_description/len(df_g1_fim))


# Metrópoles - junta tudo e limpa
# ---------------------------------------------------

print("---------------------------------------------------------")

# pega os dataframes
df_metropoles_noticias_1734043262_40 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734043262_40.csv")
df_metropoles_noticias_1734047504_23 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734047504_23.csv")
df_metropoles_noticias_1734050733_250 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734050733_250.csv")
df_metropoles_noticias_1734129289_977 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734129289_977.csv")
df_metropoles_noticias_1734194144_231 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734194144_231.csv")
df_metropoles_noticias_1734199815_2430 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734199815_2430.csv")
df_metropoles_noticias_1734218031_291 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734206983_71.csv")
df_metropoles_noticias_1734218031_291 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734218031_291.csv")
df_metropoles_noticias_1734222435_1669 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734222435_1669.csv")
df_metropoles_noticias_1734271653_832 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734271653_832.csv")
df_metropoles_noticias_1734295787_9985 = pd.read_csv("../metropoles_dados/metropoles_noticias_1734295787_9985.csv")
df_metropoles_noticias_1735504786_2498 = pd.read_csv("../metropoles_dados/metropoles_noticias_1735504786_2498.csv")

# append todos os dataframes
df_metro_fim = df_metropoles_noticias_1734043262_40._append(df_metropoles_noticias_1734047504_23)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734050733_250)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734129289_977)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734194144_231)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734199815_2430)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734218031_291)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734222435_1669)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734271653_832)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1734295787_9985)
df_metro_fim = df_metro_fim._append(df_metropoles_noticias_1735504786_2498)

df_metro_fim = df_metro_fim.drop_duplicates(subset='link')

total_words_g1_content = df_metro_fim['content'].str.split().str.len().sum()
total_words_g1_title = df_metro_fim['title'].str.split().str.len().sum()
total_words_g1_description = df_metro_fim['description'].str.split().str.len().sum()

print("\n")
print("Quantidade de notícias recuperadas do Metropoles no total")
print(len(df_metro_fim))
print("Quantidade de palavras no total - corpo da notícia")
print(total_words_g1_content)
print("Quantidade de palavras no total - título da notícia")
print(total_words_g1_title)
print("Quantidade de palavras no total - descrição da notícia")
print(total_words_g1_description)
print("Média do tamanho da notícia - corpo da notícia")
print(total_words_g1_content/len(df_metro_fim))
print("Média do tamanho da notícia - título da notícia")
print(total_words_g1_title/len(df_metro_fim))
print("Média do tamanho da notícia - descrição da notícia")
print(total_words_g1_description/len(df_metro_fim))

print("Quantidade de palavras no total")
print(total_words_g1_content + total_words_g1_title + total_words_g1_description)

# ---------------------------------------------------

print("---------------------------------------------------------")
print("\n") 

print("Total de notícias")
print(len(df_metro_fim) + len(df_g1_fim))

print("Total de palavras - título da notícia")
print(int(total_words_g1_title + total_words_metro_title))

print("Total de palavras - descrição da notícia")
print(int(total_words_g1_description + total_words_metro_description))

print("Total de palavras - corpo da notícia")
print(int(total_words_g1_content + total_words_metro_content))

print("Total de palavras - total")
print(int(total_words_g1_content + total_words_metro_content + total_words_g1_description + total_words_metro_description + total_words_g1_title + total_words_metro_title))


# ---------------------------------------------------

fim = df_metro_fim._append(df_g1_fim)

fim_colunas_preservadas = df_metro_fim._append(df_g1_fim)

# ---------------------------------------------------
# Junta todas as colunas na coluna "text"

fim = fim.dropna(subset=['title', 'description', 'content'])

# Junta todas as colunas na coluna "text"
fim['text'] = fim[['title', 'description', 'content']].astype(str).agg(' '.join, axis=1)

# Drop the original columns
fim.drop(['title', 'description', 'link', 'content'], axis=1, inplace=True)

# termos referentes a origem são tags desconhecidas ao modelo
# [fonte]

fim['text'] = fim['text'].replace('g1', '[fonte]')

fim['text'] = fim['text'].replace('G1', '[fonte]')

fim['text'] = fim['text'].replace('metropoles', '[fonte]')
fim['text'] = fim['text'].replace('metrópoles', '[fonte]')
fim['text'] = fim['text'].replace('Metrópoles', '[fonte]')
fim['text'] = fim['text'].replace('Metropoles', '[fonte]')

fim['text'] = fim['text'].dropna()

# ---------------------------------------------------

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab')

def normalize_text(text):
    
    # Tokenizar o texto
    tokens = word_tokenize(text, language='portuguese')
    
    # Reunir tokens em uma string normalizada
    return ' '.join(tokens)

def trim_unnecessary_spaces(text):

    # Remover espaços antes de pontuação
    text = re.sub(r'\s+([.,!?;:"])', r'\1', text)
    
    # Remover espaços dentro de parênteses
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)

    return ' '.join(text.split()).strip()


print("---------------------------------------------------------")
print("\n") 

fim['text'] = fim['text'].apply(normalize_text)

fim['text'] = fim['text'].apply(trim_unnecessary_spaces)

fim.to_csv("dataset_noticias_final.csv", sep=',', index=False, encoding='utf-8')

# ---------------------------------------------------


fim_colunas_preservadas['title'] = fim_colunas_preservadas[['title', 'description']].astype(str).agg(' '.join, axis=1)

# Drop the original columns
fim_colunas_preservadas.drop(['link', 'description'], axis=1, inplace=True)

# termos referentes a origem são tags desconhecidas ao modelo
# [fonte]

fim_colunas_preservadas['content'] = fim_colunas_preservadas['content'].replace('g1', '[fonte]')
fim_colunas_preservadas['content'] = fim_colunas_preservadas['content'].replace('G1', '[fonte]')
fim_colunas_preservadas['content'] = fim_colunas_preservadas['content'].replace('metropoles', '[fonte]')
fim_colunas_preservadas['content'] = fim_colunas_preservadas['content'].replace('metrópoles', '[fonte]')
fim_colunas_preservadas['content'] = fim_colunas_preservadas['content'].replace('Metrópoles', '[fonte]')
fim_colunas_preservadas['content'] = fim_colunas_preservadas['content'].replace('Metropoles', '[fonte]')

fim_colunas_preservadas = fim_colunas_preservadas.drop_duplicates(subset=None, keep='first', inplace=False)

fim_colunas_preservadas.to_csv("dataset_noticias_final_colunas_preservadas.csv", sep=',', index=False, encoding='utf-8')
