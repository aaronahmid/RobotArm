#!/usr/bin/env bash
# INSTALL_DIR V0.1
# This scripts installs(adds) the robot-arm 
# users PATH scripts dir

PATH_TO_SCRIPT="$(pwd)"

echo "$PATH" > paths.txt

if ! grep $PATH_TO_SCRIPT ./paths.txt
    then
        echo "export PATH="\"\$PATH:$PATH_TO_SCRIPT"\"" >> ~/.bashrc
else
    echo "Already Installed"
fi

rm paths.txt