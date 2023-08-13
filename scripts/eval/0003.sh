#!/usr/bin/env sh

MODEL_ID=0003

if [ ! -v DATA_DIR ]; then
    echo "ERROR: DATA_DIR not set, exiting"
    exit
fi

printf "\n`date`\n\n\n"                                  >  ${REPO_DIR}/results/${MODEL_ID}.txt
printf "Eval results calculated by machamp\n"            >> ${REPO_DIR}/results/${MODEL_ID}.txt
printf "==================================\n\n"          >> ${REPO_DIR}/results/${MODEL_ID}.txt
cat ${DATA_DIR}/predictions/${MODEL_ID}/test.conllu.eval >> ${REPO_DIR}/results/${MODEL_ID}.txt
printf "\n\n\n"                                          >> ${REPO_DIR}/results/${MODEL_ID}.txt
printf "UD eval script output\n"                         >> ${REPO_DIR}/results/${MODEL_ID}.txt
printf "=====================\n\n"                       >> ${REPO_DIR}/results/${MODEL_ID}.txt
python ${REPO_DIR}/scripts/ud_tools/eval.py -v \
    ${DATA_DIR}/treebanks/ewt/clean/test_with_genre_column.conllu \
    ${DATA_DIR}/predictions/${MODEL_ID}/test.conllu      >> ${REPO_DIR}/results/${MODEL_ID}.txt
printf "\n"                                              >> ${REPO_DIR}/results/${MODEL_ID}.txt
