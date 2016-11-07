/*
 *
 * Defines the complete list of integral coefficients known to GoSam
 * Written by: template.xml, tosecdec.py
 *
 */

#ifndef amplitude_hpp_included
#define amplitude_hpp_included

%(coefficient_includes)s

struct amplitude_term_t {
    integral_coeffs_t coefficient;
    integral_t integral_sectors;
};

std::vector<amplitude_term_t> amplitude_l[%loop%]_terms
{
    %(amplitude_terms)s
};

#endif
