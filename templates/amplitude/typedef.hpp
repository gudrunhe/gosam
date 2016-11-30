/*
 *
 * Defines the type of the invariants, parameters, coefficients and integrals
 * Written by: template.xml
 *
 */

#ifndef typedef_hpp_included
#define typedef_hpp_included

#include <functional>
#include <vector>
#include <cmath> // sqrt
#include <complex>
#include <secdecutil/series.hpp> // secdecutil::Series
#include <secdecutil/sector_container.hpp> // secdecutil::SectorContainerWithDeformation

// Global Constants
const std::complex<double> i_(0.,1.);
const double sqrt2 = sqrt(2.);

// Invariants
typedef double invariant_t;
#include "invariants.hpp"

// Physical Parameters
typedef double real_parameter_t;
typedef std::complex<double> complex_parameter_t;
#include "parameters.hpp"

// Coefficients
typedef double coeff_return_t;
typedef std::function<coeff_return_t(invariants_t, parameters_t)> coeff_func_t;
typedef secdecutil::Series<coeff_func_t> integral_coeff_t;
typedef std::vector<std::vector<integral_coeff_t>> integral_coeffs_t;

// Integrals
typedef double integral_real_t;
typedef std::complex<double> integral_complex_t;
typedef std::array<integral_real_t,[% @for mandelstam sym_prefix=es non-zero non-mass%][% @if is_last %][% index %][% @end @if %][% @end @for mandelstam %]+[% @for all_masses %][% @if is_last %][% index %][% @end @if %][% @end @for all_masses %]> integral_real_parameters_t;
typedef std::array<integral_complex_t,0> integral_complex_parameters_t;
typedef std::vector<secdecutil::Series<secdecutil::SectorContainerWithDeformation<integral_real_parameters_t,integral_complex_parameters_t,integral_real_t,integral_complex_t>>> integral_t;

// Amplitude
struct amplitude_term_t {
    integral_coeffs_t coefficient;
    integral_t integral_sectors;
};
typedef std::vector<amplitude_term_t> amplitude_t;

#endif
