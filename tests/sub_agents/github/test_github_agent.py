import pytest
from click.testing import CliRunner

from misstea.main import cli


@pytest.mark.flaky(reruns=5)
def test_github_agent_e2e(caplog):
    """Test that the github agent can be called and returns the expected output."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["run"],
        input="When was the 'godatadriven/dbt-bouncer' repository created? Return only the date value, do not include any other characters. Use the yyyy-MM-dd format.",
    )

    assert "name: call_github_agent" in caplog.text
    assert result.stdout.split("\n")[-2].split(":")[-1].strip() == "2024-06-25"
