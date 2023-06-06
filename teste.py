import pandas as pd
import numpy as np
import requests
import streamlit as st
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.parse import urlparse

def adicionar_prefixo_url(url):
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = 'http://' + url
    except Exception:
        st.error("URL inválida. Certifique-se de incluir um esquema válido (por exemplo, 'http://' ou 'https://').")
        return None

    return url

def analisar_site(url):
    try:
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
    except requests.exceptions.RequestException:
        st.error("Ocorreu um erro ao fazer a requisição para a URL.")
        return None

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

st.title("Análise de Sites")

with st.form('insere_url'):
    url_inputs = st.text_input("Coloque as URLs (separadas por vírgula):")
    botao = st.form_submit_button(label='Analisar')

if botao:
    urls = url_inputs.split(",")
    resultados = []
    notas_finais = []

    for url in urls:
        url = adicionar_prefixo_url(url.strip())
        if url:
            resultado = analisar_site(url)
            if resultado:
                resultados.append(resultado)
                nota_final = calcular_nota_final(resultado)
                notas_finais.append(nota_final)

    if resultados:
        st.subheader("Resultados da Análise:")

        for i, resultado in enumerate(resultados):
            st.subheader(f"Análise do site {i+1}:")
            st.write("URL:", urls[i].strip())
            st.write("Header:", resultado['tem_header'])
            st.write("Autor:", resultado['tem_autor'])
            st.write("Keywords:", resultado['tem_keywords'])
            st.write("Definição:", resultado['tem_definicao'])
            st.write("Tags 'og':", resultado['tem_tags_og'])
            st.write("Definição de idioma:", resultado['tem_idioma'])
            st.write("Nota Final:", notas_finais[i])
            st.write("---")
        
        st.subheader("Gráfico de Notas Finais")
        df = pd.DataFrame({'URL': urls, 'Nota Final': notas_finais})
        fig, ax = plt.subplots()
        sns.barplot(x='URL', y='Nota Final', data=df, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)
    else:
        st.warning("Nenhum resultado encontrado.")
