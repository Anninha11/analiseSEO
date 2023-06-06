import pandas as pd
import numpy as np
import requests
import streamlit as st
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import io

def analisar_site(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    header = soup.find('header')
    tem_header = bool(header)
    autor = soup.find('meta', attrs={'name': 'author'})
    tem_autor = bool(autor)
    keywords = soup.find('meta', attrs={'name': 'keywords'})
    tem_keywords = bool(keywords)
    definicao = soup.find('meta', attrs={'name': 'description'})
    tem_definicao = bool(definicao)
    tags_og = soup.find_all('meta', attrs={'property': lambda p: p and p.startswith('og:')})
    tem_tags_og = len(tags_og) > 0
    idioma = soup.find('html').get('lang', None)
    tem_idioma = bool(idioma)
    resultado = {
        'tem_header': tem_header,
        'tem_autor': tem_autor,
        'tem_keywords': tem_keywords,
        'tem_definicao': tem_definicao,
        'tem_tags_og': tem_tags_og,
        'tem_idioma': tem_idioma
    }
    return resultado

def calcular_nota_final(resultado):
    nota_final = (
        resultado['tem_header'] +
        resultado['tem_autor'] +
        resultado['tem_keywords'] +
        resultado['tem_definicao'] +
        resultado['tem_tags_og'] +
        resultado['tem_idioma']
    )  
    return nota_final

def plotar_grafico_analise(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    index = np.arange(len(df['Categoria']))

    for i, col in enumerate(df.columns[1:]):
        ax.bar(index + i * bar_width, df[col], bar_width, label=col)

    ax.set_xlabel('Categorias')
    ax.set_ylabel('Valores')
    ax.set_title('Análise de Sites')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(df['Categoria'])
    ax.legend()

    st.pyplot(fig)

st.title("Análise de Sites")

num_urls = st.number_input("Quantidade de URLs:", min_value=1, step=1, value=2)
urls = []
for i in range(num_urls):
    url = st.text_input(f"Coloque a URL {i+1}:")
    urls.append(url)

resultados = []
notas_finais = []
for url in urls:
    resultado = analisar_site(url)
    nota_final = calcular_nota_final(resultado)
    resultados.append(resultado)
    notas_finais.append(nota_final)

for i, resultado in enumerate(resultados):
    st.subheader(f"Análise do site {i+1}:")
    st.write("URL:", urls[i])
    st.write("Header:", resultado['tem_header'])
    st.write("Autor:", resultado['tem_autor'])
    st.write("Keywords:", resultado['tem_keywords'])
    st.write("Definição:", resultado['tem_definicao'])
    st.write("Tags 'og':", resultado['tem_tags_og'])
    st.write("Definição de idioma:", resultado['tem_idioma'])
    st.write("")

for i, nota_final in enumerate(notas_finais):
    st.subheader(f"Nota Final do site {i+1}:")
    st.write(nota_final)
    st.write("")

resultado_geral = {}
for categoria in ['tem_header', 'tem_autor', 'tem_keywords', 'tem_definicao', 'tem_tags_og', 'tem_idioma']:
    resultado_geral[categoria] = sum(resultado[categoria] for resultado in resultados)

categorias = ['Header', 'Autor', 'Keywords', 'Definição', 'Tags "og"', 'Idioma']
valores_sites = []
for resultado in resultados:
    valores_sites.append([resultado[categoria] for categoria in categorias])
valores_geral = [resultado_geral[categoria] for categoria in categorias]

df = pd.DataFrame({'Categoria': categorias})
for i, url in enumerate(urls):
    df[f'Site {i+1}'] = valores_sites[i]
df['Sites'] = valores_geral

plotar_grafico_analise(df)
