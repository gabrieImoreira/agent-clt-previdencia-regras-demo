
# 🤖📚 Chatbot LLM com PDFs usando ChromaDB + LangChain + HuggingFace  
### LLM Chatbot with PDFs using ChromaDB + LangChain + HuggingFace

Este projeto demonstra como construir um chatbot baseado em arquivos PDF com busca por similaridade vetorial. Utiliza embeddings gerados com modelos da HuggingFace e banco vetorial local com ChromaDB.

This project shows how to build a chatbot based on PDF files using vector similarity search. It uses HuggingFace embeddings and local vector storage with ChromaDB.

---

## 🚀 Tecnologias | Technologies

- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- PyPDFLoader

---

## 🗂️ Estrutura do Projeto | Project Structure

```
📂 data/             # PDFs de entrada | Input PDFs
📂 chroma_db/        # Banco vetorial persistente | Persistent vector DB
📄 main.py           # Script principal | Main script
📄 requirements.txt  # Dependências | Dependencies
```

---

## ▶️ Como usar | How to use

1. **Clone o repositório | Clone the repository:**

```bash
git clone https://github.com/your-user/chatbot-pdf-chroma.git
cd chatbot-pdf-chroma
```

2. **Instale as dependências | Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Coloque os arquivos PDF na pasta `/data` | Add your PDF files to the `/data` folder.**

4. **Execute o script | Run the script:**

```bash
python main.py
```

---

## ❓ Exemplo de Pergunta | Example Query

```text
Query: "Quem tem direito à aposentadoria por invalidez?"
```

O sistema buscará os 3 trechos mais relevantes com suas similaridades.

The system will return the top 3 most relevant text chunks with similarity scores.

---

## 📝 Notas | Notes

- O banco vetorial é salvo localmente em `chroma_db/`.  
  Vector database is stored locally at `chroma_db/`.

- O modelo de embedding padrão é `"all-MiniLM-L6-v2"` da HuggingFace.  
  Default embedding model is `"all-MiniLM-L6-v2"` from HuggingFace.

- Pontuações mais próximas de 1 indicam maior similaridade.  
  Scores closer to 1 mean higher similarity.

---

## 📫 Contato | Contact

Gabriel Moreira  
[LinkedIn](https://www.linkedin.com/in/seu-perfil)  
