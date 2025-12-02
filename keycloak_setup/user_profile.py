import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class UserProfileManager:
    """
    Manage Keycloak user profile attributes (KC 25–26 compatible).
    """

    def __init__(self, server_url: str, token: str, realm: str):
        self.server_url = server_url.rstrip("/")
        self.token = token
        self.realm = realm
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _url(self):
        return f"{self.server_url}/admin/realms/{self.realm}/users/profile"

    def get_profile(self) -> dict:
        response = requests.get(self._url(), headers=self.headers, verify=False)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user profile: {response.text}")
        return response.json()

    def save_profile(self, profile: dict):
        response = requests.put(self._url(), headers=self.headers, json=profile, verify=False)
        if response.status_code not in [200, 204]:
            raise Exception(f"Failed to update user profile: {response.text}")
        logger.info("✅ User profile updated successfully.")

    def add_attribute(self, name: str, display_name: str, input_type="text",
                      view_permissions=None, edit_permissions=None):

        view_permissions = view_permissions or ["admin", "user"]
        edit_permissions = edit_permissions or ["admin", "user"]

        # Load exact live profile structure
        profile = self.get_profile()

        attributes = profile.get("attributes", [])

        # Skip if exists
        if any(attr["name"] == name for attr in attributes):
            logger.info(f"ℹ️ Attribute '{name}' already exists.")
            return

        new_attr = {
            "name": name,
            "displayName": display_name,
            "validations": {},   # You can add URL validation later
            "permissions": {
                "view": view_permissions,
                "edit": edit_permissions
            },
            "multivalued": False,
            "annotations": {
                "inputType": input_type
            }
        }

        attributes.append(new_attr)
        profile["attributes"] = attributes  # PUT only replaces attributes array

        self.save_profile(profile)
        logger.info(f"✅ Added user profile attribute '{name}'.")
