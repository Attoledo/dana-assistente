import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def carregar_pdf():
    st.subheader("📄 Leitor de PDF")
    arquivo_pdf = st.file_uploader("Faça upload do seu arquivo PDF:", type=["pdf"])
    if arquivo_pdf:
        with open("temp.pdf", "wb") as f:
            f.write(arquivo_pdf.read())
        loader = PyPDFLoader("temp.pdf")
        docs = loader.load()
        texto = " ".join([doc.page_content for doc in docs])[:15000]
        return texto
    return ""

