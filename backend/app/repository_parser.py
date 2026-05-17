"""
Repository Parser Service
Analyzes code repositories to extract structure, dependencies, and relationships
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
import git
from pygments.lexers import get_lexer_for_filename, guess_lexer
from pygments.util import ClassNotFound


@dataclass
class CodeEntity:
    """Represents a code entity (class, function, etc.)"""
    id: str
    name: str
    type: str  # 'class', 'function', 'method', 'variable', 'import'
    file_path: str
    line_number: int
    docstring: Optional[str] = None
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    parent: Optional[str] = None  # For methods, the parent class


@dataclass
class CodeRelationship:
    """Represents a relationship between code entities"""
    source: str
    target: str
    type: str  # 'imports', 'calls', 'inherits', 'uses', 'defines'
    file_path: str


@dataclass
class FileInfo:
    """Information about a file in the repository"""
    path: str
    language: str
    lines_of_code: int
    entities: List[CodeEntity] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)


class RepositoryParser:
    """Parses code repositories to extract structure and relationships"""
    
    SUPPORTED_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        '.jsx': 'JavaScript',
        '.java': 'Java',
        '.go': 'Go',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C/C++',
        '.hpp': 'C++',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.rs': 'Rust',
    }
    
    IGNORE_DIRS = {
        'node_modules', '.git', '__pycache__', 'venv', 'env',
        '.venv', 'dist', 'build', 'target', '.next', '.nuxt',
        'coverage', '.pytest_cache', '.mypy_cache', 'vendor'
    }
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.entities: Dict[str, CodeEntity] = {}
        self.relationships: List[CodeRelationship] = []
        self.files: Dict[str, FileInfo] = {}
        
    def parse_repository(self) -> Dict:
        """Parse the entire repository"""
        print(f"Parsing repository: {self.repo_path}")
        
        # Get repository info
        repo_info = self._get_repo_info()
        
        # Walk through all files
        for file_path in self._walk_files():
            try:
                self._parse_file(file_path)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
                continue
        
        # Build graph structure
        graph_data = self._build_graph()
        
        return {
            'repository': repo_info,
            'graph': graph_data,
            'statistics': self._calculate_statistics()
        }
    
    def _get_repo_info(self) -> Dict:
        """Get repository metadata"""
        try:
            repo = git.Repo(self.repo_path)
            return {
                'name': self.repo_path.name,
                'path': str(self.repo_path),
                'branch': repo.active_branch.name,
                'commit': repo.head.commit.hexsha[:8],
                'author': repo.head.commit.author.name,
                'last_modified': repo.head.commit.committed_datetime.isoformat(),
            }
        except:
            return {
                'name': self.repo_path.name,
                'path': str(self.repo_path),
                'branch': 'unknown',
                'commit': 'unknown',
                'author': 'unknown',
                'last_modified': 'unknown',
            }
    
    def _walk_files(self):
        """Walk through repository files"""
        for root, dirs, files in os.walk(self.repo_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.SUPPORTED_EXTENSIONS:
                    yield file_path
    
    def _parse_file(self, file_path: Path):
        """Parse a single file"""
        ext = file_path.suffix
        language = self.SUPPORTED_EXTENSIONS.get(ext, 'Unknown')
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Count lines of code
        loc = len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
        
        file_info = FileInfo(
            path=str(file_path.relative_to(self.repo_path)),
            language=language,
            lines_of_code=loc
        )
        
        # Parse based on language
        if ext == '.py':
            self._parse_python_file(file_path, content, file_info)
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            self._parse_javascript_file(file_path, content, file_info)
        
        self.files[file_info.path] = file_info
    
    def _parse_python_file(self, file_path: Path, content: str, file_info: FileInfo):
        """Parse Python file using AST"""
        try:
            tree = ast.parse(content)
            rel_path = str(file_path.relative_to(self.repo_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    entity = CodeEntity(
                        id=f"{rel_path}::{node.name}",
                        name=node.name,
                        type='class',
                        file_path=rel_path,
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node),
                        decorators=[d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
                    )
                    self.entities[entity.id] = entity
                    file_info.entities.append(entity)
                    
                    # Parse methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_entity = CodeEntity(
                                id=f"{rel_path}::{node.name}.{item.name}",
                                name=item.name,
                                type='method',
                                file_path=rel_path,
                                line_number=item.lineno,
                                docstring=ast.get_docstring(item),
                                parameters=[arg.arg for arg in item.args.args],
                                parent=entity.id
                            )
                            self.entities[method_entity.id] = method_entity
                            file_info.entities.append(method_entity)
                            
                            # Add relationship
                            self.relationships.append(CodeRelationship(
                                source=entity.id,
                                target=method_entity.id,
                                type='defines',
                                file_path=rel_path
                            ))
                
                elif isinstance(node, ast.FunctionDef):
                    # Top-level function
                    if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                        entity = CodeEntity(
                            id=f"{rel_path}::{node.name}",
                            name=node.name,
                            type='function',
                            file_path=rel_path,
                            line_number=node.lineno,
                            docstring=ast.get_docstring(node),
                            parameters=[arg.arg for arg in node.args.args]
                        )
                        self.entities[entity.id] = entity
                        file_info.entities.append(entity)
                
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        file_info.imports.append(alias.name)
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        file_info.imports.append(node.module)
        
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
    
    def _parse_javascript_file(self, file_path: Path, content: str, file_info: FileInfo):
        """Parse JavaScript/TypeScript file using regex patterns"""
        rel_path = str(file_path.relative_to(self.repo_path))
        
        # Find class declarations
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            line_number = content[:match.start()].count('\n') + 1
            
            entity = CodeEntity(
                id=f"{rel_path}::{class_name}",
                name=class_name,
                type='class',
                file_path=rel_path,
                line_number=line_number
            )
            self.entities[entity.id] = entity
            file_info.entities.append(entity)
        
        # Find function declarations
        func_pattern = r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[^=]+)\s*=>)'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1) or match.group(2)
            if func_name:
                line_number = content[:match.start()].count('\n') + 1
                
                entity = CodeEntity(
                    id=f"{rel_path}::{func_name}",
                    name=func_name,
                    type='function',
                    file_path=rel_path,
                    line_number=line_number
                )
                self.entities[entity.id] = entity
                file_info.entities.append(entity)
        
        # Find imports
        import_pattern = r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(import_pattern, content):
            file_info.imports.append(match.group(1))
    
    def _build_graph(self) -> Dict:
        """Build graph structure from parsed data"""
        nodes = []
        edges = []
        
        # Create nodes from entities
        for entity_id, entity in self.entities.items():
            nodes.append({
                'id': entity_id,
                'label': entity.name,
                'type': entity.type.capitalize(),
                'properties': {
                    'file': entity.file_path,
                    'line': entity.line_number,
                    'docstring': entity.docstring,
                    'parameters': entity.parameters,
                    'decorators': entity.decorators,
                }
            })
        
        # Create nodes from files
        for file_path, file_info in self.files.items():
            file_id = f"file::{file_path}"
            nodes.append({
                'id': file_id,
                'label': Path(file_path).name,
                'type': 'File',
                'properties': {
                    'path': file_path,
                    'language': file_info.language,
                    'loc': file_info.lines_of_code,
                }
            })
            
            # Create edges from file to entities
            for entity in file_info.entities:
                edges.append({
                    'id': f"{file_id}->{entity.id}",
                    'source': file_id,
                    'target': entity.id,
                    'type': 'contains',
                    'label': 'contains',
                    'properties': {}
                })
        
        # Add relationship edges
        for rel in self.relationships:
            edges.append({
                'id': f"{rel.source}->{rel.target}",
                'source': rel.source,
                'target': rel.target,
                'type': rel.type,
                'label': rel.type,
                'properties': {'file': rel.file_path}
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def _calculate_statistics(self) -> Dict:
        """Calculate repository statistics"""
        total_files = len(self.files)
        total_loc = sum(f.lines_of_code for f in self.files.values())
        
        languages = {}
        for file_info in self.files.values():
            lang = file_info.language
            if lang not in languages:
                languages[lang] = {'files': 0, 'loc': 0}
            languages[lang]['files'] += 1
            languages[lang]['loc'] += file_info.lines_of_code
        
        entity_types = {}
        for entity in self.entities.values():
            entity_type = entity.type
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
        
        return {
            'total_files': total_files,
            'total_lines_of_code': total_loc,
            'total_entities': len(self.entities),
            'languages': languages,
            'entity_types': entity_types,
            'total_relationships': len(self.relationships)
        }


# Made with Bob