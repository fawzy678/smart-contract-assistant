# 🔐 Smart Contract Summary & Q&A Assistant

An AI-powered modular application that analyzes Solidity smart contracts using **LangChain**, **RAG (Retrieval Augmented Generation)**, **Groq LLM**, and **Gradio UI** — with local API deployment via **LangServe + FastAPI**.

---

## 🎯 Project Goal

- 📄 **Summarize** any Solidity smart contract automatically
- 💬 **Chat & Ask questions** about the contract using RAG
- 🔍 **Identify risks** and security vulnerabilities
- 🛡️ **Guard Rails** — blocks off-topic questions
- 🧠 **Memory** — remembers conversation history
- 📁 **Multi-format support** — `.sol`, `.txt`, `.pdf`, `.docx`
- 🚀 **Local API** via LangServe + FastAPI

---

## 🧠 Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core language |
| LangChain | LLM framework & chains |
| Groq (Llama 3.3 70B) | Language model |
| FAISS | Vector store for RAG |
| Gradio | Web UI |
| LangServe + FastAPI | Local API deployment |
| PyMuPDF | PDF reading |
| python-docx | Word document reading |
| python-dotenv | Environment management |

---

## 🏗️ Project Structure

```
smart-contract-assistant/
├── app.py                      ← Gradio UI entry point
├── serve.py                    ← LangServe + FastAPI local API
├── requirements.txt            ← Python dependencies
├── .env                        ← API keys (never commit this)
├── .gitignore                  ← Git ignore rules
├── README.md                   ← Project documentation
├── chains/
│   ├── __init__.py
│   ├── summary_chain.py        ← LLM summarization chain
│   └── qa_chain.py             ← RAG Q&A + Memory + Guard Rails
├── vectorstore/
│   ├── __init__.py
│   └── store.py                ← FAISS embedding & retrieval
├── utils/
│   ├── __init__.py
│   └── loader.py               ← File reader (.sol .txt .pdf .docx)
└── data/
    └── samples_contracts/
        ├── sample_contract1.sol
        ├── sample_contract2.sol
        └── sample_contract3.sol
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-contract-assistant.git
cd smart-contract-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Free Groq API Key
1. Go to **https://console.groq.com**
2. Sign up with Google
3. Click **API Keys** → **Create API Key**
4. Copy the key

### 4. Create `.env` File
```
GROQ_API_KEY=gsk_your_key_here
```

### 5. Run Gradio UI
```bash
python app.py
```
Open browser at: **http://127.0.0.1:7860**

### 6. Run LangServe API (optional)
```bash
python serve.py
```
Open browser at: **http://localhost:8000/docs**

---

## 🚀 How to Use

1. **Upload or paste** your smart contract (`.sol`, `.txt`, `.pdf`, `.docx`)
2. Go to **Summarize tab** → Click **Generate Summary**
3. Go to **Q&A tab** → Ask any question about the contract
4. Click **Clear History** to reset the conversation

---

## 🛡️ Features

### Guard Rails
The assistant **only answers questions about smart contracts**.
If you ask an off-topic question (e.g. "who won the World Cup?"), it will respond:
> ⚠️ Sorry, I can only answer questions about smart contracts.

### Memory
The assistant **remembers previous questions** in the same session.
You can ask follow-up questions like:
- "What does the mint function do?"
- "Is it safe?" ← remembers you were asking about mint

### Multi-format Upload
Supports: `.sol` `.txt` `.pdf` `.docx`

---

## 🧪 Sample Contracts

| Contract | Difficulty | Description |
|----------|-----------|-------------|
| SimpleToken | ⭐ Easy | Basic ERC-20 token |
| Voting | ⭐⭐ Medium | Voting system with candidates |
| Escrow | ⭐⭐ Medium | Escrow with arbiter |
| DeFiVault | ⭐⭐⭐ Hard | DeFi vault with whitelist/blacklist |

---

## 🏛️ Architecture

```
User Input (paste / upload file)
           ↓
    utils/loader.py
           ↓
  vectorstore/store.py  ←  FAISS
           ↓
  ┌─────────────────┐
  │  Summary Tab    │ → chains/summary_chain.py → Groq LLM
  └─────────────────┘
  ┌─────────────────┐
  │    Q&A Tab      │ → Guard Rails → chains/qa_chain.py → RAG → Groq LLM
  └─────────────────┘        ↑
                          Memory
           ↓
      Gradio UI Output

  serve.py → LangServe + FastAPI → REST API
```

---

## ⚠️ Important Notes

- **Never commit `.env`** to GitHub — it contains your API key
- `.gitignore` already excludes `.env` and `__pycache__`
- Groq free tier is sufficient for testing

---

## 👨‍💻 Author

Built as part of an AI & Prompt Engineering Course Project.
> Domain: LLM Pipelines · LangChain · Vector Stores · Gradio · LangServe
