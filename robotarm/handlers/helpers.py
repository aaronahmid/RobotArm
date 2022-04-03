#!/usr/bin/python3
"""
A helper module
"""
import os
import subprocess
import pathlib

#BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# TODO: implemet a way to install requirements.txt file into the python envionment


def mkVenvLinux(vpath):
    """
    Creates a python virtual environment on linux
    """
    #print(vpath)
    if os.path.isdir(vpath):
        print('virtual env exists, activate it instead')
        return False

    try:
        try:
            with open('logfile', mode='w', encoding='utf8') as file:
                subprocess.Popen(['virtualenv', f'{vpath}'], stdout=file, stderr=file)
            os.mkdir('scripts')
            with open('scripts/env', mode='w', encoding='utf8') as file:
                text = f"#!/bin/bash\nsource {vpath}/bin/activate\nalias activate='source {vpath}/bin/activate'"
                file.write(text)
            subprocess.Popen(['chmod', 'u+x', 'scripts/env'])
            #subprocess.Popen(['{vpath}/bin/python', '-m', 'pip', 'install -r requirements.txt'])
        except FileExistsError:
            return True
    except Exception as e:
        print(e)
        return False

    return True

# TODO: fix database helper


def installPostgres():
    """
    installs a postgresql database server
    """
    with open(f'{BASE_DIR}/logfile', mode='w', encoding='utf8') as file:
        subprocess.run(['./install_postgresql_server'],
                       stderr=file, cwd=f'{BASE_DIR}/scripts')


def postgresCreate(db_name, db_user, db_host='localhost', db_port='5432'):
    """
    creates a postgresql database
    """
    installPostgres()
    print('creating postgresql database...')
    with open('{BASE_DIR}/logfile', mode='w', encoding='utf8') as file:
        subprocess.run([
            'createdb',
            f'-h {db_host}',
            f'-p {db_port}',
            f'-U {db_user}',
            f'{db_name}'], stderr=file)
