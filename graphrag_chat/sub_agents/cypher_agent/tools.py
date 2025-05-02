
from typing import Any, Optional, Dict, List

from neo4j_graphrag.schema import get_structured_schema

from graphrag_chat.neo4j_for_adk import (
    Neo4jGraphCatalog,
    is_write_query,
    tool_success, tool_error,
    ToolResult
)


async def list_graphs() -> List[str]:
    """Lists available named Neo4j graphs.
    """
    return Neo4jGraphCatalog.list_graphs()

async def refresh_graphs():
    """Refreshes the known Neo4j connections.
        This can be useful to re-establish connections 
        which have dropped or failed.
    """
    return Neo4jGraphCatalog.refresh()

async def graph_is_ready(graph_name: str):
    """Tool to check that the named Neo4j graph is ready.
    Replies with either a positive message about the database being ready or an error message.

    Args:
        graph_name: The name of the Neo4j graph to check.
    """
    graphdb = Neo4jGraphCatalog.get_graphdb(graph_name)
    results = graphdb.send_query("RETURN 'Neo4j is Ready!' as message")
    return results


async def get_physical_schema(graph_name: str) -> Dict[str, Any]:
    """Tool to get the physical schema of a Neo4j graph database.

    Args:
        graph_name: The name of the Neo4j graph to get the schema for.

    Returns:
        The schema is returned as a JSON object containing a description
        of the node labels and relationship types.
    """
    graphdb = Neo4jGraphCatalog.get_graphdb(graph_name)
    driver = graphdb.get_direct_driver()
    
    try:
        schema = get_structured_schema(driver, database=graphdb._settings["database"])
        return tool_success(schema)
    except Exception as e:
        return tool_error(str(e))


async def read_neo4j_cypher(
    database: str,
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> ToolResult:
    """Submits a Cypher query to read from a Neo4j database.

    Args:
        database: The name of the Neo4j database to query.
        query: The Cypher query string to execute.
        params: Optional parameters to pass to the query.

    Returns:
        A list of dictionaries containing the results of the query.
        Returns an empty list "[]" if no results are found.

    """    
    if is_write_query(query):
        return tool_error("Only MATCH queries are allowed for read-query")

    graphdb = Neo4jGraphCatalog.get_graphdb(database)
    results = graphdb.send_query(query, params)
    return results

async def write_neo4j_cypher(
    database: str,
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> ToolResult:
    """Submits a Cypher query to write to a Neo4j database.
    Make sure you have permission to write before calling this.

    Args:
        database: The name of the Neo4j database to query.
        query: The Cypher query string to execute.
        params: Optional parameters to pass to the query.

    Returns:
        A list of dictionaries containing the results of the query.
        Returns an empty list "[]" if no results are found.
    """
    graphdb = Neo4jGraphCatalog.get_graphdb(database)
    results = graphdb.send_query(query, params)
    return results