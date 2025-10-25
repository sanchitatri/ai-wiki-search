# 🧠 AI Internal Wiki Search

A simple AI-powered internal knowledge search system that allows employees to ask natural language questions and get instant answers from company documents.

## 🎯 Overview

This application provides a clean, simple interface for searching company knowledge. Employees can ask questions in plain English and get instant answers with source citations.

## ✨ Features

- **Natural Language Queries**: Ask questions in plain English
- **Instant Answers**: Get immediate responses with source citations
- **Simple Interface**: Clean, modern web interface
- **Docker Ready**: Easy deployment with Docker Compose
- **No Caching Issues**: Reliable refresh behavior

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation Steps

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-wiki-search
```

#### 2. Start the System

```bash
# Start both frontend and backend
docker-compose up -d

# Check status
docker ps
```

#### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/health

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
# Test the /api/ask endpoint
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is our vacation policy?", "n_results": 5}'

# Health check
curl http://localhost:8000/health
```

## 📁 Project Structure

```
ai-wiki-search/
├── backend/                    # Python backend
│   ├── main_simple.py         # Simple FastAPI application
│   ├── Dockerfile.simple      # Backend Docker configuration
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
│   └── developer_guide.md     # Developer documentation
│
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## 🛠️ Commands

| Action | Command |
|--------|---------|
| **Start** | `docker-compose up -d` |
| **Stop** | `docker-compose down` |
| **View Logs** | `docker logs ai-wiki-search-frontend-1` |
| **Check Status** | `docker ps` |

## 🔧 How It Works

1. **Frontend**: Static HTML served by Python HTTP server with no-cache headers
2. **Backend**: Simple FastAPI server with demo responses
3. **No React**: Eliminates caching and refresh issues
4. **Docker**: Easy deployment and management

## 🎯 Key Benefits

- **No Caching Issues**: Normal refresh (F5) works perfectly
- **Simple Setup**: Just run `docker-compose up -d`
- **Reliable**: Static HTML with proper cache headers
- **Fast**: No complex build processes
- **Demo Ready**: Works out of the box

## 🆘 Troubleshooting

### System won't start
- Check Docker is running: `docker --version`
- Check ports are available: 3000 and 8000
- View logs: `docker logs ai-wiki-search-frontend-1`

### Blank page on refresh
- This system eliminates refresh issues with static HTML
- If you see blank pages, check browser console for errors

### API not responding
- Check backend logs: `docker logs ai-wiki-search-backend-simple-1`
- Test health endpoint: `curl http://localhost:8000/health`

## 📝 License

MIT License - Free to use for internal company use

## 🎉 Success Metrics

This application demonstrates:
- ✅ Simple, reliable architecture
- ✅ No caching or refresh issues
- ✅ Easy deployment with Docker
- ✅ Clean, modern interface
- ✅ Working demo with sample data

**Ready to use!** 🚀