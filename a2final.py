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
    ) / 6.0  
    return nota_final

st.title("Análise de Sites")

with st.form('insere_url'):
    url1 = st.text_input("Coloque a URL 1:")
    url2 = st.text_input("Coloque a URL 2:")
    botao = st.form_submit_button(label='Analisar')

if botao:
    resultado1 = analisar_site(url1)
    resultado2 = analisar_site(url2)
    
    st.subheader("Análise do site 1:")
    st.write("URL:", url1)
    st.write("Header:", resultado1['tem_header'])
    st.write("Autor:", resultado1['tem_autor'])
    st.write("Keywords:", resultado1['tem_keywords'])
    st.write("Definição:", resultado1['tem_definicao'])
    st.write("Tags 'og':", resultado1['tem_tags_og'])
    st.write("Definição de idioma:", resultado1['tem_idioma'])
    st.write("")

    st.subheader("Análise do site 2:")
    st.write("URL:", url2)
    st.write("Header:", resultado2['tem_header'])
    st.write("Autor:", resultado2['tem_autor'])
    st.write("Keywords:", resultado2['tem_keywords'])
    st.write("Definição:", resultado2['tem_definicao'])
    st.write("Tags 'og':", resultado2['tem_tags_og'])
    st.write("Definição de idioma:", resultado2['tem_idioma'])
    st.write("")

    nota_final1 = calcular_nota_final(resultado1)
    nota_final2 = calcular_nota_final(resultado2)
    
    st.subheader("Resultado:")
    st.write("Nota Final do site 1:", nota_final1)
    st.write("Nota Final do site 2:", nota_final2)

    
    categorias = ['Header', 'Autor', 'Keywords', 'Definição', 'Tags "og"', 'Idioma']
    valores1 = [resultado1['tem_header'], resultado1['tem_autor'], resultado1['tem_keywords'],
               resultado1['tem_definicao'], resultado1['tem_tags_og'], resultado1['tem_idioma']]
    valores2 = [resultado2['tem_header'], resultado2['tem_autor'], resultado2['tem_keywords'],
               resultado2['tem_definicao'], resultado2['tem_tags_og'], resultado2['tem_idioma']]
    dataframe = pd.DataFrame({'Categoria': categorias, 'Valor Site 1': valores1, 'Valor Site 2': valores2})
    fig = plt.subplots(figsize=(10, 4))
    sns.barplot(x='Valor Site 1', y='Categoria', data=dataframe, color='blue', label='Site 1')
    sns.barplot(x='Valor Site 2', y='Categoria', data=dataframe, color='red', label='Site 2')
    for i, valor1, valor2 in zip(range(len(categorias)), valores1, valores2):
        if valor1 and valor2:
            plt.text(i, valor1 / 2, 'Ambos', ha='center', va='center')
            plt.text(i, valor1 + valor2 / 2, 'Ambos', ha='center', va='center')
    plt.legend()
    st.pyplot(fig)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    st.image(buffer, use_column_width=True)
