# 🚀 GraphMind AI - Quick Start Guide

## Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed
- Internet connection for dependencies

## 🎯 One-Command Startup

### Option 1: Using Startup Scripts (Recommended)

**Start Backend:**
```bash
start-backend.bat
```

**Start Frontend (in a new terminal):**
```bash
start-frontend.bat
```

### Option 2: Manual Startup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Access the Application

Once both servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎮 Demo Features

### 1. 3D Graph Visualization
- **Drag nodes** to reposition them
- **Zoom** with mouse wheel
- **Rotate** by clicking and dragging
- **Click nodes** to see details and AI explanations

### 2. AI Chat Interface
Try these queries:
- "Explain the authentication flow"
- "What services depend on Redis?"
- "Show me the payment workflow"
- "What happens if AuthService fails?"

### 3. Workflow Visualization
- Click "Workflows" tab
- Select a workflow (User Registration or Order Processing)
- See step-by-step execution flow

### 4. Node Details Panel
- Click any node in the graph
- View node properties
- Get AI-generated explanations
- See connected nodes

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
```bash
# Backend (port 8000)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (port 3000)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

## 📊 Sample Data

The demo includes a pre-built e-commerce system graph:

**Services:**
- AuthService
- ProductService
- CartService
- PaymentService
- OrderService

**Infrastructure:**
- PostgreSQL
- Redis
- RabbitMQ

**Workflows:**
- User Registration Flow
- Order Processing Flow

## 🎓 Learning Path

1. **Start with the graph** - Explore the 3D visualization
2. **Click nodes** - Understand individual components
3. **Ask AI questions** - Get contextual explanations
4. **View workflows** - See how services interact
5. **Experiment** - Try different queries and interactions

## 📝 Next Steps

After exploring the demo:
1. Review the code in `backend/app/` and `frontend/app/`
2. Modify `backend/data/sample_graph.json` to add your own data
3. Extend the AI prompts in `backend/app/ai_service.py`
4. Customize the 3D visualization in `frontend/components/Graph3D.tsx`

## 🆘 Need Help?

Check these files:
- `TROUBLESHOOTING.md` - Common issues and solutions
- `DEMO_SUMMARY.md` - Complete project overview
- `PROJECT_STRUCTURE.md` - Code organization

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Backend shows "Application startup complete"
- ✅ Frontend shows "Ready in X ms"
- ✅ Browser displays 3D graph at localhost:3000
- ✅ Clicking nodes shows AI explanations
- ✅ Chat responds to queries

---

**Enjoy exploring GraphMind AI! 🚀**