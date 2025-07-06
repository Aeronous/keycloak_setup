import pytest
from unittest.mock import patch, MagicMock
from keycloak_setup.installer import Installer

@patch('os.path.isfile', return_value=True)
@patch('subprocess.run')
def test_install_docker_success(mock_run, mock_isfile):
    mock_run.return_value = MagicMock(returncode=0)
    installer = Installer()
    installer.install('docker')
    mock_run.assert_called_once()

@patch('os.path.isfile', return_value=False)
def test_install_docker_compose_missing(mock_isfile):
    installer = Installer()
    with pytest.raises(FileNotFoundError):
        installer.install('docker')

@patch('os.path.isfile', return_value=True)
@patch('subprocess.run')
def test_install_docker_subprocess_error(mock_run, mock_isfile):
    mock_run.return_value = MagicMock(returncode=1, stderr='error')
    installer = Installer()
    with pytest.raises(Exception):
        installer.install('docker')


def test_install_invalid_method():
    installer = Installer()
    with pytest.raises(ValueError):
        installer.install('invalid')


def test_install_helm_not_implemented():
    installer = Installer()
    with pytest.raises(NotImplementedError):
        installer.install('helm') 