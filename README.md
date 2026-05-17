<div align="center">
  <img src="assets/logo.png" alt="GraphMind AI Logo" width="250" />
  <h1>GraphMind AI</h1>
  <p><strong>AI-Native Engineering Cognition Platform</strong></p>
  <p>Transform repositories into interactive 3D semantic intelligence graphs.</p>

  <br />

  <a href="https://graphmind-ai-kappa.vercel.app/">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Vercel-000000?style=for-the-badge&logo=vercel" alt="Live Demo" />
  </a>
  &nbsp;
  <a href="https://ibm-bob-challenge.onrender.com/docs">
    <img src="https://img.shields.io/badge/📡_API_Docs-Render-4353FF?style=for-the-badge&logo=render" alt="API Docs" />
  </a>

  <br /><br />

  <img src="https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js" alt="Next.js 15" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Firebase-Auth-FFCA28?style=flat-square&logo=firebase" alt="Firebase Auth" />
  <img src="https://img.shields.io/badge/Neo4j-5.16-4581C3?style=flat-square&logo=neo4j" alt="Neo4j" />
  <img src="https://img.shields.io/badge/Three.js-3D_Viz-black?style=flat-square&logo=three.js" alt="Three.js" />
  <img src="https://img.shields.io/badge/IBM_watsonx.ai-Granite-054ADA?style=flat-square&logo=ibm" alt="IBM watsonx.ai" />
</div>

---

## 🚀 Live Deployments

| Layer | URL | Platform |
|-------|-----|----------|
| **Frontend** | [graphmind-ai-kappa.vercel.app](https://graphmind-ai-kappa.vercel.app/) | Vercel |
| **Backend API** | [ibm-bob-challenge.onrender.com](https://ibm-bob-challenge.onrender.com) | Render |
| **API Documentation** | [ibm-bob-challenge.onrender.com/docs](https://ibm-bob-challenge.onrender.com/docs) | Swagger UI |

---

## 🌟 The Vision: Enterprise-Level Production Idea

GraphMind AI was conceived to be a fully enterprise-grade **AI-native engineering cognition platform**. The initial vision was to fundamentally transform how developers understand, navigate, and interact with large-scale software systems.

Instead of viewing repositories as static text files, GraphMind AI aims to create a **living, interactive 3D semantic graph digital twin** of the entire codebase.

- **Deep AST Parsing**: Multi-language true AST parsing mapping out services, APIs, databases, and every function call.
- **Neo4j Graph Backend**: Scalable knowledge graph engine powering instantaneous traversal across millions of nodes.
- **Watsonx LLM Integration**: True contextual AI that reads the actual repository structure and generates insights on failure propagation, technical debt, and architecture recommendations.
- **Advanced Workflow Orchestration**: Real-time CI/CD execution mapping mapped directly onto the 3D semantic graph.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Vercel)                        │
│  Next.js 15 · React 18 · React Three Fiber · Framer Motion     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Graph3D  │  │ AIChat   │  │ Workflow │  │  Repository   │   │
│  │ (Three.js)│  │ Panel    │  │ View     │  │  Upload/List  │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ AuthModal│  │ NodeDet. │  │ Floating │                      │
│  │ Firebase │  │ Sidebar  │  │ Elements │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTPS / Bearer Token
┌─────────────────────────▼───────────────────────────────────────┐
│                       BACKEND (Render)                          │
│  FastAPI · Uvicorn · Firebase Admin SDK                         │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────────┐  │
│  │ Auth Router   │  │ Repo Router   │  │ AI / Graph APIs    │  │
│  │ /api/auth/*   │  │ /api/repo/*   │  │ /api/ai/* /graph   │  │
│  └───────┬───────┘  └───────┬───────┘  └────────┬───────────┘  │
│          │                  │                    │              │
│  ┌───────▼───────┐  ┌──────▼────────┐  ┌────────▼───────────┐  │
│  │ Firebase Svc  │  │ Repo Parser   │  │ AI Service (Mock)  │  │
│  │ Token Verify  │  │ Python AST +  │  │ IBM Granite LLM    │  │
│  └───────────────┘  │ Regex (JS/TS) │  └────────────────────┘  │
│                     └───────┬───────┘                           │
│  ┌──────────────────────────▼───────────────────────────────┐   │
│  │           Neo4j Service        │   R2 Storage Service    │   │
│  │     Graph DB (AuraDB)          │   Cloudflare R2 (S3)    │   │
│  └────────────────────────────────┴─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ What Has Been Implemented (Prototype)

Within the constraints of a rapid hackathon environment, we successfully built a powerful **Proof of Concept (PoC) prototype** that demonstrates the core user experience and frontend visualizations.

| Feature | Status | Details |
|---------|--------|---------|
| **3D Semantic Graph** | ✅ Implemented | Interactive force-directed 3D graph with React Three Fiber — drag, zoom, and explore nodes spatially |
| **Glassmorphic UI** | ✅ Implemented | Sleek Next.js 15 frontend with animated backgrounds, floating elements, and Framer Motion transitions |
| **Firebase Auth** | ✅ Implemented | Email/password sign-up and sign-in via Google Firebase SDK |
| **FastAPI Backend** | ✅ Implemented | JWT-protected endpoints serving graph data, AI responses, and workflow orchestration |
| **Repository Upload** | ✅ Implemented | Upload `.zip` / `.tar.gz` repos; parsed via Python AST (Python) + regex (JS/TS) |
| **Repository Parser** | ✅ Implemented | Multi-language parser extracting classes, functions, methods, imports, and relationships |
| **AI Chat Panel** | ✅ Implemented | Context-aware AI explanations for nodes and natural-language graph queries |
| **Workflow Visualization** | ✅ Implemented | Step-by-step pipeline viewer with animated timeline and summary stats |
| **Node Detail Sidebar** | ✅ Implemented | Click any graph node to inspect properties, connections, and AI explanations |
| **Repository Management** | ✅ Implemented | List, select, and delete uploaded repositories per authenticated user |
| **Cloud Storage** | ✅ Implemented | Cloudflare R2 (S3-compatible) for persistent archive uploads |
| **Neo4j Integration** | ✅ Scaffold | Service layer for graph persistence (falls back to in-memory / JSON) |
| **Watsonx AI** | ✅ Scaffold | `ibm/granite-13b-chat-v2` integration scaffolded; mock fallback active |

---

## ⚠️ Prototype Limitations (The 48-Hour Constraint)

While the prototype looks and feels like the final product, several technical realities prevented the delivery of the full enterprise architecture within the 48-hour timeframe:

1. **Mocked Watsonx Responses** — Tuning prompts with LangChain to consume massive graph contexts requires extensive prompt engineering; we bypass with static-but-realistic simulated responses.
2. **Mocked Neo4j Database** — Setting up, securing, and seeding a Neo4j AuraDB with complex real-world repository relationships was replaced with a static JSON response to ensure flawless 3D visualization.
3. **Limited AST Parsing** — Python files get true AST parsing; JavaScript/TypeScript files use regex-based extraction. Multi-language Tree-sitter integration was descoped.
4. **Local Execution Only** — Full CI/CD pipelines, container orchestration, and production monitoring were descoped to focus on the UI/UX.

> [!WARNING]
> **I've used antigravity in the later stage because the 40 BOBcoins got exhausted.**

---

## 📸 Screenshots

<div align="center">
  <img src="assets/Screenshot 2026-05-17 172252.png" alt="GraphMind AI — Landing & 3D Graph View" width="800" />
  <br /><br />
  <img src="assets/Screenshot 2026-05-17 172305.png" alt="GraphMind AI — AI Chat & Node Inspection" width="800" />
  <br /><br />
  <img src="assets/Screenshot 2026-05-17 172328.png" alt="GraphMind AI — Workflow Visualization" width="800" />
</div>

---

## 🛠️ Tech Stack

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| [Next.js](https://nextjs.org/) | 15.1 | React framework with SSR & routing |
| [React](https://react.dev/) | 18.3 | Component-based UI library |
| [React Three Fiber](https://docs.pmnd.rs/react-three-fiber/) | 8.17 | Declarative Three.js for 3D graph rendering |
| [Three.js](https://threejs.org/) | 0.170 | WebGL 3D engine |
| [react-force-graph-3d](https://github.com/vasturiano/react-force-graph) | 1.24 | Force-directed 3D graph layout |
| [Framer Motion](https://www.framer.com/motion/) | 11.15 | Declarative animations & transitions |
| [Firebase SDK](https://firebase.google.com/) | 12.13 | Client-side authentication |
| [Zustand](https://zustand.docs.pmnd.rs/) | 5.0 | Lightweight state management |
| [Lucide React](https://lucide.dev/) | 1.16 | Icon system |
| [Tailwind CSS](https://tailwindcss.com/) | 3.4 | Utility-first CSS framework |
| [TypeScript](https://www.typescriptlang.org/) | 5.7 | Type-safe JavaScript |

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.110+ | Async Python web framework |
| [Uvicorn](https://www.uvicorn.org/) | 0.27 | ASGI server |
| [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) | 6.4 | Server-side token verification |
| [Neo4j Driver](https://neo4j.com/docs/python-manual/) | 5.16 | Graph database client |
| [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) | 1.34 | Cloudflare R2 / S3-compatible storage |
| [GitPython](https://gitpython.readthedocs.io/) | 3.1 | Repository metadata extraction |
| [Pygments](https://pygments.org/) | 2.17 | Source code language detection |
| [Pydantic](https://docs.pydantic.dev/) | 2.7+ | Data validation & settings |
| [python-jose](https://github.com/mpdavis/python-jose) | 3.3 | JWT token handling |

### Infrastructure

| Service | Purpose |
|---------|---------|
| **Vercel** | Frontend hosting & CDN |
| **Render** | Backend hosting (Python runtime) |
| **Firebase** | Authentication (Email/Password) |
| **Neo4j AuraDB** | Graph database (scaffolded) |
| **Cloudflare R2** | Object storage for repository archives |

---

## 📁 Project Structure

```
IBM_BOB_challenge/
├── frontend/                        # Next.js 15 frontend application
│   ├── app/
│   │   ├── page.tsx                 # Main SPA — graph, auth, upload, workflow
│   │   ├── layout.tsx               # Root layout with metadata
│   │   └── globals.css              # Global styles
│   ├── components/
│   │   ├── Graph3D.tsx              # 3D force-directed graph (Three.js + ForceGraph3D)
│   │   ├── AIChat.tsx               # AI chat panel for node explanations & queries
│   │   ├── WorkflowView.tsx         # CI/CD workflow step visualizer
│   │   ├── NodeDetails.tsx          # Node detail sidebar (properties, connections)
│   │   ├── AuthModal.tsx            # Firebase sign-in / sign-up modal
│   │   ├── RepositoryUpload.tsx     # Repository archive upload (.zip/.tar.gz)
│   │   ├── RepositoryList.tsx       # User repository list & selector
│   │   ├── AnimatedBackground.tsx   # Animated 3D particle background
│   │   └── FloatingElements.tsx     # Parallax floating UI elements
│   ├── lib/
│   │   └── firebase.ts             # Firebase client initialization
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next.config.js
│
├── backend/                         # FastAPI backend application
│   ├── app/
│   │   ├── main.py                  # FastAPI app — routes, CORS, middleware
│   │   ├── firebase_service.py      # Firebase Admin SDK — token verification
│   │   ├── auth_service.py          # JWT auth service (legacy, pre-Firebase)
│   │   ├── ai_service.py            # IBM watsonx.ai Granite LLM integration
│   │   ├── ai_service_mock.py       # Mock AI service (fallback when watsonx unavailable)
│   │   ├── graph_service.py         # Graph data retrieval & manipulation
│   │   ├── neo4j_service.py         # Neo4j AuraDB graph database client
│   │   ├── repository_parser.py     # Multi-language code parser (AST + regex)
│   │   ├── storage_service.py       # Cloudflare R2 object storage client
│   │   └── routers/
│   │       ├── auth.py              # Auth endpoints (/api/auth/*)
│   │       └── repository.py        # Repository CRUD (/api/repository/*)
│   ├── data/
│   │   └── sample_graph.json        # Sample e-commerce system graph data
│   ├── requirements.txt             # Full Python dependencies
│   ├── requirements-minimal.txt     # Minimal dependencies (no watsonx)
│   ├── runtime.txt                  # Python 3.11.9 for Render
│   ├── start_server.py              # Server startup script
│   └── .env.example                 # Environment variable template
│
├── assets/                          # Static assets
│   ├── logo.png                     # GraphMind AI logo
│   └── Screenshot *.png             # Application screenshots
│
├── vercel.json                      # Vercel frontend deployment config
├── render.yaml                      # Render backend deployment config (IaC)
├── sample-graph.json                # Root-level sample graph data
├── start-backend.bat                # Windows batch — start backend locally
├── start-frontend.bat               # Windows batch — start frontend locally
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 🔌 API Endpoints

All secured endpoints require a `Bearer` token in the `Authorization` header.

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/verify` | 🔒 | Verify Firebase ID token |
| `GET` | `/api/auth/me` | 🔒 | Get current user info |
| `POST` | `/api/auth/logout` | — | Logout (client-side) |
| `GET` | `/api/auth/health` | — | Auth service health check |

### Graph & AI

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/graph` | 🔒 | Get complete graph data |
| `GET` | `/api/graph/node/{id}` | 🔒 | Get specific node details |
| `GET` | `/api/graph/stats` | 🔒 | Get graph statistics |
| `POST` | `/api/ai/explain` | 🔒 | AI explanation for a node |
| `POST` | `/api/ai/query` | 🔒 | Natural language graph query |
| `POST` | `/api/ai/analyze-workflow` | 🔒 | AI analysis of a workflow |

### Workflows

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/workflows` | 🔒 | List all workflows |
| `GET` | `/api/workflow/{id}` | 🔒 | Get workflow details |

### Repository Management

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/repository/upload` | 🔒 | Upload & parse a repo archive |
| `GET` | `/api/repository/` | 🔒 | List user repositories |
| `GET` | `/api/repository/{id}` | 🔒 | Get repository graph data |
| `DELETE` | `/api/repository/{id}` | 🔒 | Delete a repository |
| `GET` | `/api/repository/{id}/search?q=` | 🔒 | Search nodes in a repo |
| `GET` | `/api/repository/{id}/node/{nid}/relationships` | 🔒 | Get node relationships |

### Health

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | — | Root — API info & version |
| `GET` | `/health` | — | Health check |

---

## 🚀 Developer Quick Start Guide

### Prerequisites

- **Node.js** v18+
- **Python** v3.11+
- **Firebase Project** configured for Email/Password authentication

### 1. Clone the Repository

```bash
git clone https://github.com/pratyush06-aec/IBM_BOB_challenge.git
cd IBM_BOB_challenge
```

### 2. Backend Setup (FastAPI)

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Firebase, Neo4j, Cloudflare R2, and watsonx credentials

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

> The backend will be available at `http://localhost:8000`. Interactive API Docs at `http://localhost:8000/docs`.

### 3. Frontend Setup (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Configure Firebase
# Create a .env.local file:
cat > .env.local << EOF
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

# Start the development server
npm run dev
```

> The frontend will be available at `http://localhost:3000`.

### 4. Quick Start (Windows)

Use the provided batch scripts to start both services:

```bash
# Terminal 1
start-backend.bat

# Terminal 2
start-frontend.bat
```

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `WATSONX_API_KEY` | Optional | IBM watsonx.ai API key |
| `WATSONX_PROJECT_ID` | Optional | IBM watsonx.ai project ID |
| `WATSONX_URL` | Optional | watsonx endpoint (default: `https://us-south.ml.cloud.ibm.com`) |
| `SECRET_KEY` | Yes | App secret key for JWT signing |
| `ALLOWED_ORIGINS` | Yes | Comma-separated CORS origins |
| `FIREBASE_PROJECT_ID` | Yes | Firebase project ID |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Recommended | Firebase service account JSON (single-line) |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Alternative | Path to Firebase service account key file |
| `NEO4J_URI` | Optional | Neo4j AuraDB connection URI |
| `NEO4J_USER` | Optional | Neo4j username |
| `NEO4J_PASSWORD` | Optional | Neo4j password |
| `CLOUDFLARE_ACCOUNT_ID` | Optional | Cloudflare account ID for R2 |
| `CLOUDFLARE_R2_ACCESS_KEY_ID` | Optional | R2 API access key |
| `CLOUDFLARE_R2_SECRET_ACCESS_KEY` | Optional | R2 API secret key |
| `CLOUDFLARE_R2_BUCKET_NAME` | Optional | R2 bucket name |
| `UPLOAD_DIR` | Optional | Local upload fallback directory |
| `MAX_UPLOAD_SIZE` | Optional | Max upload size in bytes (default: 100MB) |

### Frontend (`frontend/.env.local`)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_FIREBASE_API_KEY` | Yes | Firebase web API key |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | Yes | Firebase auth domain |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | Yes | Firebase project ID |
| `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` | Yes | Firebase storage bucket |
| `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Yes | Firebase messaging sender ID |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | Yes | Firebase app ID |
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |

---

## 🔒 Security Posture

- **Authentication**: Client-side authentication via Firebase SDK (Email/Password). ID tokens verified server-side using Firebase Admin SDK.
- **API Protection**: All `/api/graph`, `/api/ai/*`, and `/api/repository/*` routes are protected by a `get_current_user` dependency that verifies the Firebase ID Token.
- **CORS Configuration**: The backend dynamically accepts CORS from configured `ALLOWED_ORIGINS`.
- **Security Headers**: Vercel deployment includes `X-Content-Type-Options`, `X-Frame-Options`, and `X-XSS-Protection` headers.
- **File Validation**: Repository uploads are validated for type (`.zip`, `.tar.gz`) and size (configurable, default 100MB).

---

## 📄 License

This project is licensed under the **MIT License**. Built for the **IBM BOB Challenge**.
