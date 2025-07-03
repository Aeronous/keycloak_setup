import pytest
from unittest.mock import patch, mock_open
from keycloak_setup.config_loader import ConfigLoader

@patch('os.path.isfile', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='server_url: http://localhost')
@patch('yaml.safe_load', return_value={'server_url': 'http://localhost'})
def test_load_config_success(mock_yaml, mock_file, mock_isfile):
    config = ConfigLoader.load_config('config.yaml')
    assert config['server_url'] == 'http://localhost'

@patch('os.path.isfile', return_value=False)
def test_load_config_file_not_found(mock_isfile):
    with pytest.raises(FileNotFoundError):
        ConfigLoader.load_config('missing.yaml')

@patch('os.path.isfile', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='bad: [unclosed')
@patch('yaml.safe_load', side_effect=Exception('YAML error'))
def test_load_config_yaml_error(mock_yaml, mock_file, mock_isfile):
    with pytest.raises(Exception):
        ConfigLoader.load_config('bad.yaml') 