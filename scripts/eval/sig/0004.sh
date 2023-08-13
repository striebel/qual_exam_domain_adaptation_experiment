#!/usr/bin/env sh

if [ ! -v REPO_DIR ]; then
    echo "ERROR: REPO_DIR not set, exiting"
    exit
fi

$REPO_DIR/$VENV_NAME/bin/python \
    $REPO_DIR/scripts/eval/sig/0004.py \
        $REPO_DIR

