import subprocess
import os
from keycloak_setup.logger import get_logger

logger = get_logger()

class Uninstaller:
    """
    Handles uninstallation of the Keycloak server via Docker or Helm.
    """

    def uninstall(self, method: str):
        if method == "docker":
            self._uninstall_docker()
        elif method == "helm":
            raise NotImplementedError("Helm uninstallation is not implemented yet.")
        else:
            raise ValueError("Invalid uninstallation method")

    def _uninstall_docker(self):
        compose_file = os.path.join(os.path.dirname(__file__), "..", "infra", "docker", "docker-compose.yaml")
        if not os.path.isfile(compose_file):
            raise FileNotFoundError("docker-compose.yaml not found in infra/docker")

        logger.info("🧹 Stopping and removing Docker containers...")
        result = subprocess.run(["docker-compose", "-f", compose_file, "down", "-v"], capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"❌ Docker Compose down failed:\n{result.stderr}")
            raise Exception("Docker Compose down failed")

        logger.info("✅ Docker-based Keycloak has been removed successfully.")
