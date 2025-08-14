import pytest
from click.testing import CliRunner

from misstea.main import cli


@pytest.mark.flaky(reruns=5)
def test_coding_agent_e2e(tmp_path):
    """Test that the coding agent can be called and returns the expected output."""
    # Create a dummy file to read, write and replace
    dummy_file = tmp_path / "dummy_file.txt"
    dummy_file.write_text("Hello, world!")

    runner = CliRunner()
    # Test read_file
    result = runner.invoke(
        cli,
        ["run"],
        input=f"Read the file at {dummy_file}",
    )
    assert "Hello, world!" in result.stdout

    # Test write_to_file
    runner.invoke(
        cli,
        ["run"],
        input=f"Write 'Hello, Miss Tea!' to the file at {dummy_file}",
    )
    assert dummy_file.read_text() == "Hello, Miss Tea!"

    # Test replace_in_file
    runner.invoke(
        cli,
        ["run"],
        input=f"In the file at {dummy_file}, replace 'Miss Tea' with 'Mrs. Doyle'",
    )
    assert dummy_file.read_text() == "Hello, Mrs. Doyle!"
