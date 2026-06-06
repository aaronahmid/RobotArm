# 🦾 RobotArm

RobotArm is a polyglot development environment manager, scaffolding engine, and background orchestrator built in Go. It empowers you to instantly scaffold complex architectures, provision local databases, manage dependencies, and orchestrate development pipelines from anywhere on your machine.

## ✨ Features

- **Polyglot Scaffolding Engine:** Instantly generate clean architecture templates for Go (Gin) and Python (FastAPI).
- **Dependency Automation:** Automatically resolves and installs dependencies via `go mod`, `pip`, `poetry`, `pipenv`, and `npm`.
- **Database Provisioning:** Automatically provisions PostgreSQL development databases via Docker-Compose.
- **Centralized API Registry:** The `robotarm-api` background Docker daemon acts as a master orchestrator, using a persistent SQLite database to track every project across your entire machine.
- **Run Commands Anywhere:** Run management commands and test suites from any directory without needing to CD into your project.

## 🚀 Installation

### Prerequisites
- **Docker & Docker Compose** (Required for the API service and database provisioning)
- **Go 1.21+** (If building from source)

### Option 1: Pre-compiled Binaries (Recommended)
You can download the latest pre-compiled binary for your OS (macOS, Linux, Windows) from the GitHub [Releases](https://github.com/aaronahmid/robotarm/releases) page.

1. Download the binary.
2. Extract the archive.
3. Move `arm` to your PATH (e.g., `sudo mv arm /usr/local/bin/arm`).

### Option 2: Build from Source
```bash
git clone https://github.com/aaronahmid/robotarm.git
cd robotarm
make build
sudo mv bin/arm /usr/local/bin/arm
```

## 🛠 Quick Start

### 1. Start the Background API Service
The API service runs in the background inside Docker to track your projects globally and manage provisioning.
```bash
arm service start
```

*(You can verify it is running with `arm service status` or stop it with `arm service stop`)*

### 2. Define your Project State
Create a `state.yaml` file defining your project requirements:

```yaml
name: my-awesome-api
version: v1.0.0
language: python
framework: fastapi
architecture: clean
package_manager: poetry
wdir: /absolute/path/to/my-awesome-api

databases:
  - name: my-api-db
    type: postgresql
    user: admin
    password: securepassword
    port: 5432
    on_create: true
```

### 3. Scaffold the Environment
Point the CLI at your state file:
```bash
arm state create state.yaml
```
RobotArm will automatically:
1. Generate the folder structure and boilerplate code (FastAPI + Clean Architecture).
2. Create virtual environments (`python3 -m venv`).
3. Install packages via your chosen `package_manager` (Poetry).
4. Provision the PostgreSQL database via Docker.
5. Register the project in the global SQLite registry.

### 4. View Global Registry
Because RobotArm tracks your projects globally, you can list your environments from any directory on your computer:
```bash
arm state list
```

### 5. State Activation & Omnipresent Commands
You can activate a state to tell RobotArm which project you're currently working on:
```bash
arm state activate my-awesome-api
```
Once activated, you can run commands from **anywhere** on your computer, and RobotArm will execute them seamlessly inside your project's directory:
- **Git:** Run `arm git status`, `arm git push`, etc.
- **Python Envs:** Run `arm env list`, `arm env create my_env`, or `arm env activate my_env` (spawns a subshell).

For full details on the YAML configuration and CLI commands, please see the [CLI Reference](docs/CLI_REFERENCE.md).

## 🌐 Supported Generators
- **Go**: Gin (Clean Architecture)
- **Python**: FastAPI (Clean Architecture)

**Coming Soon:** Node.js (MERN, MEAN, MEVN), Python (Django, Flask), Go (Monolith)

---
> "To infinity and beyond" - Buzz Lightyear
