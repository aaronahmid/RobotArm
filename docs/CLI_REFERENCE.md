# RobotArm CLI Reference

This document outlines the available configuration blocks in `state.yaml` and the commands available in the `arm` CLI.

## State Configuration (`state.yaml`)

### Root Properties
| Property | Type | Description |
|----------|------|-------------|
| `name` | string | **(Required)** The unique name of your project. |
| `version` | string | Version string (e.g., `v1.0.0`). |
| `language` | string | **(Required)** `python`, `go`, `node`, etc. |
| `framework` | string | `fastapi`, `django`, `gin`, etc. |
| `architecture` | string | `clean`, `monolith`. |
| `git` | string | HTTPS Git URL to initialize. |
| `git_ssh` | string | SSH Git URL to initialize. |
| `wdir` | string | **(Required)** Absolute path to scaffold the project into. |
| `package_manager` | string | `pip`, `poetry`, `pipenv`, `npm`, `yarn`, `go mod`. |

### Virtual Environments (`venvs`)
*(Primarily for Python)*
```yaml
venvs:
  - name: testing_env
    on_create: true
```

### Databases (`databases`)
*(Provisions Docker Compose services)*
```yaml
databases:
  - name: my-db
    type: postgres
    user: admin
    password: password
    port: "5432"
    on_create: true
```

---

## Command Line Interface

### `arm service`
Controls the background API daemon.
- `arm service start`: Builds and starts the API in Docker.
- `arm service stop`: Stops and removes the API containers.
- `arm service status`: Checks if the API is running.

### `arm state`
Manages project registration and scaffolding.
- `arm state create <file.yaml>`: Scaffolds a project, creates environments, installs dependencies, sets up Git, provisions databases, and registers the project.
- `arm state list`: Lists all registered projects on the machine.
- `arm state activate <name>`: Sets the active project globally, allowing you to run commands from anywhere.

### `arm git`
Executes native Git commands inside the active project directory.
- `arm git <args...>`: Examples include `arm git status`, `arm git push`, `arm git pull`.

### `arm env`
Manages virtual environments within the active project.
- `arm env list`: Lists all python environments.
- `arm env create <name>`: Creates a new environment.
- `arm env delete <name>`: Deletes an environment.
- `arm env activate <name>`: Spawns a new subshell with the environment injected.
