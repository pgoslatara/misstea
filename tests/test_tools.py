from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from misstea import tools


@pytest.mark.asyncio
@patch("misstea.tools.AgentTool")
async def test_call_github_agent(mock_agent_tool):
    mock_agent_tool.return_value.run_async = AsyncMock(return_value="github_output")
    tool_context = MagicMock()
    tool_context.state = {}

    result = await tools.call_github_agent("test question", tool_context)

    assert result == "github_output"
    assert tool_context.state["github_agent_output"] == "github_output"


@pytest.mark.asyncio
@patch("misstea.tools.AgentTool")
async def test_call_google_search_agent(mock_agent_tool):
    mock_agent_tool.return_value.run_async = AsyncMock(return_value="google_output")
    tool_context = MagicMock()
    tool_context.state = {}

    result = await tools.call_google_search_agent("test question", tool_context)

    assert result == "google_output"
    assert tool_context.state["github_agent_output"] == "google_output"


@pytest.mark.asyncio
@patch("misstea.tools.AgentTool")
async def test_call_outlook_agent(mock_agent_tool):
    mock_agent_tool.return_value.run_async = AsyncMock(return_value="outlook_output")
    tool_context = MagicMock()
    tool_context.state = {}

    result = await tools.call_outlook_agent("test question", tool_context)

    assert result == "outlook_output"
    assert tool_context.state["outlook_agent_output"] == "outlook_output"


@pytest.mark.asyncio
@patch("misstea.tools.AgentTool")
async def test_call_terraform_agent(mock_agent_tool):
    mock_agent_tool.return_value.run_async = AsyncMock(return_value="terraform_output")
    tool_context = MagicMock()
    tool_context.state = {}

    result = await tools.call_terraform_agent("test question", tool_context)

    assert result == "terraform_output"
    assert tool_context.state["terraform_agent_output"] == "terraform_output"
