import os
import glob
from typing import List, Dict, Any
import chromadb
import hashlib
import google.generativeai as genai

class IndexingPipeline:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        genai.configure(api_key=api_key)

        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def load_documents(self, documents_path: str) -> List[Dict[str, Any]]:
        """Load documents from various formats"""
        documents = []
        
        # Supported file patterns
        patterns = [
            "*.txt", "*.md", "*.pdf", "*.docx"
        ]
        
        for pattern in patterns:
            files = glob.glob(os.path.join(documents_path, pattern))
            for file_path in files:
                try:
                    if file_path.endswith('.txt'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    elif file_path.endswith('.md'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    else:
                        # For PDF and DOCX, we'll use simple text extraction
                        # In a real implementation, you'd use libraries like PyPDF2 or python-docx
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    
                    documents.append({
                        'file_path': file_path,
                        'content': content,
                        'file_name': os.path.basename(file_path)
                    })
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        return documents
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start + chunk_size - 100, start), -1):
                    if text[i] in '.!?\n':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
        
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini text-embedding-004"""
        embeddings: List[List[float]] = []
        batch_size = 100  # Process in batches to avoid rate limits

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                # Gemini API currently supports per-item embed calls; loop batch
                batch_embeddings: List[List[float]] = []
                for item in batch:
                    embed_resp = genai.embed_content(model="models/text-embedding-004", content=item)
                    vec = embed_resp["embedding"] if isinstance(embed_resp, dict) else embed_resp.embedding
                    batch_embeddings.append(vec)
                embeddings.extend(batch_embeddings)
            except Exception as e:
                print(f"Error generating embeddings for batch {i//batch_size + 1}: {e}")
                # Fallback: create zero embeddings with typical Gemini embedding size 768 or 3072.
                # Conservatively choose 768 to avoid excessive storage; adjust if needed.
                fallback_dim = 768
                batch_embeddings = [[0.0] * fallback_dim for _ in batch]
                embeddings.extend(batch_embeddings)

        return embeddings
    
    def store_in_database(self, chunks: List[str], metadata: List[Dict[str, Any]]):
        """Store chunks and embeddings in ChromaDB"""
        if not chunks:
            return
        
        # Generate embeddings
        embeddings = self.generate_embeddings(chunks)
        
        # Generate unique IDs
        ids = [hashlib.md5(chunk.encode()).hexdigest() for chunk in chunks]
        
        # Store in ChromaDB
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadata,
            ids=ids
        )
    
    def run(self, documents_path: str) -> Dict[str, Any]:
        """Run the complete indexing pipeline"""
        print("=" * 50)
        print("Starting Paid Indexing Pipeline")
        print("=" * 50)
        
        # Step 1: Load documents
        print("\n[Step 1] Loading documents...")
        documents = self.load_documents(documents_path)
        print(f"Loaded {len(documents)} document(s)")
        
        if not documents:
            print("No documents found!")
            return {"documents_processed": 0, "chunks_created": 0}
        
        # Step 2: Chunk documents
        print("\n[Step 2] Chunking documents...")
        all_chunks = []
        all_metadata = []
        
        for doc in documents:
            chunks = self.chunk_text(doc['content'])
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    'file_name': doc['file_name'],
                    'file_path': doc['file_path'],
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
        
        print(f"Created {len(all_chunks)} chunk(s)")
        
        # Step 3: Generate embeddings
        print("\n[Step 3] Generating embeddings...")
        # Clear existing collection
        try:
            self.chroma_client.delete_collection("documents")
            self.collection = self.chroma_client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
        except:
            pass
        
        # Store in database
        print("\n[Step 4] Storing in vector database...")
        self.store_in_database(all_chunks, all_metadata)
        print(f"Added {len(all_chunks)} documents to vector database")
        
        print("\n" + "=" * 50)
        print("Paid Indexing Complete!")
        print("=" * 50)
        
        return {
            "documents_processed": len(documents),
            "chunks_created": len(all_chunks)
        }

if __name__ == "__main__":
    pipeline = IndexingPipeline()
    result = pipeline.run("../demo-data")
    print(f"Result: {result}")
