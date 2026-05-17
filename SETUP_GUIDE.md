# GraphMind AI - Setup Guide

## Quick Start Demo

This is a simplified demo of GraphMind AI showing the complete workflow with a sample e-commerce application.

---

## Prerequisites

- **Node.js**: 18.x or higher
- **Python**: 3.11 or higher
- **npm** or **yarn**
- **IBM watsonx.ai**: API credentials (already configured)

---

## Installation Steps

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify .env file exists with your credentials
# The file should already be configured with your IBM watsonx.ai credentials
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

---

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Backend will be available at**: `http://localhost:8000`  
**API Documentation**: `http://localhost:8000/docs`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
# or
yarn dev
```

You should see:
```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

**Frontend will be available at**: `http://localhost:3000`

---

## Using the Demo

### 1. View the 3D Graph

- Open `http://localhost:3000` in your browser
- You'll see an interactive 3D graph of the e-commerce system
- **Controls**:
  - 🖱️ **Click** on any node to see details
  - 🔄 **Drag** to rotate the graph
  - 🔍 **Scroll** to zoom in/out
  - 🎯 **Right-click + drag** to pan

### 2. Explore Nodes

- Click on any node (Service, API, Function, Database, etc.)
- The left panel will show:
  - Node type and properties
  - AI-generated explanation (powered by IBM watsonx.ai)
  - Connections and relationships

### 3. Ask AI Questions

- Use the AI Chat panel on the right
- Try these example questions:
  - "How does authentication work?"
  - "Explain the checkout process"
  - "What happens if the database fails?"
  - "Show me the payment workflow"

### 4. View Workflows

- Click the "Show Workflows" button in the header
- Explore predefined workflows:
  - **User Registration**: Complete signup flow
  - **Product Purchase**: End-to-end purchase process
- Each workflow shows step-by-step execution with visual flow

---

## Sample E-Commerce System

The demo includes a realistic e-commerce application with:

### Services
- **Auth Service**: User authentication and authorization
- **Products Service**: Product catalog management
- **Cart Service**: Shopping cart operations
- **Payment Service**: Payment processing
- **Orders Service**: Order management

### APIs
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /products` - Get products
- `POST /cart/add` - Add to cart
- `POST /cart/checkout` - Checkout

### Databases
- **Users DB**: User accounts and sessions
- **Products DB**: Product catalog and inventory
- **Orders DB**: Orders and transactions

### Workflows
1. **User Registration Flow**
2. **Product Purchase Flow**

---

## API Endpoints

### Backend API

#### Get Graph Data
```bash
GET http://localhost:8000/api/graph
```

#### Get Node Details
```bash
GET http://localhost:8000/api/graph/node/{node_id}
```

#### AI Explain Node
```bash
POST http://localhost:8000/api/ai/explain
Content-Type: application/json

{
  "node_id": "func_authenticate",
  "context": "optional context"
}
```

#### AI Query
```bash
POST http://localhost:8000/api/ai/query
Content-Type: application/json

{
  "query": "How does authentication work?"
}
```

#### Get Workflows
```bash
GET http://localhost:8000/api/workflows
```

#### Get Workflow Details
```bash
GET http://localhost:8000/api/workflow/{workflow_id}
```

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'ibm_watsonx_ai'`  
**Solution**: Make sure you installed all dependencies:
```bash
pip install -r requirements.txt
```

**Problem**: `Error loading graph data`  
**Solution**: Verify `sample_graph.json` exists in `backend/data/` directory

**Problem**: IBM watsonx.ai authentication error  
**Solution**: Check your `.env` file has correct credentials:
```
WATSONX_API_KEY=your_key_here
WATSONX_PROJECT_ID=your_project_id_here
```

### Frontend Issues

**Problem**: `Cannot find module 'react'`  
**Solution**: Install dependencies:
```bash
npm install
```

**Problem**: Graph not loading  
**Solution**: 
1. Check backend is running on port 8000
2. Check browser console for CORS errors
3. Verify API endpoint in browser: `http://localhost:8000/api/graph`

**Problem**: 3D graph not rendering  
**Solution**: 
1. Try a different browser (Chrome recommended)
2. Check browser console for WebGL errors
3. Update your graphics drivers

### CORS Issues

If you see CORS errors in the browser console:
1. Verify backend is running
2. Check `backend/app/main.py` has correct CORS configuration
3. Try accessing from `http://localhost:3000` (not `127.0.0.1`)

---

## Project Structure

```
graphmind-ai-demo/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── ai_service.py        # IBM watsonx.ai integration
│   │   └── graph_service.py     # Graph operations
│   ├── data/
│   │   └── sample_graph.json    # E-commerce graph data
│   ├── requirements.txt
│   └── .env                     # Environment variables
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main page
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── Graph3D.tsx         # 3D graph visualization
│   │   ├── NodeDetails.tsx     # Node details panel
│   │   ├── AIChat.tsx          # AI chat interface
│   │   └── WorkflowView.tsx    # Workflow visualization
│   └── package.json
│
└── sample-graph.json           # Graph data (root copy)
```

---

## Features Demonstrated

### ✅ Implemented
- [x] 3D interactive graph visualization
- [x] Sample e-commerce system graph
- [x] Node details with properties
- [x] AI-powered explanations (IBM watsonx.ai)
- [x] Natural language queries
- [x] Workflow visualization
- [x] Real-time AI responses
- [x] Responsive UI

### 🚧 Future Enhancements
- [ ] Real repository parsing
- [ ] Neo4j graph database
- [ ] User authentication
- [ ] Multiple repository support
- [ ] Advanced graph analytics
- [ ] Export functionality
- [ ] Collaboration features

---

## Technology Stack

### Frontend
- **Next.js 14**: React framework
- **React Three Fiber**: 3D rendering
- **ForceGraph3D**: Graph visualization
- **TailwindCSS**: Styling
- **Framer Motion**: Animations
- **TypeScript**: Type safety

### Backend
- **FastAPI**: Python web framework
- **IBM watsonx.ai**: AI explanations
- **Python 3.11+**: Backend language

### AI
- **IBM watsonx.ai**: LLM for explanations
- **Granite 13B Chat**: Model for responses

---

## Performance Tips

1. **Graph Performance**: The 3D graph performs best with < 1000 nodes
2. **AI Responses**: First AI query may take 3-5 seconds (model initialization)
3. **Browser**: Chrome or Edge recommended for best WebGL performance
4. **Memory**: Close other tabs if graph rendering is slow

---

## Next Steps

After exploring the demo:

1. **Modify the Graph**: Edit `sample-graph.json` to add your own nodes/edges
2. **Customize AI Prompts**: Edit `backend/app/ai_service.py` to change AI behavior
3. **Add New Workflows**: Add workflows to the JSON file
4. **Extend Features**: Add new components or API endpoints

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API documentation at `http://localhost:8000/docs`
3. Check browser console for errors
4. Verify all dependencies are installed

---

## Demo Walkthrough

### Recommended Demo Flow

1. **Start**: Open `http://localhost:3000`
2. **Explore Graph**: Rotate and zoom the 3D graph
3. **Click Service**: Click on "Auth Service" node
4. **Read AI Explanation**: See IBM watsonx.ai explanation
5. **Ask Question**: Type "How does authentication work?" in AI chat
6. **View Workflow**: Click "Show Workflows" button
7. **Explore Workflow**: Select "Product Purchase" workflow
8. **Return to Graph**: Click "Show Graph" to return

---

## Estimated Time

- **Setup**: 5-10 minutes
- **First Run**: 2-3 minutes
- **Demo Walkthrough**: 5-10 minutes
- **Total**: ~15-20 minutes

---

**Enjoy exploring GraphMind AI! 🚀**