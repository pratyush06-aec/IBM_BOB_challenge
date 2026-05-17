"""
Neo4j Database Service
Manages graph data storage and retrieval using Neo4j
"""

from typing import Dict, List, Optional
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
import os
from dotenv import load_dotenv

load_dotenv()


class Neo4jService:
    """Service for interacting with Neo4j graph database"""
    
    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = os.getenv('NEO4J_USER', 'neo4j')
        self.password = os.getenv('NEO4J_PASSWORD', 'password')
        self.driver = None
        self._connected = False
    
    def _connect(self):
        """Establish connection to Neo4j (lazy connection)"""
        if self._connected:
            return
            
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Verify connectivity
            self.driver.verify_connectivity()
            print(f"[OK] Connected to Neo4j at {self.uri}")
            self._connected = True
        except (ServiceUnavailable, AuthError) as e:
            print(f"[WARNING] Failed to connect to Neo4j: {e}")
            print("[INFO] Falling back to in-memory storage")
            self.driver = None
            self._connected = False
    
    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()
    
    def is_connected(self) -> bool:
        """Check if connected to Neo4j"""
        return self.driver is not None
    
    def create_repository(self, repo_data: Dict) -> str:
        """Create a repository node"""
        if not self.driver:
            return "mock-repo-id"
        
        with self.driver.session() as session:
            result = session.execute_write(
                self._create_repository_tx,
                repo_data
            )
            return result
    
    @staticmethod
    def _create_repository_tx(tx, repo_data):
        """Transaction to create repository"""
        query = """
        CREATE (r:Repository {
            name: $name,
            path: $path,
            branch: $branch,
            commit: $commit,
            author: $author,
            last_modified: $last_modified,
            created_at: datetime()
        })
        RETURN elementId(r) as id
        """
        result = tx.run(query, **repo_data)
        return result.single()['id']
    
    def store_graph_data(self, repo_id: str, graph_data: Dict, user_id: Optional[str] = None):
        """Store parsed graph data in Neo4j"""
        if not self.driver:
            print("⚠️  Neo4j not connected, skipping storage")
            return
        
        with self.driver.session() as session:
            # Store nodes
            for node in graph_data['nodes']:
                session.execute_write(
                    self._create_node_tx,
                    repo_id,
                    node,
                    user_id
                )
            
            # Store edges
            for edge in graph_data['edges']:
                session.execute_write(
                    self._create_edge_tx,
                    repo_id,
                    edge
                )
    
    @staticmethod
    def _create_node_tx(tx, repo_id, node, user_id):
        """Transaction to create a node"""
        query = f"""
        MATCH (r:Repository) WHERE elementId(r) = $repo_id
        CREATE (n:{node['type']} {{
            id: $id,
            label: $label,
            properties: $properties,
            repo_id: $repo_id,
            user_id: $user_id,
            created_at: datetime()
        }})
        CREATE (r)-[:CONTAINS]->(n)
        RETURN elementId(n) as id
        """
        tx.run(
            query,
            repo_id=repo_id,
            id=node['id'],
            label=node['label'],
            properties=node['properties'],
            user_id=user_id
        )
    
    @staticmethod
    def _create_edge_tx(tx, repo_id, edge):
        """Transaction to create an edge"""
        query = """
        MATCH (source) WHERE source.id = $source_id AND source.repo_id = $repo_id
        MATCH (target) WHERE target.id = $target_id AND target.repo_id = $repo_id
        CREATE (source)-[r:RELATES {
            type: $type,
            label: $label,
            properties: $properties
        }]->(target)
        RETURN elementId(r) as id
        """
        tx.run(
            query,
            source_id=edge['source'],
            target_id=edge['target'],
            type=edge['type'],
            label=edge['label'],
            properties=edge['properties'],
            repo_id=repo_id
        )
    
    def get_repository_graph(self, repo_id: str) -> Dict:
        """Retrieve graph data for a repository"""
        if not self.driver:
            return {'nodes': [], 'edges': []}
        
        with self.driver.session() as session:
            nodes = session.execute_read(self._get_nodes_tx, repo_id)
            edges = session.execute_read(self._get_edges_tx, repo_id)
            
            return {
                'nodes': nodes,
                'edges': edges
            }
    
    @staticmethod
    def _get_nodes_tx(tx, repo_id):
        """Transaction to get all nodes"""
        query = """
        MATCH (n) WHERE n.repo_id = $repo_id
        RETURN n.id as id, n.label as label, labels(n)[0] as type, n.properties as properties
        """
        result = tx.run(query, repo_id=repo_id)
        return [dict(record) for record in result]
    
    @staticmethod
    def _get_edges_tx(tx, repo_id):
        """Transaction to get all edges"""
        query = """
        MATCH (source)-[r:RELATES]->(target)
        WHERE source.repo_id = $repo_id AND target.repo_id = $repo_id
        RETURN 
            source.id as source,
            target.id as target,
            r.type as type,
            r.label as label,
            r.properties as properties
        """
        result = tx.run(query, repo_id=repo_id)
        edges = []
        for record in result:
            edges.append({
                'id': f"{record['source']}->{record['target']}",
                'source': record['source'],
                'target': record['target'],
                'type': record['type'],
                'label': record['label'],
                'properties': record['properties']
            })
        return edges
    
    def get_user_repositories(self, user_id: str) -> List[Dict]:
        """Get all repositories for a user"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.execute_read(
                self._get_user_repositories_tx,
                user_id
            )
            return result
    
    @staticmethod
    def _get_user_repositories_tx(tx, user_id):
        """Transaction to get user repositories"""
        query = """
        MATCH (r:Repository)
        WHERE EXISTS {
            MATCH (r)-[:CONTAINS]->(n)
            WHERE n.user_id = $user_id
        }
        RETURN DISTINCT
            elementId(r) as id,
            r.name as name,
            r.branch as branch,
            r.commit as commit,
            r.last_modified as last_modified,
            r.created_at as created_at
        ORDER BY r.created_at DESC
        """
        result = tx.run(query, user_id=user_id)
        return [dict(record) for record in result]
    
    def delete_repository(self, repo_id: str):
        """Delete a repository and all its nodes"""
        if not self.driver:
            return
        
        with self.driver.session() as session:
            session.execute_write(self._delete_repository_tx, repo_id)
    
    @staticmethod
    def _delete_repository_tx(tx, repo_id):
        """Transaction to delete repository"""
        query = """
        MATCH (r:Repository) WHERE elementId(r) = $repo_id
        OPTIONAL MATCH (r)-[:CONTAINS]->(n)
        DETACH DELETE r, n
        """
        tx.run(query, repo_id=repo_id)
    
    def search_nodes(self, repo_id: str, search_term: str) -> List[Dict]:
        """Search for nodes by name or label"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.execute_read(
                self._search_nodes_tx,
                repo_id,
                search_term
            )
            return result
    
    @staticmethod
    def _search_nodes_tx(tx, repo_id, search_term):
        """Transaction to search nodes"""
        query = """
        MATCH (n) WHERE n.repo_id = $repo_id
        AND (toLower(n.label) CONTAINS toLower($search_term) 
             OR toLower(n.id) CONTAINS toLower($search_term))
        RETURN n.id as id, n.label as label, labels(n)[0] as type, n.properties as properties
        LIMIT 50
        """
        result = tx.run(query, repo_id=repo_id, search_term=search_term)
        return [dict(record) for record in result]
    
    def get_node_relationships(self, repo_id: str, node_id: str) -> Dict:
        """Get all relationships for a specific node"""
        if not self.driver:
            return {'incoming': [], 'outgoing': []}
        
        with self.driver.session() as session:
            incoming = session.execute_read(
                self._get_incoming_relationships_tx,
                repo_id,
                node_id
            )
            outgoing = session.execute_read(
                self._get_outgoing_relationships_tx,
                repo_id,
                node_id
            )
            
            return {
                'incoming': incoming,
                'outgoing': outgoing
            }
    
    @staticmethod
    def _get_incoming_relationships_tx(tx, repo_id, node_id):
        """Get incoming relationships"""
        query = """
        MATCH (source)-[r:RELATES]->(target)
        WHERE target.id = $node_id AND target.repo_id = $repo_id
        RETURN 
            source.id as source_id,
            source.label as source_label,
            r.type as type,
            r.label as label
        """
        result = tx.run(query, repo_id=repo_id, node_id=node_id)
        return [dict(record) for record in result]
    
    @staticmethod
    def _get_outgoing_relationships_tx(tx, repo_id, node_id):
        """Get outgoing relationships"""
        query = """
        MATCH (source)-[r:RELATES]->(target)
        WHERE source.id = $node_id AND source.repo_id = $repo_id
        RETURN 
            target.id as target_id,
            target.label as target_label,
            r.type as type,
            r.label as label
        """
        result = tx.run(query, repo_id=repo_id, node_id=node_id)
        return [dict(record) for record in result]


# Global instance
neo4j_service = Neo4jService()

# Made with Bob