from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from embedding_pipeline import IndexingPipeline
from rag_engine import RAGEngine
import uvicorn
import os

app = FastAPI(title="AI Wiki Search - Paid Version", version="1.0.0")

# CORS configuration
origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8000",  # Backend itself
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
indexing_pipeline = IndexingPipeline()
rag_engine = None

class AskRequest(BaseModel):
    question: str
    n_results: int = 3

class IndexRequest(BaseModel):
    documents_path: str = "../demo-data"

@app.on_event("startup")
async def startup_event():
    global rag_engine
    try:
        # Check if Gemini API key is available
        if not os.getenv("GEMINI_API_KEY"):
            print("⚠️  GEMINI_API_KEY not found. Please set it in your environment.")
            print("💠 This version requires Google Gemini API key (chat + embeddings).")
            return
        
        # Initialize the RAG engine
        rag_engine = RAGEngine()
        print("✅ Paid RAG Engine initialized successfully!")
        print("💠 Using Google Gemini (gemini-1.5-pro + text-embedding-004)!")
    except Exception as e:
        print(f"❌ Failed to initialize RAG engine: {e}")
        rag_engine = None

@app.get("/health")
async def health_check():
        return {
            "status": "healthy",
            "rag_engine": "initialized" if rag_engine else "not initialized",
            "model_type": "paid_gemini_models"
        }

@app.post("/api/ask")
async def ask_question(request: AskRequest):
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG engine not initialized. Please check OPENAI_API_KEY.")
    
    try:
        answer, sources = rag_engine.ask(request.question, request.n_results)
        return {
            "answer": answer,
            "sources": sources,
            "model_type": "paid_gemini_models"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/index")
async def index_documents(request: IndexRequest):
    try:
        result = indexing_pipeline.run(request.documents_path)
        return {
            "message": "Documents indexed successfully",
            "documents_processed": result.get("documents_processed", 0),
            "chunks_created": result.get("chunks_created", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    if not rag_engine:
        return {"error": "RAG engine not initialized"}
    
    try:
        stats = rag_engine.get_stats()
        return {
            "total_documents": stats.get("total_documents", 0),
            "model_type": "paid_gemini_models"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
