#!/usr/bin/python3
"""
A helper module
"""
import os
import subprocess
import pathlib
import sys

try:
    from decouple import config as getenv
except ModuleNotFoundError:
    print(
        "python decouple not found, please install\
using os.getenv for now but some things won't work"
    )
    from os import getenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
setup_db_file = 'setupdb'


def install_db():
    """installs a database by running script
    """
    install_pgsql = ['./scripts/install_postgresql_server']
    subprocess.run(install_pgsql, cwd=BASE_DIR)


def create_db(db_name: str, user: str, h=None, p=None, E=None):
    """creates a postgresql database
    """
    if type(db_name) and type(user) != str:
        TypeError('unexpected argument type provided for db_name or user\
            , must be a string')

    if len(db_name) == 0:
        db_name = 'proj-dev-db-local1'

    host = 'localhost'
    port = 5432
    enconding = 'utf8'
    if h and p and E != None:
        host = h
        port = p
        enconding = E

    create_db_args = f'createdb/-U {user}/-h{host}/-p {port}/-E {enconding}/{db_name}'.split(
        sep='/')
    with open('logfile', mode='w+', encoding='utf8') as logfile:
        try:
            os.system(' '.join(create_db_args))
        except Exception:
            raise(Exception)
    print(f'database {db_name} created with user {user}.')


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


def postgresCreate(db_name, db_user, db_host='localhost', db_port='5432', password=None):
    """
    creates a postgresql database
    """
    idb = input('install a postgresql db (y/n)? ')
    if idb != ('n', 'No', 'no', 'NO'):
        try:
            install_db()
        except Exception as e:
            print(str(e))

    cdb = input('create a postgresql database (y/n)? ')
    if cdb != ('n', 'No', 'no', 'NO'):
        #dbname = input('dbname default(proj-dev-db-local1): ')
        #username = input('user: ')
        #host = input('host default(localhost): ')
        #port = input('port default(5432): ')
        #econding = input('encoding default(utf8): ')
        if db_user.startswith('[') and db_user.endswith(']'):
            db_user = db_user.strip('[]')
            db_user = getenv(db_user)
        try:
            create_db(db_name=db_name, user=db_user)
        except Exception as e:
            print(str(e))