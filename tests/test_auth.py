import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.auth import KeycloakAuth

@patch('keycloak_setup.auth.requests.post')
def test_get_admin_token_success(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"access_token": "token123"}
    mock_post.return_value = mock_response

    auth = KeycloakAuth('http://localhost', 'admin', 'pass')
    token = auth.get_admin_token()
    assert token == "token123"
    mock_post.assert_called_once()

@patch('keycloak_setup.auth.requests.post')
def test_get_admin_token_no_token_in_response(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    mock_post.return_value = mock_response

    auth = KeycloakAuth('http://localhost', 'admin', 'pass')
    with pytest.raises(Exception, match="Admin authentication failed."):
        auth.get_admin_token()

@patch('keycloak_setup.auth.requests.post')
def test_get_admin_token_http_error(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP error")
    mock_post.return_value = mock_response

    auth = KeycloakAuth('http://localhost', 'admin', 'pass')
    with pytest.raises(Exception, match="Admin authentication failed."):
        auth.get_admin_token() 