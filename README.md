# ROBOT-ARM

RobotArm is a Python dev configuration management and automation tool that enables quick and easy creation and management of development environments.

## Features

- start and stop the arm service easily
- Easily create development evironment from a yaml file as states
- run management commands easily from any directory in your terminal
- run tests easily from any directory in your terminal
- manage your virtual environments without breaking a sweat

## Future Features

- create ci/cd cycles from yaml files
- use multiple environments
- provision development databases easily
- setting up local git repo, and using git commands easily from any directory in your terminal

## How to install

> The current versions only run on Ubuntu-20.04+

- download latest release
- extract source file
- install with pip

> ``pip install .``

## Basics

- start arm api service

> `` arm service start ``
> confirm apis are running ``arm service status``

- to stop the api service

> `` arm service stop ``

- create a state

> ``arm [-s, --state] create full/path/file_name.yaml (tips: `pwd`\file_name.yaml)``

- list available states

> ``arm [-s, --state] list``

- activate state

> ``arm [-s, --state] activate state_id``

- run management commands e.g django

>``arm [-c, --command] management_cmd``

- run tests

>``arm [-t, --tests] run [defaults to test discorvery)``

------------------------------------------------------------------------------------------------------------------------

## Yaml Config File Template

```yaml
name: error-response-handler
version: v0.0.1

git: https://github.com/aaronahmid/error-response-handler
git_ssh: git@github.com/aaronahmid/error-response-handler

wdir: /home/.../.../error-response-handler
frameworks: none

venvs:
  - venv

databases:
  - name: error-handler-db
    type: postgresql
    user: [DB_USER]
    password: [DB_PASSWORD]
    host: [DB_HOST]
    port: [DB_PORT]


tests:
  - tool: unittest
    discovery: .
    test_dir: tests

```

------------------------------------------------------------------------------------------------------------------------

### Arm currently only supports only the Django web framwork, when used with a framework

> this tool is not ready for use, it's not completed and there are several bugs, not yet documented properly. Use with care!!
> Contribute?? Uhhhhhhhhm! Nope Not yet...
> To infinity and beyond
> -Buzz Lightyear's
