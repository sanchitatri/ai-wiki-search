# 🔄 AI Wiki Search - Version Switching Guide

## 🎯 Overview

This guide explains how to switch between the FREE and PAID versions of the AI Wiki Search system.

## 🛠️ Available Switching Methods

### 1. Python Script (Recommended)
- **File**: `switch_version.py`
- **Cross-platform**: Works on Windows, Mac, Linux
- **Features**: Status checking, error handling, automatic testing

### 2. Bash Script (Linux/Mac)
- **File**: `quick_switch.sh`
- **Platform**: Linux, Mac, WSL
- **Features**: Colored output, simple commands

### 3. Manual Docker Commands
- **Method**: Direct docker-compose commands
- **Platform**: Any Docker environment
- **Features**: Full control, manual process

## 🚀 Quick Start

### Method 1: Python Script (Recommended)

```bash
# Check current status
python switch_version.py status

# Switch to FREE version (local models)
python switch_version.py free

# Switch to PAID version (OpenAI models)
python switch_version.py paid

# Stop all services
python switch_version.py stop
```

### Method 2: Bash Script (Linux/Mac)

```bash
# Make script executable (first time only)
chmod +x quick_switch.sh

# Check current status
./quick_switch.sh status

# Switch to FREE version
./quick_switch.sh free

# Switch to PAID version
./quick_switch.sh paid

# Stop all services
./quick_switch.sh stop
```

### Method 3: Manual Docker Commands

```bash
# Stop current services
docker-compose -f docker-compose-free.yml down
docker-compose -f docker-compose-paid.yml down

# Start FREE version
docker-compose -f docker-compose-free.yml up --build -d

# Start PAID version
docker-compose -f docker-compose-paid.yml up --build -d
```

## 📋 Step-by-Step Instructions

### Switching to FREE Version

1. **Check current status**:
   ```bash
   python switch_version.py status
   ```

2. **Switch to free version**:
   ```bash
   python switch_version.py free
   ```

3. **Wait for startup** (about 10-15 seconds)

4. **Test the service**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/health

### Switching to PAID Version

1. **Set OpenAI API key**:
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

2. **Switch to paid version**:
   ```bash
   python switch_version.py paid
   ```

3. **Wait for startup** (about 10-15 seconds)

4. **Test the service**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/health

## 🔍 Understanding the Switch Process

### What Happens During a Switch:

1. **Stop Current Services**: All running containers are stopped
2. **Clean Up**: Orphaned containers are removed
3. **Build New Images**: Fresh Docker images are built
4. **Start New Services**: New version containers are started
5. **Health Check**: Service is tested to ensure it's working
6. **Status Report**: Current version and URLs are displayed

### Docker Compose Files:

- **FREE Version**: `docker-compose-free.yml`
  - Uses `backend/Dockerfile.free`
  - Runs `main_free.py`
  - No API keys required

- **PAID Version**: `docker-compose-paid.yml`
  - Uses `backend/Dockerfile.paid`
  - Runs `main.py`
  - Requires `OPENAI_API_KEY`

## 🧪 Testing Your Switch

### Health Check Commands:

```bash
# Check if backend is responding
curl http://localhost:8000/health

# Check if frontend is responding
curl http://localhost:3000

# Check running containers
docker ps
```

### Expected Responses:

**FREE Version Health Check**:
```json
{
  "status": "healthy",
  "rag_engine": "initialized",
  "model_type": "free_local_models"
}
```

**PAID Version Health Check**:
```json
{
  "status": "healthy",
  "rag_engine": "initialized",
  "model_type": "paid_openai_models"
}
```

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Port Already in Use
```bash
# Error: Bind for 0.0.0.0:8000 failed: port is already allocated
# Solution: Stop all services first
python switch_version.py stop
```

#### 2. Docker Not Running
```bash
# Error: Docker not found
# Solution: Start Docker Desktop or Docker daemon
```

#### 3. OpenAI API Key Missing (Paid Version)
```bash
# Error: OPENAI_API_KEY not found
# Solution: Set environment variable
export OPENAI_API_KEY=your_key_here
```

#### 4. Permission Denied (Bash Script)
```bash
# Error: Permission denied
# Solution: Make script executable
chmod +x quick_switch.sh
```

#### 5. Build Failures
```bash
# Error: Build failed
# Solution: Clean up and retry
docker system prune -f
python switch_version.py free
```

### Debug Commands:

```bash
# View container logs
docker logs ai-wiki-search-backend-free-1
docker logs ai-wiki-search-backend-paid-1
docker logs ai-wiki-search-frontend-1

# Check container status
docker ps -a

# View Docker Compose logs
docker-compose -f docker-compose-free.yml logs
docker-compose -f docker-compose-paid.yml logs
```

## 🔄 Switching Best Practices

### 1. Always Check Status First
```bash
python switch_version.py status
```

### 2. Stop Before Switching
The scripts automatically stop services, but you can manually stop if needed:
```bash
python switch_version.py stop
```

### 3. Wait for Startup
Give services 10-15 seconds to fully start before testing.

### 4. Test After Switch
Always test the service after switching:
- Check health endpoint
- Try a sample question
- Verify frontend loads

### 5. Monitor Resources
- FREE version: Uses more local memory
- PAID version: Uses network bandwidth

## 📊 Version Comparison

| Aspect | FREE Version | PAID Version |
|--------|-------------|--------------|
| **Startup Time** | ~30 seconds | ~15 seconds |
| **Memory Usage** | Higher (local models) | Lower (API calls) |
| **Network Usage** | None | API calls |
| **Response Quality** | Basic | High |
| **Cost** | $0 | API costs |

## 🎯 Quick Reference

### Commands Summary:
```bash
# Status and control
python switch_version.py status    # Check current version
python switch_version.py stop      # Stop all services

# Version switching
python switch_version.py free      # Switch to free version
python switch_version.py paid      # Switch to paid version

# Alternative (Linux/Mac)
./quick_switch.sh status           # Check status
./quick_switch.sh free             # Switch to free
./quick_switch.sh paid             # Switch to paid
./quick_switch.sh stop             # Stop all
```

### URLs:
- **Frontend**: http://localhost:3000
- **Backend Health**: http://localhost:8000/health
- **Backend API**: http://localhost:8000/api/ask

### Environment Variables:
```bash
# For paid version only
export OPENAI_API_KEY=your_key_here
```

## 🆘 Getting Help

If you encounter issues:

1. **Check the status**: `python switch_version.py status`
2. **Review logs**: `docker logs ai-wiki-search-backend-free-1`
3. **Try stopping and restarting**: `python switch_version.py stop`
4. **Check Docker**: Ensure Docker is running
5. **Verify ports**: Ensure ports 3000 and 8000 are available

**Happy switching! 🔄**
