#!/usr/bin/env sh

if ! [ -v DATA_DIR ]; then
    echo "variable DATA_DIR not set, exiting"
    exit
fi

for treebank in 'gum' 'ewt'
do
    $REPO_DIR/$VENV_NAME/bin/python \
        $REPO_DIR/scripts/setup/data/stats.py \
            $DATA_DIR/treebanks \
            $treebank
    if [ $? -ne 0 ]; then
        exit
    fi
done
