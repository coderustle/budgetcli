import pytest
from typer.testing import CliRunner


from budgetcli.commands import config


@pytest.fixture(scope="session", autouse=True)
def runner():
    """Fixture to get the typer app runner"""

    runner = CliRunner()

    return runner


class TestConfigCommand:
    """Tests for config command"""

    def test_config_cmd_without_any_subcommands(self, runner):
        """
        Test the config command without passing any sub-commands.

        command: budgetcli config
        """
        result = runner.invoke(config.app)
        assert result.exit_code == 0

    def test_spreadsheet_cmd_without_spreadsheet_id(self, runner):
        """
        Test config spreadsheet command without passing
        the spreadsheet id argument.

        command: bugetcli config spreadsheet 'SPREADSHEET_ID'
        """
        result = runner.invoke(config.app, ["spreadsheet"])
        assert result.exit_code == 2
        assert "Missing argument 'SPREADSHEET_ID'" in result.stdout


    def test_spreadsheet_cmd_with_spreadsheet_id(self, runner):
        """
        Test config spreadsheet command with spreadsheet id argument
        passed.
        """
        result = runner.invoke(config.app, ["spreadsheet", "id"])
        assert result.exit_code == 0
