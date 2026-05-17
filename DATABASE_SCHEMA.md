# GraphMind AI - Neo4j Database Schema

## Overview

This document defines the complete Neo4j graph database schema for GraphMind AI, including node types, relationships, properties, constraints, and indexes.

---

## Schema Design Principles

1. **Entity-Centric**: Each node represents a distinct engineering entity
2. **Relationship-Rich**: Edges capture semantic relationships with metadata
3. **Queryable**: Optimized for common traversal patterns
4. **Extensible**: Easy to add new node and edge types
5. **Performant**: Proper indexing and constraints

---

## Node Types

### 1. Repository Node

Represents a code repository.

```cypher
(:Repository {
    id: string,                    // Unique identifier
    name: string,                  // Repository name
    url: string,                   // Git URL (if applicable)
    description: string,           // Repository description
    language_primary: string,      // Primary language
    languages: list<string>,       // All languages used
    total_files: int,              // Total file count
    total_lines: int,              // Total lines of code
    created_at: datetime,          // Creation timestamp
    updated_at: datetime,          // Last update timestamp
    status: string,                // "active" | "archived" | "processing"
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT repository_id IF NOT EXISTS 
FOR (r:Repository) REQUIRE r.id IS UNIQUE;

// Indexes
CREATE INDEX repository_name IF NOT EXISTS 
FOR (r:Repository) ON (r.name);
```

---

### 2. File Node

Represents a source code file.

```cypher
(:File {
    id: string,                    // Unique identifier
    path: string,                  // Relative file path
    name: string,                  // File name
    extension: string,             // File extension
    language: string,              // Programming language
    size_bytes: int,               // File size
    lines: int,                    // Line count
    complexity_score: float,       // Overall complexity
    last_modified: datetime,       // Last modification
    hash: string,                  // File content hash
    is_test: boolean,              // Is test file
    is_config: boolean,            // Is config file
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT file_id IF NOT EXISTS 
FOR (f:File) REQUIRE f.id IS UNIQUE;

// Indexes
CREATE INDEX file_path IF NOT EXISTS 
FOR (f:File) ON (f.path);

CREATE INDEX file_language IF NOT EXISTS 
FOR (f:File) ON (f.language);
```

---

### 3. Function Node

Represents a function or method.

```cypher
(:Function {
    id: string,                    // Unique identifier
    name: string,                  // Function name
    qualified_name: string,        // Fully qualified name
    file_path: string,             // Source file path
    line_start: int,               // Starting line number
    line_end: int,                 // Ending line number
    complexity: int,               // Cyclomatic complexity
    parameters: list<map>,         // Parameter definitions
    return_type: string,           // Return type
    is_async: boolean,             // Is async function
    is_generator: boolean,         // Is generator function
    is_exported: boolean,          // Is exported
    is_public: boolean,            // Is public method
    docstring: string,             // Documentation string
    code_snippet: string,          // Function code
    signature: string,             // Function signature
    calls_count: int,              // Number of function calls
    called_by_count: int,          // Times called by others
    risk_score: float,             // Risk assessment score
    importance: int,               // Importance ranking
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT function_id IF NOT EXISTS 
FOR (f:Function) REQUIRE f.id IS UNIQUE;

// Indexes
CREATE INDEX function_name IF NOT EXISTS 
FOR (f:Function) ON (f.name);

CREATE INDEX function_file IF NOT EXISTS 
FOR (f:Function) ON (f.file_path);

CREATE FULLTEXT INDEX function_search IF NOT EXISTS 
FOR (f:Function) ON EACH [f.name, f.docstring];
```

---

### 4. Class Node

Represents a class or interface.

```cypher
(:Class {
    id: string,                    // Unique identifier
    name: string,                  // Class name
    qualified_name: string,        // Fully qualified name
    file_path: string,             // Source file path
    line_start: int,               // Starting line number
    line_end: int,                 // Ending line number
    type: string,                  // "class" | "interface" | "abstract"
    is_exported: boolean,          // Is exported
    is_abstract: boolean,          // Is abstract class
    methods: list<string>,         // Method names
    properties: list<map>,         // Property definitions
    extends: string,               // Parent class
    implements: list<string>,      // Implemented interfaces
    decorators: list<string>,      // Decorators/annotations
    docstring: string,             // Documentation string
    complexity: int,               // Overall complexity
    risk_score: float,             // Risk assessment score
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT class_id IF NOT EXISTS 
FOR (c:Class) REQUIRE c.id IS UNIQUE;

// Indexes
CREATE INDEX class_name IF NOT EXISTS 
FOR (c:Class) ON (c.name);

CREATE FULLTEXT INDEX class_search IF NOT EXISTS 
FOR (c:Class) ON EACH [c.name, c.docstring];
```

---

### 5. Service Node

Represents a microservice or major system component.

```cypher
(:Service {
    id: string,                    // Unique identifier
    name: string,                  // Service name
    type: string,                  // "api" | "worker" | "gateway" | "database"
    description: string,           // Service description
    base_path: string,             // Base directory path
    entry_point: string,           // Main entry file
    port: int,                     // Service port
    dependencies: list<string>,    // External dependencies
    endpoints_count: int,          // Number of API endpoints
    functions_count: int,          // Number of functions
    risk_score: float,             // Risk assessment score
    importance: int,               // Importance ranking
    status: string,                // "active" | "deprecated" | "experimental"
    version: string,               // Service version
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT service_id IF NOT EXISTS 
FOR (s:Service) REQUIRE s.id IS UNIQUE;

// Indexes
CREATE INDEX service_name IF NOT EXISTS 
FOR (s:Service) ON (s.name);

CREATE INDEX service_type IF NOT EXISTS 
FOR (s:Service) ON (s.type);
```

---

### 6. API Node

Represents an API endpoint.

```cypher
(:API {
    id: string,                    // Unique identifier
    endpoint: string,              // API endpoint path
    method: string,                // HTTP method
    handler: string,               // Handler function name
    file_path: string,             // Source file path
    line_number: int,              // Line number
    auth_required: boolean,        // Requires authentication
    auth_type: string,             // Authentication type
    rate_limit: int,               // Rate limit per minute
    timeout_ms: int,               // Timeout in milliseconds
    request_schema: map,           // Request body schema
    response_schema: map,          // Response schema
    query_params: list<map>,       // Query parameters
    path_params: list<map>,        // Path parameters
    description: string,           // Endpoint description
    tags: list<string>,            // API tags
    deprecated: boolean,           // Is deprecated
    version: string,               // API version
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT api_id IF NOT EXISTS 
FOR (a:API) REQUIRE a.id IS UNIQUE;

// Indexes
CREATE INDEX api_endpoint IF NOT EXISTS 
FOR (a:API) ON (a.endpoint);

CREATE INDEX api_method IF NOT EXISTS 
FOR (a:API) ON (a.method);
```

---

### 7. Database Node

Represents a database or data store.

```cypher
(:Database {
    id: string,                    // Unique identifier
    name: string,                  // Database name
    type: string,                  // "sql" | "nosql" | "cache" | "queue"
    engine: string,                // Database engine
    host: string,                  // Database host
    port: int,                     // Database port
    schema: string,                // Database schema
    tables: list<string>,          // Table/collection names
    connection_pool_size: int,     // Connection pool size
    read_replicas: int,            // Number of read replicas
    description: string,           // Database description
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT database_id IF NOT EXISTS 
FOR (d:Database) REQUIRE d.id IS UNIQUE;

// Indexes
CREATE INDEX database_name IF NOT EXISTS 
FOR (d:Database) ON (d.name);
```

---

### 8. Queue Node

Represents a message queue or event stream.

```cypher
(:Queue {
    id: string,                    // Unique identifier
    name: string,                  // Queue name
    type: string,                  // "queue" | "topic" | "stream"
    engine: string,                // Queue engine
    topics: list<string>,          // Topic names
    consumers: list<string>,       // Consumer service names
    producers: list<string>,       // Producer service names
    message_format: string,        // Message format
    retention_hours: int,          // Message retention
    description: string,           // Queue description
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT queue_id IF NOT EXISTS 
FOR (q:Queue) REQUIRE q.id IS UNIQUE;

// Indexes
CREATE INDEX queue_name IF NOT EXISTS 
FOR (q:Queue) ON (q.name);
```

---

### 9. Workflow Node

Represents an engineering workflow.

```cypher
(:Workflow {
    id: string,                    // Unique identifier
    name: string,                  // Workflow name
    type: string,                  // "ci_cd" | "testing" | "deployment" | "documentation"
    description: string,           // Workflow description
    steps: list<map>,              // Workflow steps
    triggers: list<string>,        // Trigger conditions
    status: string,                // "active" | "paused" | "failed"
    last_run: datetime,            // Last execution time
    success_rate: float,           // Success rate percentage
    avg_duration_ms: int,          // Average duration
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT workflow_id IF NOT EXISTS 
FOR (w:Workflow) REQUIRE w.id IS UNIQUE;

// Indexes
CREATE INDEX workflow_name IF NOT EXISTS 
FOR (w:Workflow) ON (w.name);
```

---

### 10. Module Node

Represents a code module or package.

```cypher
(:Module {
    id: string,                    // Unique identifier
    name: string,                  // Module name
    path: string,                  // Module path
    type: string,                  // "internal" | "external" | "builtin"
    version: string,               // Module version
    exports: list<string>,         // Exported entities
    imports: list<string>,         // Imported modules
    description: string,           // Module description
    is_entry_point: boolean,       // Is entry point
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT module_id IF NOT EXISTS 
FOR (m:Module) REQUIRE m.id IS UNIQUE;

// Indexes
CREATE INDEX module_name IF NOT EXISTS 
FOR (m:Module) ON (m.name);
```

---

### 11. Variable Node

Represents a significant variable or constant.

```cypher
(:Variable {
    id: string,                    // Unique identifier
    name: string,                  // Variable name
    type: string,                  // Variable type
    scope: string,                 // "global" | "local" | "module"
    file_path: string,             // Source file path
    line_number: int,              // Line number
    is_constant: boolean,          // Is constant
    is_exported: boolean,          // Is exported
    value: string,                 // Initial value
    description: string,           // Variable description
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT variable_id IF NOT EXISTS 
FOR (v:Variable) REQUIRE v.id IS UNIQUE;
```

---

### 12. Middleware Node

Represents middleware or interceptor.

```cypher
(:Middleware {
    id: string,                    // Unique identifier
    name: string,                  // Middleware name
    type: string,                  // "auth" | "logging" | "validation" | "error"
    file_path: string,             // Source file path
    line_number: int,              // Line number
    order: int,                    // Execution order
    applies_to: list<string>,      // Routes it applies to
    description: string,           // Middleware description
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT middleware_id IF NOT EXISTS 
FOR (m:Middleware) REQUIRE m.id IS UNIQUE;
```

---

### 13. Test Node

Represents a test case or test suite.

```cypher
(:Test {
    id: string,                    // Unique identifier
    name: string,                  // Test name
    type: string,                  // "unit" | "integration" | "e2e"
    file_path: string,             // Test file path
    line_number: int,              // Line number
    target: string,                // What is being tested
    status: string,                // "passing" | "failing" | "skipped"
    duration_ms: int,              // Test duration
    coverage: float,               // Code coverage percentage
    description: string,           // Test description
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT test_id IF NOT EXISTS 
FOR (t:Test) REQUIRE t.id IS UNIQUE;
```

---

### 14. Configuration Node

Represents configuration files or settings.

```cypher
(:Configuration {
    id: string,                    // Unique identifier
    name: string,                  // Config name
    file_path: string,             // Config file path
    type: string,                  // "env" | "json" | "yaml" | "toml"
    environment: string,           // "development" | "staging" | "production"
    settings: map,                 // Configuration settings
    secrets: list<string>,         // Secret keys (not values)
    description: string,           // Configuration description
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT config_id IF NOT EXISTS 
FOR (c:Configuration) REQUIRE c.id IS UNIQUE;
```

---

### 15. Infrastructure Node

Represents infrastructure components.

```cypher
(:Infrastructure {
    id: string,                    // Unique identifier
    name: string,                  // Component name
    type: string,                  // "container" | "pod" | "vm" | "serverless"
    provider: string,              // Cloud provider
    region: string,                // Deployment region
    resources: map,                // Resource allocation
    status: string,                // "running" | "stopped" | "error"
    description: string,           // Component description
    metadata: map                  // Additional metadata
})

// Constraints
CREATE CONSTRAINT infra_id IF NOT EXISTS 
FOR (i:Infrastructure) REQUIRE i.id IS UNIQUE;
```

---

## Relationship Types

### 1. CONTAINS

Repository contains files, services contain functions.

```cypher
(:Repository)-[:CONTAINS {
    created_at: datetime           // When added
}]->(:File|Service)

(:File)-[:CONTAINS {
    line_start: int,               // Starting line
    line_end: int                  // Ending line
}]->(:Function|Class)

(:Service)-[:CONTAINS {
    role: string                   // Component role
}]->(:Function|API)
```

---

### 2. CALLS

Function calls another function.

```cypher
(:Function)-[:CALLS {
    line_number: int,              // Call location
    execution_order: int,          // Order in execution
    frequency: int,                // Call frequency
    latency_ms: float,             // Average latency
    failure_rate: float,           // Failure rate
    is_async: boolean,             // Is async call
    is_conditional: boolean,       // Is conditional call
    call_type: string              // "direct" | "callback" | "promise"
}]->(:Function)
```

---

### 3. DEPENDS_ON

Dependency relationships.

```cypher
(:Service)-[:DEPENDS_ON {
    dependency_type: string,       // "runtime" | "build" | "dev"
    critical: boolean,             // Is critical dependency
    version: string,               // Required version
    optional: boolean,             // Is optional
    fallback_available: boolean    // Has fallback
}]->(:Service|Module)

(:Function)-[:DEPENDS_ON {
    dependency_type: string,       // Type of dependency
    required: boolean              // Is required
}]->(:Function|Class|Module)
```

---

### 4. IMPORTS

Import relationships.

```cypher
(:File)-[:IMPORTS {
    line_number: int,              // Import location
    import_type: string,           // "default" | "named" | "namespace"
    imported_names: list<string>,  // Imported entities
    alias: string                  // Import alias
}]->(:File|Module)

(:Function)-[:IMPORTS {
    line_number: int,              // Import location
    usage_count: int               // Times used
}]->(:Module)
```

---

### 5. EXPORTS

Export relationships.

```cypher
(:File)-[:EXPORTS {
    export_type: string,           // "default" | "named"
    exported_names: list<string>   // Exported entities
}]->(:Function|Class|Variable)
```

---

### 6. EXTENDS

Inheritance relationships.

```cypher
(:Class)-[:EXTENDS {
    override_methods: list<string>, // Overridden methods
    inherited_methods: list<string> // Inherited methods
}]->(:Class)
```

---

### 7. IMPLEMENTS

Interface implementation.

```cypher
(:Class)-[:IMPLEMENTS {
    implemented_methods: list<string> // Implemented methods
}]->(:Class)
```

---

### 8. WRITES_TO

Database write operations.

```cypher
(:Function|Service)-[:WRITES_TO {
    operation: string,             // "insert" | "update" | "delete"
    table: string,                 // Table/collection name
    frequency: int,                // Write frequency
    batch_size: int,               // Batch size
    transaction: boolean           // Uses transaction
}]->(:Database)
```

---

### 9. READS_FROM

Database read operations.

```cypher
(:Function|Service)-[:READS_FROM {
    query_type: string,            // "select" | "find" | "aggregate"
    table: string,                 // Table/collection name
    frequency: int,                // Read frequency
    cache_enabled: boolean,        // Uses caching
    index_used: boolean            // Uses index
}]->(:Database)
```

---

### 10. CALLS_API

API call relationships.

```cypher
(:Function|Service)-[:CALLS_API {
    method: string,                // HTTP method
    endpoint: string,              // API endpoint
    timeout_ms: int,               // Request timeout
    retry_count: int,              // Retry attempts
    circuit_breaker: boolean       // Uses circuit breaker
}]->(:API)
```

---

### 11. HANDLES

API handler relationships.

```cypher
(:API)-[:HANDLES {
    handler_type: string           // "controller" | "middleware"
}]->(:Function)
```

---

### 12. TRIGGERS

Event trigger relationships.

```cypher
(:Function|Service)-[:TRIGGERS {
    event_type: string,            // Event type
    async: boolean,                // Is async
    payload_schema: map            // Event payload schema
}]->(:Queue)
```

---

### 13. LISTENS_TO

Event listener relationships.

```cypher
(:Function|Service)-[:LISTENS_TO {
    event_type: string,            // Event type
    handler: string,               // Handler function
    priority: int                  // Listener priority
}]->(:Queue)
```

---

### 14. USES_MIDDLEWARE

Middleware usage.

```cypher
(:API|Service)-[:USES_MIDDLEWARE {
    order: int,                    // Execution order
    required: boolean              // Is required
}]->(:Middleware)
```

---

### 15. TESTS

Test relationships.

```cypher
(:Test)-[:TESTS {
    coverage: float,               // Coverage percentage
    assertions: int                // Number of assertions
}]->(:Function|Class|API)
```

---

### 16. CONFIGURES

Configuration relationships.

```cypher
(:Configuration)-[:CONFIGURES {
    settings: list<string>         // Configured settings
}]->(:Service|Database|Queue)
```

---

### 17. DEPLOYS_TO

Deployment relationships.

```cypher
(:Service)-[:DEPLOYS_TO {
    environment: string,           // Deployment environment
    replicas: int,                 // Number of replicas
    resources: map                 // Resource allocation
}]->(:Infrastructure)
```

---

### 18. FAILS_BECAUSE_OF

Failure propagation.

```cypher
(:Service|Function)-[:FAILS_BECAUSE_OF {
    probability: float,            // Failure probability
    impact_severity: string,       // "low" | "medium" | "high" | "critical"
    propagation_time_ms: int,      // Propagation time
    mitigation: string             // Mitigation strategy
}]->(:Service|Function|Database)
```

---

### 19. ORCHESTRATES

Workflow orchestration.

```cypher
(:Workflow)-[:ORCHESTRATES {
    step_number: int,              // Step number
    condition: string,             // Execution condition
    timeout_ms: int                // Step timeout
}]->(:Service|Function)
```

---

### 20. BELONGS_TO

Ownership relationships.

```cypher
(:File|Function|Class)-[:BELONGS_TO {
    role: string                   // Component role
}]->(:Service|Module)
```

---

## Indexes and Constraints

### Full-Text Search Indexes

```cypher
// Search across all code entities
CREATE FULLTEXT INDEX entity_search IF NOT EXISTS
FOR (n:Function|Class|Service|API)
ON EACH [n.name, n.description, n.docstring];

// Search files
CREATE FULLTEXT INDEX file_search IF NOT EXISTS
FOR (f:File)
ON EACH [f.name, f.path];

// Search workflows
CREATE FULLTEXT INDEX workflow_search IF NOT EXISTS
FOR (w:Workflow)
ON EACH [w.name, w.description];
```

### Composite Indexes

```cypher
// Function lookup by file and line
CREATE INDEX function_location IF NOT EXISTS
FOR (f:Function) ON (f.file_path, f.line_start);

// API lookup by method and endpoint
CREATE INDEX api_route IF NOT EXISTS
FOR (a:API) ON (a.method, a.endpoint);

// Service lookup by type and status
CREATE INDEX service_status IF NOT EXISTS
FOR (s:Service) ON (s.type, s.status);
```

---

## Query Patterns

### 1. Find All Functions in a File

```cypher
MATCH (f:File {path: $file_path})-[:CONTAINS]->(fn:Function)
RETURN fn
ORDER BY fn.line_start;
```

### 2. Trace Function Call Chain

```cypher
MATCH path = (start:Function {id: $function_id})-[:CALLS*1..5]->(end:Function)
RETURN path;
```

### 3. Find Service Dependencies

```cypher
MATCH (s:Service {id: $service_id})-[:DEPENDS_ON*1..3]->(dep)
RETURN s, dep;
```

### 4. Find Database Interactions

```cypher
MATCH (s:Service {id: $service_id})-[:CONTAINS]->(f:Function)
MATCH (f)-[r:WRITES_TO|READS_FROM]->(db:Database)
RETURN f, type(r) as operation, db;
```

### 5. Find Failure Propagation Path

```cypher
MATCH path = (failed:Service {id: $failed_service_id})
             -[:FAILS_BECAUSE_OF*1..5]->(affected)
RETURN path
ORDER BY length(path);
```

### 6. Find API Endpoints for Service

```cypher
MATCH (s:Service {id: $service_id})-[:CONTAINS]->(api:API)
RETURN api
ORDER BY api.endpoint;
```

### 7. Find Most Complex Functions

```cypher
MATCH (f:Function)
WHERE f.complexity > 10
RETURN f
ORDER BY f.complexity DESC
LIMIT 20;
```

### 8. Find Untested Functions

```cypher
MATCH (f:Function)
WHERE NOT EXISTS {
    MATCH (t:Test)-[:TESTS]->(f)
}
RETURN f;
```

---

## Performance Optimization

### Query Optimization Tips

1. **Use Indexes**: Always create indexes on frequently queried properties
2. **Limit Depth**: Use depth limits in path queries to prevent expensive traversals
3. **Use PROFILE**: Profile queries to identify bottlenecks
4. **Batch Operations**: Use batch operations for bulk inserts/updates
5. **Connection Pooling**: Use connection pooling for concurrent queries

### Recommended Settings

```properties
# neo4j.conf
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
dbms.memory.pagecache.size=2G
dbms.connector.bolt.thread_pool_max_size=400
```

---

## Data Migration Strategy

### Version 1.0 Schema

Initial schema with core node and relationship types.

### Future Versions

- Add new node types as needed
- Add new relationship types for new features
- Maintain backward compatibility
- Use schema versioning in metadata

---

## Conclusion

This comprehensive Neo4j schema provides the foundation for GraphMind AI's semantic graph intelligence. The schema is designed to:

1. Capture rich engineering semantics
2. Support complex traversal queries
3. Enable AI-powered analysis
4. Scale to large repositories
5. Maintain query performance

The schema will evolve as new features are added, but the core structure provides a solid foundation for the platform's graph intelligence capabilities.