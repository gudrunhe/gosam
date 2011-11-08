#!/bin/sh

PWD=`dirname $0`

FCFLAGS="[%
@for subprocesses %] \
	`sh ${PWD}/[%path%]/config.sh -[%
   @if is_first %][% @else %]p[% @end @if %]cflags`[%
@end @for %]"
CFLAGS="-I${PWD}"
LDFLAGS="${PWD}/olp_module.o[%
@for subprocesses %] \
	`sh ${PWD}/[%path%]/config.sh -[%
   @if is_first %][% @else %]p[% @end @if %]libs`[%
@end @for %]"[%
@for subprocesses %][%
   @if is_first %]

FC=`sh ${PWD}/[% path %]/config.sh -fortcom`
OLIBS=`sh ${PWD}/[% path %]/config.sh -olibs`
OCFLAGS=`sh ${PWD}/[% path %]/config.sh -ocflags`[%
   @end @if %][%
@end @for %]

while [ $# -gt 0 ]; do
   case "$1" in
      -libs)
              echo -n " $LDFLAGS"
   ;;
      -olibs)
              echo -n " $OLIBS"
   ;;
      -cflags)
              echo -n " $CFLAGS"
   ;;
      -ocflags)
              echo -n " $OCFLAGS"
   ;;
      -fcflags)
              echo -n " $FCFLAGS"
   ;;
      -fortcom)
              echo -n " $FC"
   ;;
      -help)
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
              echo "   -fortcom the name of the fortran compiler in use"
              echo "   -help    prints this screen"
   ;;
      *)
              echo -n " $1"
   ;;
   esac
   shift
done
echo

