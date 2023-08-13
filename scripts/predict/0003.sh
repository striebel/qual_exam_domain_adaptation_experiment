#!/usr/bin/env sh

if [ ! -v DATA_DIR ]; then
    echo "ERROR: DATA_DIR not set, exiting"
    exit
fi

export MODEL_ID=0003

MODEL_DIR_NAME=`ls -1 $REPO_DIR/logs/model_${MODEL_ID} | tail -n 1`

mkdir --parents $DATA_DIR/predictions/$MODEL_ID

$REPO_DIR/$VENV_NAME/bin/python \
    $REPO_DIR/parser/machamp-${MACHAMP_VERSION}/predict.py \
        $REPO_DIR/logs/model_${MODEL_ID}/${MODEL_DIR_NAME}/model.tar.gz \
        $DATA_DIR/treebanks/ewt/clean/test_with_genre_column.conllu \
        $DATA_DIR/predictions/$MODEL_ID/test.conllu \
        --device 0

for genre in "answer" "email" "newsgroup" "reviews" "weblog";
do
    $REPO_DIR/$VENV_NAME/bin/python \
        $REPO_DIR/parser/machamp-${MACHAMP_VERSION}/predict.py \
            $REPO_DIR/logs/model_${MODEL_ID}/${MODEL_DIR_NAME}/model.tar.gz \
            $DATA_DIR/treebanks/ewt/clean/test_with_genre_column/${genre}.conllu \
            $DATA_DIR/predictions/$MODEL_ID/${genre}.conllu \
            --device 0
done
