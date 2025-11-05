# IntelliFind - The Company's Smart Answer Engine

An AI-powered internal knowledge search system powered by Azure OpenAI that allows employees to ask natural language questions and get instant answers from company documents using RAG (Retrieval-Augmented Generation).

##  Overview

This application provides a clean, simple interface for searching company knowledge. Employees can ask questions in plain English and get instant answers with source citations. The system uses Azure OpenAI for both chat completions and embeddings, combined with ChromaDB for vector storage and retrieval.

##  Features

- **Natural Language Queries**: Ask questions in plain English
- **Instant Answers**: Get immediate responses with source citations
- **Azure OpenAI Powered**: Uses GPT-4o for chat and text-embedding-3-large for embeddings
- **Vector Search**: Semantic search using ChromaDB vector database
- **Simple Interface**: Clean, modern web interface
- **Docker Ready**: Easy deployment with Docker Compose
- **RAG Architecture**: Retrieval-Augmented Generation for accurate, context-aware responses

##  Quick Start

### Prerequisites

- Docker and Docker Compose
- Azure OpenAI account with:
  - Chat model deployment (e.g., `gpt-4o`)
  - Embedding model deployment (e.g., `text-embedding-3-large`)
  - API key and endpoint

### Installation Steps

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-wiki-search
```

#### 2. Configure Azure OpenAI

Create a `.env` file in the project root:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

**Note**: Make sure your Azure OpenAI resource has both chat and embedding model deployments created.

#### 3. Start the System

```bash
# Start both frontend and backend
docker-compose -f docker-compose-paid.yml up --build -d

# Check status
docker-compose -f docker-compose-paid.yml ps
```

#### 4. Index Documents

Before asking questions, you need to index your documents:

```bash
curl -X POST http://localhost:8000/api/index \
  -H "Content-Type: application/json" \
  -d '{"documents_path": "/demo-data"}'
```

Or use the demo data that's already included:
```bash
curl -X POST http://localhost:8000/api/index \
  -H "Content-Type: application/json" \
  -d '{"documents_path": "../demo-data"}'
```

#### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## 🎪 Demo & Testing

### Using the Web Interface

1. Open http://localhost:3000 in your browser
2. Try these example questions:
   - "What's our vacation policy?"
   - "How do I request time off?"
   - "What are the remote work guidelines?"
   - "How do I submit expense reports?"
   - "What's the process for performance reviews?"

### Testing the API Directly

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is our vacation policy?", "n_results": 3}'

# Check stats
curl http://localhost:8000/api/stats
```

## 📁 Project Structure

```
ai-wiki-search/
├── backend/                    # Python backend
│   ├── main.py                # FastAPI application
│   ├── rag_engine.py          # RAG engine with Azure OpenAI
│   ├── embedding_pipeline.py  # Document indexing pipeline
│   ├── Dockerfile.paid        # Backend Docker configuration
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Static HTML frontend
│   ├── public/
│   │   └── index-static.html  # Main HTML file
│   ├── simple_server.py       # Python HTTP server
│   └── Dockerfile.python      # Frontend Docker configuration
│
├── demo-data/                  # Demo documents
│   ├── hr_handbook.txt        # HR policies
│   ├── it_policies.txt        # IT guidelines
│   ├── developer_guide.md     # Developer documentation
│   ├── onboarding_guide.md    # Onboarding guide
│   ├── security_policies.txt  # Security policies
│   └── benefits.md            # Employee benefits
│
├── docker-compose-paid.yml    # Docker Compose configuration
├── AZURE_OPENAI_SETUP.md     # Detailed Azure OpenAI setup guide
├── QUICK_START_AZURE.md       # Quick start guide
└── README.md                  # This file
```

##  Commands

| Action | Command |
|--------|---------|
| **Start** | `docker-compose -f docker-compose-paid.yml up -d` |
| **Stop** | `docker-compose -f docker-compose-paid.yml down` |
| **View Logs** | `docker-compose -f docker-compose-paid.yml logs -f` |
| **Rebuild** | `docker-compose -f docker-compose-paid.yml up --build -d` |
| **Check Status** | `docker-compose -f docker-compose-paid.yml ps` |

## How It Works

1. **Document Indexing**: 
   - Documents are loaded from the specified path
   - Text is chunked into overlapping segments
   - Embeddings are generated using Azure OpenAI `text-embedding-3-large`
   - Chunks and embeddings are stored in ChromaDB

2. **Question Answering**:
   - User asks a question via the frontend or API
   - Question is embedded using the same Azure OpenAI model
   - Vector similarity search finds relevant document chunks
   - Context is passed to GPT-4o along with the question
   - GPT-4o generates an answer based on the retrieved context
   - Answer and sources are returned to the user

3. **Architecture**:
   - **Frontend**: Static HTML served by Python HTTP server
   - **Backend**: FastAPI server with RAG engine
   - **Vector DB**: ChromaDB for storing embeddings
   - **AI Models**: Azure OpenAI (GPT-4o + text-embedding-3-large)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AZURE_OPENAI_ENDPOINT` | Yes | - | Your Azure OpenAI endpoint URL |
| `AZURE_OPENAI_API_KEY` | Yes | - | Your Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | No | `gpt-4o` | Chat model deployment name |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | No | `text-embedding-3-large` | Embedding model deployment name |
| `AZURE_OPENAI_API_VERSION` | No | `2024-12-01-preview` | API version |
| `AZURE_OPENAI_MAX_TOKENS` | No | `4096` | Maximum tokens for responses |
| `AZURE_OPENAI_TEMPERATURE` | No | `1.0` | Temperature for generation |
| `AZURE_OPENAI_TOP_P` | No | `1.0` | Top-p sampling parameter |

## 📚 API Endpoints

### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "rag_engine": "initialized",
  "model_type": "azure_openai"
}
```

### `POST /api/ask`
Ask a question
```json
{
  "question": "What is the vacation policy?",
  "n_results": 3
}
```

Response:
```json
{
  "answer": "Based on the documents...",
  "sources": [
    {
      "content": "...",
      "source": "hr_handbook.txt",
      "score": 0.95
    }
  ],
  "model_type": "azure_openai"
}
```

### `POST /api/index`
Index documents
```json
{
  "documents_path": "../demo-data"
}
```

### `GET /api/stats`
Get indexing statistics
```json
{
  "total_documents": 24,
  "model_type": "azure_openai"
}
```

## Troubleshooting

### Azure OpenAI 403 Error
If you see `403 - Public access is disabled`:
- Go to Azure Portal → Your Azure OpenAI resource
- Navigate to **Networking**
- Enable **Public network access** or configure private endpoints
- Ensure your API key has proper permissions

### Documents Not Found
- Make sure documents are indexed: `POST /api/index`
- Check that the `documents_path` is correct
- Verify documents are in supported formats: `.txt`, `.md`, `.pdf`, `.docx`

### System Won't Start
- Check Docker is running: `docker --version`
- Check ports are available: 3000 and 8000
- View logs: `docker-compose -f docker-compose-paid.yml logs`

### API Not Responding
- Check backend logs: `docker logs ai-wiki-search-backend-paid-1`
- Test health endpoint: `curl http://localhost:8000/health`
- Verify Azure OpenAI credentials are set correctly

### Embedding Errors
- Verify the embedding deployment exists in Azure Portal
- Check that the deployment name matches `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`
- Ensure the embedding model is deployed and active

##  Documentation

- **[AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md)**: Detailed setup instructions for Azure OpenAI
- **[QUICK_START_AZURE.md](QUICK_START_AZURE.md)**: Quick start guide

## 🎯 Key Benefits

- **Accurate Answers**: RAG architecture ensures answers are based on your documents
- **Source Citations**: Every answer includes source references
- **Scalable**: Vector search handles large document collections efficiently
- **Easy Deployment**: Docker Compose for simple setup
- **Azure OpenAI**: Enterprise-grade AI with reliable performance

## 🔄 Development

### Running Locally (Without Docker)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Make sure to set environment variables in a `.env` file or export them:
```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-key"
```

### Adding New Documents

1. Place documents in the `demo-data/` folder (or your custom path)
2. Index them: `POST /api/index` with the correct path
3. Start asking questions!

## 📝 License

MIT License - Free to use for internal company use

## Success Metrics

This application demonstrates:
- ✅ RAG (Retrieval-Augmented Generation) architecture
- ✅ Azure OpenAI integration
- ✅ Vector search with ChromaDB
- ✅ Simple, reliable deployment
- ✅ Clean, modern interface
- ✅ Production-ready architecture

**Ready to use!** 🚀
