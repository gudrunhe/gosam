import pySecDec as psd
prefactor=1 # todo

# these lines are replaced by tosecdec.py
dim='%(dim)s-2*eps' 
proplist=[ %(proplist)s ]
powerlist=[ %(powerlist)s ]
name='%(graph)s'
epsord=%(epsord)s

gosamIncoming = [[% @for particles initial %]'k[%index%]'[% @if eval index .lt. num_in %], [% @end @if %][%@end @for %]]
gosamOutgoing = [[% @for particles final %]'k[%index%]'[% @if eval index .lt. num_out %], [% @end @if %][%@end @for %]]
gosamExternal = gosamIncoming+gosamOutgoing
gosamInternal = ['p%%s' %% (i+1) for i in range( [% loop %] )]

scalarProductRules = [ [%@for mandelstam_subs diagonal upper %]
  ('k[% index1 %]*k[% index2 %]', '0[%
    @for mandelstam_subs_rhs %][%
      @select coeff
      @case -1 %] - 1/2 * [%
      @case 1 %] + 1/2 * [%
      @case -2 %] - [%
      @case 2 %] + [%
      @else %][%
         @if eval coeff .gt. 0 %][%
            @if is_first %] [%
            @else %] +[%
            @end @if %] [%coeff%] * [%
         @else %] - [%eval .abs. coeff%]/2 * [%
         @end @if %][%
      @end @select %][%$_%][%
      @if eval exponent .gt. 1 %]^[%exponent%][%
      @end @if %][%
   @end @for %]'),[%
@end @for %]
]
numerator=1 #todo

li = psd.loop_integral.LoopIntegralFromPropagators(proplist,gosamInternal,gosamExternal,replacement_rules=scalarProductRules,
                                                   dimensionality=dim, powerlist=powerlist)

kinematicInvariants=[[% @for mandelstam sym_prefix=es non-zero non-mass %]'[% symbol %]',[% @end @for %]]
masses=[[% @for all_masses %]'[% mass %]',[% @end @for %]]

li_info = psd.loop_integral.loop_package(
name,
li,
epsord,
form_optimization_level=2, form_work_space='[%form.workspace%]M',decomposition_method='iterative',
contour_deformation=True, # TODO - may not need this
force_unsafe_deformation=True, # TODO - investigate if this is necessary
real_parameters=kinematicInvariants+masses
)

# write FORM file containing information about 'eps' orders appearing in the expansion of the prefactor and integral
form_outfilename = name + ".hh"
with open(form_outfilename, 'w') as form_outfile:
   form_outfile.write("Id INT(" + name + ") = INT(" + name + "," + li_info["lowest_prefactor_orders"] + "," + li_info["lowest_orders"] + ");\n" )
