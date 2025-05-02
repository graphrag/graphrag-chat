from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

from google.adk.models.lite_llm import LiteLlm

from graphrag_chat.models import by_role

from .prompts import return_instructions_agent_smith


# Export the root agent so adk can find it
agent_smith = Agent(
    name="agent_smith_v1",
    model=LiteLlm(model=by_role["chat"]),
    description="Provides acccess to a Neo4j database through Cypher queries.", # Crucial for delegation later
    instruction=return_instructions_agent_smith(),
)

# Export the root agent so adk can find it
root_agent = agent_smith
