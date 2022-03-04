#!/usr/bin/python3
"""
RobotArm entry script v0.01
"""
import controllers
import sys

# maps keys to controllers
STATE_CONTROLLERS = {
    'create': 'controllers.StateController().create',
    'load': 'controllers.StateController().load',
    'stop': 'controllers.StateController().stop',
    'delete': 'controllers.StateController().delete'
}

COMMAND_CONTROLLERS = {

}

TEST_CONTROLLERS = {

}

API_STATUS_CONTROLLERS = {
    'health': 'controllers.APIStatusController().health_check',
}

if __name__ == '__main__':
    # maps keys to controller classes
    options = {
        '-v': 'v0.01',
        '-h': 'help',
        '-s': STATE_CONTROLLERS,
        '-c': COMMAND_CONTROLLERS,
        '-t': TEST_CONTROLLERS,
        '-p': 'Pipeline controller/handler',
        'status': API_STATUS_CONTROLLERS,
    }

    # extract file name and remove it
    args = sys.argv
    args_length = len(args)  # store args length

    arm_usage = 'Usage'
    file_name = args[0]

    # make sure length isn't less than 2
    if args_length < 2:
        exit(arm_usage)

    # remove file name
    del(args[0])

    # extract option and check if
    # option is valid
    option = args[0]
    if option in options.keys():
        pass
    else:
        exit(arm_usage)

    # remove option
    del(args[0])

    # check if option is version or help
    if args_length == 2:
        if option in ('-v', '-h'):
            print(options[option])
        else:
            exit(arm_usage)

    # builds controller path by evaluating fails if
    # controller commands doesn't exists
    try:
        ct = options[option]
        eval(ct[args[0]])(args)
    except KeyError:
        exit('Unknown option command')
