#!/bin/bash

# AI Wiki Search - Quick Version Switcher
# Simple bash script for quick switching

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to stop all services
stop_services() {
    print_info "Stopping all services..."
    
    # Stop all possible compose files
    for compose_file in docker-compose.yml docker-compose-free.yml docker-compose-paid.yml; do
        if [ -f "$compose_file" ]; then
            docker-compose -f "$compose_file" down 2>/dev/null || true
        fi
    done
    
    print_status "All services stopped"
}

# Function to start free version
start_free() {
    print_info "Starting FREE version (Local Models)..."
    
    # Check if docker-compose-free.yml exists
    if [ ! -f "docker-compose-free.yml" ]; then
        print_error "docker-compose-free.yml not found!"
        exit 1
    fi
    
    # Start the free version
    docker-compose -f docker-compose-free.yml up --build -d
    
    # Wait a bit for services to start
    sleep 5
    
    # Test the service
    if curl -s http://localhost:8000/health > /dev/null; then
        print_status "FREE version is running!"
        echo -e "${GREEN}💰 Cost: \$0.00 - Using local models!${NC}"
        echo -e "${BLUE}🌐 Frontend: http://localhost:3000${NC}"
        echo -e "${BLUE}🔧 Backend: http://localhost:8000/health${NC}"
    else
        print_error "Failed to start free version"
        exit 1
    fi
}

# Function to start paid version
start_paid() {
    print_info "Starting PAID version (OpenAI Models)..."
    
    # Check for OpenAI API key
    if [ -z "$OPENAI_API_KEY" ]; then
        print_warning "OPENAI_API_KEY not found in environment variables."
        echo "Please set your OpenAI API key:"
        echo "export OPENAI_API_KEY=your_key_here"
        exit 1
    fi
    
    # Check if docker-compose-paid.yml exists
    if [ ! -f "docker-compose-paid.yml" ]; then
        print_error "docker-compose-paid.yml not found!"
        exit 1
    fi
    
    # Start the paid version
    docker-compose -f docker-compose-paid.yml up --build -d
    
    # Wait a bit for services to start
    sleep 5
    
    # Test the service
    if curl -s http://localhost:8000/health > /dev/null; then
        print_status "PAID version is running!"
        echo -e "${YELLOW}💰 Cost: Uses OpenAI API (GPT-4 + embeddings)${NC}"
        echo -e "${BLUE}🌐 Frontend: http://localhost:3000${NC}"
        echo -e "${BLUE}🔧 Backend: http://localhost:8000/health${NC}"
    else
        print_error "Failed to start paid version"
        exit 1
    fi
}

# Function to show status
show_status() {
    echo "=================================================="
    echo "🧠 AI Wiki Search - Current Status"
    echo "=================================================="
    
    # Check running containers
    if docker ps --format "{{.Names}}" | grep -q "ai-wiki-search-backend-free-1"; then
        echo -e "${GREEN}✅ Currently running: FREE version${NC}"
        echo -e "${GREEN}💰 Cost: \$0.00 - Using local models${NC}"
        echo -e "${BLUE}🔧 Models: Sentence Transformers + Simple templates${NC}"
    elif docker ps --format "{{.Names}}" | grep -q "ai-wiki-search-backend-paid-1"; then
        echo -e "${YELLOW}✅ Currently running: PAID version${NC}"
        echo -e "${YELLOW}💰 Cost: Uses OpenAI API${NC}"
        echo -e "${BLUE}🔧 Models: GPT-4 + OpenAI embeddings${NC}"
    else
        echo -e "${RED}❌ No version currently running${NC}"
    fi
    
    echo -e "${BLUE}🌐 Frontend: http://localhost:3000${NC}"
    echo -e "${BLUE}🔧 Backend: http://localhost:8000/health${NC}"
}

# Main script logic
case "${1:-}" in
    "free")
        stop_services
        start_free
        echo ""
        echo -e "${BLUE}🎯 To switch to paid version: ./quick_switch.sh paid${NC}"
        ;;
    "paid")
        stop_services
        start_paid
        echo ""
        echo -e "${BLUE}🎯 To switch to free version: ./quick_switch.sh free${NC}"
        ;;
    "stop")
        stop_services
        ;;
    "status")
        show_status
        ;;
    *)
        echo "🧠 AI Wiki Search - Quick Version Switcher"
        echo "=========================================="
        echo "Usage:"
        echo "  ./quick_switch.sh free     # Switch to free version"
        echo "  ./quick_switch.sh paid     # Switch to paid version"
        echo "  ./quick_switch.sh status   # Show current status"
        echo "  ./quick_switch.sh stop     # Stop all services"
        echo ""
        echo "Examples:"
        echo "  ./quick_switch.sh free"
        echo "  ./quick_switch.sh paid"
        echo "  ./quick_switch.sh status"
        ;;
esac
