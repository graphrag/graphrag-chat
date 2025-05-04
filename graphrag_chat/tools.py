from google.adk.tools import ToolContext

def set_user(name:str, tool_context: ToolContext) -> str:
    """Sets the current user participating in the chat.
    """
    tool_context.state["current_user"] = name
    return f"Nice to have you here, {name}!"

def get_user(tool_context: ToolContext) -> str:
    if "current_user" in tool_context.state:
        return tool_context.state["current_user"]
    return "User hasn't been identified. Politely ask them to introduce themselves. If you haven't yet, remind them who you are."
