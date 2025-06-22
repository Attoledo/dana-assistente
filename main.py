# main.py

import streamlit as st
from utils.pdf_utils import carregar_pdf
from utils.youtube_utils import processar_youtube
from utils.site_utils import carregar_site
from chat.assistente_dana import iniciar_assistente, gerar_resumo, salvar_como_pdf, salvar_como_txt
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Carrega chave da API # streamlit run main.py
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
if not api_key or not api_key.startswith("gsk_"):
    st.error("❌ API Key inválida ou ausente. Verifique o arquivo .env.")
    st.stop()
os.environ['GROQ_API_KEY'] = api_key
chat = ChatGroq(model='llama3-70b-8192')

# Página
st.set_page_config(page_title="Assistente Dana", page_icon="🦙")
st.title("Dana, seu Assistente Pessoal 😎")

# Seleção de fonte
opcao = st.sidebar.selectbox("Escolha a fonte de conteúdo:", ["PDF", "YouTube", "Site"])
doc_texto = ""

if opcao == "PDF":
    doc_texto = carregar_pdf()
elif opcao == "YouTube":
    doc_texto = processar_youtube()
elif opcao == "Site":
    doc_texto = carregar_site()

# Download e interação
if doc_texto:
    salvar_como_txt(doc_texto, "transcricao_formatada.txt")
    salvar_como_pdf(doc_texto, "transcricao_formatada.pdf")
    st.download_button("📄 Baixar TXT", data=doc_texto, file_name="transcricao_formatada.txt")
    with open("transcricao_formatada.pdf", "rb") as f:
        st.download_button("📄 Baixar PDF", data=f, file_name="transcricao_formatada.pdf")

    if st.sidebar.button("Gerar Resumo"):
        resumo = gerar_resumo(chat, doc_texto)
        st.markdown("## 📝 Resumo do Conteúdo")
        st.markdown(resumo)
        salvar_como_txt(resumo, "resumo.txt")
        salvar_como_pdf(resumo, "resumo.pdf")
        st.download_button("📄 Baixar Resumo (.txt)", data=resumo, file_name="resumo_llama3.txt")
        with open("resumo_llama3.pdf", "rb") as f:
            st.download_button("📄 Baixar Resumo (.pdf)", data=f, file_name="resumo_llama3.pdf")

    iniciar_assistente(chat, doc_texto)

