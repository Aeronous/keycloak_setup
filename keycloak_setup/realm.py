import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class RealmManager:
    """
    Manages creation of a Keycloak realm.

    Parameters:
        server_url (str): Base Keycloak URL
        token (str): Admin access token

    Methods:
        create_realm(realm_name): Ensures realm exists (creates if not)
    """

    def __init__(self, server_url: str, token: str):
        self.server_url = server_url.rstrip("/")
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def realm_exists(self, realm_name: str) -> bool:
        url = f"{self.server_url}/admin/realms/{realm_name}"
        response = requests.get(url, headers=self.headers)
        return response.status_code == 200

    def create_realm(self, realm_name: str):
        if self.realm_exists(realm_name):
            logger.info(f"✅ Realm '{realm_name}' already exists.")
            return

        url = f"{self.server_url}/admin/realms"
        payload = {
            "realm": realm_name,
            "enabled": True
        }
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code in [201, 204]:
            logger.info(f"✅ Realm '{realm_name}' created successfully.")
        else:
            logger.error(f"❌ Failed to create realm '{realm_name}': {response.text}")
            raise Exception(f"Failed to create realm '{realm_name}'")
