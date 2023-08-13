#!/usr/bin/env sh

if [ ! -v MACHAMP_VERSION ]; then
    echo "ERROR: MACHAMP_VERSION not set, exiting"
    exit
fi

if [ ! -v REPO_DIR ]; then
    echo "ERROR: REPO_DIR not set, exiting"
    exit
fi

if [ ! -v VENV_NAME ]; then
    echo "ERROR: VENV_NAME not set, exiting"
    exit
fi

# notebook is a requirement of checklist
# which is a requirement of AllenNLP
# which is a requirement of pre-v0.4.0 Machamp;
# however, the current version of notebook that
# is automatically (indirectly) installed by the Machamp
# requirements file is not compatible with the version
# of checklist that is likewise installed;
# so we begin by installing a compatible version
#python -m pip install "notebook==6.5.1"

$REPO_DIR/$VENV_NAME/bin/python -m pip install \
    "allennlp==1.3" \
    "transformers==4.0.0" \
    "torch==1.7.1" \
    "networkx" \
    "statsmodels"
