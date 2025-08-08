from click.testing import CliRunner

from misstea.main import cli


def test_google_search_agent_e2e(caplog):
    """Test that the google_search agent can be called and returns the expected output."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["run"],
        input="What is the capital of France?",
    )

    assert caplog.text.find("name: call_google_search_agent, args: {'question': ") >= 0
    assert "paris" in result.stdout.lower()
