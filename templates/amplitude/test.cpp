#include <iostream>
#include <numeric> // std::accumulate

#include <secdecutil/integrators/cuba.hpp> // secdecutil::cuba::Vegas
#include <secdecutil/deep_apply.hpp> // secdecutil::deep_apply


#include "amplitudel1.hpp"

int main()
{
    std::cout.precision(15);
    std::cout << "---- Test Program Launched ----" << std::endl;

    invariants_t invariants;
    parameters_t parameters;

    [% @for mandelstam sym_prefix=invariants.es non-zero non-mass %][% symbol %]=1.;
    [% @end @for %]

    secdecutil::cuba::Vegas<integral_complex_t> integrator;
    integrator.flags = 2; // verbose output --> see cuba manual

    // Evaluates amplitude terms with numerical invariants and physical parameters
    std::function<evaluated_amplitude_term_t(amplitude_term_t)> evaluate_amplitude =
    [invariants, parameters, integrator] (amplitude_term_t amplitude_term)
    {

        // Evaluates coefficient function with numerical invariants and physical parameters
        std::function<coeff_return_t(coeff_func_t)> evaluate_coefficient =
        [invariants, parameters] (coeff_func_t coeff_func)
        {
            return coeff_func(invariants, parameters);
        };

        coeffs_series_t coefficient = secdecutil::deep_apply(amplitude_term.coefficient, evaluate_coefficient);

        // set real_parameters, complex_parameters
        integral_prefactor_t integral_prefactor = amplitude_term.integral_prefactor(
        {
            [% @for mandelstam sym_prefix=invariants.es non-zero non-mass %][% symbol %],[% @end @for %]
            [% @for prefix=parameters. all_masses %][% mass %],[% @end @for %]
        },{});

        // set real_parameters, complex_parameters, number_of_samples, deformation_parameters_maximum, deformation_parameters_minimum, deformation_parameters_decrease_factor
        sector_make_integrands_return_t sector_integrands =  amplitude_term.sector_make_integrands(
        {
            [% @for mandelstam sym_prefix=invariants.es non-zero non-mass %][% symbol %],[% @end @for %]
            [% @for prefix=parameters. all_masses %][% mass %],[% @end @for %]
        },{},100000,1.,1.e-5,0.9);

        auto all_sectors = std::accumulate(++sector_integrands.begin(), sector_integrands.end(), *sector_integrands.begin() ); // TODO: add type box1L::nested_series_t<box1L::integrand_t>
        integral_return_t integral = secdecutil::deep_apply( all_sectors,  integrator.integrate );
        integral_return_t integral_with_prefactor = integral_prefactor*integral;

        return evaluated_amplitude_term_t {coefficient, integral_with_prefactor};

    };

    auto evaluated_amplitude = secdecutil::deep_apply(amplitude_l1_terms, evaluate_amplitude);

    for (auto term : evaluated_amplitude )
    {
        std::cout << "  + (" << term.integral << ") * " << std::endl << std::endl;
        std::cout << "    (" << std::endl;
        for (auto projector_coefficient : term.coefficient )
            for (auto color_projector_coefficient : projector_coefficient )
                std::cout << "      + (" << color_projector_coefficient  << ")" << std::endl;
        std::cout << "    )" << std::endl;
        
    };
    
    std::cout << "---- Fin ----" << std::endl;
    
}
