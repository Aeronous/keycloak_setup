import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.groups import GroupManager

@pytest.fixture
def group_manager():
    return GroupManager('http://localhost', 'token', 'realm')

@patch('keycloak_setup.groups.requests.get')
def test_find_root_group_id_found(mock_get, group_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[{"name": "group1", "id": "id1"}]))
    assert group_manager.find_root_group_id('group1') == 'id1'

@patch('keycloak_setup.groups.requests.get')
def test_find_root_group_id_not_found(mock_get, group_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[]))
    assert group_manager.find_root_group_id('group1') is None

@patch('keycloak_setup.groups.requests.post')
def test_create_group_success(mock_post, group_manager):
    mock_post.return_value = MagicMock(status_code=201)
    group_manager.create_group('group1')
    mock_post.assert_called_once()

@patch('keycloak_setup.groups.requests.post')
def test_create_group_conflict(mock_post, group_manager):
    mock_post.return_value = MagicMock(status_code=409)
    group_manager.create_group('group1')
    mock_post.assert_called_once()

@patch('keycloak_setup.groups.requests.post')
def test_create_group_error(mock_post, group_manager):
    mock_post.return_value = MagicMock(status_code=500, text='error')
    with pytest.raises(Exception):
        group_manager.create_group('group1')

@patch('keycloak_setup.groups.GroupManager.create_group')
@patch('keycloak_setup.groups.GroupManager.find_root_group_id', return_value=None)
def test_create_groups_calls_create_group(mock_find, mock_create, group_manager):
    groups = [{"name": "g1"}]
    group_manager.create_groups(groups)
    mock_create.assert_called_once_with('g1', None) 