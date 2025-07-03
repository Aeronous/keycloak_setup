import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from keycloak_setup.cli import cli

@patch('keycloak_setup.cli.ConfigLoader.load_config', return_value={
    'server_url': 'http://localhost', 'realm': 'realm', 'admin_user': 'admin', 'admin_password': 'pass',
    'groups': [], 'users': [], 'clients': []
})
@patch('keycloak_setup.cli.KeycloakAuth.get_admin_token', return_value='token')
@patch('keycloak_setup.cli.RealmManager.create_realm')
@patch('keycloak_setup.cli.GroupManager.create_groups')
@patch('keycloak_setup.cli.UserManager.create_users')
@patch('keycloak_setup.cli.ClientManager.create_clients')
@patch('keycloak_setup.cli.MapperManager.add_group_membership_mapper')
def test_configure_success(mock_mapper, mock_clients, mock_users, mock_groups, mock_realm, mock_token, mock_config):
    runner = CliRunner()
    result = runner.invoke(cli, ['configure', '--config', 'dummy.yaml'])
    assert result.exit_code == 0

@patch('keycloak_setup.cli.ConfigLoader.load_config', side_effect=Exception('fail'))
def test_configure_fail(mock_config):
    runner = CliRunner()
    result = runner.invoke(cli, ['configure', '--config', 'dummy.yaml'])
    assert result.exit_code == 0
    assert 'Setup failed' in result.output or 'fail' in result.output

@patch('keycloak_setup.cli.ConfigLoader.load_config', return_value={
    'server_url': 'http://localhost', 'realm': 'realm', 'admin_user': 'admin', 'admin_password': 'pass'
})
@patch('keycloak_setup.cli.KeycloakAuth.get_admin_token', return_value='token')
@patch('keycloak_setup.cli.UserManager.create_user')
def test_add_user_success(mock_create_user, mock_token, mock_config):
    runner = CliRunner()
    result = runner.invoke(cli, ['add-user', '--config', 'dummy.yaml', '-u', 'user', '-p', 'pass', '-g', 'group'])
    assert result.exit_code == 0
    mock_create_user.assert_called_once()

@patch('keycloak_setup.cli.ConfigLoader.load_config', side_effect=Exception('fail'))
def test_add_user_fail(mock_config):
    runner = CliRunner()
    result = runner.invoke(cli, ['add-user', '--config', 'dummy.yaml', '-u', 'user', '-p', 'pass', '-g', 'group'])
    assert result.exit_code == 0
    assert 'Failed to add user' in result.output or 'fail' in result.output 