
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Arquivo local para salvar dados
ARQUIVO = "paletes.csv"

# Lista de unidades
unidades = [
    "SP 10/B14", "ITAPEVI/B11", "LEOPOLDINA/B16", "SANTO ANDRÉ/B26", "DIADEMA/B09",
    "ITAPECERICA/B06", "CARAPICUÍBA/B13", "CAIEIRAS/B04", "FREGUESIA/B27",
    "SP12/B17", "SP16/B22", "COTIA/B05", "JAD SP DEP LEOPOL/B75"
]

# Carregar ou criar novo DataFrame com estrutura para 3 turnos
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
else:
    df = pd.DataFrame({
        "Unidade": unidades,
        "Turno 01": [0]*len(unidades),
        "Turno 02": [0]*len(unidades),
        "Turno 03": [0]*len(unidades)
    })

st.set_page_config(page_title="📦 Controle de Paletes", layout="wide")

st.title("📦 Controle de Paletes por Unidade")

# Mostrar e editar os dados por turno
for i, row in df.iterrows():
    with st.expander(f"🧱 {row['Unidade']}"):
        col1, col2, col3 = st.columns(3)
        df.at[i, "Turno 01"] = col1.number_input("Turno 01", min_value=0, value=int(row["Turno 01"]), key=f"t1_{i}")
        df.at[i, "Turno 02"] = col2.number_input("Turno 02", min_value=0, value=int(row["Turno 02"]), key=f"t2_{i}")
        df.at[i, "Turno 03"] = col3.number_input("Turno 03", min_value=0, value=int(row["Turno 03"]), key=f"t3_{i}")

# Botões de ação
col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Salvar"):
        df.to_csv(ARQUIVO, index=False)
        st.success("Dados salvos com sucesso!")
with col2:
    if st.button("📥 Exportar para Excel"):
        df.to_excel("paletes_export.xlsx", index=False)
        st.success("Arquivo Excel gerado: paletes_export.xlsx")

# Gráfico de barras empilhadas com totais
st.subheader("📊 Gráfico por Unidade e Turno")

cores = ["#C62828", "#424242", "#212121"]  # vermelho médio, cinza médio, preto escuro
df["Total"] = df[["Turno 01", "Turno 02", "Turno 03"]].sum(axis=1)

fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')
ax.bar(df["Unidade"], df["Turno 01"], label="Turno 01", color=cores[0])
ax.bar(df["Unidade"], df["Turno 02"], bottom=df["Turno 01"], label="Turno 02", color=cores[1])
ax.bar(df["Unidade"], df["Turno 03"],
       bottom=df["Turno 01"] + df["Turno 02"], label="Turno 03", color=cores[2])

# Rótulo total no topo de cada coluna
for idx, total in enumerate(df["Total"]):
    ax.text(idx, total + 0.5, str(total), ha="center", va="bottom", color="black", fontweight="bold")

ax.set_ylabel("Quantidade de Paletes")
ax.set_xticks(range(len(df["Unidade"])))
ax.set_xticklabels(df["Unidade"], rotation=45, ha="right")
ax.legend(title="Turnos")
ax.set_facecolor("white")  # sem preenchimento de fundo no gráfico

st.pyplot(fig)

# Rodapé com direitos autorais
st.markdown("---")
st.markdown("© Dandara Silva 2025")
