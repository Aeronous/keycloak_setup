# 🐳 Keycloak Docker Setup

This folder contains the `docker-compose.yaml` file for running a local Keycloak environment along with a PostgreSQL database — suitable for development and testing.

---

## 📦 Services

The `docker-compose.yaml` launches the following services:

### 🔐 keycloak

- Image: `quay.io/keycloak/keycloak:22.0.1`
- Mode: `start-dev`
- Depends on: `postgres`
- Environment variables used to connect to the database and set up admin credentials
- Exposed at: [http://localhost:8080](http://localhost:8080)

### 🐘 postgres

- Image: `postgres:15`
- Stores Keycloak data in a local PostgreSQL database
- Uses a named Docker volume for data persistence (`pgdata`)
- Not exposed publicly (internal only)

---

## ⚙️ Configuration

### Keycloak Environment Variables

| Variable             | Description                       | Default        |
|----------------------|-----------------------------------|----------------|
| `KEYCLOAK_ADMIN`     | Admin username                    | `admin`        |
| `KEYCLOAK_ADMIN_PASSWORD` | Admin password                    | `admin`        |
| `KC_DB`              | Database vendor                   | `postgres`     |
| `KC_DB_URL`          | PostgreSQL hostname               | `jdbc:postgresql://keycloak-db/keycloak`     |
| `KC_DB_USERNAME`     | PostgreSQL username               | `keycloak`     |
| `KC_DB_PASSWORD`     | PostgreSQL password               | `keycloak`     |

### PostgreSQL Environment Variables

| Variable       | Description             | Default     |
|----------------|-------------------------|-------------|
| `POSTGRES_DB`  | Database name           | `keycloak`  |
| `POSTGRES_USER`| Database user           | `keycloak`  |
| `POSTGRES_PASSWORD`| User password       | `keycloak`  |

---

## ▶️ Usage

### Start services

```bash
docker-compose up -d
