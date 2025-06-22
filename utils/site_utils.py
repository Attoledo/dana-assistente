import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

def carregar_site():
    st.subheader("🌐 Leitor de Site")
    url = st.text_input("Cole a URL do site:")
    if url:
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            texto = " ".join([doc.page_content for doc in docs])[:15000]
            return texto
        except Exception as e:
            st.error(f"Erro ao carregar site: {e}")
    return ""

