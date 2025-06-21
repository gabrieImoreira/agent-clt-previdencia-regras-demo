from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
import os


persist_directory = "./chroma_db"
collection_name = "docs"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Verifica se os dados já estão persistidos
if os.path.exists(persist_directory):
    print("🔁 Carregando índice existente...")
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
else:
    print("📚 Indexando PDFs...")
    pdf_dir = "./data"
    loaders = [
        PyPDFLoader(os.path.join(pdf_dir, f))
        for f in os.listdir(pdf_dir)
        if f.endswith(".pdf")
    ]
    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    docs_chunked = splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=docs_chunked,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )

# Consulta
# 4. Buscar documentos relevantes (exemplo)
query = "fórmula do salário mínimo"

results = vector_store.similarity_search_with_score(
    query, k=3
)
print(len(results), "resultados encontrados.")
for res, score in results:
    print(
        f"""
        * [SIM={score:3f}]\n
        -------\n
        Page Content: {res.page_content}\n
        -------\n
        Metadata: [{res.metadata}]
        ========\n"""
    )
