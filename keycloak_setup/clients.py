import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class ClientManager:
    """
    Manages creation of clients in Keycloak.

    Parameters:
        server_url (str): Base Keycloak URL
        token (str): Admin access token
        realm (str): Target realm name

    Methods:
        create_clients(clients_config: List[dict])
    """

    def __init__(self, server_url: str, token: str, realm: str):
        self.server_url = server_url.rstrip("/")
        self.token = token
        self.realm = realm
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def client_exists(self, client_id: str) -> bool:
        url = f"{self.server_url}/admin/realms/{self.realm}/clients?clientId={client_id}"
        response = requests.get(url, headers=self.headers)
        return bool(response.ok and response.json())

    def create_client(self, client: dict):
        client_id = client.get("client_id")
        secret = client.get("secret")
        redirect_uris = client.get("redirect_uris", [])
        web_origins = client.get("web_origins", [])

        if not client_id:
            raise ValueError("Each client must include 'client_id'.")

        if self.client_exists(client_id):
            logger.info(f"ℹ️ Client '{client_id}' already exists.")
            return

        payload = {
            "clientId": client_id,
            "enabled": True,
            "publicClient": not bool(secret),
            "redirectUris": redirect_uris,
            "webOrigins": web_origins,
        }

        if secret:
            payload["secret"] = secret
            payload["serviceAccountsEnabled"] = True
            payload["protocol"] = "openid-connect"

        url = f"{self.server_url}/admin/realms/{self.realm}/clients"
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code in [201, 204]:
            logger.info(f"✅ Client '{client_id}' created successfully.")
        else:
            logger.error(f"❌ Failed to create client '{client_id}': {response.text}")
            raise Exception(f"Failed to create client '{client_id}'")

    def create_clients(self, clients_config: list):
        for client in clients_config:
            self.create_client(client)
