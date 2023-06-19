# scrapingearj
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def fazer_raspagem():
    url = "https://www.earj.com.br/university-acceptances/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")

    if table is None:
        st.write("Tabela não encontrada.")
        return None

    colunas = table.find_all("th")
    nomes_colunas = [coluna.text.strip() for coluna in colunas]
    linhas = table.find_all("tr")[1:]
    dados = []
    for linha in linhas:
        celulas = linha.find_all("td")
        valores_celulas = [celula.text.strip() for celula in celulas]
        dados.append(valores_celulas)
    df = pd.DataFrame(dados, columns=nomes_colunas)
    return df

df = fazer_raspagem()
if df is not None:
    if "Region" in df.columns:
        regioes_especificas = ['United States', 'United Kingdom', 'Europe', 'Canada', 'Brazil']
        regiao_selecionada = st.selectbox("Escolha uma região", regioes_especificas)
        df_filtrado = df[df['Region'] == regiao_selecionada]
        if not df_filtrado.empty:
            st.write("Dados Filtrados")
            st.dataframe(df_filtrado)
            st.write("Gráfico")
            chart_data = df_filtrado.groupby("University")["Acceptances"].sum()
            st.bar_chart(chart_data)
        else:
            st.write("Dados não encontrados")
    else:
        st.write("Coluna não encontrada no DataFrame")
