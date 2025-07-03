import click
from keycloak_setup.logger import get_logger
from keycloak_setup.config_loader import ConfigLoader
from keycloak_setup.auth import KeycloakAuth
from keycloak_setup.realm import RealmManager
from keycloak_setup.groups import GroupManager
from keycloak_setup.users import UserManager
from keycloak_setup.clients import ClientManager
from keycloak_setup.mappers import MapperManager
from keycloak_setup.installer import Installer
from keycloak_setup.uninstaller import Uninstaller

logger = get_logger()

@click.group()
def cli():
    """Keycloak Setup CLI"""
    pass


@cli.command(name="configure")
@click.option('--config', required=True, help='Path to configuration YAML file.')
def configure(config):
    """Run full setup: realm, groups, users, clients, mappers"""
    try:
        # Load config
        cfg = ConfigLoader.load_config(config)
        server_url = cfg["server_url"]
        realm = cfg["realm"]
        admin_user = cfg["admin_user"]
        admin_password = cfg["admin_password"]

        # Auth
        token = KeycloakAuth(server_url, admin_user, admin_password, realm="master").get_admin_token()

        # Realm
        RealmManager(server_url, token).create_realm(realm)

        # Init managers
        group_mgr = GroupManager(server_url, token, realm)
        user_mgr = UserManager(server_url, token, realm)
        client_mgr = ClientManager(server_url, token, realm)
        mapper_mgr = MapperManager(server_url, token, realm)

        # Groups
        group_mgr.create_groups(cfg.get("groups", []))

        # Users
        user_mgr.create_users(cfg.get("users", []))

        # Clients
        client_mgr.create_clients(cfg.get("clients", []))

        # Mappers
        for client in cfg.get("clients", []):
            client_id = client.get("client_id")
            if client_id:
                mapper_mgr.add_group_membership_mapper(client_id)

        logger.info("🎉 Keycloak setup completed successfully.")
    except Exception as e:
        logger.error(f"Setup failed: {e}")


@cli.command(name="add-user")
@click.option('--config', required=True, help='Path to configuration YAML file.')
@click.option('-u','--username', required=True, help='Username to add')
@click.option('-p','--password', required=True, help='Password for the user')
@click.option('-g','--group', required=True, help='Group to assign the user to')
@click.option('-e', '--email', help='Email address (optional)')
@click.option('-f', '--first-name', help='First name (optional)')
@click.option('-l', '--last-name', help='Last name (optional)')
def add_user(config, username, password, group, email, first_name, last_name):
    """Add a new user and assign to a group."""
    try:
        cfg = ConfigLoader.load_config(config)
        server_url = cfg["server_url"]
        realm = cfg["realm"]
        admin_user = cfg["admin_user"]
        admin_password = cfg["admin_password"]

        token = KeycloakAuth(server_url, admin_user, admin_password, realm="master").get_admin_token()
        user_mgr = UserManager(server_url, token, realm)

        user_data = {
            "username": username,
            "password": password,
            "group": group
        }

        if email:
            user_data["email"] = email
        if first_name:
            user_data["firstName"] = first_name
        if last_name:
            user_data["lastName"] = last_name

        user_mgr.create_user(user_data)
        logger.info("🎉 User added successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to add user: {e}")


@cli.command(name="assign-user")
@click.option('--config', required=True, help='Path to configuration YAML file.')
@click.option('-u','--username', required=True, help='Username to assign')
@click.option('-g','--group', required=True, help='Group to assign the user to')
def assign_user_group(config, username, group):
    """Assign existing user to existing group."""
    try:
        cfg = ConfigLoader.load_config(config)
        server_url = cfg["server_url"]
        realm = cfg["realm"]
        admin_user = cfg["admin_user"]
        admin_password = cfg["admin_password"]

        token = KeycloakAuth(server_url, admin_user, admin_password, realm="master").get_admin_token()
        user_mgr = UserManager(server_url, token, realm)

        user_mgr.assign_to_group(username, group)
        logger.info("✅ User assigned to group successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to assign user to group: {e}")


@cli.command(name="add-group")
@click.option("--name", "-n", required=True, help="Group name(s), comma-separated for multiple.")
@click.option("--parent", "-p", default=None, help="Parent group name, if creating subgroups.")
@click.option("--config", "-c", required=True, help="Path to config YAML file.")
def add_group(name, parent, config):
    """
    Create group(s) in Keycloak. Supports comma-separated names and nested groups.
    """
    try:
        cfg = ConfigLoader.load_config(config)
        server_url = cfg["server_url"]
        realm = cfg["realm"]
        admin_user = cfg["admin_user"]
        admin_password = cfg["admin_password"]

        token = KeycloakAuth(server_url, admin_user, admin_password).get_admin_token()
        gm = GroupManager(server_url, token, realm)

        group_names = [n.strip() for n in name.split(",") if n.strip()]
        parent_id = gm.find_root_group_id(parent) if parent else None

        for group_name in group_names:
            gm.create_group(group_name, parent_id=parent_id)

    except Exception as e:
        logger.error(f"❌ Failed to create group(s): {e}")


@cli.command("get-client-secret")
@click.option("--client-id", "-c", required=True, help="Client ID to fetch the secret for.")
@click.option("--config", "-f", required=True, help="Path to the YAML configuration file.")
def get_client_secret(client_id, config):
    """
    Fetch and display the confidential client secret.
    """
    try:
        cfg = ConfigLoader.load_config(config)
        server_url = cfg["server_url"]
        realm = cfg["realm"]
        admin_user = cfg["admin_user"]
        admin_password = cfg["admin_password"]

        token = KeycloakAuth(server_url, admin_user, admin_password, realm="master").get_admin_token()
        clients = ClientManager(server_url, token, realm)

        secret = clients.get_client_secret(client_id)
        click.echo(f"🔐 Secret for client '{client_id}': {secret}")
    except Exception as e:
        click.echo(f"❌ Failed to retrieve secret: {e}")


@cli.command(name="install")
@click.option("--method", "-m", type=click.Choice(["docker", "helm"]), required=True, help="Installation method")
def install(method):
    """
    Install Keycloak using docker-compose or Helm.
    """

    try:
        installer = Installer()
        installer.install(method)
    except Exception as e:
        logger.error(f"❌ Installation failed: {e}")


@cli.command(name="uninstall")
@click.option("--method", "-m", type=click.Choice(["docker", "helm"]), required=True, help="Uninstallation method")
def uninstall(method):
    """
    Uninstall Keycloak using docker-compose or Helm.
    """
    try:
        uninstaller = Uninstaller()
        uninstaller.uninstall(method)
    except Exception as e:
        logger.error(f"❌ Uninstallation failed: {e}")
