import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.realm import RealmManager

@pytest.fixture
def realm_manager():
    return RealmManager('http://localhost', 'token')

@patch('keycloak_setup.realm.requests.get')
def test_realm_exists_true(mock_get, realm_manager):
    mock_get.return_value = MagicMock(status_code=200)
    assert realm_manager.realm_exists('realm1') is True

@patch('keycloak_setup.realm.requests.get')
def test_realm_exists_false(mock_get, realm_manager):
    mock_get.return_value = MagicMock(status_code=404)
    assert realm_manager.realm_exists('realm1') is False

@patch('keycloak_setup.realm.requests.post')
@patch('keycloak_setup.realm.RealmManager.realm_exists', return_value=False)
def test_create_realm_success(mock_exists, mock_post, realm_manager):
    mock_post.return_value = MagicMock(status_code=201)
    realm_manager.create_realm('realm1')
    mock_post.assert_called_once()

@patch('keycloak_setup.realm.RealmManager.realm_exists', return_value=True)
def test_create_realm_already_exists(mock_exists, realm_manager):
    realm_manager.create_realm('realm1')
    # Should not call post if already exists

@patch('keycloak_setup.realm.requests.post')
@patch('keycloak_setup.realm.RealmManager.realm_exists', return_value=False)
def test_create_realm_error(mock_exists, mock_post, realm_manager):
    mock_post.return_value = MagicMock(status_code=500, text='error')
    with pytest.raises(Exception):
        realm_manager.create_realm('realm1') 