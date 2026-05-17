"""
Repository Router
Handles repository upload, parsing, and management
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List, Optional
import tempfile
import shutil
import os
import zipfile
import tarfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..firebase_service import FirebaseUser
from .auth import get_current_user
from ..repository_parser import RepositoryParser
from ..neo4j_service import neo4j_service

router = APIRouter(prefix="/api/repository", tags=["repository"])

# Configuration
UPLOAD_DIR = os.getenv('UPLOAD_DIR', './uploads')
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 104857600))  # 100MB default

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_archive(file_path: str, extract_to: str) -> str:
    """Extract zip or tar.gz archive"""
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif file_path.endswith(('.tar.gz', '.tgz')):
        with tarfile.open(file_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    else:
        raise ValueError("Unsupported archive format. Use .zip or .tar.gz")
    
    # Find the root directory (handle archives with/without root folder)
    extracted_items = os.listdir(extract_to)
    if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_to, extracted_items[0])):
        return os.path.join(extract_to, extracted_items[0])
    return extract_to


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_repository(
    file: UploadFile = File(...),
    current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Upload and parse a code repository
    
    - **file**: ZIP or TAR.GZ archive of the repository
    
    Returns parsed graph data and repository metadata
    """
    # Validate file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Validate file type
    if not file.filename.endswith(('.zip', '.tar.gz', '.tgz')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a .zip or .tar.gz file"
        )
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Save uploaded file
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Extract archive
            extract_dir = os.path.join(temp_dir, 'extracted')
            os.makedirs(extract_dir, exist_ok=True)
            repo_path = extract_archive(file_path, extract_dir)
            
            # Parse repository
            parser = RepositoryParser(repo_path)
            result = parser.parse_repository()
            
            # Store in Neo4j if connected
            if neo4j_service.is_connected():
                # Create repository node
                repo_id = neo4j_service.create_repository(result['repository'])
                
                # Store graph data
                neo4j_service.store_graph_data(
                    repo_id,
                    result['graph'],
                    current_user.uid
                )
                
                result['repository']['id'] = repo_id
                result['repository']['stored_in_neo4j'] = True
            else:
                result['repository']['id'] = f"temp_{file.filename}"
                result['repository']['stored_in_neo4j'] = False
                result['repository']['warning'] = "Neo4j not connected, data not persisted"
            
            return {
                "message": "Repository uploaded and parsed successfully",
                "repository": result['repository'],
                "graph": result['graph'],
                "statistics": result['statistics']
            }
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing repository: {str(e)}"
            )


@router.get("/", response_model=List[dict])
async def list_repositories(current_user: FirebaseUser = Depends(get_current_user)):
    """
    List all repositories for the current user
    
    Returns list of repository metadata
    """
    if not neo4j_service.is_connected():
        return {
            "repositories": [],
            "message": "Neo4j not connected. Upload a repository to see it here."
        }
    
    repos = neo4j_service.get_user_repositories(current_user.uid)
    return {"repositories": repos}


@router.get("/{repo_id}")
async def get_repository(
    repo_id: str,
    current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Get repository graph data by ID
    
    - **repo_id**: Repository ID
    
    Returns complete graph structure
    """
    if not neo4j_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Neo4j not connected"
        )
    
    try:
        graph = neo4j_service.get_repository_graph(repo_id)
        
        if not graph['nodes']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repository not found"
            )
        
        return {
            "repository_id": repo_id,
            "graph": graph
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving repository: {str(e)}"
        )


@router.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_repository(
    repo_id: str,
    current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Delete a repository and all its data
    
    - **repo_id**: Repository ID to delete
    """
    if not neo4j_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Neo4j not connected"
        )
    
    try:
        neo4j_service.delete_repository(repo_id)
        return {"message": "Repository deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting repository: {str(e)}"
        )


@router.get("/{repo_id}/search")
async def search_repository(
    repo_id: str,
    q: str,
    current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Search for nodes in a repository
    
    - **repo_id**: Repository ID
    - **q**: Search query (searches in node names and labels)
    
    Returns matching nodes
    """
    if not neo4j_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Neo4j not connected"
        )
    
    try:
        results = neo4j_service.search_nodes(repo_id, q)
        return {
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching repository: {str(e)}"
        )


@router.get("/{repo_id}/node/{node_id}/relationships")
async def get_node_relationships(
    repo_id: str,
    node_id: str,
    current_user: FirebaseUser = Depends(get_current_user)
):
    """
    Get all relationships for a specific node
    
    - **repo_id**: Repository ID
    - **node_id**: Node ID
    
    Returns incoming and outgoing relationships
    """
    if not neo4j_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Neo4j not connected"
        )
    
    try:
        relationships = neo4j_service.get_node_relationships(repo_id, node_id)
        return {
            "node_id": node_id,
            "relationships": relationships
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving relationships: {str(e)}"
        )


# Made with Bob