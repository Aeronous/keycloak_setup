import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class MapperManager:
    """
    Manages client mappers such as Group Membership.

    Parameters:
        server_url (str): Base Keycloak URL
        token (str): Admin access token
        realm (str): Target realm name

    Methods:
        add_group_membership_mapper(client_id: str)
    """

    def __init__(self, server_url: str, token: str, realm: str):
        self.server_url = server_url.rstrip("/")
        self.token = token
        self.realm = realm
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_client_uuid(self, client_id: str) -> str:
        url = f"{self.server_url}/admin/realms/{self.realm}/clients?clientId={client_id}"
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200 and response.json():
            return response.json()[0]["id"]
        return None

    def add_group_membership_mapper(self, client_id: str):
        client_uuid = self.get_client_uuid(client_id)
        if not client_uuid:
            logger.error(f"❌ Client '{client_id}' not found.")
            raise Exception(f"Client '{client_id}' not found.")

        url = f"{self.server_url}/admin/realms/{self.realm}/clients/{client_uuid}/protocol-mappers/models"
        payload = {
            "name": "group-membership-mapper",
            "protocol": "openid-connect",
            "protocolMapper": "oidc-group-membership-mapper",
            "consentRequired": False,
            "config": {
                "access.token.claim": "true",
                "claim.name": "groups",
                "jsonType.label": "String",
                "full.path": "true"
            }
        }

        response = requests.post(url, json=payload, headers=self.headers, verify=False)
        if response.status_code in [201, 204]:
            logger.info(f"✅ Group membership mapper added to client '{client_id}'.")
        elif response.status_code == 409:
            logger.info(f"ℹ️ Mapper already exists for client '{client_id}'.")
        else:
            logger.error(f"❌ Failed to add mapper: {response.text}")
            raise Exception("Failed to add group membership mapper.")
