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

urls = st.text_area("Coloque as URLs (uma por linha):")

if st.button("Analisar"):
    urls = urls.split("\n")
    urls = [url.strip() for url in urls if url.strip()]
    resultados = []

    for url in urls:
        url = adicionar_prefixo_url(url)
        if url:
            resultado = analisar_site(url)
            if resultado:
                resultados.append(resultado)

    if resultados:
        st.subheader("Resultados da Análise:")

        categorias = [
            'tem_header',
            'tem_autor',
            'tem_keywords',
            'tem_definicao',
            'tem_tags_og',
            'tem_idioma'
        ]

        resultado_geral = {categoria: sum(resultado[categoria] for resultado in resultados) for categoria in categorias}

        for i, resultado in enumerate(resultados):
            st.subheader(f"Análise do site {i+1}:")
            st.write("URL:", urls[i])
            st.write("Header:", resultado['tem_header'])
            st.write("Autor:", resultado['tem_autor'])
            st.write("Keywords:", resultado['tem_keywords'])
            st.write("Definição:", resultado['tem_definicao'])
            st.write("Tags OG:", resultado['tem_tags_og'])
            st.write("Idioma:", resultado['tem_idioma'])
            st.write("---")

        st.subheader("Resumo Geral:")
        for categoria in categorias:
            st.write(f"{categoria}: {resultado_geral[categoria]}")
        notas_finais = [calcular_nota_final(resultado) for resultado in resultados]
        st.write("Nota Final Média:", np.mean(notas_finais))
        st.write("---")

        st.subheader("Gráfico de Notas Finais")
        df = pd.DataFrame({'URL': urls, 'Nota Final': notas_finais})
        fig, ax = plt.subplots()
        sns.barplot(x='URL', y='Nota Final', data=df, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)
    else:
        st.warning("Nenhum resultado encontrado.")

