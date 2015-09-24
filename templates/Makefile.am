[% ' vim: syntax=golem:ts=3:sw=3
 %]# vim: ts=3:sw=3
SUBDIRS=doc common[%
@for helicities generated %] \
	helicity[% helicity %][%
@end @for helicities %][%
@if helsum%] \
	sum[%
@end @if%] \
	matrix

[% 
@select olp.mc.name default=standalone
@case standalone %]lib[%
@else            %]noinst[%
@end @select %]_LTLIBRARIES=libgolem_process[% process_name assuffix=\_ %].la
libgolem_process[% process_name assuffix=\_ %]_la_SOURCES=
libgolem_process[% process_name assuffix=\_ %]_la_LIBADD= \
		$(builddir)/common/libgolem_process[%
				process_name assuffix=\_ %]_common.la[%
@for helicities generated %] \
		$(builddir)/helicity[% helicity
			%]/libgolem_process[%
				process_name assuffix=\_ %]_helicity[% helicity %].la[%
@end @for helicities %][%
@if helsum %] \
		$(builddir)/sum/libgolem_process[%
				process_name assuffix=\_ %]_sum.la[%
@end @if %] \
		$(builddir)/matrix/libgolem_process[% 
				process_name assuffix=\_ %]_matrix.la[%
@select olp.process_name default=UNDEFINED
@case UNDEFINED %]
EXTRA_DIST=m4 \
			  autogen.sh[%
@end @select %]
ACLOCAL_AMFLAGS=-I m4
