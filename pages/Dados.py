import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
file_path = 'Tabela_com_Latitudes_e_Longitudes.csv'
data = pd.read_csv(file_path)

# Substituir os meses em português para o formato em inglês
meses = {
    'jan': 'Jan', 'fev': 'Feb', 'mar': 'Mar', 'abr': 'Apr', 'mai': 'May', 'jun': 'Jun',
    'jul': 'Jul', 'ago': 'Aug', 'set': 'Sep', 'out': 'Oct', 'nov': 'Nov', 'dez': 'Dec'
}

# Verificar a estrutura da coluna 'Mês' e garantir que os valores estão no formato correto
data['Mês'] = data['Mês'].str.lower().map(meses)

# Remover a parte decimal do ano, garantindo que fique apenas o ano como inteiro
data['Ano'] = data['Ano'].astype(str).str.split('.').str[0]

# 1. Gráfico de Viagens por Ano e Mês
st.subheader("Quantidade de Viagens por Ano e Mês")
viagens_por_mes = data.groupby(['Ano', 'Mês']).size().reset_index(name='Quantidade de Viagens')

# Criar uma nova coluna Ano-Mês com o formato 'Ano-Mês' para garantir a ordenação
# Como já temos o mês em formato correto (em inglês), agora podemos fazer a concatenação de forma correta
viagens_por_mes['Ano-Mês'] = pd.to_datetime(viagens_por_mes['Ano'].astype(str) + '-' + viagens_por_mes['Mês'], format='%Y-%b')

# Ordenar os dados pelo campo Ano-Mês
viagens_por_mes = viagens_por_mes.sort_values(by='Ano-Mês')

fig1, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.bar(viagens_por_mes['Ano-Mês'].dt.strftime('%Y-%b'), viagens_por_mes['Quantidade de Viagens'])
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

ax1.set_xticklabels(viagens_por_mes['Ano-Mês'].dt.strftime('%Y-%b'), rotation=45, ha="right")
ax1.set_title("Quantidade de Viagens por Ano e Mês")
ax1.set_xlabel("Ano - Mês")
ax1.set_ylabel("Quantidade de Viagens")
st.pyplot(fig1)

# 2. Gráfico de Produtos Mais Vendidos
st.subheader("Produtos Mais Vendidos")
produtos_mais_vendidos = data.groupby('Produto').size().reset_index(name='Quantidade de Vendas')
fig2, ax2 = plt.subplots(figsize=(8, 6))
bars2 = ax2.bar(produtos_mais_vendidos['Produto'], produtos_mais_vendidos['Quantidade de Vendas'])
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')
ax2.set_title("Produtos Mais Vendidos")
ax2.set_xlabel("Produto")
ax2.set_ylabel("Quantidade de Vendas")
st.pyplot(fig2)

# 3. Gráfico de Origem e Destino Mais Comuns
st.subheader("Origens e Destinos Mais Comuns")
origens_destinos_mais_vendidos = data.groupby(['Origem', 'Destino']).size().reset_index(name='Quantidade de Viagens')
fig3, ax3 = plt.subplots(figsize=(10, 6))
bars3 = ax3.barh(origens_destinos_mais_vendidos['Origem'] + ' -> ' + origens_destinos_mais_vendidos['Destino'], 
                 origens_destinos_mais_vendidos['Quantidade de Viagens'])
for bar in bars3:
    ax3.text(bar.get_width(), bar.get_y() + bar.get_height()/2, round(bar.get_width(), 2), va='center')
ax3.set_title("Origens e Destinos Mais Comuns")
ax3.set_xlabel("Quantidade de Viagens")
ax3.set_ylabel("Origem -> Destino")
st.pyplot(fig3)

# 4. Gráfico de Clientes que mais compraram (apenas os 10 primeiros)
st.subheader("Top 10 Clientes que Mais Compraram")
clientes_compras = data.groupby('ID Cliente').size().reset_index(name='Quantidade de Compras')

# Ordenar por quantidade de compras, do maior para o menor
clientes_compras = clientes_compras.sort_values(by='Quantidade de Compras', ascending=False)

# Selecionar os top 10 clientes
top_10_clientes = clientes_compras.head(10)

# Gerar gráfico
fig4, ax4 = plt.subplots(figsize=(10, 6))
bars4 = ax4.bar(top_10_clientes['ID Cliente'].astype(str), top_10_clientes['Quantidade de Compras'])

# Adicionando os valores nas barras
for bar in bars4:
    yval = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

ax4.set_title("Top 10 Clientes que Mais Compraram")
ax4.set_xlabel("ID Cliente")
ax4.set_ylabel("Quantidade de Compras")
st.pyplot(fig4)
