# 🔧 GraphMind AI - Debugging Guide

## 📋 Current Issue: Backend Server Won't Start

### Problem
```
ModuleNotFoundError: No module named 'ibm_watsonx_ai'
```

### Root Cause
The IBM watsonx.ai SDK was not properly installed. This is a large package (~200MB) with many dependencies.

### Solution Steps

#### Step 1: Stop All Running Servers
```bash
# Press CTRL+C in all terminal windows
# Or close all terminals
```

#### Step 2: Clean Install Dependencies
```bash
cd backend
pip install --upgrade pip
pip install --no-cache-dir ibm-watsonx-ai==0.2.6
pip install -r requirements.txt
```

#### Step 3: Verify Installation
```bash
python test_install.py
```

Expected output:
```
SDK installed successfully
```

#### Step 4: Start Backend Server
```bash
python -m uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## 🎯 Common Issues and Solutions

### Issue 1: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

### Issue 2: Python Version Mismatch

**Error:**
```
SyntaxError: invalid syntax
```

**Solution:**
```bash
# Check Python version (must be 3.9+)
python --version

# If version is wrong, install Python 3.9+ from python.org
```

### Issue 3: Missing Environment Variables

**Error:**
```
KeyError: 'WATSONX_API_KEY'
```

**Solution:**
```bash
# Check if .env file exists
cd backend
dir .env

# If missing, copy from example
copy .env.example .env

# Edit .env and add your credentials
notepad .env
```

### Issue 4: Network/Firewall Issues

**Error:**
```
ConnectionError: Failed to establish connection
```

**Solution:**
1. Check internet connection
2. Disable VPN temporarily
3. Check firewall settings
4. Try using a different network

### Issue 5: Dependency Conflicts

**Error:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Solution:**
```bash
# Create a fresh virtual environment
python -m venv venv_new
venv_new\Scripts\activate
pip install -r requirements.txt
```

## 🧪 Testing Checklist

### Backend Health Check
```bash
# Test 1: Check if server is running
curl http://localhost:8000/health

# Expected: {"status": "healthy"}

# Test 2: Get graph data
curl http://localhost:8000/api/graph

# Expected: JSON with nodes and edges

# Test 3: Test AI explanation
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"node_id": "auth-service"}'

# Expected: JSON with AI-generated explanation
```

### Frontend Health Check
```bash
# Test 1: Check if server is running
curl http://localhost:3000

# Expected: HTML response

# Test 2: Check API connection
# Open browser console at http://localhost:3000
# Should see: "Graph data loaded successfully"
```

## 🔍 Debugging Tools

### 1. Check Python Environment
```bash
# Show installed packages
pip list

# Show package details
pip show ibm-watsonx-ai

# Check Python path
python -c "import sys; print(sys.executable)"
```

### 2. Check Node Environment
```bash
# Show Node version
node --version

# Show npm version
npm --version

# Show installed packages
npm list --depth=0
```

### 3. Check Running Processes
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Show all Python processes
tasklist | findstr python
```

### 4. View Logs
```bash
# Backend logs are in terminal output
# Look for:
# - "Application startup complete" (success)
# - "ModuleNotFoundError" (missing dependency)
# - "Address already in use" (port conflict)

# Frontend logs are in browser console (F12)
# Look for:
# - Network errors (API connection issues)
# - CORS errors (backend not running)
# - 404 errors (wrong API endpoint)
```

## 🚨 Emergency Reset

If nothing works, perform a complete reset:

```bash
# 1. Stop all servers (CTRL+C)

# 2. Delete all dependencies
cd backend
rmdir /s /q venv
cd ../frontend
rmdir /s /q node_modules

# 3. Reinstall everything
cd ../backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cd ../frontend
npm install

# 4. Restart servers
cd ../backend
python -m uvicorn app.main:app --reload

# In new terminal
cd frontend
npm run dev
```

## 📊 System Requirements

### Minimum Requirements
- Python 3.9+
- Node.js 18+
- 4GB RAM
- 2GB free disk space
- Internet connection

### Recommended Requirements
- Python 3.11+
- Node.js 20+
- 8GB RAM
- 5GB free disk space
- Fast internet connection

## 🆘 Getting Help

### Before Asking for Help

1. Check this debugging guide
2. Review error messages carefully
3. Check `TROUBLESHOOTING.md`
4. Verify system requirements
5. Try the emergency reset

### When Asking for Help

Include:
1. Full error message
2. Python version (`python --version`)
3. Node version (`node --version`)
4. Operating system
5. Steps you've already tried
6. Terminal output (last 50 lines)

### Useful Commands for Diagnostics

```bash
# System info
python --version
node --version
pip --version
npm --version

# Package info
pip list > installed_packages.txt
npm list --depth=0 > npm_packages.txt

# Environment info
echo %PATH%
echo %PYTHONPATH%
```

## ✅ Success Indicators

You'll know everything is working when:

1. **Backend:**
   - ✅ No errors in terminal
   - ✅ Shows "Application startup complete"
   - ✅ http://localhost:8000/health returns `{"status": "healthy"}`
   - ✅ http://localhost:8000/docs shows API documentation

2. **Frontend:**
   - ✅ No errors in terminal
   - ✅ Shows "Ready in X ms"
   - ✅ http://localhost:3000 loads the application
   - ✅ 3D graph is visible
   - ✅ Clicking nodes shows details

3. **Integration:**
   - ✅ Clicking nodes shows AI explanations
   - ✅ Chat responds to queries
   - ✅ Workflows are visible
   - ✅ No CORS errors in browser console

---

**Remember:** Most issues are due to missing dependencies or port conflicts. Always check these first!