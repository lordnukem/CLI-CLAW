from typer.testing import CliRunner
from autonomous_claw.cli import app

runner = CliRunner()

def test_status_command():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "System Status" in result.stdout

def test_start_command():
    result = runner.invoke(app, ["start", "Build a task manager"])
    assert result.exit_code == 0
    assert "Starting Autonomous Sprint" in result.stdout
    assert "Build a task manager" in result.stdout
