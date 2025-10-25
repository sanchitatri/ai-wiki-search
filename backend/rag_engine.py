import chromadb
import os
from typing import List, Dict, Any, Tuple
import google.generativeai as genai

class RAGEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        genai.configure(api_key=api_key)

        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_collection("documents")
    
    def retrieve(self, question: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant documents using vector similarity"""
        try:
            # Generate embedding for the question using Gemini embeddings
            embed_response = genai.embed_content(model="models/text-embedding-004", content=question)
            question_embedding = embed_response["embedding"] if isinstance(embed_response, dict) else embed_response.embedding
            
            # Ensure we have the latest collection handle (in case it was recreated during indexing)
            self.collection = self.chroma_client.get_collection("documents")
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=[question_embedding],
                n_results=n_results
            )
            
            # Format results
            sources = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    source = {
                        'content': doc,
                        'source': results['metadatas'][0][i].get('file_name', 'Unknown'),
                        'score': 1 - results['distances'][0][i]  # Convert distance to similarity
                    }
                    sources.append(source)
            
            return sources
        except Exception as e:
            print(f"Error in retrieve: {e}")
            return []
    
    def generate_answer(self, question: str, sources: List[Dict[str, Any]]) -> str:
        """Generate answer using Gemini 1.5"""
        if not sources:
            return "I couldn't find relevant information to answer your question. Please try rephrasing your question or check if the documents have been indexed."
        
        # Prepare context from sources
        context = "\n\n".join([f"Source: {source['source']}\nContent: {source['content']}" for source in sources])
        
        # Create prompt for GPT-4
        prompt = f"""Based on the following context from company documents, please answer the question. Be specific and cite sources when possible.

Context:
{context}

Question: {question}

Please provide a clear, helpful answer based on the context above. If the context doesn't contain enough information to fully answer the question, please say so and provide what information is available."""

        try:
            # Use a configurable model name; default to one supported by your key list
            model_name = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "I encountered an error while generating the answer. Please try again."
    
    def ask(self, question: str, n_results: int = 3) -> Tuple[str, List[Dict[str, Any]]]:
        """Main method to ask a question and get an answer"""
        # Retrieve relevant documents
        sources = self.retrieve(question, n_results)
        
        # Generate answer
        answer = self.generate_answer(question, sources)
        
        return answer, sources
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the indexed documents"""
        try:
            # Refresh collection handle before counting
            self.collection = self.chroma_client.get_collection("documents")
            count = self.collection.count()
            return {"total_documents": count}
        except:
            return {"total_documents": 0}

if __name__ == "__main__":
    # Test the RAG engine
    engine = RAGEngine()
    
    # Test question
    question = "What is the vacation policy?"
    answer, sources = engine.ask(question)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
