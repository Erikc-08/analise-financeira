import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Análise Financeira", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0b1220;
}
h1, h2, h3 {
    color: #e5e7eb;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Análise: Pagamento à Vista vs Parcelado")

st.markdown("Ferramenta para análise de decisão financeira baseada em valor do dinheiro no tempo.")

taxas = {
    "Selic": 13.75,
    "CDI": 13.65,
    "IPCA": 5.0,
    "Poupança": 6.17,
    "Taxa Personalizada": None
}

col1, col2 = st.columns(2)

with col1:
    preco = st.number_input("Valor do produto (R$)", value=1000.0)
    desconto = st.slider("Desconto à vista (%)", 0, 30, 10)
    entrada = st.number_input("Entrada (R$)", value=0.0)

with col2:
    parcelas = st.slider("Número de parcelas", 1, 36, 12)
    taxa_nome = st.selectbox("Taxa de referência", list(taxas.keys()))

    if taxa_nome == "Taxa Personalizada":
        taxa_anual = st.number_input("Taxa anual (%)", value=12.0)
    else:
        taxa_anual = taxas[taxa_nome]

taxa_mensal = (1 + taxa_anual / 100) ** (1/12) - 1

preco_avista = preco * (1 - desconto/100)

valor_financiado = preco - entrada
parcela = valor_financiado / parcelas

vp = 0
for t in range(1, parcelas + 1):
    vp += parcela / ((1 + taxa_mensal) ** t)

vp_total = vp + entrada

# Simulação de investimento
investimento = preco_avista
valores_investidos = []

for i in range(parcelas):
    investimento *= (1 + taxa_mensal)
    valores_investidos.append(investimento)

valor_final_investimento = investimento

if valor_final_investimento > preco:
    decisao = "Recomendação: Parcelar e investir o capital disponível."
    cor = "#22c55e"
else:
    decisao = "Recomendação: Efetuar pagamento à vista."
    cor = "#ef4444"

st.subheader("Resumo da análise")

col3, col4, col5 = st.columns(3)

col3.metric("Valor à vista", f"R$ {preco_avista:,.2f}")
col4.metric("Valor presente do parcelamento", f"R$ {vp_total:,.2f}")
col5.metric("Valor futuro do investimento", f"R$ {valor_final_investimento:,.2f}")

st.markdown(f"<h3 style='color:{cor}'>{decisao}</h3>", unsafe_allow_html=True)

st.subheader("Evolução do capital investido")

fig = go.Figure()

fig.add_trace(go.Scatter(
    y=valores_investidos,
    mode='lines+markers',
    name='Investimento acumulado'
))

fig.add_hline(y=preco, line_dash="dash", annotation_text="Valor do produto")

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Período (meses)",
    yaxis_title="Valor (R$)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Detalhamento por período")

data = []

for i in range(parcelas):
    data.append({
        "Período": i+1,
        "Parcela (R$)": parcela,
        "Investimento acumulado (R$)": valores_investidos[i]
    })

df = pd.DataFrame(data)
st.dataframe(df)
