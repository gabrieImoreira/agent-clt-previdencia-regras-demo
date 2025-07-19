from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langgraph.graph import StateGraph, START
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from typing_extensions import TypedDict, List
import os

# Caminhos
persist_directory = "./chroma_db_openai"
collection_name = "docs"
pdf_dir = "./data"

# LLM e embeddings
llm = ChatOpenAI(model="gpt-4o", temperature=0.0, max_tokens=1000)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Vetorização
if os.path.exists(persist_directory):
    print("🔁 Carregando índice existente...")
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
else:
    print("📚 Indexando PDFs...")
    loaders = [
        PyPDFLoader(os.path.join(pdf_dir, f))
        for f in os.listdir(pdf_dir)
        if f.endswith(".pdf")
    ]
    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_chunked = splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=docs_chunked,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )

# Prompt
prompt = ChatPromptTemplate.from_template("""
Você é um assistente jurídico especializado nas leis da CLT (Consolidação das Leis do Trabalho), e responde de forma amigável, clara e com base apenas nos documentos fornecidos.
<restricoes>
- Não use informações de fora do contexto.
- Não invente leis, artigos ou interpretações.
- Não responda perguntas fora do tema CLT (exceto saudações educadas).
- Não diga "Olá" e saudações educadas, exceto se alguém disser "oi" ou similar.
</restricoes>
Se alguém disser “oi” ou fizer uma saudação, você pode responder com simpatia e lembrar que é um assistente jurídico sobre CLT.
Caso a resposta à pergunta **não esteja nos documentos fornecidos**, diga educadamente que **não encontrou essa informação na legislação disponível**.
Sempre que possível, cite o nome do documento de onde a resposta veio.

<permissoes>
- Você pode responder perguntas sobre a CLT, direitos trabalhistas, contratos, férias, rescisão, FGTS, jornada de trabalho, entre outros temas relacionadosa CLT
- Você pode explicar artigos, parágrafos e incisos da CLT.
- Você pode fornecer informações sobre direitos e deveres de empregadores e empregados.
- Você pode esclarecer dúvidas sobre processos trabalhistas e como funcionam.
- Você pode ajudar a entender termos jurídicos e procedimentos relacionados à CLT.
- Você pode e deve lembrar que é um assistente jurídico especializado em CLT, e não um advogado.
- Você pode e deve lembrar do nome e informações do usuário, se fornecidas, para personalizar a conversa.
</permissoes>
---
- Histórico da conversa: {history}
- Pergunta: {question}
- Contexto: {context}
- Resposta:
""")

# State com histórico
class State(TypedDict):
    question: str
    context: List[Document]
    chat_history: List[dict]
    answer: str

# Retrieve
def retrieve(state: State):
    docs = vector_store.similarity_search(state["question"])
    return {"context": docs}

# Generate com histórico no prompt
def generate(state: State):
    # Formata histórico de chat
    history_lines = []
    for msg in state.get("chat_history", []):
        role = "Usuário" if msg["role"] == "user" else "Assistente"
        history_lines.append(f"{role}: {msg['content']}")
    history_text = "\n".join(history_lines)

    # Formata contexto
    docs_text = "\n\n".join(doc.page_content for doc in state["context"])

    # Prompt
    messages = prompt.invoke({
        "question": state["question"],
        "context": docs_text,
        "history": history_text
    })
    response = llm.invoke(messages)
    return {"answer": response.content}

# Graph
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()
