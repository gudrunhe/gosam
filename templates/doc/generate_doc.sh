#!/bin/sh

cd "${CURRENT_SOURCE_DIR}"
make process.pdf &> /dev/null;
cp process.pdf ${OUTDIR}/[% process_name %].pdf