import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class ClientScopeManager:
    """
    Manages Keycloak Client Scopes and their mappers.
    """

    def __init__(self, server_url: str, token: str, realm: str):
        self.server_url = server_url.rstrip("/")
        self.token = token
        self.realm = realm
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_client_scope(self, name: str) -> str:
        """
        Create client scope if missing. Returns its internal ID.
        """
        # Check existing
        url = f"{self.server_url}/admin/realms/{self.realm}/client-scopes"
        resp = requests.get(url, headers=self.headers, verify=False)
        if resp.status_code != 200:
            raise Exception("Failed to read client scopes")

        for cs in resp.json():
            if cs["name"] == name:
                logger.info(f"ℹ️ Client scope '{name}' already exists.")
                return cs["id"]

        # Create new
        payload = {"name": name, "protocol": "openid-connect"}
        resp = requests.post(url, headers=self.headers, json=payload, verify=False)
        if resp.status_code not in [201, 204]:
            raise Exception(f"Failed to create client scope '{name}': {resp.text}")

        logger.info(f"✅ Client scope '{name}' created successfully.")

        # Re-fetch to get ID
        resp = requests.get(url, headers=self.headers, verify=False)
        for cs in resp.json():
            if cs["name"] == name:
                return cs["id"]

        raise Exception("Client scope creation succeeded but ID not found.")

    def add_avatar_mapper(self, scope_id: str):
        """
        Add mapper (user attribute -> OIDC claim) to the avatar client scope.
        """
        url = f"{self.server_url}/admin/realms/{self.realm}/client-scopes/{scope_id}/protocol-mappers/models"

        payload = {
            "name": "avatar",
            "protocol": "openid-connect",
            "protocolMapper": "oidc-usermodel-attribute-mapper",
            "config": {
                "user.attribute": "avatar",
                "id.token.claim": "true",
                "access.token.claim": "true",
                "userinfo.token.claim": "true",
                "claim.name": "avatar",
                "jsonType.label": "String"
            }
        }

        resp = requests.post(url, headers=self.headers, json=payload, verify=False)
        if resp.status_code in [201, 204]:
            logger.info("✅ Avatar mapper added to client scope.")
        elif resp.status_code == 409:
            logger.info("ℹ️ Avatar mapper already exists.")
        else:
            raise Exception(f"Failed to add avatar mapper: {resp.text}")

    def assign_scope_to_client(self, client_uuid: str, scope_id: str):
        """
        Add the avatar scope as OPTIONAL client scope.
        """
        # You can choose default-client-scopes if you want
        url = f"{self.server_url}/admin/realms/{self.realm}/clients/{client_uuid}/optional-client-scopes/{scope_id}"

        resp = requests.put(url, headers=self.headers, verify=False)

        if resp.status_code in [200, 204]:
            logger.info(f"✅ Avatar scope assigned to client '{client_uuid}'.")
        elif resp.status_code == 409:
            logger.info(f"ℹ️ Avatar scope already linked to client '{client_uuid}'.")
        else:
            raise Exception(f"Failed assigning client scope: {resp.text}")
