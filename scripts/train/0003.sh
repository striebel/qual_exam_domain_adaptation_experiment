#!/usr/bin/env sh

MODEL_ID=0003

if [ ! -v REPO_DIR ]; then
    echo "ERROR: REPO_DIR not set, exiting"
    exit
fi

if [ ! -v MACHAMP_VERSION ]; then
    echo "ERROR: MACHAMP_VERSION not set, exiting"
    exit
fi

$REPO_DIR/$VENV_NAME/bin/python $REPO_DIR/scripts/misc/translate_jsonnet_to_json.py \
    $REPO_DIR/configs/$MODEL_ID/data.jsonnet \
    $REPO_DIR/configs/$MODEL_ID/data.json

$REPO_DIR/$VENV_NAME/bin/python $REPO_DIR/scripts/misc/translate_jsonnet_to_json.py \
    $REPO_DIR/configs/$MODEL_ID/params.jsonnet \
    $REPO_DIR/configs/$MODEL_ID/params.json

$REPO_DIR/$VENV_NAME/bin/python $REPO_DIR/parser/machamp-$MACHAMP_VERSION/train.py \
    --name "model_${MODEL_ID}" \
    --dataset_config    $REPO_DIR/configs/$MODEL_ID/data.json \
    --parameters_config $REPO_DIR/configs/$MODEL_ID/params.json \
    --device 0
