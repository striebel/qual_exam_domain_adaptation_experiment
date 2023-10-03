#!/usr/bin/env bash

if ! [ -v DATA_DIR ]; then
    echo "error: DATA_DIR variable not set, exiting"
    exit 1
fi

# rewrites files in place, removing annotations of ellipsis and word splitting
for treebank in 'ewt' 'gum'
do
    ${REPO_DIR}/${VENV_NAME}/bin/python \
        ${REPO_DIR}/scripts/utils/cleanconl.py \
            ${DATA_DIR}/treebanks/${treebank}/clean/all.conllu
done
