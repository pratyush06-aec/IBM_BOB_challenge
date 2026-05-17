"""
AI Service - IBM watsonx.ai Integration
Handles all AI-powered explanations and queries
"""
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import IBM watsonx.ai, fall back to None if not available
try:
    from ibm_watsonx_ai.foundation_models import Model
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False
    Model = None
    GenParams = None
    print("WARNING: ibm_watsonx_ai not available. AI features will use mock responses.")

class AIService:
    """Service for AI-powered graph intelligence"""
    
    def __init__(self):
        """Initialize IBM watsonx.ai client"""
        if not WATSONX_AVAILABLE:
            print("WARNING: Using MOCK AI Service (ibm_watsonx_ai not installed)")
            print("         Install ibm-watsonx-ai for real AI features")
            self.model = None
            return
            
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        
        if not self.api_key or not self.project_id:
            print("WARNING: WATSONX_API_KEY or WATSONX_PROJECT_ID not set")
            print("         Using mock AI responses")
            self.model = None
            return
        
        # Initialize model
        try:
            self.model = Model(
                model_id="ibm/granite-13b-chat-v2",
                params={
                    GenParams.DECODING_METHOD: "greedy",
                    GenParams.MAX_NEW_TOKENS: 500,
                    GenParams.MIN_NEW_TOKENS: 1,
                    GenParams.TEMPERATURE: 0.7,
                    GenParams.TOP_K: 50,
                    GenParams.TOP_P: 1
                },
                credentials={
                    "apikey": self.api_key,
                    "url": self.url
                },
                project_id=self.project_id
            )
        except Exception as e:
            print(f"WARNING: Failed to initialize watsonx.ai: {e}")
            print("         Using mock AI responses")
            self.model = None
    
    async def explain_node(
        self, 
        node: Dict[str, Any], 
        connections: Dict[str, List[Dict]], 
        user_context: Optional[str] = None
    ) -> str:
        """
        Generate AI explanation for a node
        
        Args:
            node: Node data
            connections: Connected nodes (incoming and outgoing)
            user_context: Optional user context
            
        Returns:
            AI-generated explanation
        """
        # Build context
        node_type = node.get("type", "Unknown")
        node_label = node.get("label", "Unknown")
        properties = node.get("properties", {})
        
        # Format connections
        incoming = connections.get("incoming", [])
        outgoing = connections.get("outgoing", [])
        
        incoming_desc = ", ".join([f"{e['source_label']} ({e['type']})" for e in incoming[:3]])
        outgoing_desc = ", ".join([f"{e['target_label']} ({e['type']})" for e in outgoing[:3]])
        
        # Build prompt
        prompt = f"""You are an expert software architect analyzing a code repository graph.

Node Information:
- Type: {node_type}
- Name: {node_label}
- Description: {properties.get('description', 'N/A')}

Properties:
{self._format_properties(properties)}

Connections:
- Called by: {incoming_desc if incoming else 'None'}
- Calls: {outgoing_desc if outgoing else 'None'}

{f"User Context: {user_context}" if user_context else ""}

Provide a clear, concise explanation of this {node_type} including:
1. Its purpose and functionality
2. Its role in the system
3. Key relationships and dependencies
4. Any notable characteristics or concerns

Keep the explanation technical but accessible, around 3-4 sentences."""

        # Use mock response if model not available
        if self.model is None:
            return self._generate_mock_explanation(node, connections)
        
        try:
            # Generate response
            response = self.model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    async def process_query(
        self,
        query: str,
        graph_data: Dict[str, Any],
        context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Process natural language query about the graph
        
        Args:
            query: User's natural language query
            graph_data: Complete graph data
            context: Optional context from previous queries
            
        Returns:
            Query result with answer and highlighted nodes
        """
        # Build graph summary
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        # Count node types
        node_types = {}
        for node in nodes:
            node_type = node.get("type", "Unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # Build prompt
        prompt = f"""You are an expert software architect analyzing an e-commerce application.

System Overview:
- Total Nodes: {len(nodes)}
- Total Edges: {len(edges)}
- Node Types: {', '.join([f"{k}: {v}" for k, v in node_types.items()])}

Key Services:
- Auth Service: Handles authentication and authorization
- Products Service: Manages product catalog
- Cart Service: Manages shopping cart
- Payment Service: Processes payments
- Orders Service: Manages orders

User Question: {query}

{f"Previous Context: {', '.join(context)}" if context else ""}

Provide a clear, technical answer that:
1. Directly answers the question
2. References specific services/components
3. Explains the workflow or architecture
4. Mentions key relationships

Keep the answer concise but informative (3-5 sentences)."""

        # Use mock response if model not available
        if self.model is None:
            highlighted_nodes = self._find_relevant_nodes(query, nodes)
            return {
                "answer": self._generate_mock_query_response(query),
                "highlighted_nodes": highlighted_nodes,
                "confidence": 0.75,
                "sources": [{"node_id": n, "relevance": 0.8} for n in highlighted_nodes[:3]]
            }
        
        try:
            # Generate response
            answer = self.model.generate_text(prompt=prompt)
            
            # Find relevant nodes based on query keywords
            highlighted_nodes = self._find_relevant_nodes(query, nodes)
            
            return {
                "answer": answer.strip(),
                "highlighted_nodes": highlighted_nodes,
                "confidence": 0.85,
                "sources": [{"node_id": n, "relevance": 0.9} for n in highlighted_nodes[:3]]
            }
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "highlighted_nodes": [],
                "confidence": 0.0,
                "sources": []
            }
    
    async def analyze_workflow(self, workflow: Dict[str, Any]) -> str:
        """
        Analyze a workflow and provide insights
        
        Args:
            workflow: Workflow data
            
        Returns:
            AI-generated workflow analysis
        """
        workflow_name = workflow.get("name", "Unknown")
        description = workflow.get("description", "")
        steps = workflow.get("steps", [])
        
        # Build steps description
        steps_desc = "\n".join([
            f"{i+1}. {step.get('description', 'N/A')}"
            for i, step in enumerate(steps)
        ])
        
        prompt = f"""You are an expert software architect analyzing a workflow.

Workflow: {workflow_name}
Description: {description}

Steps:
{steps_desc}

Provide a technical analysis including:
1. Overall workflow purpose and design
2. Key steps and their importance
3. Potential bottlenecks or issues
4. Suggestions for optimization

Keep the analysis concise (4-5 sentences)."""

        # Use mock response if model not available
        if self.model is None:
            return self._generate_mock_workflow_analysis(workflow)
        
        try:
            response = self.model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as e:
            return f"Error analyzing workflow: {str(e)}"
    
    def _format_properties(self, properties: Dict[str, Any]) -> str:
        """Format properties for display"""
        formatted = []
        for key, value in properties.items():
            if key not in ['description', 'name']:
                formatted.append(f"- {key}: {value}")
        return "\n".join(formatted) if formatted else "No additional properties"
    
    def _find_relevant_nodes(self, query: str, nodes: List[Dict]) -> List[str]:
        """Find nodes relevant to the query"""
        query_lower = query.lower()
        relevant = []
        
        # Keywords mapping
        keywords = {
            "auth": ["service_auth", "api_login", "api_register", "func_authenticate"],
            "login": ["api_login", "func_authenticate", "func_validate_password"],
            "product": ["service_products", "api_get_products", "func_get_products"],
            "cart": ["service_cart", "api_add_to_cart", "func_add_to_cart"],
            "payment": ["service_payment", "func_process_payment"],
            "order": ["service_orders", "func_create_order"],
            "checkout": ["api_checkout", "func_create_order", "func_process_payment"],
            "database": ["db_users", "db_products", "db_orders"],
            "cache": ["cache_redis"]
        }
        
        # Find matching nodes
        for keyword, node_ids in keywords.items():
            if keyword in query_lower:
                relevant.extend(node_ids)
        
        # Remove duplicates and limit
        return list(set(relevant))[:5]
    
    def _generate_mock_explanation(self, node: Dict[str, Any], connections: Dict[str, List[Dict]]) -> str:
        """Generate mock explanation when AI is not available"""
        node_type = node.get("type", "Unknown")
        node_label = node.get("label", "Unknown")
        properties = node.get("properties", {})
        
        explanation = f"**{node_label}** ({node_type})\n\n"
        
        # Type-specific explanations
        type_explanations = {
            "service": "This is a microservice component that handles specific business logic.",
            "api": "This is an API endpoint that exposes functionality to clients.",
            "database": "This is a database system that stores and manages application data.",
            "cache": "This is a caching layer that stores frequently accessed data in memory.",
            "function": "This is a function that performs a specific operation.",
            "class": "This is a class that encapsulates data and behavior.",
        }
        
        explanation += type_explanations.get(node_type.lower(), "This is a component in the system.")
        explanation += "\n\n"
        
        # Add connections info
        incoming = connections.get("incoming", [])
        outgoing = connections.get("outgoing", [])
        
        if incoming:
            explanation += f"**Called by:** {len(incoming)} component(s)\n"
        if outgoing:
            explanation += f"**Calls:** {len(outgoing)} component(s)\n"
        
        explanation += "\n*Note: This is a mock response. Install ibm-watsonx-ai for AI-powered explanations.*"
        return explanation
    
    def _generate_mock_query_response(self, query: str) -> str:
        """Generate mock query response when AI is not available"""
        query_lower = query.lower()
        
        if "auth" in query_lower or "login" in query_lower:
            return "The authentication system handles user login, registration, and session management. It validates credentials and generates secure tokens for authenticated users.\n\n*Note: This is a mock response. Install ibm-watsonx-ai for AI-powered answers.*"
        elif "payment" in query_lower:
            return "The payment system processes transactions securely, validates payment details, and coordinates with external payment gateways to complete purchases.\n\n*Note: This is a mock response. Install ibm-watsonx-ai for AI-powered answers.*"
        elif "database" in query_lower or "data" in query_lower:
            return "The database layer stores and manages application data, providing persistent storage and supporting CRUD operations across the system.\n\n*Note: This is a mock response. Install ibm-watsonx-ai for AI-powered answers.*"
        else:
            return f"Based on your query about '{query}', the system consists of interconnected components that work together to provide functionality. Each component has specific responsibilities and communicates through well-defined interfaces.\n\n*Note: This is a mock response. Install ibm-watsonx-ai for AI-powered answers.*"
    
    def _generate_mock_workflow_analysis(self, workflow: Dict[str, Any]) -> str:
        """Generate mock workflow analysis when AI is not available"""
        workflow_name = workflow.get("name", "Unknown Workflow")
        steps = workflow.get("steps", [])
        
        analysis = f"**{workflow_name}**\n\n"
        analysis += f"This workflow consists of {len(steps)} steps that execute in sequence. "
        analysis += "Each step performs a specific operation and passes data to the next step. "
        analysis += "The workflow includes error handling and validation at each stage.\n\n"
        analysis += "*Note: This is a mock response. Install ibm-watsonx-ai for AI-powered analysis.*"
        
        return analysis

# Made with Bob
