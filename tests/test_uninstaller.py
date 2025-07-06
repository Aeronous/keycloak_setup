import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.uninstaller import Uninstaller

@patch('os.path.isfile', return_value=True)
@patch('subprocess.run')
def test_uninstall_docker_success(mock_run, mock_isfile):
    mock_run.return_value = MagicMock(returncode=0)
    uninstaller = Uninstaller()
    uninstaller.uninstall('docker')
    mock_run.assert_called_once()

@patch('os.path.isfile', return_value=False)
def test_uninstall_docker_compose_missing(mock_isfile):
    uninstaller = Uninstaller()
    with pytest.raises(FileNotFoundError):
        uninstaller.uninstall('docker')

@patch('os.path.isfile', return_value=True)
@patch('subprocess.run')
def test_uninstall_docker_subprocess_error(mock_run, mock_isfile):
    mock_run.return_value = MagicMock(returncode=1, stderr='error')
    uninstaller = Uninstaller()
    with pytest.raises(Exception):
        uninstaller.uninstall('docker')

def test_uninstall_invalid_method():
    uninstaller = Uninstaller()
    with pytest.raises(ValueError):
        uninstaller.uninstall('invalid')

def test_uninstall_helm_not_implemented():
    uninstaller = Uninstaller()
    with pytest.raises(NotImplementedError):
        uninstaller.uninstall('helm') 