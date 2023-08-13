#!/usr/bin/env sh

if [ ! -v MACHAMP_VERSION ]; then
    echo "ERROR: MACHAMP_VERSION not set, exiting"
    exit
fi

if [ ! -v REPO_DIR ]; then
    echo "ERROR: REPO_DIR not set, exiting"
    exit
fi

rm -rf $REPO_DIR/parser
mkdir  $REPO_DIR/parser

wget \
    --output-document $REPO_DIR/parser/v${MACHAMP_VERSION}.tar.gz \
    https://github.com/machamp-nlp/machamp/archive/refs/tags/v${MACHAMP_VERSION}.tar.gz

(cd $REPO_DIR/parser && tar xzf v${MACHAMP_VERSION}.tar.gz && rm v${MACHAMP_VERSION}.tar.gz)

