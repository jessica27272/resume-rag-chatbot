import ollama
from typing import List, Dict

class LLMInterface:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.check_ollama_status()
    
    def check_ollama_status(self):
        try:
            models = ollama.list()
            print(f"Ollama is running. Available models: {[m['name'] for m in models['models']]}")
            model_exists = any(self.model_name in m['name'] for m in models['models'])
            if not model_exists:
                print(f"\n⚠️  Model '{self.model_name}' not found!")
                print(f"Run this command to download it: ollama pull {self.model_name}")
        except Exception as e:
            print(f"⚠️  Ollama connection error: {e}")
            print("Make sure Ollama is running. Start it with: ollama serve")
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        context = "\n\n".join([f"[Source: {doc['metadata'].get('filename', 'unknown')}]\n{doc['content']}" for doc in context_docs])
        prompt = f"""You are a helpful assistant answering questions about a candidate's resume and projects.

Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't have that information in the provided documents."

CONTEXT:
{context}

QUESTION: {query}

ANSWER (be specific and cite relevant experience/projects):"""
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt, stream=False)
            return response['response']
        except Exception as e:
            return f"Error generating response: {e}\n\nMake sure Ollama is running and model '{self.model_name}' is installed."
    
    def chat_stream(self, query: str, context_docs: List[Dict]):
        context = "\n\n".join([f"[Source: {doc['metadata'].get('filename', 'unknown')}]\n{doc['content']}" for doc in context_docs])
        prompt = f"""You are a helpful assistant answering questions about a candidate's resume and projects.

Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't have that information in the provided documents."

CONTEXT:
{context}

QUESTION: {query}

ANSWER (be specific and cite relevant experience/projects):"""
        try:
            stream = ollama.generate(model=self.model_name, prompt=prompt, stream=True)
            for chunk in stream:
                yield chunk['response']
        except Exception as e:
            yield f"Error: {e}"
