%=$
/*
 *
 * Defines the complete list of parameters known to GoSam
 * Written by: template.xml
 *
 */

#ifndef parameters_hpp_included
#define parameters_hpp_included

struct parameters_t
{
    // Input Parameters
    [$ @for parameters $]
    [$ @select type
    @case R $]real_parameter_t [$ $_ $] = [$real convert=float format=%24.15f $];[$
    @case C $]complex_parameter_t [$ $_ $] = {[$ real convert=float format=%24.15f $], [$ imag convert=float format=%24.15f $]};[$
    @case RP $]const real_parameter_t [$ $_ $] = [$real convert=float format=%24.15f $];[$
    @case CP $]const complex_parameter_t [$ $_ $] = {[$ real convert=float format=%24.15f $], [$ imag convert=float format=%24.15f $]};
    [$ @end @select type $][$ @end @for parameters $]

    // Parameters derived from input parameters
    [$ @for functions_resolved $]
    [$ @select type
    @case R $]real_parameter_t [$ $_ $] = [$ expression $];[$
    @case C $]complex_parameter_t [$ $_ $] = [$ expression $];
    [$ @end @select type $][$ @end @for functions_resolved $]

};

#endif
