#!/bin/sh

cd "${CURRENT_SOURCE_DIR}"[%
@if internal OLP_MODE %]
make -f Makefile.source color.f90 > /dev/null
cp -t "${OUTDIR}" color.f90[%
@else %]
make -f Makefile.source > /dev/null
cp -t "${OUTDIR}" color.f90 version.f90 model.f90[%
@end @if %]