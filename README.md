# ROBOT-ARM

RobotArm is micro automation tool that enables easy creation and management of development environtments.

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
> the current versions only runs on ubuntu-20.04
> download latest release
> and run the setup.py script
> if setup.py does not set things up correctly, run the ./install.sh script
> ## To install, make use of the tempoary bash install.sh script for now

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
    
-run tests
>``arm [-t, --tests] run [defaults to test discorvery)``

------------------------------------------------------------------------------------------------------------------------
## Yaml Config File Template
![yaml_file_template](https://user-images.githubusercontent.com/41565098/161405937-e4ecefe8-738b-434e-9666-4ab98f40be64.jpg)
--------------------------------------------------------------------------------------------------------------------------

### Arm currently only supports only the django web framwork, when using with a framwork...

> this tool is not ready for use, it's not completed and there are several bugs, not yet documented properly, installation method not concluded yet, to use start the api service, add the dir to path or create an alias to the arm script or use the recomended temporary setup shell script. Use with care.

> Contribute?? Uhhhhhhhhm! Nope Not yet...

> To infinity and beyond
> -Buzz Lightyear's
