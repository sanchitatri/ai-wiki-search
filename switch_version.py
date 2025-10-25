#!/usr/bin/env python3
"""
AI Wiki Search - Version Switcher
Switch between free (local models) and paid (OpenAI) versions
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_docker():
    """Check if Docker is running"""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Docker or Docker Compose not found. Please install Docker first.")
        return False

def get_current_version():
    """Determine current version based on running containers"""
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        containers = result.stdout.strip().split('\n')
        
        if 'ai-wiki-search-backend-free-1' in containers:
            return 'free'
        elif 'ai-wiki-search-backend-paid-1' in containers:
            return 'paid'
        elif 'ai-wiki-search-backend-1' in containers:
            return 'demo'
        else:
            return 'none'
    except:
        return 'none'

def stop_current_services():
    """Stop all current services"""
    print("🛑 Stopping current services...")
    
    # Try to stop all possible compose files
    compose_files = ['docker-compose.yml', 'docker-compose-free.yml', 'docker-compose-paid.yml']
    
    for compose_file in compose_files:
        if os.path.exists(compose_file):
            run_command(f"docker-compose -f {compose_file} down", f"Stopping {compose_file}")

def start_free_version():
    """Start the free version"""
    print("🚀 Starting FREE version (Local Models)...")
    
    if not run_command("docker-compose -f docker-compose-free.yml up --build -d", "Starting free version"):
        return False
    
    print("⏳ Waiting for services to start...")
    time.sleep(10)
    
    # Test the service
    if test_service():
        print("🎉 FREE version is now running!")
        print("💰 Cost: $0.00 - Using local models!")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000/health")
        return True
    else:
        print("❌ Free version failed to start properly")
        return False

def start_paid_version():
    """Start the paid version"""
    print("🚀 Starting PAID version (Google Gemini)...")
    
    # Check for Gemini API key
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not found in environment variables.")
        print("Please set your Google Gemini API key:")
        print("export GEMINI_API_KEY=your_key_here")
        return False
    
    if not run_command("docker-compose -f docker-compose-paid.yml up --build -d", "Starting paid version"):
        return False
    
    print("⏳ Waiting for services to start...")
    time.sleep(10)
    
    # Test the service
    if test_service():
        print("🎉 PAID version is now running!")
        print("💠 Uses Google Gemini (gemini-1.5-pro + text-embedding-004)")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000/health")
        return True
    else:
        print("❌ Paid version failed to start properly")
        return False

def start_demo_version():
    """Start the demo version"""
    print("🚀 Starting DEMO version (Simple Demo Responses)...")
    
    if not run_command("docker-compose up --build -d", "Starting demo version"):
        return False
    
    print("⏳ Waiting for services to start...")
    time.sleep(5)
    
    # Test the service
    if test_service():
        print("🎉 DEMO version is now running!")
        print("💰 Cost: $0.00 - Using demo responses")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000/health")
        return True
    else:
        print("❌ Demo version failed to start properly")
        return False

def test_service():
    """Test if the service is responding"""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8000/health"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def show_status():
    """Show current status"""
    current = get_current_version()
    
    print("=" * 50)
    print("🧠 AI Wiki Search - Current Status")
    print("=" * 50)
    
    if current == 'free':
        print("✅ Currently running: FREE version")
        print("💰 Cost: $0.00 - Using local models")
        print("🔧 Models: Sentence Transformers + Simple templates")
    elif current == 'paid':
        print("✅ Currently running: PAID version")
        print("💠 Uses Google Gemini")
        print("🔧 Models: gemini-1.5-pro + text-embedding-004")
    elif current == 'demo':
        print("✅ Currently running: DEMO version")
        print("💰 Cost: $0.00 - Using demo responses")
        print("🔧 Models: Simple demo responses")
    else:
        print("❌ No version currently running")
    
    print(f"🌐 Frontend: http://localhost:3000")
    print(f"🔧 Backend: http://localhost:8000/health")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🧠 AI Wiki Search - Version Switcher")
        print("=" * 40)
        print("Usage:")
        print("  python switch_version.py free     # Switch to free version")
        print("  python switch_version.py paid     # Switch to paid version")
        print("  python switch_version.py demo     # Switch to demo version")
        print("  python switch_version.py status   # Show current status")
        print("  python switch_version.py stop     # Stop all services")
        return
    
    command = sys.argv[1].lower()
    
    if not check_docker():
        return
    
    if command == 'status':
        show_status()
        return
    
    if command == 'stop':
        stop_current_services()
        print("✅ All services stopped")
        return
    
    if command == 'free':
        stop_current_services()
        if start_free_version():
            print("\n🎯 To switch to paid version: python switch_version.py paid")
        return
    
    if command == 'paid':
        stop_current_services()
        if start_paid_version():
            print("\n🎯 To switch to free version: python switch_version.py free")
        return
    
    if command == 'demo':
        stop_current_services()
        if start_demo_version():
            print("\n🎯 To switch to free version: python switch_version.py free")
            print("🎯 To switch to paid version: python switch_version.py paid")
        return
    
    print("❌ Invalid command. Use: free, paid, status, or stop")

if __name__ == "__main__":
    main()
