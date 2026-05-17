"""
Simple startup script for GraphMind AI backend
Handles import issues and starts the server
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        import uvicorn
        
        print("=" * 60)
        print("GraphMind AI Backend Server")
        print("=" * 60)
        print("Starting server on http://localhost:8000")
        print("API Documentation: http://localhost:8000/docs")
        print("=" * 60)
        
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
        
    except ImportError as e:
        print(f"\n[ERROR] Import Error: {e}")
        print("\n[INFO] Missing dependencies. Please install:")
        print("   pip install fastapi uvicorn python-jose passlib bcrypt")
        print("\nFor full features, install all dependencies:")
        print("   pip install -r requirements-minimal.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n[ERROR] Error starting server: {e}")
        print("\nPlease check:")
        print("1. All dependencies are installed")
        print("2. .env file is configured")
        print("3. Port 8000 is available")
        sys.exit(1)

# Made with Bob
