
from typing import Any, Dict, List, TypedDict, Union
import re

from google.adk.tools import ToolContext

from neo4j import (
    GraphDatabase,
    Result,
)

class ToolSuccessResult(TypedDict):
    status: str  # 'success'
    query_result: List[Dict[str, any]]

class ToolErrorResult(TypedDict):
    status: str  # 'error'
    error_message: str

ToolResult = Union[ToolSuccessResult, ToolErrorResult]

def tool_success(result: List[Dict[str, Any]]):
    return {
        'status': 'success',
        'query_result': result
    }

def tool_error(message: str):
    return {
        'status': 'error',
        'error_message': message
    }

class Neo4jConnectionSettings(TypedDict):
    uri: str
    username: str
    password: str
    database: str


def make_driver(neo4j_settings: Neo4jConnectionSettings) -> GraphDatabase | None:
    """
    Connects to a Neo4j Graph Database according to the provided settings.
    """
    # Initialize the driver
    driver_instance = GraphDatabase.driver(
        neo4j_settings["uri"],
        auth=(neo4j_settings["username"], neo4j_settings["password"])
    )
    return driver_instance


def is_write_query(query: str) -> bool:
    """Check if the Cypher query performs any write operations."""
    return (
        re.search(r"\b(MERGE|CREATE|SET|DELETE|REMOVE|ADD)\b", query, re.IGNORECASE)
        is not None
    )

def result_to_adk(result: Result) -> Dict[str, Any]:
    eager_result = result.to_eager_result()
    records = [to_python(record.data()) for record in eager_result.records]
    return tool_success(records)

def to_python(value):
    from neo4j.graph import Node, Relationship, Path
    from neo4j import Record
    import neo4j.time
    if isinstance(value, Record):
        return {k: to_python(v) for k, v in value.items()}
    elif isinstance(value, dict):
        return {k: to_python(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [to_python(v) for v in value]
    elif isinstance(value, Node):
        return {
            "id": value.id,
            "labels": list(value.labels),
            "properties": to_python(dict(value))
        }
    elif isinstance(value, Relationship):
        return {
            "id": value.id,
            "type": value.type,
            "start_node": value.start_node.id,
            "end_node": value.end_node.id,
            "properties": to_python(dict(value))
        }
    elif isinstance(value, Path):
        return {
            "nodes": [to_python(node) for node in value.nodes],
            "relationships": [to_python(rel) for rel in value.relationships]
        }
    elif isinstance(value, neo4j.time.DateTime):
        return value.iso_format()
    elif isinstance(value, (neo4j.time.Date, neo4j.time.Time, neo4j.time.Duration)):
        return str(value)
    else:
        return value

class Neo4jForADK:
    """
    A Neo4j wrapper for sending queries to Neo4j and getting
    ADK-friendly responses.
    Usage:
        neo4jADK = Neo4jForADK(settings)
        result = neo4jADK.send_query("MATCH (n) RETURN n LIMIT 1")
    """
    _driver: GraphDatabase = None   
    _settings: Neo4jConnectionSettings = None

    def __init__(self, settings: Neo4jConnectionSettings):
        self._driver = make_driver(settings)
        self._settings = settings

    def get_direct_driver(self):
        return self._driver
    
    def send_query(self, cypher_query, parameters=None) -> ToolResult:
        session = self._driver.session()
        try:
            result = session.run(
                cypher_query, 
                parameters or {},
                database=self._settings["database"]
            )
            return result_to_adk(result)
        except Exception as e:
            return tool_error(str(e))
        finally:
            session.close()


class Neo4jGraphCatalog:
    """
    A singleton catalog of named Neo4j databases.
    Usage:
        Neo4jCatalog.initialize(settings)
        catalog = Neo4jCatalog.get_instance()
        db = catalog.get_graphdb('name')
    """
    _instance: 'Neo4jGraphCatalog' = None
    _settings: None
    _graph_to_database: dict[str, Neo4jForADK] = {}
    _initialized = False

    def __init__(self, settings: Dict[str, Neo4jConnectionSettings]):
        if Neo4jGraphCatalog._initialized:
            return
        self._settings = settings
        self._refresh()
        Neo4jGraphCatalog._initialized = True

    def _refresh(self):
        self._graph_to_database = {}
        for name, neo4j_settings in self._settings.items():
            self._graph_to_database[name] = Neo4jForADK(neo4j_settings)

    @classmethod
    def initialize(cls, settings: Dict[str, Neo4jConnectionSettings]):
        """Initialize the Neo4j catalog with settings."""
        if cls._instance is None:
            cls._instance = cls(settings)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'Neo4jGraphCatalog':
        """Get the singleton instance of the catalog."""
        if cls._instance is None:
            raise Exception("Neo4jCatalog must be initialized with settings before use.")
        return cls._instance

    @classmethod
    def get_graphdb(cls, graph_name: str) -> Neo4jForADK:
        """Get a Neo4j database wrapper by named graph."""
        catalog = cls.get_instance()
        if graph_name not in catalog._graph_to_database:
            raise KeyError(f"No Neo4j database found for graph named: {graph_name}")
        return catalog._graph_to_database[graph_name]

    @classmethod
    def list_graphs(cls) -> list[str]:
        """List all available named graphs."""
        return list(cls.get_instance()._graph_to_database.keys())

    @classmethod
    def refresh(cls):
        """List all available named graphs."""
        cls.get_instance()._refresh()
