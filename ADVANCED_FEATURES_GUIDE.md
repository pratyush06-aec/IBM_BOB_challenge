# Advanced Features Implementation Guide

## Overview
This guide documents the implementation of three major features:
1. Real Repository Parsing
2. Neo4j Graph Database Integration
3. User Authentication System

---

## 1. Repository Parsing System

### Implementation: `backend/app/repository_parser.py`

**Features:**
- Multi-language support (Python, JavaScript, TypeScript, Java, Go, C++, etc.)
- AST-based parsing for Python
- Regex-based parsing for JavaScript/TypeScript
- Extracts classes, functions, methods, imports
- Builds relationship graph
- Calculates statistics

**Key Components:**

#### CodeEntity
Represents code elements (classes, functions, methods)
- ID, name, type, file path, line number
- Docstrings, parameters, decorators
- Parent relationships for methods

#### CodeRelationship
Represents connections between entities
- Source, target, type (imports, calls, inherits, uses, defines)

#### RepositoryParser
Main parser class
- `parse_repository()` - Entry point
- `_parse_file()` - File-level parsing
- `_parse_python_file()` - Python AST parsing
- `_parse_javascript_file()` - JS/TS regex parsing
- `_build_graph()` - Constructs graph structure
- `_calculate_statistics()` - Computes metrics

**Usage:**
```python
from repository_parser import RepositoryParser

parser = RepositoryParser('/path/to/repo')
result = parser.parse_repository()

# Returns:
# {
#   'repository': {...},  # Repo metadata
#   'graph': {
#     'nodes': [...],     # Code entities
#     'edges': [...]      # Relationships
#   },
#   'statistics': {...}   # Metrics
# }
```

---

## 2. Neo4j Graph Database

### Implementation: `backend/app/neo4j_service.py`

**Features:**
- Connection management with fallback
- Repository storage
- Graph data persistence
- Query operations
- User-scoped data

**Key Methods:**

#### Connection
- `_connect()` - Establishes Neo4j connection
- `is_connected()` - Checks connection status
- `close()` - Closes connection

#### Repository Operations
- `create_repository(repo_data)` - Creates repo node
- `store_graph_data(repo_id, graph_data, user_id)` - Stores parsed graph
- `get_repository_graph(repo_id)` - Retrieves graph
- `delete_repository(repo_id)` - Removes repo and nodes
- `get_user_repositories(user_id)` - Lists user's repos

#### Query Operations
- `search_nodes(repo_id, search_term)` - Searches nodes
- `get_node_relationships(repo_id, node_id)` - Gets connections

**Database Schema:**

```cypher
// Repository Node
(:Repository {
  name: string,
  path: string,
  branch: string,
  commit: string,
  author: string,
  last_modified: datetime,
  created_at: datetime
})

// Code Entity Nodes
(:Class|:Function|:Method|:File {
  id: string,
  label: string,
  properties: map,
  repo_id: string,
  user_id: string,
  created_at: datetime
})

// Relationships
(:Repository)-[:CONTAINS]->(:Entity)
(:Entity)-[:RELATES {type, label, properties}]->(:Entity)
```

**Setup Neo4j:**

1. **Install Neo4j:**
```bash
# Using Docker
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest

# Or download from https://neo4j.com/download/
```

2. **Configure Environment:**
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

3. **Verify Connection:**
- Open http://localhost:7474
- Login with credentials
- Run: `MATCH (n) RETURN count(n)`

---

## 3. Authentication System

### Implementation: `backend/app/auth_service.py`

**Features:**
- User registration
- Login with JWT tokens
- Password hashing (bcrypt)
- Token validation
- Demo user included

**Key Components:**

#### Models
- `User` - User data model
- `UserInDB` - User with hashed password
- `Token` - JWT token response
- `UserCreate` - Registration data
- `UserLogin` - Login credentials

#### AuthService Methods
- `register_user(user_data)` - Creates new user
- `authenticate_user(username, password)` - Validates credentials
- `create_access_token(data, expires_delta)` - Generates JWT
- `decode_token(token)` - Validates JWT
- `get_current_user(token)` - Gets user from token

**Security:**
- Passwords hashed with bcrypt
- JWT tokens with expiration
- Secret key configuration
- Token-based authentication

**Demo User:**
- Username: `demo`
- Password: `demo123`
- Email: `demo@graphmind.ai`

---

## 4. API Integration

### New Endpoints to Add

Create `backend/app/routers/repository.py`:

```python
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from repository_parser import RepositoryParser
from neo4j_service import neo4j_service
from auth_service import AuthService, User
import tempfile
import shutil
import git

router = APIRouter(prefix="/api/repository", tags=["repository"])

@router.post("/upload")
async def upload_repository(
    file: UploadFile,
    current_user: User = Depends(get_current_user)
):
    """Upload and parse a repository"""
    # Save uploaded file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract repository
        # Parse with RepositoryParser
        # Store in Neo4j
        # Return graph data
        pass

@router.get("/{repo_id}")
async def get_repository(
    repo_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get repository graph"""
    graph = neo4j_service.get_repository_graph(repo_id)
    return graph

@router.get("/")
async def list_repositories(
    current_user: User = Depends(get_current_user)
):
    """List user's repositories"""
    repos = neo4j_service.get_user_repositories(current_user.id)
    return repos

@router.delete("/{repo_id}")
async def delete_repository(
    repo_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a repository"""
    neo4j_service.delete_repository(repo_id)
    return {"message": "Repository deleted"}
```

Create `backend/app/routers/auth.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth_service import AuthService, UserCreate, Token, User
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", response_model=User)
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        user = AuthService.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    user = AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = AuthService.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user"""
    user = AuthService.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
```

---

## 5. Frontend Integration

### Authentication UI

Create `frontend/components/AuthModal.tsx`:

```typescript
'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

export default function AuthModal({ onClose, onSuccess }) {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    full_name: ''
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register'
    const response = await fetch(`http://localhost:8000${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
    
    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('token', data.access_token)
      onSuccess()
    }
  }

  return (
    <motion.div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <motion.div className="bg-gray-900 p-8 rounded-2xl max-w-md w-full">
        <h2 className="text-2xl font-bold text-white mb-6">
          {isLogin ? 'Login' : 'Register'}
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Form fields */}
        </form>
      </motion.div>
    </motion.div>
  )
}
```

### Repository Upload UI

Create `frontend/components/RepositoryUpload.tsx`:

```typescript
'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

export default function RepositoryUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)

  const handleUpload = async () => {
    if (!file) return
    
    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)
    
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/api/repository/upload', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData
    })
    
    if (response.ok) {
      const data = await response.json()
      onUploadComplete(data)
    }
    
    setUploading(false)
  }

  return (
    <motion.div className="p-6 bg-gray-900 rounded-2xl">
      <h3 className="text-xl font-bold text-white mb-4">
        Upload Repository
      </h3>
      
      <input
        type="file"
        accept=".zip,.tar.gz"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      
      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="px-6 py-3 bg-blue-600 text-white rounded-lg"
      >
        {uploading ? 'Uploading...' : 'Upload & Analyze'}
      </button>
    </motion.div>
  )
}
```

---

## 6. Installation & Setup

### Backend Setup

1. **Install Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure Environment:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Start Neo4j:**
```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

4. **Run Backend:**
```bash
python -m uvicorn app.main:app --reload
```

### Frontend Setup

1. **Install Dependencies:**
```bash
cd frontend
npm install
```

2. **Run Frontend:**
```bash
npm run dev
```

---

## 7. Testing

### Test Repository Parsing

```python
from repository_parser import RepositoryParser

parser = RepositoryParser('./test-repo')
result = parser.parse_repository()
print(f"Found {len(result['graph']['nodes'])} nodes")
print(f"Found {len(result['graph']['edges'])} edges")
```

### Test Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","email":"test@example.com"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=demo&password=demo123"
```

### Test Neo4j

```cypher
// In Neo4j Browser (http://localhost:7474)
MATCH (n) RETURN n LIMIT 25
```

---

## 8. Next Steps

1. **Complete API Integration** - Add all endpoints to main.py
2. **Frontend Components** - Build auth and upload UIs
3. **Error Handling** - Add comprehensive error handling
4. **Testing** - Write unit and integration tests
5. **Documentation** - API documentation with Swagger
6. **Deployment** - Docker compose for full stack

---

## Made with Bob - AI Software Engineer