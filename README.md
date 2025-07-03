# 🔐 Keycloak Setup CLI

A modular and extensible CLI tool to automate the setup of Keycloak realms, users, groups, clients, and protocol mappers — fully driven by configuration.

---

## 🚀 Features

- ✅ Automated creation of realms
- ✅ Group hierarchy support (including nested groups)
- ✅ User creation and group assignment
- ✅ Client creation with optional secrets and redirect URIs
- ✅ Built-in mappers configuration (group membership)
- ✅ Token decoding support for permission extraction
- ✅ Docker-based installation of Keycloak (Helm planned)
- ✅ Modular and extendable codebase

---

## 📦 Requirements

- Python 3.8+
- Docker (for local Keycloak installation)
- Keycloak 22+

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aeronous/keycloak_setup.git
cd keycloak-setup
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---
## ⚙️ CLI Usage

All commands are invoked using:

```bash
python main.py <command> [options]
```

### 🔧 Available Commands

| Command | Description |
| ------- | ----------- |
 | configure | Run full setup from a YAML configuration|
| add-user | Add a single user with group assignment|
 | add-group | Create root or nested groups |
 | assign-user | Assign an existing user to an existing group |
 | install | Install Keycloak using Docker (or Helm in the future) |
 | get-client-secret | Print the client secret |  

### 🧪 Examples

#### 🔁 Full setup from configuration

```bash
python main.py configure --config config/setup.yaml
```

#### 👤 Add a user manually

```bash
python main.py add-user --username daniel --password 123456 \
  --email daniel@example.com --first-name Daniel --last-name Pahima \
  --group tech_group --config config/setup.yaml
```

#### 👥 Add a group with nested groups

```bash
python main.py add-group --name frontend,backend --parent tech_group --config config/setup.yaml
```

#### 🔁 Assign user to group

```bash
python main.py assign-user --username daniel --group backend --config config/setup.yaml
```

#### 🔐 Get a Client Secret

```bash
python main.py get-client-secret --client-id <your-client-id> --config config/setup.yaml
```

#### 🐳 Start Keycloak with Docker
```bash
python main.py install --method docker
```

---

## 🧾 Configuration File (YAML)

All resources are defined in a single setup.yaml file.

### 🗂 Structure

```yaml
server:
  url: http://localhost:8080
  admin_user: admin
  admin_password: admin

realm:
  name: auth-system

groups:
  - name: tech_group
    subgroups:
      - operational__viewer
      - operational__operator

users:
  - username: daniel
    password: 123456
    email: daniel@example.com
    first_name: Daniel
    last_name: Pahima
    group: operational__viewer

clients:
  - client_id: fe-c4i
    public: false
    secret: tiZPQsoRwWvv4VaB0bxX0oRDcNY3YEuP
    redirect_uris:
      - http://localhost:3000/*
    web_origins:
      - http://localhost:3000

```

---

## 🔑 Notes

* subgroups supports recursive nesting.

* If public is false, you must provide a secret.

* Group assignment is validated; users must belong to defined groups.

