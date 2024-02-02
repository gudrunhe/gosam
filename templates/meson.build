[% process_name %]_source = files([])
subdir('common')
subdir('doc')
[%
@for helicities generated %] 
subdir('helicity[% helicity %]')[%
@end @for helicities %]
subdir('matrix')
OLP_source += [% process_name %]_source