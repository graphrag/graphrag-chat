from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

from google.adk.models.lite_llm import LiteLlm

from graphrag_chat.models import by_role

from .tools import (
    list_graphs,
    graph_is_ready,
    get_physical_schema, 
    read_neo4j_cypher,
    write_neo4j_cypher
)

from .prompts import return_instructions_cypher


# Export the root agent so adk can find it
cypher_agent = Agent(
    name="cypher_agent_v1",
    model=LiteLlm(model=by_role["chat"]),
    description="Provides acccess to a Neo4j database through Cypher queries.", # Crucial for delegation later
    instruction=return_instructions_cypher(),

    tools=[list_graphs, graph_is_ready, get_physical_schema, read_neo4j_cypher, write_neo4j_cypher], # Make the tool available to this agent
)

# Export the root agent so adk can find it
root_agent = cypher_agent
