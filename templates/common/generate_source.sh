#!/bin/sh

cd "${CURRENT_SOURCE_DIR}"[%
@if internal OLP_MODE %]
make -f Makefile.source color.f90 kinematics.f90 > /dev/null
cp -t "${OUTDIR}" color.f90 kinematics.f90[% @if extension quadruple %]
make -f Makefile.source color_qp.f90 kinematics_qp.f90> /dev/null
cp -t "${OUTDIR}" color_qp.f90 kinematics_qp.f90[% @end @if %][%
@else %]
make -f Makefile.source > /dev/null
cp -t "${OUTDIR}" color.f90 version.f90 model.f90 kinematics.f90[% @if extension quadruple %] color_qp.f90 model_qp.f90 kinematics_qp.f90[%
@end @if %][%
@end @if %]