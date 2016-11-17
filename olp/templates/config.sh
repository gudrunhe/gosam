#!/bin/sh

if command -v realpath >/dev/null 2>&1 ; then
   PWD="$(dirname $(realpath "$0"))"
else
   PWD="$(dirname "$0")"
fi

USE_INTERNAL=

CFLAGS="-I${PWD}"
FCFLAGS="${CFLAGS}[%
@for subprocesses %] \
 `sh ${PWD}/[%path%]/config.sh -[%
   @if is_first %][% @else %]p[% @end @if %]cflags`[%
@end @for %]"
LDFLAGS="${PWD}/olp_module.o[%
@for subprocesses %] \
 `sh ${PWD}/[%path%]/config.sh -[%
   @if is_first %][% @else %]p[% @end @if %]libs`[%
@end @for %]"[%
@for subprocesses %][%
   @if is_first %]

[% @if extension shared %]
LDFLAGS_ALL="-Wl,-rpath=${PWD} -L${PWD} -lgosam_process"
[% @end @if %]

FC=`sh ${PWD}/[% path %]/config.sh -fortcom`
OLIBS=`sh ${PWD}/[% path %]/config.sh -olibs`
OCFLAGS=`sh ${PWD}/[% path %]/config.sh -ocflags`[%
   @end @if %][%
@end @for %]

while [ $# -gt 0 ]; do
   case "$1" in
      -libs)
[% @if extension shared %]
        if [ -n "$USE_INTERNAL" ] ; then
              printf " $LDFLAGS"
        else
              printf " $LDFLAGS_ALL"
        fi
[% @else %]
              printf " $LDFLAGS"
[% @end @if %]
   ;;
      -olibs)
              printf " $OLIBS"
   ;;
      -cflags)
              printf " $CFLAGS"
   ;;
      -ocflags)
              printf " $OCFLAGS"
   ;;
      -fcflags)
              printf " $FCFLAGS"
   ;;
      -fortcom)
              printf " $FC"
   ;;
      -help|--help)
              echo
              echo This script helps constructing the command line
              echo for linking the matrix element with an existing
              echo program.
              echo Examples:
              echo "   ``./config.sh -fortcom -c -o test.o test.f90 -cflags``"
              echo "   ``./config.sh -fortcom -o test.exe *.o -libs``"
              echo
              echo Options:
              echo "   -libs    prints the flags needed to link this code"
              echo "            including the libraries it depends on"
              echo "   -fcflags prints the flags needed to compile this code"
              echo "            with fortran"
              echo "   -cflags  prints the flags needed to compile this code"
              echo "            with C/C++"
              echo "   -fortcom the name of the fortran compiler in use"[%
@if extension shared %]
              echo "   -intern  return flags for linking with all sub-libraries instead of the"
              echo "            libgosam_process.so, need to be the first paramter."[%
@end @if %]
              echo "   -help    prints this screen"
   ;;[%
@if extension shared %]
      -intern)
              USE_INTERNAL=1
   ;;
[% @end @if %]
      *)
              printf " $1"
   ;;
   esac
   shift
done
echo

