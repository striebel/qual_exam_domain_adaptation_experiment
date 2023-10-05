#!/usr/bin/env sh

if [ ! -v REPO_DIR ]
then
    echo 'error: REPO_DIR variable not set, exiting'
    exit 1
fi

if [ ! -v VENV_NAME ]
then
    echo 'error: VENV_NAME variable not set, exiting'
    exit 2
fi

$REPO_DIR/$VENV_NAME/bin/python \
    $REPO_DIR/scripts/eval/eval_c.py

RETCODE=$?
if [ 0 -ne $RETCODE ]
then
    echo 'error: eval part c failed'
    exit 3
fi

