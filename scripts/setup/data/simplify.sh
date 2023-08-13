#!/usr/bin/env sh

if ! [ -v DATA_DIR ]; then
    echo "ERROR: DATA_DIR not set, exiting"
    exit
fi

# rewrites files in place, removing annotations of ellipsis and word splitting
for treebank in 'ewt' 'gum'
do
    $REPO_DIR/$VENV_NAME/bin/python scripts/misc/cleanconl.py \
        "${DATA_DIR}/treebanks/${treebank}/clean/all.conllu"
done
