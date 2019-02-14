#procedure lightconedecomp()[%
  @for instructions %]
   [% @select opcode
      @case 1
      %]#call LightConeDecomposition(k[%index1%],l[%index1%],[%
            @select mass2 
            @case 0%]k[%index2%][%
            @else %]l[%index2%][%
            @end @select%],[%mass1%])[%
      @case 2
      %]#call LightConeDecomposition(k[%index1%],l[%index1%],l[%
          index2%],[%mass1%])
   #call LightConeDecomposition(k[%index2%],l[%index2%],l[%
          index1%],[%mass2%])[%
      @end @select%][%
  @end @for %]
#endprocedure
* vim: syntax=form:ts=3:sw=3
