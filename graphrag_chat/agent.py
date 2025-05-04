import os
import json

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.lite_llm import LiteLlm

from .prompts import return_instructions_root
from .models import by_role
from .tools import set_speaker, get_speaker, add_memory, search_memory
from .sub_agents import cypher_agent, agent_smith
from .neo4j_for_adk import Neo4jGraphCatalog

def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the agent."""

    with open("neo4j.json", "r") as f:
        neo4j_settings = json.load(f)
        print("Neo4j settings loaded: " + str(neo4j_settings))

    print("API Keys Set:")
    print(f"Gemini API Key set: {'Yes' if os.environ.get('GEMINI_API_KEY') and os.environ['GEMINI_API_KEY'] != 'YOUR_GEMINI_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")
    print(f"OpenAI API Key set: {'Yes' if os.environ.get('OPENAI_API_KEY') and os.environ['OPENAI_API_KEY'] != 'YOUR_OPENAI_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")

    for key, entry in neo4j_settings.items():
        print(f"Neo4j graph named '{key}' expected at: {entry['username']}@{entry['uri']}/{entry['database']}" )

    Neo4jGraphCatalog.initialize(neo4j_settings)

graphrag_chat_agent = Agent(
    name="graphrag_chat_agent_v1",
    model=LiteLlm(model=by_role["chat"]),
    description="Hosts a chat among multiple sub-agents, each with unique identities and knowledge.", # Crucial for delegation later
    
    instruction=return_instructions_root(),
    tools=[set_speaker, get_speaker, add_memory, search_memory], 
    sub_agents=[cypher_agent, agent_smith],
    before_agent_callback=setup_before_agent_call,
)

# Export the root agent so adk can find it
root_agent = graphrag_chat_agent
