# ROBOT-ARM

RobotArm is micro automation tool that enables easy creation and management of development environtments.

## Features
- Easily create development evironment from a yaml file as states
- run management commands easily from any directory in your terminal
- run tests easily from directory in your terminal
- manage your virtual environments without breaking a sweat

## Future Features
- create ci/cd cycles from yaml files
- use multiple environments
- provision development databases easily

## Basics
create a state
    ``arm -s create full/path/file_name.yaml``

activate state
    ``arm -s activate state_id``

run management commands e.g django
    ``arm -c runserver [defualts to execute command]``
    
run tests
    ``arm -t run [defaults to test discorvery)``
    
> ### Arm currently only supports only the django web framwork, when using with a framwork...

> this tool is not ready for use, it's not completed and there are several bugs, installation method not concluded yet, to use start the api service, add the dir to path or create an alias to the arm script. user with care.

> To infinity and beyond
> -Buzz Lightyear's
