import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class GroupManager:
    """
    Handles creation of groups and subgroups in Keycloak.

    Parameters:
        server_url (str): Base Keycloak URL
        token (str): Admin access token
        realm (str): Target realm name

    Methods:
        create_groups(groups_config: List[dict]): Create all groups and subgroups from config
    """

    def __init__(self, server_url: str, token: str, realm: str):
        self.server_url = server_url.rstrip("/")
        self.token = token
        self.realm = realm
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_group_id_by_name(self, parent_id: str, name: str) -> str:
        url = f"{self.server_url}/admin/realms/{self.realm}/groups/{parent_id}/children"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        for group in response.json():
            if group["name"] == name:
                return group["id"]
        return None

    def find_root_group_id(self, name: str) -> str:
        url = f"{self.server_url}/admin/realms/{self.realm}/groups"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        for group in response.json():
            if group["name"] == name:
                return group["id"]
        return None

    def create_group(self, name: str, parent_id: str = None):
        if parent_id:
            url = f"{self.server_url}/admin/realms/{self.realm}/groups/{parent_id}/children"
        else:
            url = f"{self.server_url}/admin/realms/{self.realm}/groups"

        payload = {"name": name}
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code in [201, 204]:
            logger.info(f"✅ Group '{name}' created successfully.")
        elif response.status_code == 409:
            logger.info(f"ℹ️ Group '{name}' already exists.")
        else:
            logger.error(f"❌ Failed to create group '{name}': {response.text}")
            raise Exception(f"Failed to create group '{name}'")

    def create_groups(self, groups_config: list, parent_id: str = None):
        """
        Recursively creates groups and subgroups from config.
        """
        for group in groups_config:
            group_name = group.get("name")
            if not group_name:
                continue

            # Try to find if the group already exists
            group_id = self.find_root_group_id(group_name) if not parent_id else self.get_group_id_by_name(parent_id, group_name)

            if not group_id:
                self.create_group(group_name, parent_id)
                group_id = self.find_root_group_id(group_name) if not parent_id else self.get_group_id_by_name(parent_id, group_name)

            # Handle subgroups recursively
            subgroups = group.get("subgroups", [])
            if subgroups:
                self.create_groups(subgroups, parent_id=group_id)
