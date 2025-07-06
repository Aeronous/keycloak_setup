import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.mappers import MapperManager

@pytest.fixture
def mapper_manager():
    return MapperManager('http://localhost', 'token', 'realm')

@patch('keycloak_setup.mappers.requests.get')
def test_get_client_uuid_found(mock_get, mapper_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[{"id": "uuid1"}]))
    assert mapper_manager.get_client_uuid('client1') == 'uuid1'

@patch('keycloak_setup.mappers.requests.get')
def test_get_client_uuid_not_found(mock_get, mapper_manager):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[]))
    assert mapper_manager.get_client_uuid('client1') is None

@patch('keycloak_setup.mappers.requests.post')
@patch('keycloak_setup.mappers.MapperManager.get_client_uuid', return_value='uuid1')
def test_add_group_membership_mapper_success(mock_get_uuid, mock_post, mapper_manager):
    mock_post.return_value = MagicMock(status_code=201)
    mapper_manager.add_group_membership_mapper('client1')
    mock_post.assert_called_once()

@patch('keycloak_setup.mappers.MapperManager.get_client_uuid', return_value=None)
def test_add_group_membership_mapper_client_not_found(mock_get_uuid, mapper_manager):
    with pytest.raises(Exception):
        mapper_manager.add_group_membership_mapper('client1') 