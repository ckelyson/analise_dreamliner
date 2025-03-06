import folium
import streamlit as st
import random
import pandas as pd
from streamlit.components.v1 import html

# Função para gerar uma cor aleatória para cada linha
def gerar_cor():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Função para gerar o mapa para a viagem selecionada
def gerar_mapa_para_viagem(pedido, df_limpo):
    # Filtrando os dados para a viagem com o número do pedido selecionado
    df_viagem = df_limpo[df_limpo['Nº Pedido'] == pedido]

    # Verificando se a viagem foi encontrada
    if df_viagem.empty:
        st.write(f"Viagem com o número do pedido {pedido} não encontrada.")
        return None

    # Coordenadas de origem e destino
    row = df_viagem.iloc[0]
    origem = [row['Origem_Lat'], row['Origem_Lon']]
    destino = [row['Destino_Lat'], row['Destino_Lon']]

    # Criar o mapa centrado na origem
    mapa = folium.Map(location=origem, zoom_start=4)

    # Gerar cor única para essa viagem
    cor = gerar_cor()

    # Criar a linha entre origem e destino com uma cor única
    folium.PolyLine([origem, destino], color=cor, weight=3, opacity=0.7).add_to(mapa)

    # Adicionar marcador de origem
    folium.Marker(origem, popup=f"Origem: {row['Origem']}<br>Pedido: {row['Nº Pedido']}", icon=folium.Icon(color='green')).add_to(mapa)

    # Adicionar marcador de destino
    folium.Marker(destino, popup=f"Destino: {row['Destino']}<br>Pedido: {row['Nº Pedido']}", icon=folium.Icon(color='red')).add_to(mapa)

    # Salvar o mapa em HTML
    mapa_html = mapa._repr_html_()

    return mapa_html

# Interface de Seleção no Streamlit
st.title('Mapa das Viagens')

# Caminho do arquivo CSV diretamente do diretório
file_path = 'Tabela_com_Latitudes_e_Longitudes.csv'

# Carregar o arquivo CSV
df_limpo = pd.read_csv(file_path)  # Carregar o arquivo CSV

# Dropdown para selecionar o pedido
pedido = st.selectbox('Escolha o número do pedido:', df_limpo['Nº Pedido'].unique())

# Gerar o mapa com base na seleção
mapa_html = gerar_mapa_para_viagem(pedido, df_limpo)

# Exibir o mapa no Streamlit
if mapa_html:
    html(mapa_html, height=600)  # Exibe o mapa como HTML
