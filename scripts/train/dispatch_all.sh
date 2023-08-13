#!/usr/bin/env sh

if [ ! -v REPO_DIR ]; then
    echo "ERROR: REPO_DIR not set, exiting"
    exit
fi

for domain in "answer" "email" "newsgroup" "reviews" "weblog" 'GUM_conversation' 'GUM_fiction' 'GUM_interview' 'GUM_vlog' 'GUM_whow'
do
    ${REPO_DIR}/scripts/train/${domain}_dispatch.sh 
done
