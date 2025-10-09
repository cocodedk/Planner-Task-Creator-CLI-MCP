"""
Tests for CLI list commands (plans and buckets)
"""

import json
from typer.testing import CliRunner
from planner import app

runner = CliRunner()


def test_list_plans_success(mocker, mock_config_file, mock_plans):
    """Test listing plans"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client"
    })
    mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")
    mocker.patch("planner_lib.cli_commands.list_user_plans", return_value=mock_plans)

    result = runner.invoke(app, ["list-plans"])

    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert len(output) == 2
    assert output[0]["title"] == "My Plan"


def test_list_buckets_success(mocker, mock_config_file, mock_buckets):
    """Test listing buckets"""
    mocker.patch("planner_lib.cli_commands.load_conf", return_value={
        "tenant_id": "test-tenant", "client_id": "test-client"
    })
    mocker.patch("planner_lib.cli_commands.get_tokens", return_value="mock_token")
    mocker.patch("planner_lib.cli_commands.resolve_plan", return_value={"id": "plan-id-1"})
    mocker.patch("planner_lib.cli_commands.list_plan_buckets", return_value=mock_buckets)

    result = runner.invoke(app, ["list-buckets", "--plan", "My Plan"])

    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert len(output) == 3
    assert output[0]["name"] == "To Do"


