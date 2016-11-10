/*
 *
 * Defines the complete list of invariants known to GoSam
 * Written by: template.xml
 *
 */

#ifndef invariants_hpp_included
#define invariants_hpp_included

struct invariants_t
{
[% @for mandelstam sym_prefix=es non-zero non-mass%]
    invariant_t [%symbol%];[% @end @for mandelstam non-zero%]

};

#endif
