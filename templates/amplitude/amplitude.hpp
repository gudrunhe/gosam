/*
 *
 * Defines the complete list of integral coefficients known to GoSam
 * Written by: template.xml, tosecdec.py
 *
 */

#ifndef amplitudel[%loop%]_hpp_included
#define amplitudel[%loop%]_hpp_included

#include "typedef.hpp"

%(coefficient_includes)s

amplitude_t amplitude_l[%loop%]_terms
{
    %(amplitude_terms)s
};

#endif
