#!/bin/sh

cd "${CURRENT_SOURCE_DIR}"
make -f Makefile.source source
cp -t "${OUTDIR}" model.f90 color.f90 version.f90