"""
Mock AI Service - Temporary replacement for IBM watsonx.ai
This provides hardcoded responses until Python 3.12 is installed
"""
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """Mock service for AI-powered graph intelligence"""
    
    def __init__(self):
        """Initialize mock AI service"""
        print("WARNING: Using MOCK AI Service (Python 3.13 compatibility mode)")
        print("         To use real IBM watsonx.ai, install Python 3.12")
        
        # Mock responses for different node types
        self.mock_responses = {
            "service": "This is a microservice component that handles specific business logic. It communicates with other services through APIs and may interact with databases or message queues.",
            "database": "This is a database system that stores and manages application data. It provides persistent storage and supports CRUD operations for the application.",
            "cache": "This is a caching layer that stores frequently accessed data in memory for fast retrieval. It reduces database load and improves application performance.",
            "queue": "This is a message queue system that enables asynchronous communication between services. It helps decouple services and handle high-volume message processing.",
            "api": "This is an API endpoint that exposes functionality to external clients or other services. It handles HTTP requests and returns appropriate responses.",
            "gateway": "This is an API gateway that acts as a single entry point for all client requests. It handles routing, authentication, rate limiting, and load balancing."
        }
    
    async def explain_node(
        self, 
        node: Dict[str, Any], 
        connections: Dict[str, List[Dict]], 
        user_context: Optional[str] = None
    ) -> str:
        """
        Generate mock AI explanation for a node
        """
        node_type = node.get("type", "service").lower()
        node_label = node.get("label", "Unknown")
        node_desc = node.get("description", "")
        
        # Get base explanation
        base_explanation = self.mock_responses.get(node_type, self.mock_responses["service"])
        
        # Build detailed explanation
        explanation = f"**{node_label}**\n\n"
        explanation += f"{base_explanation}\n\n"
        
        if node_desc:
            explanation += f"**Description:** {node_desc}\n\n"
        
        # Add connection information
        incoming = connections.get("incoming", [])
        outgoing = connections.get("outgoing", [])
        
        if incoming:
            explanation += f"**Incoming Connections ({len(incoming)}):**\n"
            for conn in incoming[:3]:  # Show first 3
                explanation += f"- {conn.get('source_label', 'Unknown')} → {conn.get('type', 'CONNECTS')}\n"
            if len(incoming) > 3:
                explanation += f"- ... and {len(incoming) - 3} more\n"
            explanation += "\n"
        
        if outgoing:
            explanation += f"**Outgoing Connections ({len(outgoing)}):**\n"
            for conn in outgoing[:3]:  # Show first 3
                explanation += f"- {conn.get('type', 'CONNECTS')} → {conn.get('target_label', 'Unknown')}\n"
            if len(outgoing) > 3:
                explanation += f"- ... and {len(outgoing) - 3} more\n"
            explanation += "\n"
        
        explanation += "\n*Note: This is a mock response. Install Python 3.12 for real AI explanations.*"
        
        return explanation
    
    async def answer_query(
        self, 
        query: str, 
        graph_context: Dict[str, Any]
    ) -> str:
        """
        Generate mock AI answer for a user query
        """
        query_lower = query.lower()
        
        # Pattern matching for common queries
        if "authentication" in query_lower or "auth" in query_lower:
            return """**Authentication Flow:**

The authentication system uses a multi-layered approach:

1. **AuthService** receives login requests
2. Validates credentials against the database
3. Generates JWT tokens using **JWTService**
4. Stores session data in **Redis** cache
5. Returns token to client

This ensures secure user authentication with fast token validation.

*Note: This is a mock response. Install Python 3.12 for real AI explanations.*"""
        
        elif "payment" in query_lower:
            return """**Payment Workflow:**

The payment processing follows these steps:

1. User initiates payment through **CartService**
2. **PaymentService** validates payment details
3. Processes payment through external gateway
4. Updates order status in **OrderService**
5. Sends confirmation via **RabbitMQ**

This ensures secure and reliable payment processing.

*Note: This is a mock response. Install Python 3.12 for real AI explanations.*"""
        
        elif "redis" in query_lower or "cache" in query_lower:
            return """**Redis Usage:**

Redis is used as a caching layer for:

- **Session Storage**: User authentication tokens
- **Rate Limiting**: API request throttling
- **Temporary Data**: Shopping cart contents
- **Performance**: Frequently accessed data

Services that depend on Redis:
- AuthService
- CartService
- APIGateway

*Note: This is a mock response. Install Python 3.12 for real AI explanations.*"""
        
        elif "fail" in query_lower or "break" in query_lower:
            return """**Failure Impact Analysis:**

If a critical service fails, the impact propagates through:

1. **Direct Dependencies**: Services that directly call the failed service
2. **Downstream Effects**: Services that depend on those services
3. **User Impact**: Features that become unavailable

Example: If AuthService fails:
- Login/Logout stops working
- Protected APIs become inaccessible
- User sessions cannot be validated

Mitigation strategies:
- Implement circuit breakers
- Add fallback mechanisms
- Use service mesh for resilience

*Note: This is a mock response. Install Python 3.12 for real AI explanations.*"""
        
        else:
            return f"""**Query: {query}**

Based on the graph structure, here's what I can tell you:

The system consists of multiple interconnected services that work together to provide functionality. Each service has specific responsibilities and communicates with others through well-defined interfaces.

Key components include:
- Microservices for business logic
- Databases for data persistence
- Caching layers for performance
- Message queues for async communication

For more specific information, try asking about:
- Authentication flow
- Payment processing
- Service dependencies
- Failure scenarios

*Note: This is a mock response. Install Python 3.12 for real AI explanations.*"""
    
    async def analyze_workflow(
        self, 
        workflow: Dict[str, Any]
    ) -> str:
        """
        Generate mock AI analysis for a workflow
        """
        workflow_name = workflow.get("name", "Unknown Workflow")
        steps = workflow.get("steps", [])
        
        analysis = f"**{workflow_name} Analysis**\n\n"
        analysis += f"This workflow consists of {len(steps)} steps:\n\n"
        
        for i, step in enumerate(steps, 1):
            analysis += f"{i}. **{step.get('name', 'Step')}**: {step.get('description', 'Processing step')}\n"
        
        analysis += "\n**Key Characteristics:**\n"
        analysis += "- Sequential execution flow\n"
        analysis += "- Error handling at each step\n"
        analysis += "- Data validation throughout\n"
        analysis += "- Asynchronous where possible\n\n"
        
        analysis += "*Note: This is a mock response. Install Python 3.12 for real AI explanations.*"
        
        return analysis

# Made with Bob
