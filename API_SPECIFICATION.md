# GraphMind AI - API Specification

## Overview

This document provides the complete REST API specification for GraphMind AI, including endpoints, request/response schemas, authentication, and error handling.

**Base URL**: `https://api.graphmind.ai/api/v1`

**API Version**: 1.0.0

---

## Authentication

### JWT Authentication

All API requests (except public endpoints) require JWT authentication.

**Header Format**:
```
Authorization: Bearer <jwt_token>
```

**Token Acquisition**:
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}

Response:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

---

## Error Handling

### Standard Error Response

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            "field": "Additional error details"
        },
        "timestamp": "2026-05-16T10:00:00Z",
        "request_id": "req_123456789"
    }
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Request validation failed |
| `UNAUTHORIZED` | Authentication required |
| `FORBIDDEN` | Insufficient permissions |
| `NOT_FOUND` | Resource not found |
| `CONFLICT` | Resource conflict |
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded |
| `PROCESSING_ERROR` | Processing failed |
| `INTERNAL_ERROR` | Internal server error |

---

## API Endpoints

### 1. Repository Management

#### 1.1 Upload Repository

Upload a repository as a ZIP file.

```http
POST /repository/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>

Request:
{
    "file": <binary>,
    "name": "my-repository",
    "description": "Repository description",
    "visibility": "private"
}

Response: 201 Created
{
    "id": "repo_abc123",
    "name": "my-repository",
    "description": "Repository description",
    "status": "processing",
    "visibility": "private",
    "created_at": "2026-05-16T10:00:00Z",
    "processing": {
        "status": "queued",
        "progress": 0,
        "estimated_time_seconds": 300
    }
}
```

---

#### 1.2 Clone Repository

Clone a repository from Git URL.

```http
POST /repository/clone
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "url": "https://github.com/user/repo.git",
    "branch": "main",
    "name": "my-repository",
    "description": "Repository description",
    "visibility": "private",
    "credentials": {
        "username": "git_user",
        "token": "git_token"
    }
}

Response: 201 Created
{
    "id": "repo_abc123",
    "name": "my-repository",
    "url": "https://github.com/user/repo.git",
    "branch": "main",
    "status": "cloning",
    "visibility": "private",
    "created_at": "2026-05-16T10:00:00Z",
    "processing": {
        "status": "cloning",
        "progress": 0,
        "current_step": "Cloning repository",
        "estimated_time_seconds": 180
    }
}
```

---

#### 1.3 Get Repository

Get repository details.

```http
GET /repository/{repository_id}
Authorization: Bearer <token>

Response: 200 OK
{
    "id": "repo_abc123",
    "name": "my-repository",
    "description": "Repository description",
    "url": "https://github.com/user/repo.git",
    "branch": "main",
    "status": "completed",
    "visibility": "private",
    "created_at": "2026-05-16T10:00:00Z",
    "updated_at": "2026-05-16T10:05:00Z",
    "statistics": {
        "total_files": 150,
        "total_lines": 25000,
        "languages": {
            "TypeScript": 60,
            "JavaScript": 25,
            "Python": 15
        },
        "nodes": {
            "total": 1250,
            "by_type": {
                "Function": 800,
                "Class": 150,
                "API": 50,
                "Service": 10
            }
        },
        "edges": {
            "total": 3500,
            "by_type": {
                "CALLS": 2000,
                "DEPENDS_ON": 800,
                "IMPORTS": 700
            }
        }
    },
    "metadata": {
        "primary_language": "TypeScript",
        "framework": "Next.js",
        "complexity_score": 7.5
    }
}
```

---

#### 1.4 List Repositories

List all repositories for the authenticated user.

```http
GET /repository?page=1&limit=20&status=completed&sort=created_at&order=desc
Authorization: Bearer <token>

Response: 200 OK
{
    "repositories": [
        {
            "id": "repo_abc123",
            "name": "my-repository",
            "description": "Repository description",
            "status": "completed",
            "visibility": "private",
            "created_at": "2026-05-16T10:00:00Z",
            "statistics": {
                "total_files": 150,
                "total_nodes": 1250,
                "total_edges": 3500
            }
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 45,
        "total_pages": 3
    }
}
```

---

#### 1.5 Get Repository Status

Get processing status of a repository.

```http
GET /repository/{repository_id}/status
Authorization: Bearer <token>

Response: 200 OK
{
    "id": "repo_abc123",
    "status": "processing",
    "progress": 65,
    "current_step": "Generating graph",
    "steps": [
        {
            "name": "Cloning repository",
            "status": "completed",
            "duration_seconds": 15
        },
        {
            "name": "Scanning files",
            "status": "completed",
            "duration_seconds": 5
        },
        {
            "name": "Parsing source code",
            "status": "completed",
            "duration_seconds": 120
        },
        {
            "name": "Generating graph",
            "status": "in_progress",
            "progress": 65
        },
        {
            "name": "AI analysis",
            "status": "pending"
        }
    ],
    "estimated_time_remaining_seconds": 60,
    "nodes_created": 815,
    "edges_created": 2275,
    "errors": []
}
```

---

#### 1.6 Delete Repository

Delete a repository and all associated data.

```http
DELETE /repository/{repository_id}
Authorization: Bearer <token>

Response: 204 No Content
```

---

#### 1.7 Update Repository

Update repository metadata.

```http
PATCH /repository/{repository_id}
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "name": "updated-name",
    "description": "Updated description",
    "visibility": "public"
}

Response: 200 OK
{
    "id": "repo_abc123",
    "name": "updated-name",
    "description": "Updated description",
    "visibility": "public",
    "updated_at": "2026-05-16T11:00:00Z"
}
```

---

### 2. Graph Operations

#### 2.1 Get Graph Data

Get graph data for visualization.

```http
GET /graph/{repository_id}?depth=2&node_types=Function,Service&limit=1000
Authorization: Bearer <token>

Response: 200 OK
{
    "nodes": [
        {
            "id": "node_func_001",
            "type": "Function",
            "label": "authenticateUser",
            "properties": {
                "name": "authenticateUser",
                "file_path": "src/auth/authenticate.ts",
                "line_start": 15,
                "line_end": 45,
                "complexity": 5,
                "parameters": [
                    {"name": "email", "type": "string"},
                    {"name": "password", "type": "string"}
                ],
                "return_type": "Promise<User>",
                "is_async": true,
                "risk_score": 0.3,
                "importance": 8
            },
            "metadata": {
                "calls_count": 15,
                "called_by_count": 3,
                "ai_summary": "Authenticates user credentials and returns user object"
            }
        }
    ],
    "edges": [
        {
            "id": "edge_001",
            "source": "node_func_001",
            "target": "node_func_002",
            "type": "CALLS",
            "label": "calls",
            "properties": {
                "line_number": 25,
                "execution_order": 1,
                "frequency": 100,
                "latency_ms": 15.5,
                "failure_rate": 0.01
            }
        }
    ],
    "metadata": {
        "total_nodes": 1250,
        "returned_nodes": 1000,
        "total_edges": 3500,
        "returned_edges": 2800,
        "depth": 2,
        "query_time_ms": 45
    }
}
```

---

#### 2.2 Get Node Details

Get detailed information about a specific node.

```http
GET /graph/{repository_id}/node/{node_id}
Authorization: Bearer <token>

Response: 200 OK
{
    "id": "node_func_001",
    "type": "Function",
    "properties": {
        "name": "authenticateUser",
        "qualified_name": "auth.authenticateUser",
        "file_path": "src/auth/authenticate.ts",
        "line_start": 15,
        "line_end": 45,
        "complexity": 5,
        "parameters": [
            {"name": "email", "type": "string"},
            {"name": "password", "type": "string"}
        ],
        "return_type": "Promise<User>",
        "is_async": true,
        "docstring": "Authenticates a user with email and password",
        "risk_score": 0.3,
        "importance": 8
    },
    "code_snippet": "async function authenticateUser(email: string, password: string): Promise<User> {\n  // Implementation\n}",
    "incoming_edges": [
        {
            "id": "edge_005",
            "source": "node_api_001",
            "type": "CALLS",
            "properties": {
                "line_number": 10,
                "frequency": 50
            }
        }
    ],
    "outgoing_edges": [
        {
            "id": "edge_001",
            "target": "node_func_002",
            "type": "CALLS",
            "properties": {
                "line_number": 25,
                "frequency": 100
            }
        }
    ],
    "ai_analysis": {
        "summary": "This function handles user authentication by validating credentials",
        "purpose": "Authentication",
        "complexity_assessment": "Moderate complexity with proper error handling",
        "recommendations": [
            "Consider adding rate limiting",
            "Add more detailed logging"
        ],
        "related_nodes": ["node_func_002", "node_db_001"]
    },
    "metrics": {
        "calls_count": 15,
        "called_by_count": 3,
        "avg_execution_time_ms": 45,
        "error_rate": 0.02
    }
}
```

---

#### 2.3 Traverse Graph

Traverse the graph from a starting node.

```http
POST /graph/{repository_id}/traverse
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "start_node_id": "node_func_001",
    "direction": "outgoing",
    "edge_types": ["CALLS", "DEPENDS_ON"],
    "max_depth": 3,
    "filters": {
        "node_types": ["Function", "Service"],
        "min_importance": 5
    }
}

Response: 200 OK
{
    "paths": [
        {
            "nodes": [
                {"id": "node_func_001", "type": "Function", "name": "authenticateUser"},
                {"id": "node_func_002", "type": "Function", "name": "validatePassword"},
                {"id": "node_func_003", "type": "Function", "name": "hashPassword"}
            ],
            "edges": [
                {"id": "edge_001", "type": "CALLS"},
                {"id": "edge_002", "type": "CALLS"}
            ],
            "depth": 2,
            "total_weight": 150
        }
    ],
    "graph": {
        "nodes": [...],
        "edges": [...]
    },
    "metadata": {
        "total_paths": 15,
        "max_depth_reached": 3,
        "query_time_ms": 120
    }
}
```

---

#### 2.4 Query Graph

Execute a custom Cypher query.

```http
POST /graph/{repository_id}/query
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "cypher": "MATCH (f:Function)-[:CALLS]->(target:Function) WHERE f.complexity > $min_complexity RETURN f, target LIMIT $limit",
    "parameters": {
        "min_complexity": 10,
        "limit": 50
    }
}

Response: 200 OK
{
    "results": [
        {
            "f": {
                "id": "node_func_001",
                "name": "complexFunction",
                "complexity": 15
            },
            "target": {
                "id": "node_func_002",
                "name": "helperFunction",
                "complexity": 3
            }
        }
    ],
    "metadata": {
        "rows_returned": 45,
        "execution_time_ms": 85,
        "query_plan": "NodeIndexSeek -> Expand -> Filter"
    }
}
```

---

#### 2.5 Find Path Between Nodes

Find the shortest path between two nodes.

```http
GET /graph/{repository_id}/path?from=node_func_001&to=node_func_050&max_depth=5
Authorization: Bearer <token>

Response: 200 OK
{
    "path": {
        "nodes": [
            {"id": "node_func_001", "type": "Function", "name": "start"},
            {"id": "node_func_010", "type": "Function", "name": "intermediate"},
            {"id": "node_func_050", "type": "Function", "name": "end"}
        ],
        "edges": [
            {"id": "edge_001", "type": "CALLS"},
            {"id": "edge_025", "type": "CALLS"}
        ],
        "length": 2,
        "total_weight": 75
    },
    "alternative_paths": [
        {
            "length": 3,
            "total_weight": 120,
            "nodes": [...]
        }
    ]
}
```

---

#### 2.6 Search Graph

Search for nodes by name or properties.

```http
GET /graph/{repository_id}/search?q=authenticate&types=Function,Class&limit=20
Authorization: Bearer <token>

Response: 200 OK
{
    "results": [
        {
            "id": "node_func_001",
            "type": "Function",
            "name": "authenticateUser",
            "file_path": "src/auth/authenticate.ts",
            "score": 0.95,
            "highlight": {
                "name": "<em>authenticate</em>User",
                "docstring": "Function to <em>authenticate</em> users"
            }
        }
    ],
    "metadata": {
        "total_results": 15,
        "returned_results": 15,
        "search_time_ms": 25
    }
}
```

---

### 3. AI Operations

#### 3.1 Explain Node

Get AI explanation for a node.

```http
POST /ai/explain
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "repository_id": "repo_abc123",
    "node_id": "node_func_001",
    "context": "I want to understand how authentication works",
    "detail_level": "detailed"
}

Response: 200 OK (Streaming)
{
    "explanation": "The authenticateUser function is the primary entry point for user authentication...",
    "key_points": [
        "Validates email and password",
        "Checks against database",
        "Returns JWT token on success"
    ],
    "related_nodes": [
        {
            "id": "node_func_002",
            "name": "validatePassword",
            "relationship": "Called by this function to validate password"
        }
    ],
    "code_flow": [
        "Receives email and password",
        "Calls validatePassword",
        "Queries database",
        "Generates JWT token"
    ],
    "suggestions": [
        "Consider adding rate limiting",
        "Add more detailed error messages"
    ],
    "complexity_analysis": {
        "score": 5,
        "assessment": "Moderate complexity",
        "factors": ["Multiple database calls", "Error handling"]
    }
}
```

---

#### 3.2 Natural Language Query

Query the repository using natural language.

```http
POST /ai/query
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "repository_id": "repo_abc123",
    "query": "Where does authentication happen and what services does it depend on?",
    "context": []
}

Response: 200 OK (Streaming)
{
    "answer": "Authentication happens primarily in the auth service, specifically in the authenticateUser function...",
    "highlighted_nodes": [
        "node_func_001",
        "node_service_001",
        "node_db_001"
    ],
    "highlighted_paths": [
        {
            "nodes": ["node_func_001", "node_func_002", "node_db_001"],
            "description": "Authentication flow from API to database"
        }
    ],
    "confidence": 0.92,
    "sources": [
        {
            "node_id": "node_func_001",
            "relevance": 0.95
        }
    ],
    "follow_up_questions": [
        "How is the JWT token generated?",
        "What happens if authentication fails?",
        "Are there any rate limits on authentication?"
    ]
}
```

---

#### 3.3 Analyze Architecture

Get AI analysis of repository architecture.

```http
POST /ai/analyze
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "repository_id": "repo_abc123",
    "analysis_type": "architecture",
    "focus_areas": ["security", "performance", "maintainability"]
}

Response: 200 OK
{
    "summary": "The repository follows a microservices architecture with clear separation of concerns...",
    "architecture_pattern": "Microservices with API Gateway",
    "findings": [
        {
            "category": "security",
            "severity": "medium",
            "title": "Missing rate limiting on authentication endpoints",
            "description": "Authentication endpoints lack rate limiting...",
            "affected_nodes": ["node_api_001", "node_api_002"],
            "recommendation": "Implement rate limiting middleware"
        }
    ],
    "metrics": {
        "complexity_score": 7.5,
        "maintainability_index": 72,
        "test_coverage": 65,
        "security_score": 78
    },
    "recommendations": [
        {
            "priority": "high",
            "category": "security",
            "title": "Add rate limiting",
            "description": "Implement rate limiting on all public APIs",
            "estimated_effort": "2-4 hours"
        }
    ],
    "strengths": [
        "Clear service boundaries",
        "Good error handling",
        "Comprehensive logging"
    ],
    "weaknesses": [
        "Missing rate limiting",
        "Some functions have high complexity",
        "Limited test coverage in auth module"
    ]
}
```

---

#### 3.4 Get Suggestions

Get AI suggestions for improvements.

```http
GET /ai/suggestions/{repository_id}?category=all&limit=10
Authorization: Bearer <token>

Response: 200 OK
{
    "suggestions": [
        {
            "id": "sugg_001",
            "category": "performance",
            "priority": "high",
            "title": "Add caching to database queries",
            "description": "Several frequently called functions make repeated database queries...",
            "affected_nodes": ["node_func_010", "node_func_015"],
            "estimated_impact": "30% performance improvement",
            "estimated_effort": "4-6 hours",
            "implementation_steps": [
                "Add Redis caching layer",
                "Implement cache invalidation",
                "Update query functions"
            ]
        }
    ],
    "metadata": {
        "total_suggestions": 25,
        "by_category": {
            "performance": 8,
            "security": 5,
            "maintainability": 7,
            "testing": 5
        }
    }
}
```

---

### 4. Workflow Operations

#### 4.1 Get Workflows

Get all workflows in a repository.

```http
GET /workflow/{repository_id}?type=ci_cd&status=active
Authorization: Bearer <token>

Response: 200 OK
{
    "workflows": [
        {
            "id": "workflow_001",
            "name": "CI/CD Pipeline",
            "type": "ci_cd",
            "description": "Main deployment pipeline",
            "status": "active",
            "steps": [
                {
                    "name": "Build",
                    "type": "build",
                    "status": "completed",
                    "duration_ms": 45000
                },
                {
                    "name": "Test",
                    "type": "test",
                    "status": "completed",
                    "duration_ms": 120000
                },
                {
                    "name": "Deploy",
                    "type": "deploy",
                    "status": "in_progress",
                    "progress": 65
                }
            ],
            "triggers": ["push", "pull_request"],
            "last_run": "2026-05-16T10:00:00Z",
            "success_rate": 0.95,
            "avg_duration_ms": 180000
        }
    ]
}
```

---

#### 4.2 Trace Execution Flow

Trace the execution flow of a workflow.

```http
POST /workflow/{repository_id}/trace
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "entry_point": "node_api_001",
    "trace_type": "execution",
    "max_depth": 5
}

Response: 200 OK
{
    "trace": {
        "entry_point": {
            "id": "node_api_001",
            "name": "POST /api/auth/login",
            "type": "API"
        },
        "execution_path": [
            {
                "step": 1,
                "node": {"id": "node_func_001", "name": "authenticateUser"},
                "execution_time_ms": 45,
                "status": "success"
            },
            {
                "step": 2,
                "node": {"id": "node_func_002", "name": "validatePassword"},
                "execution_time_ms": 15,
                "status": "success"
            }
        ],
        "total_execution_time_ms": 150,
        "nodes_visited": 8,
        "database_calls": 3,
        "external_api_calls": 1
    },
    "visualization": {
        "nodes": [...],
        "edges": [...],
        "highlighted_path": [...]
    }
}
```

---

### 5. Debug Operations

#### 5.1 Analyze Failure Propagation

Analyze how a failure propagates through the system.

```http
POST /debug/{repository_id}/propagation
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "failed_node_id": "node_db_001",
    "failure_type": "connection_timeout",
    "max_depth": 5
}

Response: 200 OK
{
    "failure_analysis": {
        "root_cause": {
            "node": {"id": "node_db_001", "name": "UserDatabase", "type": "Database"},
            "failure_type": "connection_timeout",
            "description": "Database connection timeout"
        },
        "propagation_tree": [
            {
                "level": 1,
                "affected_nodes": [
                    {
                        "id": "node_func_002",
                        "name": "getUserById",
                        "impact": "high",
                        "probability": 1.0,
                        "propagation_time_ms": 50
                    }
                ]
            },
            {
                "level": 2,
                "affected_nodes": [
                    {
                        "id": "node_func_001",
                        "name": "authenticateUser",
                        "impact": "high",
                        "probability": 0.95,
                        "propagation_time_ms": 100
                    }
                ]
            }
        ],
        "total_affected_nodes": 15,
        "critical_affected_nodes": 5,
        "estimated_downtime_seconds": 300
    },
    "recommendations": [
        {
            "priority": "critical",
            "action": "Implement connection pooling",
            "description": "Add connection pooling to prevent timeout issues"
        },
        {
            "priority": "high",
            "action": "Add circuit breaker",
            "description": "Implement circuit breaker pattern to prevent cascade failures"
        }
    ],
    "mitigation_strategies": [
        "Add retry logic with exponential backoff",
        "Implement fallback to read replica",
        "Add health checks"
    ]
}
```

---

#### 5.2 Find Root Cause

Find the root cause of an issue.

```http
POST /debug/{repository_id}/root-cause
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "symptom_node_id": "node_api_001",
    "error_message": "500 Internal Server Error",
    "timestamp": "2026-05-16T10:00:00Z"
}

Response: 200 OK
{
    "root_causes": [
        {
            "node": {"id": "node_db_001", "name": "UserDatabase"},
            "probability": 0.85,
            "reason": "Database connection pool exhausted",
            "evidence": [
                "High connection count",
                "Slow query performance",
                "Timeout errors in logs"
            ],
            "path_to_symptom": [
                {"id": "node_db_001", "name": "UserDatabase"},
                {"id": "node_func_002", "name": "getUserById"},
                {"id": "node_api_001", "name": "GET /api/user/:id"}
            ]
        }
    ],
    "analysis": {
        "confidence": 0.85,
        "factors_considered": [
            "Error patterns",
            "Dependency graph",
            "Historical data",
            "System metrics"
        ]
    },
    "suggested_fixes": [
        {
            "priority": "critical",
            "fix": "Increase database connection pool size",
            "implementation": "Update database configuration",
            "estimated_time": "15 minutes"
        }
    ]
}
```

---

### 6. Documentation Operations

#### 6.1 Generate Documentation

Generate documentation for the repository.

```http
POST /documentation/{repository_id}/generate
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "doc_type": "architecture",
    "sections": ["overview", "services", "api", "database"],
    "format": "markdown",
    "include_diagrams": true
}

Response: 202 Accepted
{
    "job_id": "doc_job_001",
    "status": "processing",
    "estimated_time_seconds": 120
}

// Get result
GET /documentation/{repository_id}/job/{job_id}

Response: 200 OK
{
    "job_id": "doc_job_001",
    "status": "completed",
    "result": {
        "documentation": "# Architecture Overview\n\n...",
        "diagrams": [
            {
                "type": "architecture",
                "format": "mermaid",
                "content": "graph TB\n..."
            }
        ],
        "download_url": "https://api.graphmind.ai/downloads/doc_abc123.md"
    }
}
```

---

#### 6.2 Generate API Documentation

Generate API documentation.

```http
POST /documentation/{repository_id}/api
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "format": "openapi",
    "include_examples": true
}

Response: 200 OK
{
    "openapi": "3.0.0",
    "info": {
        "title": "My API",
        "version": "1.0.0"
    },
    "paths": {
        "/api/auth/login": {
            "post": {
                "summary": "Authenticate user",
                "requestBody": {...},
                "responses": {...}
            }
        }
    }
}
```

---

### 7. Onboarding Operations

#### 7.1 Generate Onboarding Path

Generate a learning path for new developers.

```http
POST /onboarding/{repository_id}/path
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
    "role": "backend_developer",
    "experience_level": "intermediate",
    "focus_areas": ["authentication", "database"]
}

Response: 200 OK
{
    "path": {
        "id": "path_001",
        "title": "Backend Developer Onboarding",
        "estimated_duration_hours": 8,
        "steps": [
            {
                "step": 1,
                "title": "Understand Project Structure",
                "description": "Learn about the overall architecture",
                "nodes_to_explore": ["node_service_001", "node_service_002"],
                "resources": [
                    {"type": "documentation", "url": "..."},
                    {"type": "video", "url": "..."}
                ],
                "estimated_time_minutes": 30
            },
            {
                "step": 2,
                "title": "Authentication Flow",
                "description": "Understand how authentication works",
                "nodes_to_explore": ["node_func_001", "node_api_001"],
                "tasks": [
                    "Read authenticateUser function",
                    "Trace authentication flow",
                    "Review JWT implementation"
                ],
                "estimated_time_minutes": 60
            }
        ]
    }
}
```

---

### 8. Infrastructure Operations

#### 8.1 Get Infrastructure Graph

Get infrastructure visualization data.

```http
GET /infrastructure/{repository_id}
Authorization: Bearer <token>

Response: 200 OK
{
    "infrastructure": {
        "nodes": [
            {
                "id": "infra_001",
                "type": "container",
                "name": "api-server",
                "provider": "docker",
                "status": "running",
                "resources": {
                    "cpu": "2 cores",
                    "memory": "4GB",
                    "storage": "20GB"
                }
            }
        ],
        "edges": [
            {
                "source": "infra_001",
                "target": "infra_002",
                "type": "connects_to",
                "protocol": "http"
            }
        ]
    }
}
```

---

## Rate Limiting

All API endpoints are rate-limited to ensure fair usage.

**Rate Limits**:
- Free tier: 100 requests/minute
- Pro tier: 1000 requests/minute
- Enterprise tier: Custom limits

**Rate Limit Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1621234567
```

**Rate Limit Exceeded Response**:
```json
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded. Please try again later.",
        "retry_after": 60
    }
}
```

---

## Pagination

List endpoints support pagination using cursor-based pagination.

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `sort`: Sort field
- `order`: Sort order (`asc` or `desc`)

**Response Format**:
```json
{
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 150,
        "total_pages": 8,
        "has_next": true,
        "has_prev": false
    }
}
```

---

## Webhooks

GraphMind AI supports webhooks for real-time notifications.

**Webhook Events**:
- `repository.created`
- `repository.processing.completed`
- `repository.processing.failed`
- `graph.updated`
- `analysis.completed`

**Webhook Payload**:
```json
{
    "event": "repository.processing.completed",
    "timestamp": "2026-05-16T10:00:00Z",
    "data": {
        "repository_id": "repo_abc123",
        "status": "completed",
        "statistics": {...}
    }
}
```

---

## Conclusion

This API specification provides a comprehensive reference for integrating with GraphMind AI. The API is designed to be:

1. **RESTful**: Following REST principles
2. **Consistent**: Uniform response formats
3. **Well-documented**: Clear descriptions and examples
4. **Secure**: JWT authentication and rate limiting
5. **Scalable**: Pagination and efficient queries

For additional support, visit our [API documentation portal](https://docs.graphmind.ai) or contact support@graphmind.ai.