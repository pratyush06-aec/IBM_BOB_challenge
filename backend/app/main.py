"""
GraphMind AI - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path

# Import AI service (using mock due to Python 3.13 compatibility)
from .ai_service_mock import AIService
from .graph_service import GraphService

# Import routers
from .routers import auth, repository
from .routers.auth import get_current_user

# Initialize FastAPI app
app = FastAPI(
    title="GraphMind AI API",
    description="AI-Native Engineering Cognition Platform",
    version="1.0.0"
)

# Configure CORS
# Read allowed origins from env, fallback to localhost
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
# Secure repository router
app.include_router(
    repository.router, 
    tags=["Repository"],
    dependencies=[Depends(get_current_user)]
)

# Initialize services
ai_service = AIService()
graph_service = GraphService()

# Pydantic models
class NodeExplainRequest(BaseModel):
    node_id: str
    context: Optional[str] = None

class QueryRequest(BaseModel):
    query: str
    context: Optional[List[str]] = None

class WorkflowRequest(BaseModel):
    workflow_id: str

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GraphMind AI API",
        "version": "1.0.0",
        "status": "running"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Get graph data - Secured
@app.get("/api/graph", dependencies=[Depends(get_current_user)])
async def get_graph():
    """
    Get the complete graph data for visualization
    """
    try:
        graph_data = graph_service.get_graph()
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get node details - Secured
@app.get("/api/graph/node/{node_id}", dependencies=[Depends(get_current_user)])
async def get_node(node_id: str):
    """
    Get detailed information about a specific node
    """
    try:
        node = graph_service.get_node(node_id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        return node
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Explain node with AI - Secured
@app.post("/api/ai/explain", dependencies=[Depends(get_current_user)])
async def explain_node(request: NodeExplainRequest):
    """
    Get AI explanation for a node
    """
    try:
        # Get node details
        node = graph_service.get_node(request.node_id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        
        # Get connected nodes for context
        connections = graph_service.get_node_connections(request.node_id)
        
        # Generate AI explanation
        explanation = await ai_service.explain_node(
            node=node,
            connections=connections,
            user_context=request.context
        )
        
        return {
            "node_id": request.node_id,
            "explanation": explanation,
            "node": node,
            "connections": connections
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Natural language query - Secured
@app.post("/api/ai/query", dependencies=[Depends(get_current_user)])
async def query_graph(request: QueryRequest):
    """
    Query the graph using natural language
    """
    try:
        # Get graph context
        graph_data = graph_service.get_graph()
        
        # Process query with AI
        result = await ai_service.process_query(
            query=request.query,
            graph_data=graph_data,
            context=request.context
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get workflow - Secured
@app.get("/api/workflow/{workflow_id}", dependencies=[Depends(get_current_user)])
async def get_workflow(workflow_id: str):
    """
    Get workflow details and visualization data
    """
    try:
        workflow = graph_service.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return workflow
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all workflows - Secured
@app.get("/api/workflows", dependencies=[Depends(get_current_user)])
async def get_workflows():
    """
    Get all available workflows
    """
    try:
        workflows = graph_service.get_all_workflows()
        return {"workflows": workflows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analyze workflow with AI - Secured
@app.post("/api/ai/analyze-workflow", dependencies=[Depends(get_current_user)])
async def analyze_workflow(request: WorkflowRequest):
    """
    Get AI analysis of a workflow
    """
    try:
        workflow = graph_service.get_workflow(request.workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        analysis = await ai_service.analyze_workflow(workflow)
        
        return {
            "workflow_id": request.workflow_id,
            "workflow": workflow,
            "analysis": analysis
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get graph statistics - Secured
@app.get("/api/graph/stats", dependencies=[Depends(get_current_user)])
async def get_graph_stats():
    """
    Get graph statistics
    """
    try:
        stats = graph_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Made with Bob
