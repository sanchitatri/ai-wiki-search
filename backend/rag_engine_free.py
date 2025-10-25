import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple

class FreeRAGEngine:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="./chroma_db_free", settings=chromadb.Settings(anonymized_telemetry=False))
        try:
            self.collection = self.client.get_collection("documents")
        except Exception as e:
            print(f"Collection not found, creating new one: {e}")
            self.collection = self.client.create_collection("documents")
    
    def retrieve(self, question: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant documents using vector similarity"""
        try:
            # Check if collection exists and has documents
            if self.collection.count() == 0:
                print("No documents found in collection")
                return []
            
            # Generate embedding for the question
            question_embedding = self.embedding_model.encode([question])
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=question_embedding.tolist(),
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
            # Try to return some fallback content
            return [{"content": "I couldn't retrieve relevant information from the documents. Please ensure documents are properly indexed.", "source": "System", "score": 0.0}]
    
    def generate_answer(self, question: str, sources: List[Dict[str, Any]]) -> str:
        """Generate answer using simple template-based approach"""
        if not sources:
            return "I couldn't find relevant information to answer your question. Please try rephrasing your question or check if the documents have been indexed."
        
        # Create a simple answer based on the sources
        answer_parts = []
        
        # Add context from sources
        for source in sources[:2]:  # Use top 2 sources
            content = source['content']
            if len(content) > 200:
                content = content[:200] + "..."
            answer_parts.append(content)
        
        # Create a simple response
        if answer_parts:
            answer = "Based on the available information:\n\n" + "\n\n".join(answer_parts)
        else:
            answer = "I found some relevant information but couldn't generate a specific answer. Please check the sources below for more details."
        
        return answer
    
    def ask(self, question: str, n_results: int = 3) -> Tuple[str, List[Dict[str, Any]]]:
        """Main method to ask a question and get an answer"""
        try:
            # Retrieve relevant documents
            sources = self.retrieve(question, n_results)
            
            # Generate answer
            answer = self.generate_answer(question, sources)
            
            return answer, sources
        except Exception as e:
            print(f"Error in ask method: {e}")
            # Return a fallback response
            return f"I apologize, but I encountered an error while processing your question: '{question}'. Please try again or use the demo version for testing.", [{"content": "Error occurred", "source": "System", "score": 0.0}]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the indexed documents"""
        try:
            count = self.collection.count()
            return {"total_documents": count}
        except:
            return {"total_documents": 0}

if __name__ == "__main__":
    # Test the RAG engine
    engine = FreeRAGEngine()
    
    # Test question
    question = "What is the vacation policy?"
    answer, sources = engine.ask(question)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
