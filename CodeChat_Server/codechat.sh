#!/bin/bash

# Installs CodeChat
# test
# To download this script and automatically run it, run in a terminal (without the # or $ signs):
# $ wget https://raw.githubusercontent.com/bjones1/CodeChat_system/master/CodeChat_Server/codechat.sh && bash codechat.sh

# check for Python 3
if ! hash python3; then
    echo "Python 3 is not installed"
    exit 1
fi

# check python version
if ! python3 -c 'import sys; assert sys.version_info >= (3,7)' 2> /dev/null; then
    echo "Upgrade Python to version 3.7 or above"
    exit 1
fi

# install / upgrade pip
python3 -m pip install --user --upgrade pip

# create virtual environment
python3 -m venv codechat

# install CodeChat
codechat/bin/python3 -m pip install --upgrade CodeChat_Server

# echo server directory to user
echo
echo "CodeChat installation complete!"
echo "Install directory: ${PWD}/codechat/bin"
