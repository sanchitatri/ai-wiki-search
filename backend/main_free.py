from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from embedding_pipeline_free import FreeIndexingPipeline
from rag_engine_free import FreeRAGEngine
import uvicorn

app = FastAPI(title="AI Wiki Search - Free Version", version="1.0.0")

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
indexing_pipeline = FreeIndexingPipeline()
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
        print("🔄 Initializing Free RAG Engine...")
        # Initialize the RAG engine
        rag_engine = FreeRAGEngine()
        print("✅ Free RAG Engine initialized successfully!")
        print("💰 $0.00 - Using local models!")
        
        # Try to index documents automatically
        try:
            print("🔄 Auto-indexing documents...")
            result = indexing_pipeline.run("/demo-data")
            print(f"✅ Indexed {result.get('documents_processed', 0)} documents")
        except Exception as e:
            print(f"⚠️ Auto-indexing failed: {e}")
            print("📝 Documents will be indexed on first request")
            
    except Exception as e:
        print(f"❌ Failed to initialize RAG engine: {e}")
        print("🔄 Will retry on first request...")
        rag_engine = None

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "rag_engine": "initialized" if rag_engine else "not initialized",
        "model_type": "free_local_models"
    }

@app.post("/api/ask")
async def ask_question(request: AskRequest):
    global rag_engine
    
    # Try to initialize RAG engine if not already done
    if not rag_engine:
        try:
            print("🔄 Retrying RAG engine initialization...")
            rag_engine = FreeRAGEngine()
            print("✅ Free RAG Engine initialized successfully!")
        except Exception as e:
            print(f"❌ Failed to initialize RAG engine: {e}")
            # Return a fallback response instead of crashing
            return {
                "answer": f"I apologize, but I'm experiencing technical difficulties. Your question was: '{request.question}'. Please try again or use the demo version for testing.",
                "sources": [{"content": "Error occurred", "source": "System", "score": 0.0}],
                "model_type": "free_local_models",
                "error": f"RAG engine initialization failed: {str(e)}"
            }
    
    try:
        answer, sources = rag_engine.ask(request.question, request.n_results)
        return {
            "answer": answer,
            "sources": sources,
            "model_type": "free_local_models"
        }
    except Exception as e:
        print(f"Error in ask_question: {e}")
        # Return a fallback response instead of crashing
        return {
            "answer": f"I apologize, but I'm experiencing technical difficulties. Your question was: '{request.question}'. Please try again or use the demo version for testing.",
            "sources": [{"content": "Error occurred", "source": "System", "score": 0.0}],
            "model_type": "free_local_models",
            "error": str(e)
        }

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
            "model_type": "free_local_models"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
