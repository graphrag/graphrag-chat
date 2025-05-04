
from typing import Any, Optional, Dict, List

from google.adk.tools import ToolContext
from google.adk.memory.base_memory_service import SearchMemoryResponse

from graphrag_chat.memory.in_memory import InMemoryService
from graphrag_chat.memory.multi_memory_delegate import MultiMemoryDelegate

graphrag_memory = MultiMemoryDelegate([InMemoryService()])

def set_speaker(name:str, tool_context: ToolContext) -> str:
    """Sets the current human spaker participating in the chat.
    """
    tool_context.state["current_speaker"] = name
    return f"Nice to have you here, {name}!"

def get_speaker(tool_context: ToolContext) -> str:
    if "current_speaker" in tool_context.state:
        return tool_context.state["current_speaker"]
    return "Current human speaker hasn't been identified. Politely ask them to introduce themselves. If you haven't yet, remind them who you are."

def add_memory(tool_context: ToolContext) -> Dict[str, Any]:
    graphrag_memory.add_memory(tool_context._invocation_context.session)

def search_memory(query: str, tool_context: ToolContext) -> SearchMemoryResponse:
    session = tool_context._invocation_context.session
    return graphrag_memory.search_memory(app_name=session.app_name, user_id=session.user_id, query=query)
