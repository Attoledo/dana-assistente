import streamlit as st
import re
from langchain.prompts import ChatPromptTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def salvar_como_pdf(texto, caminho):
    doc = SimpleDocTemplate(caminho, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    estilo = styles["Normal"]
    estilo.fontName = "Helvetica"
    estilo.fontSize = 12
    estilo.leading = 16
    estilo.alignment = 4  # Justificado

    partes = texto.split("\n\n")
    elementos = [Paragraph(par.strip(), estilo) for par in partes if par.strip()]
    for i in range(len(elementos)-1):
        elementos.insert(i*2 + 1, Spacer(1, 12))

    doc.build(elementos)

def salvar_como_txt(texto, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)

def gerar_resumo(chat, texto_base):
    prompt = ChatPromptTemplate.from_template(
        "Resuma o conteúdo abaixo em tópicos objetivos, em português do Brasil:\n\n{texto}\nEste resumo deve ser um pouco mais descritivo de modo a dar um entendimento mais claro sobre o assunto."
    )
    mensagem = prompt.format_messages(texto=texto_base[:3000])
    resposta = chat.invoke(mensagem)
    return resposta.content.strip()

def iniciar_assistente(chat, texto_base):
    template = ChatPromptTemplate.from_messages([
        ('system', 'O seu nome é Dana, um assistente pessoal sempre disponível. Fale com empatia, entusiasmo e com uma linguagem comum a todos.'
                   'Voce possui características técnicas quando necessário usando todo o seu conhecimento '
                   'Use as informações abaixo:\n\n{informacoes}'),
        ('user', '{input}')
    ])
    chain = template | chat

    if 'chat' not in st.session_state:
        st.session_state.chat = []
    if 'nome_usuario' not in st.session_state:
        nome = st.text_input("Olá, qual é o seu nome?", placeholder="Ex: Roberto")
        if nome:
            st.session_state.nome_usuario = nome
            st.rerun()
    else:
        nome = st.session_state.nome_usuario
        for entrada in st.session_state.chat:
            with st.chat_message("user"):
                st.markdown(entrada["pergunta"])
            with st.chat_message("assistant"):
                st.markdown(entrada["resposta"])

        pergunta = st.chat_input(f"Como posso te ajudar, {nome}:")
        if pergunta:
            with st.chat_message("user"):
                st.markdown(pergunta)
            with st.spinner("Estou analisando a melhor resposta..."):
                resposta = chain.invoke({
                    'informacoes': texto_base,
                    'input': pergunta,
                    'nome_usuario': nome
                }).content
            with st.chat_message("assistant"):
                st.markdown(resposta)
            st.session_state.chat.append({
                "pergunta": pergunta,
                "resposta": resposta
            })




