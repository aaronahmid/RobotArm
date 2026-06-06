#!/usr/bin/python3
"""
RobotArm entry script v0.1.0
"""
import os
import pathlib
import sys

#BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
#sys.path.append(BASE_DIR)
#print(BASE_DIR)

from robotarm import controllers

# mappings for state controllers
STATE_CONTROLLERS = {
    'list': 'controllers.StateController().list',
    'create': 'controllers.StateController().create',
    'activate': 'controllers.StateController().activate',
    'stop': 'controllers.StateController().stop',
    'delete': 'controllers.StateController().delete',
}

# mappings for command controllers
COMMAND_CONTROLLERS = {
    'execute': 'controllers.CommandController().executeCommand',
    'list': 'controllers.CommandController().listCommands'
}

# mappings for test controllers
TEST_CONTROLLERS = {
    'run': 'cotrollers.TestController().run'
}

# mappings for api service controller
API_SERVICE_CONTROLLERS = {
    'status': 'controllers.APIServiceController().health_check',
    'start': 'controllers.APIServiceController().start_service',
    'stop': 'controllers.APIServiceController().stop_service'
}


def main():
    """
    parses command line arguments
    and maps keyword options to controllers
    """
    # maps keyword options to controller mappings
    options = {
        ('-v', '--version'): 'v0.1.4',
        ('-h', '--help'): 'help',
        ('-s', '--state'): STATE_CONTROLLERS,
        ('-c', '--command'): COMMAND_CONTROLLERS,
        ('-t', '--test'): TEST_CONTROLLERS,
        ('-p', '--pipline'): 'Pipeline controller/handler',
        'service': API_SERVICE_CONTROLLERS,
    }

    # extract arguments and length
    args = sys.argv
    args_length = len(args)  # store args length

    arm_usage = "error: \
garbage command option\n\narm [-option, --option] \
[action]\n\ntry arm \
[-h, --help]\n For help text"

    file_name = args[0]

    # make sure length isn't less than 2
    if args_length < 2:
        exit(arm_usage)

    # remove file name
    del(args[0])

    # extract option
    option = args[0]

    # remove option
    del(args[0])

    # check if option is version or help
    if args_length == 2:
        # Prints arm script version or help

        print(option)
        if option in ('-v', '-h', '--version', '--help'):
            for option_keywords in options.keys():
                if option in option_keywords:
                    print(options[option_keywords])
            exit()
        else:
            exit(arm_usage)

    # builds controller method calls
    # fails if controller keyword option
    # or controller method doesn't exists
    try:
        for keyword_options in options.keys():
            if option in keyword_options or option is keyword_options:
                keyword_option = options[keyword_options]
        try:
            if keyword_option is COMMAND_CONTROLLERS:
                try:
                    function = eval(keyword_option[args[0]])
                    function(args)
                except KeyError:
                    function = eval(keyword_option['execute'])
                    function(args)
                #exit()
            if keyword_option is API_SERVICE_CONTROLLERS:
                function = eval(keyword_option[args[0]])
                function()
            else:
                function = eval(keyword_option[args[0]])
                function(args)
        except UnboundLocalError:
            exit(arm_usage)
    except KeyError:
        exit('Unknown command option')


# runs the main funtion
# when script is invoked
if __name__ == '__main__':
    main()
