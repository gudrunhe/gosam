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

//    [% @for mandelstam sym_prefix=invariants.es non-zero %]
//    [% @if is_non-mass %][% symbol %]=1.;[% @end @if %]
//    [% @if is_first %]invariants.factoutscale = [% symbol %];[% @end @if %]
//    [% @end @for %]
    invariants.factoutscale = 1.;

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
            invariants.factoutscale,
            [% @for mandelstam sym_prefix=invariants.es non-zero non-mass %][% symbol %],[% @end @for %]
            [% @for prefix=parameters. all_masses %][% mass %],[% @end @for %]
        },{},100000,1.,1.e-5,0.9);

        auto all_sectors = std::accumulate(++sector_integrands.begin(), sector_integrands.end(), *sector_integrands.begin() ); // TODO: add type box1L::nested_series_t<box1L::integrand_t>
        integral_return_t integral = secdecutil::deep_apply( all_sectors,  integrator.integrate );
        integral_return_t integral_with_prefactor = integral_prefactor*integral;

        return evaluated_amplitude_term_t {coefficient, integral_with_prefactor};

    };

    evaluated_amplitude_t evaluated_amplitude = secdecutil::deep_apply(amplitude_l1_terms, evaluate_amplitude);

    for (evaluated_amplitude_term_t term : evaluated_amplitude )
    {
        std::cout << "  + (" << term.integral << ") * " << std::endl << std::endl;
        std::cout << "    (" << std::endl;
        for (std::vector<coeff_series_t> projector_coefficient : term.coefficient )
            for (coeff_series_t color_projector_coefficient : projector_coefficient )
                std::cout << "      + (" << color_projector_coefficient  << ")" << std::endl;
        std::cout << "    )" << std::endl;
    };

    int number_of_projectors = evaluated_amplitude.front().coefficient.size();
    int number_of_color_structures = evaluated_amplitude.front().coefficient.front().size();

    // Initialise empty result matrix
    std::vector<std::vector<integral_return_t>> result; // TODO: typedef this, inner type should be integral_return_t * coeff_series_t
    for(int i = 0; i<number_of_projectors; i++)
    {
        std::vector<integral_return_t> temp; // TODO: inner type should be integral_return_t * coeff_series_t
        for(int j = 0; j<number_of_color_structures; j++)
        {
            temp.push_back({0,0,{0},false,"eps"});
        }
        result.push_back(temp);
    }

    // Add each term of the amplitude to the result
    for (evaluated_amplitude_term_t term : evaluated_amplitude )
    {
        int p = 0;
        for (std::vector<coeff_series_t> projector_coefficient : term.coefficient )
        {
            int c = 0;
            for (coeff_series_t color_projector_coefficient : projector_coefficient )
            {
                result.at(p).at(c) += color_projector_coefficient * term.integral;
                ++c;
            }
            ++p;
        }
    };

    std::cout << "---- Result ----" << std::endl;
    int p = 0;
    for(std::vector<integral_return_t> projector_result: result )
    {
        int c = 0;
        for(integral_return_t color_projector_result: projector_result)
        {
            std::cout << "c" << c <<"p" << p << ": " << color_projector_result  << ")" << std::endl;
            ++c;
        }
        ++p;
    }

    std::cout << "---- Fin ----" << std::endl;
    
}
