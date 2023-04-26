[%' vim: syntax=golem
	 This template defines the Makefiles that go under
    <process_dir>/helicity*/
'%]# vim: ts=3:sw=3

[% @if internal OLP_MODE %]
include ../../Makefile.conf[%
@else %]
include ../Makefile.conf[%
@end @if %]

[% @if extension shared %]
compile: source libgosam_process[% process_name assuffix=\_ %]_amplitude[%helicity%]_0.so libgosam_process[% process_name assuffix=\_ %]_amplitude[%helicity%]_1.so libgosam_process[% process_name assuffix=\_ %]_amplitude[%helicity%]_2.so
[% @else %]
compile: source amplitude[%helicity%]_0.a amplitude[%helicity%]_1.a amplitude[%helicity%]_2.a
[% @end @if %]

-include Makefile.source

HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)[%
@if diagsum %]
HAVE_ORIG_DIAGRAM_FILE=$(if $(shell test -e ../diagrams-1.hh && head -n 100 ../diagrams-1.hh | grep 'Local'),1,0)[%
@end @if %]

OBJECTS_0= \
	globals.o amplitudeh[%helicity%]_0.o[%
@if extension quadruple %] globals_qp.o amplitudeh[%helicity%]_0_qp.o[%
@end @if %][%
@if helsum %][%
@else %][%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] golem95_0h[%helicity%].o[%
   @end @if %][%
   @if extension samurai %] samuraih[%helicity%].o[%
   @end @if %][%
   @if extension ninja %] ninja_0h[%helicity%].o[%
     @if extension quadruple %] ninja_0h[%helicity%]_qp.o[%
     @end @if %][%
   @end @if %][%
@end @select %][%
@end @if %][%
@if generate_lo_diagrams %] \
	diagramsl0_0.o[%
   @if extension quadruple %] diagramsl0_0_qp.o [%
   @end @if %][%
   @if group %][%
   @else %][%
      @for elements topolopy.keep.tree %] \
	d[%$_%]_0h[%helicity%]l0.o[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %] \
	   diagramsl0_0fr5.o[%
      @if group %][%
		@else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]_0h[%helicity%]l0fr5.o[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].o[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].o[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_0h[%helicity%].o[%
      @end @for %][%
   @end @select %][%
   @if extension quadruple %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%]_qp.o[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%]_qp.o[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_0h[%helicity%]_qp.o[%
      @end @for %][%
   @end @select %][%
   @end @if %][%
	@select r2
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]_0h[%helicity%]l1.o[%
                   @if extension quadruple %] \
	d[%$_%]_0h[%helicity%]l1_qp.o[%
                   @end @if %][%
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]_0h[%helicity%]l1d.o[%
                      @if extension quadruple %] \
	d[%$_%]_0h[%helicity%]l1d_qp.o[%
                      @end @if %][%
		   @end @if %][%
		   @if extension ninja %] \
	d[%$_%]_0h[%helicity%]l131.o \
	d[%$_%]_0h[%helicity%]l132.o \
	d[%$_%]_0h[%helicity%]l121.o[%
                       @if extension quadruple %] \
	d[%$_%]_0h[%helicity%]l131_qp.o \
	d[%$_%]_0h[%helicity%]l132_qp.o \
	d[%$_%]_0h[%helicity%]l121_qp.o[%
                       @end @if %][%
		   @end @if %][%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %][%
@if generate_uv_counterterms %] \
	diagramsct.o[%
	@for elements topolopy.keep.ct %] \
	d[%$_%]_0h[%helicity%]l1c.o[%
	@end @for %][%
@end @if %]
GENERATED_SRC_0=[%
@if generate_lo_diagrams %][%
   @if group %] \
	diagramsl0_0.f90[%
    @if extension quadruple %] \
	diagramsl0_0_qp.f90[%
    @end @if %][%
   @else %][%
      @for elements topolopy.keep.tree %] \
	d[%$_%]_0h[%helicity%]l0.f90[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %][%
      @if group %] \
	   diagramsl0_0fr5.f90[%
      @else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]_0h[%helicity%]l0fr5.f90[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_0h[%helicity%].f90[%
      @end @for %][%
   @end @select %][%
   @if extension quadruple %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%]_qp.f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%]_qp.f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_0h[%helicity%]_qp.f90[%
      @end @for %][%
   @end @select %][%
   @end @if %][%
	@select r2
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]_0h[%helicity%]l1.f90[%
           @if extension quadruple %] \
	d[%$_%]_0h[%helicity%]l1_qp.f90[%
           @end @if %][%
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]_0h[%helicity%]l1d.f90[%
                     @if extension quadruple %] \
	d[%$_%]_0h[%helicity%]l1d_qp.f90[%
                     @end @if %][%
		   @end @if %][%
		   @if extension ninja %] \
	d[%$_%]_0h[%helicity%]l131.f90 \
	d[%$_%]_0h[%helicity%]l132.f90 \
	d[%$_%]_0h[%helicity%]l121.f90[%
                       @if extension quadruple %] \
	d[%$_%]_0h[%helicity%]l131_qp.f90 \
	d[%$_%]_0h[%helicity%]l132_qp.f90 \
	d[%$_%]_0h[%helicity%]l121_qp.f90[%
                       @end @if %][%
		   @end @if %][%
	@end @for %][%
	@end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %][%
@if generate_uv_counterterms %][%
	@for elements topolopy.keep.ct %] \
	d[%$_%]_0h[%helicity%]l1c.f90[%
	@end @for %] \
	diagramsct.f90 [%
@end @if %]


OBJECTS_1= \
	globals.o amplitudeh[%helicity%]_1.o[%
@if extension quadruple %] globals_qp.o amplitudeh[%helicity%]_1_qp.o[%
@end @if %][%
@if helsum %][%
@else %][%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] golem95_1h[%helicity%].o[%
   @end @if %][%
   @if extension samurai %] samuraih[%helicity%].o[%
   @end @if %][%
   @if extension ninja %] ninja_1h[%helicity%].o[%
     @if extension quadruple %] ninja_1h[%helicity%]_qp.o[%
     @end @if %][%
   @end @if %][%
@end @select %][%
@end @if %][%
@if generate_lo_diagrams %] \
	diagramsl0_1.o[%
   @if extension quadruple %] diagramsl0_1_qp.o [%
   @end @if %][%
   @if group %][%
   @else %][%
      @for elements topolopy.keep.tree %] \
	d[%$_%]_1h[%helicity%]l0.o[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %] \
	   diagramsl0_1fr5.o[%
      @if group %][%
		@else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]_1h[%helicity%]l0fr5.o[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].o[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].o[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_1h[%helicity%].o[%
      @end @for %][%
   @end @select %][%
   @if extension quadruple %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%]_qp.o[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%]_qp.o[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_1h[%helicity%]_qp.o[%
      @end @for %][%
   @end @select %][%
   @end @if %][%
	@select r2
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]_1h[%helicity%]l1.o[%
                   @if extension quadruple %] \
	d[%$_%]_1h[%helicity%]l1_qp.o[%
                   @end @if %][%
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]_1h[%helicity%]l1d.o[%
                      @if extension quadruple %] \
	d[%$_%]_1h[%helicity%]l1d_qp.o[%
                      @end @if %][%
		   @end @if %][%
		   @if extension ninja %] \
	d[%$_%]_1h[%helicity%]l131.o \
	d[%$_%]_1h[%helicity%]l132.o \
	d[%$_%]_1h[%helicity%]l121.o[%
                       @if extension quadruple %] \
	d[%$_%]_1h[%helicity%]l131_qp.o \
	d[%$_%]_1h[%helicity%]l132_qp.o \
	d[%$_%]_1h[%helicity%]l121_qp.o[%
                       @end @if %][%
		   @end @if %][%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %][%
@if generate_uv_counterterms %] \
	diagramsct.o[%
	@for elements topolopy.keep.ct %] \
	d[%$_%]_1h[%helicity%]l1c.o[%
	@end @for %][%
@end @if %]
GENERATED_SRC_1=[%
@if generate_lo_diagrams %][%
   @if group %] \
	diagramsl0_1.f90[%
    @if extension quadruple %] \
	diagramsl0_1_qp.f90[%
    @end @if %][%
   @else %][%
      @for elements topolopy.keep.tree %] \
	d[%$_%]_1h[%helicity%]l0.f90[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %][%
      @if group %] \
	   diagramsl0_1fr5.f90[%
      @else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]_1h[%helicity%]l0fr5.f90[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_1h[%helicity%].f90[%
      @end @for %][%
   @end @select %][%
   @if extension quadruple %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%]_qp.f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%]_qp.f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_1h[%helicity%]_qp.f90[%
      @end @for %][%
   @end @select %][%
   @end @if %][%
	@select r2
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]_1h[%helicity%]l1.f90[%
           @if extension quadruple %] \
	d[%$_%]_1h[%helicity%]l1_qp.f90[%
           @end @if %][%
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]_1h[%helicity%]l1d.f90[%
                     @if extension quadruple %] \
	d[%$_%]_1h[%helicity%]l1d_qp.f90[%
                     @end @if %][%
		   @end @if %][%
		   @if extension ninja %] \
	d[%$_%]_1h[%helicity%]l131.f90 \
	d[%$_%]_1h[%helicity%]l132.f90 \
	d[%$_%]_1h[%helicity%]l121.f90[%
                       @if extension quadruple %] \
	d[%$_%]_1h[%helicity%]l131_qp.f90 \
	d[%$_%]_1h[%helicity%]l132_qp.f90 \
	d[%$_%]_1h[%helicity%]l121_qp.f90[%
                       @end @if %][%
		   @end @if %][%
	@end @for %][%
	@end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %][%
@if generate_uv_counterterms %][%
	@for elements topolopy.keep.ct %] \
	d[%$_%]_1h[%helicity%]l1c.f90[%
	@end @for %] \
	diagramsct.f90 [%
@end @if %]


OBJECTS_2= \
	globals.o amplitudeh[%helicity%]_2.o[%
@if extension quadruple %] globals_qp.o amplitudeh[%helicity%]_2_qp.o[%
@end @if %][%
@if helsum %][%
@else %][%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] golem95_2h[%helicity%].o[%
   @end @if %][%
   @if extension samurai %] samuraih[%helicity%].o[%
   @end @if %][%
   @if extension ninja %] ninja_2h[%helicity%].o[%
     @if extension quadruple %] ninja_2h[%helicity%]_qp.o[%
     @end @if %][%
   @end @if %][%
@end @select %][%
@end @if %][%
@if generate_lo_diagrams %] \
	diagramsl0_2.o[%
   @if extension quadruple %] diagramsl0_2_qp.o [%
   @end @if %][%
   @if group %][%
   @else %][%
      @for elements topolopy.keep.tree %] \
	d[%$_%]_2h[%helicity%]l0.o[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %] \
	   diagramsl0_2fr5.o[%
      @if group %][%
		@else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]_2h[%helicity%]l0fr5.o[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].o[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].o[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_2h[%helicity%].o[%
      @end @for %][%
   @end @select %][%
   @if extension quadruple %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%]_qp.o[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%]_qp.o[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_2h[%helicity%]_qp.o[%
      @end @for %][%
   @end @select %][%
   @end @if %][%
	@select r2
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]_2h[%helicity%]l1.o[%
                   @if extension quadruple %] \
	d[%$_%]_2h[%helicity%]l1_qp.o[%
                   @end @if %][%
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]_2h[%helicity%]l1d.o[%
                      @if extension quadruple %] \
	d[%$_%]_2h[%helicity%]l1d_qp.o[%
                      @end @if %][%
		   @end @if %][%
		   @if extension ninja %] \
	d[%$_%]_2h[%helicity%]l131.o \
	d[%$_%]_2h[%helicity%]l132.o \
	d[%$_%]_2h[%helicity%]l121.o[%
                       @if extension quadruple %] \
	d[%$_%]_2h[%helicity%]l131_qp.o \
	d[%$_%]_2h[%helicity%]l132_qp.o \
	d[%$_%]_2h[%helicity%]l121_qp.o[%
                       @end @if %][%
		   @end @if %][%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %][%
@if generate_uv_counterterms %] \
	diagramsct.o[%
	@for elements topolopy.keep.ct %] \
	d[%$_%]_2h[%helicity%]l1c.o[%
	@end @for %][%
@end @if %]
GENERATED_SRC_2=[%
@if generate_lo_diagrams %][%
   @if group %] \
	diagramsl0_2.f90[%
    @if extension quadruple %] \
	diagramsl0_2_qp.f90[%
    @end @if %][%
   @else %][%
      @for elements topolopy.keep.tree %] \
	d[%$_%]_2h[%helicity%]l0.f90[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %][%
      @if group %] \
	   diagramsl0_2fr5.f90[%
      @else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]_2h[%helicity%]l0fr5.f90[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_2h[%helicity%].f90[%
      @end @for %][%
   @end @select %][%
   @if extension quadruple %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%]_qp.f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%]_qp.f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]_2h[%helicity%]_qp.f90[%
      @end @for %][%
   @end @select %][%
   @end @if %][%
	@select r2
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]_2h[%helicity%]l1.f90[%
           @if extension quadruple %] \
	d[%$_%]_2h[%helicity%]l1_qp.f90[%
           @end @if %][%
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]_2h[%helicity%]l1d.f90[%
                     @if extension quadruple %] \
	d[%$_%]_2h[%helicity%]l1d_qp.f90[%
                     @end @if %][%
		   @end @if %][%
		   @if extension ninja %] \
	d[%$_%]_2h[%helicity%]l131.f90 \
	d[%$_%]_2h[%helicity%]l132.f90 \
	d[%$_%]_2h[%helicity%]l121.f90[%
                       @if extension quadruple %] \
	d[%$_%]_2h[%helicity%]l131_qp.f90 \
	d[%$_%]_2h[%helicity%]l132_qp.f90 \
	d[%$_%]_2h[%helicity%]l121_qp.f90[%
                       @end @if %][%
		   @end @if %][%
	@end @for %][%
	@end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %][%
@if generate_uv_counterterms %][%
	@for elements topolopy.keep.ct %] \
	d[%$_%]_2h[%helicity%]l1c.f90[%
	@end @for %] \
	diagramsct.f90 [%
@end @if %]

.PHONY: compile source clean very-clean doc [% @if diagsum %]convert[%@end @if%]
.SUFFIXES:

TEMPFILE:=$(shell mktemp -u -t gosam.tempfile.XXXXXX || echo gosam.tempfile.tmp)

[% @if diagsum 
%]convert:
ifeq ($(HAVE_ORIG_DIAGRAM_FILE),1)
	$(shell sed -e "s/Local diagram/Id diag/g" ../diagrams-1.hh > $(TEMPFILE))
	$(shell mv $(TEMPFILE) ../diagrams-1.hh)
endif[%
@end @if %]

ifeq ($(HAVE_MAKEFILE_SOURCE),1)
source:[% @if diagsum %] convert [% @end @if 
	%] $(SOURCE_TREE) $(SOURCE_VIRT)
else
source:
endif


[% @for elements topolopy.keep.virt %]

d[%$_%]_0h[%helicity%]l1: d[%$_%]_0h[%helicity%]l1.f90 abbrevd[%$_%]_0h[%helicity%].f90 globals.o[%
@if extension quadruple %] d[%$_%]_0h[%helicity%]l1_qp.f90 abbrevd[%$_%]_0h[%helicity%]_qp.f90 globals_qp.o[%
@end @if %][%
@if diagsum %]
ifeq ($(HAVE_ORIG_DIAGRAM_FILE),1)
	$(shell sed -e "s/Local diagram/Id diag/g" ../diagrams-1.hh > $(TEMPFILE))
	$(shell mv $(TEMPFILE) ../diagrams-1.hh)
endif[%
@end @if %]
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source d[%$_%]_0h[%helicity%]l1.txt
	$(MAKE) $(S) -f Makefile.source d[%$_%]_0h[%helicity%]l1.f90
	$(MAKE) $(S) -f Makefile.source abbrevd[%$_%]_0h[%helicity%].f90[%
	@if extension quadruple %]
	$(MAKE) $(S) -f Makefile.source d[%$_%]_0h[%helicity%]l1_qp.f90
	$(MAKE) $(S) -f Makefile.source abbrevd[%$_%]_0h[%helicity%]_qp.f90[%
	@end @if %]
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o abbrevd[%$_%]_0h[%helicity%].o -I../common abbrevd[%$_%]_0h[%helicity%].f90
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o d[%$_%]_0h[%helicity%]l1.o -I../common d[%$_%]_0h[%helicity%]l1.f90[%
	@if extension quadruple %]
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o abbrevd[%$_%]_0h[%helicity%]_qp.o -I../common abbrevd[%$_%]_0h[%helicity%]_qp.f90
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o d[%$_%]_0h[%helicity%]l1_qp.o -I../common d[%$_%]_0h[%helicity%]l1_qp.f90[%
	@end @if %]
endif

d[%$_%]_1h[%helicity%]l1: d[%$_%]_1h[%helicity%]l1.f90 abbrevd[%$_%]_1h[%helicity%].f90 globals.o[%
@if extension quadruple %] d[%$_%]_1h[%helicity%]l1_qp.f90 abbrevd[%$_%]_1h[%helicity%]_qp.f90 globals_qp.o[%
@end @if %][%
@if diagsum %]
ifeq ($(HAVE_ORIG_DIAGRAM_FILE),1)
	$(shell sed -e "s/Local diagram/Id diag/g" ../diagrams-1.hh > $(TEMPFILE))
	$(shell mv $(TEMPFILE) ../diagrams-1.hh)
endif[%
@end @if %]
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source d[%$_%]_1h[%helicity%]l1.txt
	$(MAKE) $(S) -f Makefile.source d[%$_%]_1h[%helicity%]l1.f90
	$(MAKE) $(S) -f Makefile.source abbrevd[%$_%]_1h[%helicity%].f90[%
	@if extension quadruple %]
	$(MAKE) $(S) -f Makefile.source d[%$_%]_1h[%helicity%]l1_qp.f90
	$(MAKE) $(S) -f Makefile.source abbrevd[%$_%]_1h[%helicity%]_qp.f90[%
	@end @if %]
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o abbrevd[%$_%]_1h[%helicity%].o -I../common abbrevd[%$_%]_1h[%helicity%].f90
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o d[%$_%]_1h[%helicity%]l1.o -I../common d[%$_%]_1h[%helicity%]l1.f90[%
	@if extension quadruple %]
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o abbrevd[%$_%]_1h[%helicity%]_qp.o -I../common abbrevd[%$_%]_1h[%helicity%]_qp.f90
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o d[%$_%]_1h[%helicity%]l1_qp.o -I../common d[%$_%]_1h[%helicity%]l1_qp.f90[%
	@end @if %]
endif

d[%$_%]_2h[%helicity%]l1: d[%$_%]_2h[%helicity%]l1.f90 abbrevd[%$_%]_2h[%helicity%].f90 globals.o[%
@if extension quadruple %] d[%$_%]_2h[%helicity%]l1_qp.f90 abbrevd[%$_%]_2h[%helicity%]_qp.f90 globals_qp.o[%
@end @if %][%
@if diagsum %]
ifeq ($(HAVE_ORIG_DIAGRAM_FILE),1)
	$(shell sed -e "s/Local diagram/Id diag/g" ../diagrams-1.hh > $(TEMPFILE))
	$(shell mv $(TEMPFILE) ../diagrams-1.hh)
endif[%
@end @if %]
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source d[%$_%]_2h[%helicity%]l1.txt
	$(MAKE) $(S) -f Makefile.source d[%$_%]_2h[%helicity%]l1.f90
	$(MAKE) $(S) -f Makefile.source abbrevd[%$_%]_2h[%helicity%].f90[%
	@if extension quadruple %]
	$(MAKE) $(S) -f Makefile.source d[%$_%]_2h[%helicity%]l1_qp.f90
	$(MAKE) $(S) -f Makefile.source abbrevd[%$_%]_2h[%helicity%]_qp.f90[%
	@end @if %]
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o abbrevd[%$_%]_2h[%helicity%].o -I../common abbrevd[%$_%]_2h[%helicity%].f90
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o d[%$_%]_2h[%helicity%]l1.o -I../common d[%$_%]_2h[%helicity%]l1.f90[%
	@if extension quadruple %]
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o abbrevd[%$_%]_2h[%helicity%]_qp.o -I../common abbrevd[%$_%]_2h[%helicity%]_qp.f90
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o d[%$_%]_2h[%helicity%]l1_qp.o -I../common d[%$_%]_2h[%helicity%]l1_qp.f90[%
	@end @if %]
endif

[% @end @for %]

$(OBJECTS_0): %.o: %.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o $@ -I../common $<

$(OBJECTS_1): %.o: %.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o $@ -I../common $<

$(OBJECTS_2): %.o: %.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o $@ -I../common $<


[% @if extension shared %]
libgosam_process[% process_name assuffix=\_ %]_amplitude[%helicity%]_0.so: $(OBJECTS)
	$(vecho) "-> Linking $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) $(LDFLAGS) -shared -Wl,-rpath="\$ORIGIN/../common" -o $@ $+
libgosam_process[% process_name assuffix=\_ %]_amplitude[%helicity%]_1.so: $(OBJECTS)
	$(vecho) "-> Linking $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) $(LDFLAGS) -shared -Wl,-rpath="\$ORIGIN/../common" -o $@ $+
libgosam_process[% process_name assuffix=\_ %]_amplitude[%helicity%]_2.so: $(OBJECTS)
	$(vecho) "-> Linking $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) $(LDFLAGS) -shared -Wl,-rpath="\$ORIGIN/../common" -o $@ $+
[% @else %]
amplitude[%helicity%]_0.a: $(OBJECTS_0)
	$(Q) ar rs $@ $+
amplitude[%helicity%]_1.a: $(OBJECTS_1)
	$(Q) ar rs $@ $+
amplitude[%helicity%]_2.a: $(OBJECTS_2)
	$(Q) ar rs $@ $+
[% @end @if %]

doc:

clean:
	$(Q)$(FIND) $(FIND_OPT) . \( -name '*.o' \
		-or -name '*.mod' -or -name '*.a' -or -name '*.so' \) \
		-exec rm \{} \;

very-clean: clean
	$(Q)rm -f filelist-source
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(Q)$(FIND) $(FIND_OPT) . \( \
		-name 'd*h[%helicity%]l[01].f90'[%
@if extension quadruple %] \
		-or -name 'd*h[%helicity%]l[01]_qp.f90'[%
@end @if %] \
		-or -name 'd*h[%helicity%]l[01]fr5.f90' \
		-or -name 'd*h[%helicity%]l[014]*.txt' \
		-or -name 'd*h[%helicity%]l1[123dmu]*.txt' \
		-or -name 'd*h[%helicity%]l1[123dmu]*.f90' \
		-or -name 'd*h[%helicity%]l[01]c.txt' \
		-or -name 'd*h[%helicity%]l[01]c.f90' \
		-or -name 'd*h[%helicity%]l[01]d.txt' \
		-or -name 'd*h[%helicity%]l[01]d.hh' \
		-or -name 'd*h[%helicity%]l[01].hh' \
		-or -name 'd*h[%helicity%]l1d.txt' \
		-or -name 'd*h[%helicity%]l1d.f90' \
		-or -name 'd*h[%helicity%]l[01]-fr.txt' \
		-or -name 'd*h[%helicity%]l[01].dat' \
		-or -name 'd*h[%helicity%]l[01].abb'[%
@if group %] \
		-or -name 'diagramsl0_0.f90'[%
@if extension quadruple %] \
		-or -name 'diagramsl0_0_qp.f90'[%
@end @if %][%
@end @if %][%
@if extension formopt %] \
		-or -name 'abbrevd*h[%helicity%].f90'[%
@if extension quadruple %] \
		-or -name 'abbrevd*h[%helicity%]_qp.f90'[%
@end @if %] \
		-or -name 'd*h[%helicity%]l[01].prc' \
		-or -name 'borndiag*.prc' \
		-or -name 'born*.txt' \
		-or -name 'born*.dat' \
		-or -name '*-stamp' [%
@end @if %] \
		-or -name 'lightconedecomp.prc' \
		\) -exec rm \{} \;
endif

filelist-source: source
	$(Q)$(FIND) $(FIND_OPT) . \( \
		-name '*.f90' \
		-or -name 'Makefile' \
		-or -name 'Makefile.dep' \
		\) -print > $@

include Makefile.dep
