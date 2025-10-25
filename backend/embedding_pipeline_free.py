import os
import glob
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
import hashlib

class FreeIndexingPipeline:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="./chroma_db_free", settings=chromadb.Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(
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
        """Generate embeddings using local sentence transformer"""
        return self.embedding_model.encode(texts).tolist()
    
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
        print("Starting Free Indexing Pipeline")
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
            self.client.delete_collection("documents")
            self.collection = self.client.create_collection(
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
        print("Free Indexing Complete!")
        print("=" * 50)
        
        return {
            "documents_processed": len(documents),
            "chunks_created": len(all_chunks)
        }

if __name__ == "__main__":
    pipeline = FreeIndexingPipeline()
    result = pipeline.run("../demo-data")
    print(f"Result: {result}")
