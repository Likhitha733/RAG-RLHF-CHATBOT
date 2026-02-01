import google.generativeai as genai
from typing import List, Dict
import PyPDF2
from pathlib import Path
from config import Config
from vector_store import VectorStore

class RAGEngine:
    def __init__(self):
        self.config = Config
        self.vector_store = VectorStore()
        genai.configure(api_key=self.config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(self.config.MODEL_NAME)
    
    def initialize_database(self, pdf_path: str, force: bool = False):
        if not Path(pdf_path).exists(): return False
        self.vector_store.create_collection(force=force)
        
        # Simple Chunking Logic
        reader = PyPDF2.PdfReader(pdf_path)
        full_text = ""
        page_map = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                page_map.append((len(full_text), i + 1))
                full_text += text + "\n"
        
        chunks = []
        start = 0
        idx = 0
        while start < len(full_text):
            end = start + self.config.CHUNK_SIZE
            chunk_text = full_text[start:end]
            # Find page
            page_num = 1
            for pos, p_num in page_map:
                if start >= pos: page_num = p_num
                else: break
            
            chunks.append({
                "chunk_index": idx, "text": chunk_text,
                "page": page_num, "source": "PDF", "section": "Body"
            })
            start += (self.config.CHUNK_SIZE - self.config.CHUNK_OVERLAP)
            idx += 1
            
        self.vector_store.add_documents(chunks)
        return True

    def answer_query(self, query: str, context_chunks: List[Dict]) -> str:
        if not context_chunks:
            return "I couldn't find any relevant information in the document."

        context_str = "\n\n".join([f"[Page {c['metadata']['page']}] {c['text']}" for c in context_chunks])
        
        # --- PROMPT ENGINEERING FOR TABLES ---
        instruction = "Answer the question based on the context."
        if any(w in query.lower() for w in ['table', 'capabilities', 'list', 'compare', 'vs']):
            instruction += "\nIMPORTANT: The user wants a structured overview. FORMAT THE OUTPUT AS A MARKDOWN TABLE."

        prompt = f"""You are an Agentic AI assistant.
        
        CONTEXT:
        {context_str}
        
        USER QUERY: {query}
        
        INSTRUCTIONS:
        1. {instruction}
        2. If the answer is not in the context, say "I don't know."
        3. Cite the page number.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {e}"