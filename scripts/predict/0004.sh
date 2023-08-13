#!/usr/bin/env sh

if [ ! -v DATA_DIR ]; then
    echo "ERROR: DATA_DIR not set, exiting"
    exit
fi

for genre in "answer" "email" "newsgroup" "reviews" "weblog";
do
    mkdir --parents $DATA_DIR/predictions/0004/${genre}
    
    for proportion in "00" "02" "04" "06" "08" "10";
    do
        export MODEL_NAME=model_0004_${genre}_${proportion}
        
        MODEL_DIR_NAME=`ls -1 ${REPO_DIR}/logs/${MODEL_NAME} | tail -n 1`
        
        $REPO_DIR/$VENV_NAME/bin/python \
            $REPO_DIR/parser/machamp-${MACHAMP_VERSION}/predict.py \
                $REPO_DIR/logs/${MODEL_NAME}/${MODEL_DIR_NAME}/model.tar.gz \
                $DATA_DIR/treebanks/ewt/clean/test/${genre}.conllu \
                $DATA_DIR/predictions/0004/${genre}/${proportion}.conllu \
                --device 0
    done
done
