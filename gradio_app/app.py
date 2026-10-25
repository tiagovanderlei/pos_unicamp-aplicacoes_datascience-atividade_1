# Atividade Aula 1 - Parte 1: cadastro de pacientes em Gradio

import gradio as gr
import pandas as pd
import os
from datetime import datetime

# CSV ao lado deste script, independente da pasta de onde ele é executado
ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def ultimos_pacientes(n=5):
    """Últimos n pacientes do CSV, o mais recente primeiro"""
    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=COLUNAS)
    return pd.read_csv(ARQUIVO_CSV).tail(n).iloc[::-1]


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    """Valida o formulário e grava uma nova linha no CSV"""
    nome = (nome or "").strip()
    if not nome:
        raise gr.Error("Informe o nome do paciente.")
    if idade is None or not 0 <= idade <= 120:
        raise gr.Error("Informe uma idade entre 0 e 120 anos.")
    if not convenio:
        raise gr.Error("Selecione o convênio.")

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": (motivo or "").strip(),
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    # Cria o arquivo com cabeçalho na primeira execução; depois só acrescenta
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    mensagem = f"Paciente {nome} cadastrado com sucesso!"

    # Limpa o formulário para o próximo paciente
    return mensagem, ultimos_pacientes(), "", None, "Particular", 1, ""


# Layout em coluna única para funcionar no celular
with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## Cadastro de Pacientes")

    nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = gr.Number(label="Idade", minimum=0, maximum=120, precision=0)
    convenio = gr.Dropdown(CONVENIOS, value="Particular", label="Convênio")
    prioridade = gr.Slider(1, 5, value=1, step=1, label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)

    botao = gr.Button("Cadastrar", variant="primary")

    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados", interactive=False, wrap=True)

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela, nome, idade, convenio, prioridade, motivo],
    )

    # Mostra os cadastros já existentes ao abrir a página
    demo.load(ultimos_pacientes, None, tabela)

if __name__ == "__main__":
    demo.launch()
