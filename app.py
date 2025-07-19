import streamlit as st
from rag_pipeline import graph
from tinydb import TinyDB, Query
from datetime import datetime

# === CONFIG ===
st.set_page_config(page_title="Chat CLT", layout="wide")
db = TinyDB("conversas_db.json")
Conversa = Query()

# === INICIALIZAÇÃO DO ESTADO ===
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# === FUNÇÕES AUXILIARES ===
def listar_conversas():
    return db.all()

def carregar_conversa(chat_id):
    conversa = db.get(doc_id=chat_id)
    if conversa:
        st.session_state.chat_id = chat_id

def salvar_conversa(nome, mensagens):
    if st.session_state.chat_id:
        db.update({"nome": nome, "mensagens": mensagens}, doc_ids=[st.session_state.chat_id])
    else:
        chat_id = db.insert({"nome": nome, "mensagens": mensagens})
        st.session_state.chat_id = chat_id

def nova_conversa():
    st.session_state.chat_id = None

# === SIDEBAR: LISTA DE CONVERSAS ===
with st.sidebar:
    st.markdown("### 💬 Conversas")
    conversas = listar_conversas()
    for c in conversas:
        if st.button(c["nome"], key=f"btn_{c.doc_id}"):
            carregar_conversa(c.doc_id)

    st.markdown("---")
    if st.button("➕ Nova conversa"):
        nova_conversa()

# === TÍTULO DA PÁGINA ===
st.markdown("<h2 style='text-align: center;'>🧑‍⚖️ Chat CLT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Tire dúvidas com base na legislação trabalhista (CLT)</p>", unsafe_allow_html=True)

# === HISTÓRICO DA CONVERSA ATUAL ===
mensagens = []
if st.session_state.chat_id:
    conversa = db.get(doc_id=st.session_state.chat_id)
    mensagens = conversa["mensagens"] if conversa else []

# === EXIBE MENSAGENS NO CHAT ===
for msg in mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === INPUT DO USUÁRIO ===
if question := st.chat_input("Digite sua pergunta sobre CLT..."):
    mensagens.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Processa a resposta
    with st.chat_message("assistant"):
        with st.spinner("Consultando os documentos..."):
            response = graph.invoke({
                "question": question,
                "chat_history": mensagens
            })
            answer = response["answer"]
            st.markdown(answer)
            mensagens.append({"role": "assistant", "content": answer})

    # Salva conversa no banco
    nome_conversa = mensagens[0]["content"][:50]  # Nome = primeira pergunta
    salvar_conversa(nome_conversa, mensagens)
