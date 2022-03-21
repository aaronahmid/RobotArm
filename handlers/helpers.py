import os
import subprocess

def mkVenvUbuntu(vpath):
    """
    Creates a python virtual environment on ubuntu
    """
    if os.path.isdir(vpath):
        print('virtual env exists, activate it instead')
        return False
    
    try:
        try:
            subprocess.run(['virtualenv', f'{vpath}'])
            os.mkdir('scripts')
            with open('scripts/env', mode='w', encoding='utf8') as file:
                text=f"#!/bin/bash\nsource {vpath}/bin/activate\nalias activate='source {vpath}/bin/activate'"
                file.write(text)
            subprocess.run(['chmod', 'u+x', 'scripts/env'])
            #subprocess.run(['{vpath}/bin/python', '-m', 'pip', 'install -r requirements.txt'])
        except FileExistsError:
            return True
    except Exception as e:
        print(e)
        return False

    return True

def postgresCreate(db_name, db_user):
    """
    creates a postgresql database
    """
    print('creating postgresql database...')
