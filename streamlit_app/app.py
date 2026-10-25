# Atividade Aula 1 - Parte 2: cadastro de pacientes em Streamlit

import streamlit as st
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]

st.set_page_config(page_title="Cadastro de Pacientes", layout="centered")
st.title("Cadastro de Pacientes")

if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)


def gravar_csv(linha):
    """Grava uma linha no CSV (cabeçalho só na primeira vez)"""
    novo = pd.DataFrame([linha], columns=COLUNAS)
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)


with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox("Convênio", CONVENIOS)
    prioridade = st.slider("Prioridade do atendimento (5 = urgente)", 1, 5)
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar", type="primary", width="stretch")

if enviado:
    if not nome.strip():
        st.error("Informe o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip(),
        }
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha])],
            ignore_index=True,
        )
        gravar_csv(nova_linha)
        st.success("Paciente cadastrado!")

pacientes = st.session_state.pacientes

st.subheader("Últimos pacientes cadastrados")
st.dataframe(pacientes.tail(5).iloc[::-1], hide_index=True, width="stretch")

# No Streamlit Cloud o disco é efêmero, então os dados precisam ser exportados
# utf-8-sig para o Excel mostrar os acentos
csv = pacientes.to_csv(index=False).encode("utf-8-sig")
st.download_button("Baixar CSV", csv, "pacientes.csv", "text/csv")
