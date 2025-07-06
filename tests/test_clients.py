import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.clients import ClientManager

@pytest.fixture
def client_manager():
    return ClientManager('http://localhost', 'token', 'realm')

@patch('keycloak_setup.clients.requests.get')
def test_client_exists_true(mock_get, client_manager):
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = [{"id": "abc"}]
    mock_get.return_value = mock_response
    assert client_manager.client_exists('client1') is True

@patch('keycloak_setup.clients.requests.get')
def test_client_exists_false(mock_get, client_manager):
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = []
    mock_get.return_value = mock_response
    assert client_manager.client_exists('client1') is False

@patch('keycloak_setup.clients.requests.post')
@patch('keycloak_setup.clients.ClientManager.client_exists', return_value=False)
def test_create_client_success(mock_exists, mock_post, client_manager):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response
    client = {"client_id": "client1"}
    client_manager.create_client(client)
    mock_post.assert_called_once()

@patch('keycloak_setup.clients.requests.post')
def test_create_client_missing_id(mock_post, client_manager):
    with pytest.raises(ValueError):
        client_manager.create_client({})

@patch('keycloak_setup.clients.requests.get')
def test_get_client_secret_success(mock_get, client_manager):
    mock_get.side_effect = [
        MagicMock(ok=True, json=MagicMock(return_value=[{"id": "abc"}])),
        MagicMock(ok=True, json=MagicMock(return_value={"value": "secret!"}))
    ]
    secret = client_manager.get_client_secret('client1')
    assert secret == "secret!"

@patch('keycloak_setup.clients.requests.get')
def test_get_client_secret_not_found(mock_get, client_manager):
    mock_get.return_value = MagicMock(ok=False, json=MagicMock(return_value=[]))
    with pytest.raises(Exception):
        client_manager.get_client_secret('client1') 