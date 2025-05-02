
"""Module for storing and retrieving agent instructions.

This module defines functions that return instruction prompts for the cypher agent.
These instructions guide the agent's behavior, workflow, and tool usage.
"""


def return_instructions_cypher() -> str:

    instruction_prompt_cypher_v1 = """

    You are an expert in Neo4j's Cypher query language and property graphs.
    Your primary goal is to help the user interact with a named Neo4j database
    through Cypher queries.
    """
    return instruction_prompt_cypher_v1