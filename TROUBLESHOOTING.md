# GraphMind AI - Troubleshooting Guide

## Common Issues and Solutions

### 1. Backend Won't Start - Missing Modules

**Error:**
```
ModuleNotFoundError: No module named 'ibm_watsonx_ai'
```

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

**Why it happens:** Python dependencies need to be installed before running the server.

**Time required:** 2-5 minutes depending on internet speed

---

### 2. Installation Taking Long Time

**What's happening:**
- IBM watsonx.ai SDK is a large package (~200MB)
- Pandas is also large (~100MB)
- Total installation: 2-5 minutes

**This is normal!** Just wait for it to complete.

**Progress indicators:**
- You'll see "Installing build dependencies"
- Then "Getting requirements to build wheel"
- Finally "Successfully installed..."

---

### 3. Python Version Issues

**Check your Python version:**
```bash
python --version
```

**Required:** Python 3.11 or higher
**Your version:** Python 3.13.7 ✅ (Perfect!)

---

### 4. Port Already in Use

**Error:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Solution:**
```bash
# Use a different port
python -m uvicorn app.main:app --reload --port 8001
```

Or kill the process using port 8000:
```bash
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

---

### 5. IBM watsonx.ai Authentication Error

**Error:**
```
401 Unauthorized
```

**Solution:**
1. Check your `.env` file exists in `backend/` directory
2. Verify credentials are correct:
```env
WATSONX_API_KEY=your_key_here
WATSONX_PROJECT_ID=your_project_id_here
```

3. Test credentials:
```bash
cd backend
python -c "from app.ai_service import AIService; ai = AIService(); print('✅ Credentials valid!')"
```

---

### 6. CORS Errors in Browser

**Error in browser console:**
```
Access to fetch at 'http://localhost:8000/api/graph' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
1. Make sure backend is running
2. Check `backend/app/main.py` has CORS configured:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 7. Frontend Won't Start

**Error:**
```
Cannot find module 'react'
```

**Solution:**
```bash
cd frontend
npm install
# or
yarn install
```

**Time required:** 1-2 minutes

---

### 8. 3D Graph Not Rendering

**Symptoms:**
- Black screen
- No graph visible
- Console errors about WebGL

**Solutions:**

1. **Update browser** (Chrome recommended)
2. **Enable hardware acceleration:**
   - Chrome: Settings → System → Use hardware acceleration
3. **Update graphics drivers**
4. **Try different browser**

---

### 9. Slow Graph Performance

**If graph is laggy:**

1. **Reduce node count** in `sample-graph.json`
2. **Close other tabs** to free memory
3. **Use Chrome** (best WebGL performance)
4. **Check CPU usage** (should be < 50%)

---

### 10. Backend Starts But API Returns Errors

**Test the API:**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test graph endpoint
curl http://localhost:8000/api/graph
```

**Expected response:**
```json
{
  "nodes": [...],
  "edges": [...],
  "metadata": {...}
}
```

**If you get errors:**
1. Check `backend/data/sample_graph.json` exists
2. Check file permissions
3. Look at backend terminal for error messages

---

## Step-by-Step Debugging Process

### When Backend Won't Start:

1. **Check Python version:**
   ```bash
   python --version
   ```
   Should be 3.11+

2. **Check if dependencies installed:**
   ```bash
   cd backend
   pip list | findstr fastapi
   pip list | findstr ibm-watsonx-ai
   ```

3. **Try installing one package at a time:**
   ```bash
   pip install fastapi
   pip install uvicorn
   pip install ibm-watsonx-ai
   ```

4. **Check for error messages:**
   - Read the full error output
   - Look for the actual error (usually at the bottom)
   - Google the specific error if needed

5. **Test imports:**
   ```bash
   python -c "import fastapi; print('✅ FastAPI works')"
   python -c "from ibm_watsonx_ai.foundation_models import Model; print('✅ IBM SDK works')"
   ```

---

## Getting Help

### Information to Provide:

1. **Python version:** `python --version`
2. **Operating System:** Windows/Mac/Linux
3. **Error message:** Full error output
4. **What you tried:** Steps you've already taken
5. **Terminal output:** Copy the full terminal output

### Useful Commands:

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check if port is in use
netstat -ano | findstr :8000

# Test backend manually
cd backend
python -c "from app.main import app; print('✅ App loads successfully')"

# Check environment variables
cd backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('WATSONX_API_KEY')[:10] + '...')"
```

---

## Quick Fixes Checklist

Before asking for help, try these:

- [ ] Installed all dependencies (`pip install -r requirements.txt`)
- [ ] Python version is 3.11 or higher
- [ ] `.env` file exists in `backend/` directory
- [ ] Backend terminal shows no errors
- [ ] Port 8000 is not in use
- [ ] Tried restarting both backend and frontend
- [ ] Checked browser console for errors
- [ ] Tried a different browser (Chrome recommended)
- [ ] Cleared browser cache
- [ ] Restarted VS Code / terminal

---

## Still Having Issues?

### Create a Debug Report:

```bash
# Run this in backend directory
python -c "
import sys
print('Python:', sys.version)
print('Platform:', sys.platform)

try:
    import fastapi
    print('✅ FastAPI installed')
except:
    print('❌ FastAPI not installed')

try:
    from ibm_watsonx_ai.foundation_models import Model
    print('✅ IBM SDK installed')
except Exception as e:
    print('❌ IBM SDK error:', e)

import os
from dotenv import load_dotenv
load_dotenv()
print('✅ API Key configured' if os.getenv('WATSONX_API_KEY') else '❌ API Key missing')
"
```

Share the output of this script when asking for help.

---

## Success Indicators

### Backend Running Successfully:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Frontend Running Successfully:
```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

### API Working:
- Visit `http://localhost:8000/docs` - Should show API documentation
- Visit `http://localhost:8000/health` - Should return `{"status": "healthy"}`

---

**Remember:** Most issues are solved by:
1. Installing dependencies properly
2. Checking environment variables
3. Restarting the servers
4. Reading error messages carefully

Good luck! 🚀