import requests
from keycloak_setup.logger import get_logger

logger = get_logger()

class UserManager:
    """
    Handles user creation and group assignment in Keycloak.

    Parameters:
        server_url (str): Base Keycloak URL
        token (str): Admin access token
        realm (str): Target realm

    Methods:
        create_users(users_config: List[dict])
    """

    def __init__(self, server_url: str, token: str, realm: str):
        self.server_url = server_url.rstrip("/")
        self.token = token
        self.realm = realm
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_group_id_by_name(self, name: str) -> str:
        url = f"{self.server_url}/admin/realms/{self.realm}/groups"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        for group in response.json():
            if group["name"] == name:
                return group["id"]
        return None

    def create_user(self, user: dict):
        username = user.get("username")
        first_name = user.get("firstName")
        last_name = user.get("lastName")
        password = user.get("password")
        email = user.get("email")
        group_name = user.get("group")

        if not (username and password and group_name):
            raise ValueError("Each user must have 'username', 'password', and 'group'.")

        group_id = self.get_group_id_by_name(group_name)
        if not group_id:
            raise Exception(f"Group '{group_name}' not found for user '{username}'")

        # Step 1: Create the user
        user_payload = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "enabled": True,
            "email": email,
            "credentials": [
                {
                    "type": "password",
                    "value": password,
                    "temporary": False
                }
            ]
        }

        url = f"{self.server_url}/admin/realms/{self.realm}/users"
        response = requests.post(url, json=user_payload, headers=self.headers)

        if response.status_code == 201:
            logger.info(f"✅ User '{username}' created.")
        elif response.status_code == 409:
            logger.info(f"ℹ️ User '{username}' already exists.")
        else:
            logger.error(f"❌ Failed to create user '{username}': {response.text}")
            raise Exception(f"Failed to create user '{username}'")

        # Step 2: Get user ID
        user_id = self.get_user_id_by_username(username)
        if not user_id:
            raise Exception(f"Cannot find ID of user '{username}' after creation.")

        # Step 3: Assign to group
        assign_url = f"{self.server_url}/admin/realms/{self.realm}/users/{user_id}/groups/{group_id}"
        assign_response = requests.put(assign_url, headers=self.headers)

        if assign_response.status_code in [204, 201]:
            logger.info(f"✅ User '{username}' assigned to group '{group_name}'.")
        else:
            logger.error(f"❌ Failed to assign user '{username}' to group '{group_name}': {assign_response.text}")
            raise Exception(f"Failed to assign user to group")

    def get_user_id_by_username(self, username: str) -> str:
        url = f"{self.server_url}/admin/realms/{self.realm}/users?username={username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        users = response.json()
        if users:
            return users[0]["id"]
        return None

    def create_users(self, users_config: list):
        for user in users_config:
            self.create_user(user)

    def assign_to_group(self, username: str, group_name: str):
        """
        Assigns an existing user to a group by name.

        Parameters:
            username (str): Username to assign
            group_name (str): Group name to assign the user to

        Raises:
            Exception: if user or group not found or API call fails
        """
        user_id = self.get_user_id_by_username(username)
        if not user_id:
            raise Exception(f"User '{username}' not found.")

        group_id = self.get_group_id_by_name(group_name)
        if not group_id:
            raise Exception(f"Group '{group_name}' not found.")

        url = f"{self.server_url}/admin/realms/{self.realm}/users/{user_id}/groups/{group_id}"
        response = requests.put(url, headers=self.headers)

        if response.status_code in [204, 201]:
            logger.info(f"✅ User '{username}' assigned to group '{group_name}'.")
        else:
            logger.error(f"❌ Failed to assign user '{username}' to group '{group_name}': {response.text}")
            raise Exception("Failed to assign user to group")

