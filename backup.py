import pandas as pd
import numpy as np
import requests
import streamlit as st
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt

resultados_anteriores = []

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

def comparar_com_anteriores(nota_final):
    if len(resultados_anteriores) > 0:
        media_sites_anteriores = np.mean(resultados_anteriores)
        if nota_final > media_sites_anteriores:
            return "O site está acima da média dos sites anteriores."
        elif nota_final < media_sites_anteriores:
            return "O site está abaixo da média dos sites anteriores."
        else:
            return "O site tem a mesma nota média dos sites anteriores."
    else:
        return "Não há sites anteriores para comparar."

st.title("Análise de Sites")

with st.form('insere_url'):
    url = st.text_input("Coloque a URL:")
    botao = st.form_submit_button(label='Analisar')

if botao:
    resultado = analisar_site(url)
    st.write("Análise do site:", url)
    st.write("Header:", resultado['tem_header'])
    st.write("Autor:", resultado['tem_autor'])
    st.write("Keywords:", resultado['tem_keywords'])
    st.write("Definição:", resultado['tem_definicao'])
    st.write("Tags 'og':", resultado['tem_tags_og'])
    st.write("Definição de idioma:", resultado['tem_idioma'])
    st.subheader("Análise do site:")
    
    nota_final = calcular_nota_final(resultado)
    st.write("Nota Final:", nota_final)
    
    comparacao = comparar_com_anteriores(nota_final)
    st.write(comparacao)
    
    resultados_anteriores.append(nota_final)
    
    categorias = ['Header', 'Autor', 'Keywords', 'Definição', 'Tags "og"', 'Idioma']
    valores = [resultado['tem_header'], resultado['tem_autor'], resultado['tem_keywords'],
               resultado['tem_definicao'], resultado['tem_tags_og'], resultado['tem_idioma']]
    dataframe = pd.DataFrame({'Categoria': categorias, 'Valor': valores})
    
    fig = plt.figure(figsize=(10, 4))
    sns.barplot(x='Valor', y='Categoria', data=dataframe)
    st.pyplot(fig)
