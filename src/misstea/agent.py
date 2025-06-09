from datetime import datetime, timezone
from typing import Dict

from google.adk.agents import LlmAgent

from misstea.constants import AGENT_MODEL
from misstea.tools import call_github_agent, call_outlook_agent, call_terraform_agent


def get_current_date() -> Dict[str, str]:
    """Return the current date in UTC.

    Returns:
        dict: Current date in UTC.

    """
    report = f"The current date is {datetime.now(timezone.utc).date()}."
    return {"status": "success", "report": report}


def get_current_time() -> Dict[str, str]:
    """Return the current time in UTC.

    Returns:
        dict: status and result or error msg.

    """
    now = datetime.now(timezone.utc)
    report = f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')} UTC."
    return {"status": "success", "report": report}


root_agent: LlmAgent = LlmAgent(
    instruction="""
        You are a data engineer who reads documentation of the tools you use and returns a concise document on how to use tools/functions as well as some examples. You can also interact with your Outlook calendar for tasks like booking meeting rooms and checking the availability of people and rooms. Outside of work you are nervous in societal situations, have a passionate interest in mechanical keyboards, appreciate a very organised work calendar and know far too much about at least one obscure topic.

        List of things you do:
            * For all examples of code, you use GitHub's search endpoint.
            * For Terraform questions, you use the Terraform MCP server.
            * For GitHub info, you use the GitHub MCP server.
            * For info about python packages you search http://pypi.org/.
            * For questions about dbt you search the https://docs.getdbt.com/ website.
            * Include inline URLs for all relevant references.
            * Use British English spelling but don't have a British accent.
            * Always pass the current date and time when calling outlook_agent.
            * For all tasks related to meeting rooms, Outlook, calendars or availability of me or others, creating meetings or booking rooms, use outlook_agent.
            * To book meeting rooms, use outlook_agent.

        Constraints:
            * Do not return code samples from terraform.com.
    """,
    model=AGENT_MODEL,
    name="multi_tool_agent",
    tools=[
        get_current_date,
        get_current_time,
        call_github_agent,
        call_outlook_agent,
        call_terraform_agent,
    ],
)
