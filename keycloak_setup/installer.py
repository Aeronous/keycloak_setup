import subprocess
import os
from keycloak_setup.logger import get_logger

logger = get_logger()

class Installer:
    """
    Handles installation of the Keycloak server via Docker or Helm.
    """

    def install(self, method: str):
        if method == "docker":
            self._install_docker()
        elif method == "helm":
            raise NotImplementedError("Helm installation is not implemented yet.")
        else:
            raise ValueError("Invalid installation method")

    def _install_docker(self):
        compose_file = os.path.join(os.path.dirname(__file__), "..", "infra", "docker", "docker-compose.yaml")
        if not os.path.isfile(compose_file):
            raise FileNotFoundError("docker-compose.yaml not found in infra/docker")

        logger.info("📦 Starting Keycloak via Docker Compose...")
        result = subprocess.run(["docker-compose", "-f", compose_file, "up", "-d"], capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"❌ Docker Compose failed:\n{result.stderr}")
            raise Exception("Docker Compose failed")

        logger.info("✅ Keycloak has been started using Docker Compose.")

