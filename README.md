# 🤖📚 Chat CLT com RAG & OpenAI(Embbedings e LLM) & LangChain

Este projeto demonstra como construir um assistente jurídico especializado em CLT (Consolidação das Leis do Trabalho), baseado em arquivos PDF com busca vetorial usando ChromaDB, LangChain e OpenAI.

---

## 🚀 Tecnologias Utilizadas

- Python
- LangChain
- OpenAI (GPT-4o e embeddings)
- ChromaDB
- Streamlit
- TinyDB

---

## 🗂️ Estrutura do Projeto

```
📂 data/               # PDFs da CLT e documentos jurídicos
📂 chroma_db_openai/   # Banco vetorial persistente (ChromaDB)
📄 rag_pipeline.py     # Pipeline RAG com recuperação e geração
📄 app.py              # Interface de chat com Streamlit
📄 requirements.txt    # Dependências do projeto
```

---

## ▶️ Como Usar

1. **Clone o repositório:**

```bash
git clone https://github.com/gabrieImoreira/agent-clt-previdencia-regras-demo.git
cd agent-clt-previdencia-regras-demo
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Adicione os PDFs na pasta `/data`:**

Copie os arquivos PDF com a legislação da CLT ou documentos jurídicos relacionados para a pasta `./data`.

4. **Execute o app:**

```bash
streamlit run app.py
```

---

## ❓ Exemplo de Pergunta

```text
"Quantos dias tenho direito de férias por ano?"
```

O sistema irá recuperar os trechos relevantes dos documentos PDF da CLT e responder com base neles.

---

## 🆚 Versões

### v1

- Usava embeddings da HuggingFace
- Sem histórico de conversa
- Integração simples via script `main.py`
- Sem interface gráfica

### v2 (Atual)

- Uso de GPT-4o via LangChain para respostas
- Armazenamento do histórico com TinyDB
- Interface de chat com Streamlit
- Prompt jurídico especializado com regras e restrições
- Integração completa com RAG (retrieval + geração)

---

## 💡 Funcionalidades

- Busca vetorial usando ChromaDB
- Histórico de conversa com armazenamento no TinyDB
- Interface amigável com Streamlit
- Geração de respostas jurídicas com base apenas nos documentos

---

## ⚠️ Observações

- O assistente **não substitui um advogado**.
- Ele responde **apenas com base nos documentos fornecidos**.
- Perguntas fora do escopo da CLT são gentilmente recusadas.

---

## 📫 Contato

Gabriel Moreira  
[LinkedIn](https://www.linkedin.com/in/ga-brielmoreira)
