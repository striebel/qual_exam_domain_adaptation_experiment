#!/usr/bin/env sh

if [ ! -v REPO_DIR ]; then
    echo "ERROR: REPO_DIR not set, exiting"
    exit
fi

for genre in "answer" "email" "newsgroup" "reviews" "weblog";
do
    for proportion in "00" "02" "04" "06" "08" "10";
    do
        sbatch ${REPO_DIR}/scripts/train/0004/${genre}/${proportion}.sbatch
    done
done
