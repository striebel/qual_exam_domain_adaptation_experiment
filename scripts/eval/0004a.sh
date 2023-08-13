#!/usr/bin/env sh

if [ ! -v REPO_DIR ]; then
    echo "ERROR: REPO_DIR not set, exiting"
    exit
fi

printf "\n`date`\n\n\n"                                                     >  ${REPO_DIR}/results/0004.txt

for genre in "answer" "email" "newsgroup" "reviews" "weblog";
do
    printf "0002 ${genre}\n"                                               >> ${REPO_DIR}/results/0004.txt
    printf "======================\n\n"                                    >> ${REPO_DIR}/results/0004.txt
    $REPO_DIR/$VENV_NAME/bin/python \
        ${REPO_DIR}/scripts/ud_tools/eval.py \
            ${DATA_DIR}/treebanks/ewt/clean/test/${genre}.conllu \
            ${DATA_DIR}/predictions/0002/${genre}.conllu                   >> ${REPO_DIR}/results/0004.txt
    printf "\n"                                                            >> ${REPO_DIR}/results/0004.txt
    printf "0003 ${genre}\n"                                               >> ${REPO_DIR}/results/0004.txt
    printf "======================\n\n"                                    >> ${REPO_DIR}/results/0004.txt
    $REPO_DIR/$VENV_NAME/bin/python \
        ${REPO_DIR}/scripts/ud_tools/eval.py \
            ${DATA_DIR}/treebanks/ewt/clean/test_with_genre_column/${genre}.conllu \
            ${DATA_DIR}/predictions/0003/${genre}.conllu                   >> ${REPO_DIR}/results/0004.txt
    printf "\n"                                                            >> ${REPO_DIR}/results/0004.txt
    for proportion in "00" "02" "04" "06" "08" "10";
    do
        printf "0004 ${genre} ${proportion}\n"                             >> ${REPO_DIR}/results/0004.txt
        printf "======================\n\n"                                >> ${REPO_DIR}/results/0004.txt
        $REPO_DIR/$VENV_NAME/bin/python \
            ${REPO_DIR}/scripts/ud_tools/eval.py \
                ${DATA_DIR}/treebanks/ewt/clean/test/${genre}.conllu \
                ${DATA_DIR}/predictions/0004/${genre}/${proportion}.conllu >> ${REPO_DIR}/results/0004.txt
        printf "\n"                                                        >> ${REPO_DIR}/results/0004.txt
    done
done
