#!/bin/sh

cd "${CURRENT_SOURCE_DIR}"
[% @if diagsum %]
if [ -e ../diagrams-1.hh ] && head -n 100 ../diagrams-1.hh | grep -q 'Local' ;
	then
		sed -i -e "s/Local diagram/Id diag/g" ../diagrams-1.hh;
fi[%
@end @if %]
if [ -f Makefile.source ];
	then
		make -f Makefile.source > /dev/null;
fi
cp -t "${OUTDIR}" [% @if generate_lo_diagrams %]diagramsl0*.f90 [% @end @if generate_lo_diagrams %] [% @if generate_nlo_virt %]d*h*.f90 abbrev*h*.f90[% @end @if generate_nlo_virt %]