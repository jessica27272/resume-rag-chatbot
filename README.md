
# Resume RAG Chatbot

A free chatbot that lets people ask questions about your resume using AI. Runs 100% locally on your computer.

## What It Does

- Upload your resume (PDF, Word, or text file)
- Ask questions in natural language
- Get AI-powered answers with sources
- Completely free, no API costs

## Tech Stack

- **ChromaDB** - Stores your documents
- **Sentence Transformers** - Converts text to searchable format
- **Ollama + Llama 3.2** - AI that answers questions
- **Streamlit** - Web interface

## Installation

### 1. Install Ollama

**Mac:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:** Download from https://ollama.ai/download

### 2. Clone & Setup
```bash
git clone https://github.com/jessica27272/resume-rag-chatbot.git
cd resume-rag-chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Download AI model
ollama pull llama3.2
```

### 3. Run

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
streamlit run app.py
```

Open browser to `http://localhost:8501`

## How to Use

1. Upload your resume in the sidebar
2. Click "Load & Index Documents"
3. Ask questions like:
   - "What skills does this person have?"
   - "Tell me about their experience"
   - "What projects have they worked on?"

## Cost

₹0 - Everything is free and runs locally!

## Author

Jessica Wadhwa - [@jessica27272](https://github.com/jessica27272)



