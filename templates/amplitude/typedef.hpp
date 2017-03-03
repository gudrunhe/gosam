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
#include <secdecutil/uncertainties.hpp> // secdecutil::UncorrelatedDeviation
#include <secdecutil/sector_container.hpp> // secdecutil::SectorContainerWithDeformation
#include <secdecutil/integrand_container.hpp> // secdecutil::IntegrandContainer


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
typedef secdecutil::Series<coeff_func_t> coeff_func_series_t;
typedef std::vector<std::vector<coeff_func_series_t>> coeffs_func_series_t;
typedef secdecutil::Series<coeff_return_t> coeff_series_t;
typedef std::vector<std::vector<coeff_series_t>> coeffs_series_t;

// Integrals
typedef double integral_real_t;
typedef std::complex<double> integral_complex_t;
typedef std::vector<integral_real_t> integral_real_parameters_t;
typedef std::vector<integral_complex_t> integral_complex_parameters_t;
typedef std::vector<secdecutil::Series<secdecutil::IntegrandContainer<integral_complex_t, integral_real_t const * const>>> sector_make_integrands_return_t;
typedef std::function<sector_make_integrands_return_t(const integral_real_parameters_t&, const integral_complex_parameters_t&,unsigned,integral_real_t,integral_real_t,integral_real_t)> sector_make_integrands_t;
typedef secdecutil::Series<secdecutil::UncorrelatedDeviation<integral_complex_t>> integral_return_t;
typedef secdecutil::Series<integral_complex_t> integral_prefactor_t;
typedef std::function<integral_prefactor_t(integral_real_parameters_t,integral_complex_parameters_t)> integral_prefactor_function_t;


// Amplitude
struct amplitude_term_t {
    coeffs_func_series_t coefficient;
    integral_prefactor_function_t integral_prefactor;
    sector_make_integrands_t sector_make_integrands;
};
typedef std::vector<amplitude_term_t> amplitude_t;

// Evaluated Amplitude
struct evaluated_amplitude_term_t {
    coeffs_series_t coefficient;
    integral_return_t integral;
};

#endif
