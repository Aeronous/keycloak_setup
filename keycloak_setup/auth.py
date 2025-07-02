import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class KeycloakAuth:
    """
    Handles authentication against the Keycloak server.

    Parameters:
        server_url (str): Base URL of Keycloak server
        admin_user (str): Admin username
        admin_password (str): Admin password
        realm (str): Realm to authenticate against (default 'master')

    Methods:
        get_admin_token(): Returns an admin access token string
    """
    def __init__(self, server_url: str, admin_user: str, admin_password: str, realm: str = "master"):
        self.token_url = f"{server_url}/realms/{realm}/protocol/openid-connect/token"
        self.admin_user = admin_user
        self.admin_password = admin_password

    def get_admin_token(self) -> str:
        data = {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": self.admin_user,
            "password": self.admin_password,
        }
        try:
            response = requests.post(self.token_url, data=data)
            response.raise_for_status()
            token = response.json().get("access_token")
            if not token:
                raise Exception("No access_token in response.")
            logger.info("✅ Admin token acquired successfully.")
            return token
        except Exception as e:
            logger.error(f"❌ Failed to obtain admin token: {e}")
            raise Exception("Admin authentication failed.")
