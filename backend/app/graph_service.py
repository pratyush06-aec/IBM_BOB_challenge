"""
Graph Service - Manages graph data operations
Loads and serves the sample e-commerce graph
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class GraphService:
    """Service for graph data operations"""
    
    def __init__(self):
        """Initialize graph service and load data"""
        self.graph_data = self._load_graph_data()
        self.nodes = {node["id"]: node for node in self.graph_data.get("nodes", [])}
        self.edges = self.graph_data.get("edges", [])
        self.workflows = {wf["id"]: wf for wf in self.graph_data.get("workflows", [])}
        
        # Build edge index for quick lookups
        self.incoming_edges = {}
        self.outgoing_edges = {}
        for edge in self.edges:
            source = edge["source"]
            target = edge["target"]
            
            if target not in self.incoming_edges:
                self.incoming_edges[target] = []
            self.incoming_edges[target].append(edge)
            
            if source not in self.outgoing_edges:
                self.outgoing_edges[source] = []
            self.outgoing_edges[source].append(edge)
    
    def _load_graph_data(self) -> Dict[str, Any]:
        """Load graph data from JSON file"""
        # Try multiple possible locations
        possible_paths = [
            Path(__file__).parent.parent / "data" / "sample_graph.json",
            Path(__file__).parent.parent.parent / "sample-graph.json",
            Path("sample-graph.json"),
            Path("data/sample_graph.json")
        ]
        
        for path in possible_paths:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        # If no file found, return empty graph
        print("Warning: Could not find sample-graph.json, using empty graph")
        return {"nodes": [], "edges": [], "workflows": []}
    
    def get_graph(self) -> Dict[str, Any]:
        """Get complete graph data"""
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "metadata": self.graph_data.get("metadata", {})
        }
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific node by ID"""
        return self.nodes.get(node_id)
    
    def get_node_connections(self, node_id: str) -> Dict[str, List[Dict]]:
        """
        Get all connections for a node
        
        Returns:
            Dictionary with 'incoming' and 'outgoing' edge lists
        """
        incoming = []
        for edge in self.incoming_edges.get(node_id, []):
            source_node = self.nodes.get(edge["source"])
            incoming.append({
                "edge_id": edge["id"],
                "source_id": edge["source"],
                "source_label": source_node.get("label", "Unknown") if source_node else "Unknown",
                "type": edge["type"],
                "properties": edge.get("properties", {})
            })
        
        outgoing = []
        for edge in self.outgoing_edges.get(node_id, []):
            target_node = self.nodes.get(edge["target"])
            outgoing.append({
                "edge_id": edge["id"],
                "target_id": edge["target"],
                "target_label": target_node.get("label", "Unknown") if target_node else "Unknown",
                "type": edge["type"],
                "properties": edge.get("properties", {})
            })
        
        return {
            "incoming": incoming,
            "outgoing": outgoing
        }
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific workflow by ID"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        
        # Enrich workflow with node details
        enriched_steps = []
        for step in workflow.get("steps", []):
            node_id = step.get("node_id")
            node = self.nodes.get(node_id)
            enriched_steps.append({
                **step,
                "node": node
            })
        
        return {
            **workflow,
            "steps": enriched_steps
        }
    
    def get_all_workflows(self) -> List[Dict[str, Any]]:
        """Get all workflows"""
        return list(self.workflows.values())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        # Count nodes by type
        node_types = {}
        for node in self.nodes.values():
            node_type = node.get("type", "Unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # Count edges by type
        edge_types = {}
        for edge in self.edges:
            edge_type = edge.get("type", "Unknown")
            edge_types[edge_type] = edge_types.get(edge_type, 0) + 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "total_workflows": len(self.workflows),
            "node_types": node_types,
            "edge_types": edge_types,
            "metadata": self.graph_data.get("metadata", {})
        }
    
    def search_nodes(self, query: str, node_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search nodes by name or properties
        
        Args:
            query: Search query
            node_types: Optional list of node types to filter
            
        Returns:
            List of matching nodes
        """
        query_lower = query.lower()
        results = []
        
        for node in self.nodes.values():
            # Filter by type if specified
            if node_types and node.get("type") not in node_types:
                continue
            
            # Search in label and properties
            label = node.get("label", "").lower()
            properties = node.get("properties", {})
            
            if query_lower in label:
                results.append(node)
                continue
            
            # Search in properties
            for value in properties.values():
                if isinstance(value, str) and query_lower in value.lower():
                    results.append(node)
                    break
        
        return results
    
    def get_path(self, start_node_id: str, end_node_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """
        Find shortest path between two nodes using BFS
        
        Args:
            start_node_id: Starting node ID
            end_node_id: Target node ID
            max_depth: Maximum search depth
            
        Returns:
            List of node IDs representing the path, or None if no path found
        """
        if start_node_id not in self.nodes or end_node_id not in self.nodes:
            return None
        
        if start_node_id == end_node_id:
            return [start_node_id]
        
        # BFS
        queue = [(start_node_id, [start_node_id])]
        visited = {start_node_id}
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            # Check outgoing edges
            for edge in self.outgoing_edges.get(current, []):
                next_node = edge["target"]
                
                if next_node == end_node_id:
                    return path + [next_node]
                
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))
        
        return None

# Made with Bob
