import chromadb
import os
from typing import List, Dict, Any, Tuple
from openai import AzureOpenAI

class RAGEngine:
    def __init__(self):
        # Check for Azure OpenAI credentials
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
        azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        
        if not azure_endpoint or not azure_api_key:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set")
        
        # Initialize Azure OpenAI client
        self.azure_client = AzureOpenAI(
            api_version=azure_api_version,
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
        )
        self.azure_deployment = azure_deployment
        self.azure_embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
        print("✅ Using Azure OpenAI")
        
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_collection("documents")
    
    def retrieve(self, question: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant documents using vector similarity"""
        try:
            # Generate embedding for the question using Azure OpenAI
            embed_response = self.azure_client.embeddings.create(
                model=self.azure_embedding_deployment,
                input=question
            )
            question_embedding = embed_response.data[0].embedding
            
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
        """Generate answer using Azure OpenAI"""
        if not sources:
            return "I couldn't find relevant information to answer your question. Please try rephrasing your question or check if the documents have been indexed."
        
        # Prepare context from sources
        context = "\n\n".join([f"Source: {source['source']}\nContent: {source['content']}" for source in sources])
        
        # Create prompt
        prompt = f"""Based on the following context from company documents, please answer the question. Be specific and cite sources when possible.

Context:
{context}

Question: {question}

Please provide a clear, helpful answer based on the context above. If the context doesn't contain enough information to fully answer the question, please say so and provide what information is available."""

        try:
            # Use Azure OpenAI
            response = self.azure_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions based on provided context.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "4096")),
                temperature=float(os.getenv("AZURE_OPENAI_TEMPERATURE", "1.0")),
                top_p=float(os.getenv("AZURE_OPENAI_TOP_P", "1.0")),
                model=self.azure_deployment,
            )
            return response.choices[0].message.content
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
