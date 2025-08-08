from click.testing import CliRunner

from misstea.main import cli


def test_terraform_agent_e2e():
    """Test that the terraform agent can be called and returns the expected output."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["run"],
        input="Using Terraform AWS provider version 6.0.0, how many attributes are exported by the aws_s3_bucket resource? Return the result as an integer, do not include any other information or string characters.",
    )

    assert int(result.stdout.split("\n")[-2].split(":")[-1]) == 9
