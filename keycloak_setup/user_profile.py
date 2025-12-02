import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class UserProfileManager:
    """
    Manage the Keycloak User Profile configuration (attributes).
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
        """Retrieve User Profile configuration."""
        response = requests.get(self._url(), headers=self.headers, verify=False)
        if response.status_code != 200:
            logger.error(f"❌ Failed to fetch user profile config: {response.text}")
            raise Exception("Failed to load user profile")
        return response.json()

    def save_profile(self, profile: dict):
        """Save entire User Profile JSON."""
        response = requests.put(self._url(), headers=self.headers, json=profile, verify=False)
        if response.status_code not in [200, 204]:
            logger.error(f"❌ Failed to update user profile: {response.text}")
            raise Exception("Failed to update user profile")
        logger.info("✅ User profile updated successfully.")

    def add_attribute(self, name: str, display_name: str, input_type: str = "text",
                      view_permissions=None, edit_permissions=None):
        view_permissions = view_permissions or ["user", "admin"]
        edit_permissions = edit_permissions or ["user", "admin"]

        profile = self.get_profile()
        attributes = profile.get("attributes", [])

        # Check existence
        if any(a["name"] == name for a in attributes):
            logger.info(f"ℹ️ Attribute '{name}' already exists.")
            return

        attributes.append({
            "name": name,
            "displayName": display_name,
            "required": False,
            "permissions": {
                "view": view_permissions,
                "edit": edit_permissions
            },
            "validators": {},
            "annotations": {
                "inputType": input_type
            }
        })

        profile["attributes"] = attributes
        self.save_profile(profile)
        logger.info(f"✅ Added user profile attribute '{name}'")
