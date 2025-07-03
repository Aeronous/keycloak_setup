import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.users import UserManager

@pytest.fixture
def user_manager():
    return UserManager('http://localhost', 'token', 'realm')

@patch('keycloak_setup.users.requests.get')
def test_get_group_id_by_name_found(mock_get, user_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[{"name": "g1", "id": "id1"}]))
    assert user_manager.get_group_id_by_name('g1') == 'id1'

@patch('keycloak_setup.users.requests.get')
def test_get_group_id_by_name_not_found(mock_get, user_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[]))
    assert user_manager.get_group_id_by_name('g1') is None

@patch('keycloak_setup.users.requests.post')
@patch('keycloak_setup.users.UserManager.get_group_id_by_name', return_value='gid')
@patch('keycloak_setup.users.UserManager.get_user_id_by_username', return_value='uid')
@patch('keycloak_setup.users.requests.put')
def test_create_user_success(mock_put, mock_get_uid, mock_get_gid, mock_post, user_manager):
    mock_post.return_value = MagicMock(status_code=201)
    mock_put.return_value = MagicMock(status_code=204)
    user = {"username": "u1", "password": "p1", "group": "g1"}
    user_manager.create_user(user)
    mock_post.assert_called_once()
    mock_put.assert_called_once()

@patch('keycloak_setup.users.UserManager.get_group_id_by_name', return_value=None)
def test_create_user_group_not_found(mock_get_gid, user_manager):
    user = {"username": "u1", "password": "p1", "group": "g1"}
    with pytest.raises(Exception):
        user_manager.create_user(user)

@patch('keycloak_setup.users.requests.post')
@patch('keycloak_setup.users.UserManager.get_group_id_by_name', return_value='gid')
def test_create_user_missing_fields(mock_get_gid, mock_post, user_manager):
    user = {"username": "u1", "password": "p1"}
    with pytest.raises(ValueError):
        user_manager.create_user(user)

@patch('keycloak_setup.users.requests.get')
def test_get_user_id_by_username_found(mock_get, user_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[{"id": "uid"}]))
    assert user_manager.get_user_id_by_username('u1') == 'uid'

@patch('keycloak_setup.users.requests.get')
def test_get_user_id_by_username_not_found(mock_get, user_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[]))
    assert user_manager.get_user_id_by_username('u1') is None

@patch('keycloak_setup.users.UserManager.get_user_id_by_username', return_value=None)
def test_assign_to_group_user_not_found(mock_get_uid, user_manager):
    with pytest.raises(Exception):
        user_manager.assign_to_group('u1', 'g1')

@patch('keycloak_setup.users.UserManager.get_user_id_by_username', return_value='uid')
@patch('keycloak_setup.users.UserManager.get_group_id_by_name', return_value=None)
def test_assign_to_group_group_not_found(mock_get_gid, mock_get_uid, user_manager):
    with pytest.raises(Exception):
        user_manager.assign_to_group('u1', 'g1')

@patch('keycloak_setup.users.UserManager.get_user_id_by_username', return_value='uid')
@patch('keycloak_setup.users.UserManager.get_group_id_by_name', return_value='gid')
@patch('keycloak_setup.users.requests.put')
def test_assign_to_group_success(mock_put, mock_get_gid, mock_get_uid, user_manager):
    mock_put.return_value = MagicMock(status_code=204)
    user_manager.assign_to_group('u1', 'g1')
    mock_put.assert_called_once() 