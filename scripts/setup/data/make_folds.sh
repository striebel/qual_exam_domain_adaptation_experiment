#!/usr/bin/env sh

if ! [ -v DATA_DIR ]; then
    echo "variable DATA_DIR not set, exiting"
    exit
fi

if ! [ -v REPO_DIR ]; then
    echo 'REPO_DIR not set, exiting'
    exit
fi

$REPO_DIR/$VENV_NAME/bin/python \
    $REPO_DIR/scripts/setup/data/make_folds.py \
        $DATA_DIR/treebanks \
        $REPO_DIR
