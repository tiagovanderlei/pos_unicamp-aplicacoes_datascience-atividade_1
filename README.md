# Atividade Aula 1 - Cadastro de Pacientes (Gradio x Streamlit)

Aplicações em Data Science - Pós UNICAMP

Sistema de cadastro de pacientes para a recepção de um consultório, feito em duas versões:

- `gradio_app/` - versão em Gradio, roda localmente e grava em `pacientes.csv`
- `streamlit_app/` - versão em Streamlit, publicada no Streamlit Community Cloud

Campos: nome, idade, convênio, prioridade (1 a 5) e motivo da consulta. Cada cadastro gera uma linha no CSV com a data/hora.

## Como rodar

```
pip install -r requirements.txt

python gradio_app/app.py
streamlit run streamlit_app/app.py
```

## Observações

- No Streamlit Cloud o sistema de arquivos é efêmero, então os cadastros ficam no `st.session_state` e podem ser exportados pelo botão "Baixar CSV".
- O Gradio só executa a função do botão, enquanto o Streamlit roda o script inteiro a cada interação (por isso o uso do `st.form`).
- `print_gradio_local.jpg` mostra a versão Gradio rodando localmente.
