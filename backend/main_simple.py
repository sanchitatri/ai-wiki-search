"""
Simple AI Wiki Search Backend - No Large Models
Uses minimal dependencies for testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import os

app = FastAPI(title="AI Wiki Search - Simple Version", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple data storage
demo_data = {
    "vacation": "Employees are entitled to 20 days of paid vacation per year. Vacation requests should be submitted at least 2 weeks in advance through the HR portal.",
    "remote work": "The company supports remote work arrangements. Employees can work from home up to 3 days per week with manager approval. All remote work must follow the IT security guidelines.",
    "expense": "Expense reports should be submitted monthly through the company portal. All receipts must be attached and expenses must be business-related. Reimbursement typically takes 5-7 business days.",
    "performance": "Performance reviews are conducted annually in December. The process includes self-assessment, manager review, and goal setting for the next year. Reviews are used for promotion and salary decisions.",
    "it policies": "All employees must follow IT security guidelines including strong passwords, regular software updates, and secure file sharing practices.",
    "hr handbook": "The HR handbook contains all company policies, procedures, and employee benefits information. It's updated annually and available on the company intranet."
}

class QuestionRequest(BaseModel):
    question: str
    n_results: int = 3

class IndexRequest(BaseModel):
    directory: str

class QuestionResponse(BaseModel):
    answer: str
    sources: List[Dict]
    model_type: str = "simple_demo"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_engine": "initialized",
        "model_type": "simple_demo"
    }

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer"""
    question = request.question.lower()
    
    # Simple keyword matching
    answer = "I'm sorry, I couldn't find specific information about that topic in our knowledge base."
    sources = []
    
    for keyword, content in demo_data.items():
        if keyword in question:
            answer = content
            sources.append({
                "content": content,
                "source": f"Company Policy - {keyword.title()}",
                "score": 0.9
            })
            break
    
    # If no specific match, provide a general response
    if answer == "I'm sorry, I couldn't find specific information about that topic in our knowledge base.":
        answer = f"Based on your question '{request.question}', here's what I found: This is a demo response from the AI Wiki Search system. The system is designed to help employees find information about company policies, procedures, and guidelines. Try asking about vacation policies, remote work, expenses, or performance reviews."
        sources.append({
            "content": "This is a demo system for testing the AI Wiki Search functionality.",
            "source": "System Information",
            "score": 0.5
        })
    
    return QuestionResponse(
        answer=answer,
        sources=sources,
        model_type="simple_demo"
    )

@app.post("/api/index")
async def index_documents(request: IndexRequest):
    """Index documents (demo version)"""
    return {
        "message": "Documents indexed successfully (demo mode)",
        "directory": request.directory,
        "documents_processed": len(demo_data)
    }

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "total_documents": len(demo_data),
        "model_type": "simple_demo",
        "status": "ready"
    }

if __name__ == "__main__":
    print("🚀 Starting Simple AI Wiki Search Backend...")
    print("💰 Cost: $0.00 - Using simple demo responses!")
    print("🌐 Server will be available at: http://localhost:8000")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
