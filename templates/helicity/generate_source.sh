#!/bin/sh

cd "${CURRENT_SOURCE_DIR}"
make -f Makefile.source all_source
cp -t "${OUTDIR}" diagramsl0.f90