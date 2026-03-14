# Resume RAG Chatbot

A 100% FREE RAG chatbot for your resume and projects that runs locally.

## Quick Start

### 1. Start Ollama (in separate terminal)
```bash
ollama serve
```

### 2. Download Model (in another terminal)
```bash
ollama pull llama3.2
```

### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the App
```bash
streamlit run app.py
```

### 6. Upload Your Documents
- Go to http://localhost:8501
- Upload your resume/projects in sidebar
- Click "Load & Index Documents"
- Start chatting!

## Tech Stack
- Streamlit (UI)
- ChromaDB (Vector DB)
- Sentence Transformers (Embeddings)
- Ollama + Llama 3.2 (LLM)

## Cost
₹0 - Everything runs locally!
