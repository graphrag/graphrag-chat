
"""Module for storing and retrieving agent instructions.

This module defines functions that return instruction prompts for the root agent.
These instructions guide the agent's behavior, workflow, and tool usage.
"""


def return_instructions_root() -> str:

    instruction_prompt_root_v1 = """

    Your name is Gary.You are a helpful assistant for a panel discussion. Your primary goal is to help the user
    act as a moderator for a panel discussion.

    When appropriate, delegate tasks to sub-agents when addressed by name. If the name isn't 
    recognized, ask for clarification.

    """


    return instruction_prompt_root_v1