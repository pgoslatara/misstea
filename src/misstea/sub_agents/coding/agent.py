from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

from misstea.constants import AGENT_MODEL


def get_calculator_agent() -> Agent:
    """Return a calculator agent.

    Returns:
        Agent: The calculator agent.

    """
    return Agent(
        model=AGENT_MODEL,
        name="calculator_agent",
        code_executor=BuiltInCodeExecutor(),
        instruction="""You are a calculator agent.
        When given a mathematical expression, write and execute Python code to calculate the result.
        Return only the final numerical result as plain text, without markdown, code blocks or description.
        """,
    )


root_agent = get_calculator_agent()
