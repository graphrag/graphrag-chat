
from typing import Any, Optional, Dict, List

from google.adk.tools import ToolContext
from google.adk.memory.base_memory_service import SearchMemoryResponse

from graphrag_chat.memory.in_memory import InMemoryService

agent_memory = InMemoryService()

# NOTE: don't add memory on the agent-level. 
# memories are added at the graphrag_agent to all available memory services.
# def add_memory(tool_context: ToolContext) -> Dict[str, Any]:
#     graphrag_memory.add_memory(tool_context._invocation_context.session)

def search_memory(query: str, tool_context: ToolContext) -> SearchMemoryResponse:
    session = tool_context._invocation_context.session
    return agent_memory.search_memory(app_name=session.app_name, user_id=session.user_id, query=query)
