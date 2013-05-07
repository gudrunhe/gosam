[% ' # vim: ts=3:sw=3:syntax=golem
%]#procedure spva
* vim[% ' %]: syntax=form

[% @if extension formopt %][%
@for pairs distinct %]
   Id Spab3([%
            @if is_lightlike1%]k[%index1%][% @else %]l[%index1%][%
            @end @if %], Q, [%
            @if is_lightlike2%]k[%index2%][% @else %]l[%index2%][%
            @end @if %]) = Qspva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %];[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Spab3([%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %], Q, e[%
         index2 %]) = Qspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %];
   Id Spab3(e[% index2 %], Q, [% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][%
          index1 %]) = Qspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %];[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Spab3(e[%index1%], Q, e[%index2%]) = Qspvae[%index1%]e[%index2%];
   Id Spab3(e[%index2%], Q, e[%index1%]) = Qspvae[%index2%]e[%index1%];[%
      @end @if %][%
   @end @for %][%
@end @if %][%
@end @if %]


[% @for pairs distinct %]
   Id Spab3([%
            @if is_lightlike1%]k[%index1%][% @else %]l[%index1%][%
            @end @if %], Q?, [%
            @if is_lightlike2%]k[%index2%][% @else %]l[%index2%][%
            @end @if %]) = spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %].Q;[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Spab3([%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %], Q?, e[%
         index2 %]) = spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %].Q;
   Id Spab3(e[% index2 %], Q?, [% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][%
          index1 %]) = spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %].Q;[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   Id Spab3(e[%index1%], Q?, e[%index2%]) = spvae[%index1%]e[%index2%].Q;
   Id Spab3(e[%index2%], Q?, e[%index1%]) = spvae[%index2%]e[%index1%].Q;[%
      @end @if %][%
   @end @for %][%
@end @if %]

#EndProcedure
