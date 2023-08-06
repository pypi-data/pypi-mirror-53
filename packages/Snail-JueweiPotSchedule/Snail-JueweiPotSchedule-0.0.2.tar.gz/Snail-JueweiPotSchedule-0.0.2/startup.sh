#!/bin/bash

export APP_HOME=$(cd `dirname $0`;pwd)
export PYTHONPATH=$APP_HOME:$PYTHONPATH

python3 $APP_HOME/snailwebs/main.py
