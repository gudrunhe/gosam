#!/bin/sh

cd "${CURRENT_SOURCE_DIR}"
make -f Makefile.source > /dev/null
cp -t "${OUTDIR}" model.f90 version.f90