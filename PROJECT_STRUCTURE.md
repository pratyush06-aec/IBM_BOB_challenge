# GraphMind AI - Simplified Demo Structure

## Project Overview
A working prototype demonstrating the core GraphMind AI workflow with a sample e-commerce application graph.

## Directory Structure

```
graphmind-ai-demo/
├── frontend/                      # Next.js frontend
│   ├── app/                      # Next.js app directory
│   │   ├── page.tsx             # Main page with 3D graph
│   │   ├── layout.tsx           # Root layout
│   │   └── globals.css          # Global styles
│   ├── components/               # React components
│   │   ├── Graph3D.tsx          # 3D graph visualization
│   │   ├── NodeDetails.tsx      # Node details panel
│   │   ├── AIChat.tsx           # AI chat interface
│   │   └── WorkflowView.tsx     # Workflow visualization
│   ├── lib/                     # Utilities
│   │   ├── api.ts               # API client
│   │   └── types.ts             # TypeScript types
│   ├── data/                    # Mock data
│   │   └── sample-graph.json    # E-commerce graph data
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.js
│
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # Pydantic models
│   │   ├── ai_service.py        # IBM watsonx.ai integration
│   │   └── graph_service.py     # Graph operations
│   ├── data/
│   │   └── sample_graph.json    # Same graph data
│   ├── requirements.txt
│   └── .env.example
│
├── docs/                        # Documentation
│   ├── SETUP.md                # Setup instructions
│   └── DEMO_GUIDE.md           # Demo walkthrough
│
├── .gitignore
└── README_DEMO.md              # Demo-specific README
```

## Key Features

### 1. Sample E-Commerce Graph
- **Services**: Auth, Products, Cart, Payment, Orders
- **APIs**: Login, Register, GetProducts, AddToCart, Checkout
- **Functions**: ~30 functions showing realistic relationships
- **Databases**: Users DB, Products DB, Orders DB
- **Workflows**: User Registration, Product Purchase, Order Processing

### 2. 3D Visualization
- Interactive force-directed graph
- Color-coded nodes by type
- Clickable nodes for details
- Zoom, pan, rotate controls

### 3. AI Explanations
- Click any node to get AI explanation
- Natural language queries
- Workflow analysis
- Architecture insights

### 4. Workflow View
- Visual representation of key workflows
- Step-by-step execution flow
- Service dependencies

## Technology Stack (Simplified)

### Frontend
- Next.js 14 (App Router)
- React Three Fiber (3D visualization)
- TailwindCSS (styling)
- TypeScript

### Backend
- FastAPI (Python)
- IBM watsonx.ai (AI explanations)
- JSON file storage (no database needed)

## Setup Time
- **Installation**: ~5 minutes
- **First Run**: ~2 minutes
- **Total**: ~7 minutes to see it working

## Demo Flow

1. Start backend: `cd backend && python -m uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: `http://localhost:3000`
4. See 3D graph of e-commerce app
5. Click nodes to see AI explanations
6. Ask questions like "How does checkout work?"
7. View workflow visualizations

## Next Steps After Demo

If you want to extend this:
1. Add real repository parsing
2. Add Neo4j for graph storage
3. Add more AI agents
4. Add user authentication
5. Deploy to production