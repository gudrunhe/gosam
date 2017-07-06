#include <iostream>
#include <numeric> // std::accumulate
#include <complex> // std::conj

#include <secdecutil/integrators/cuba.hpp> // secdecutil::cuba::Vegas
//#include <secdecutil/integrators/Qmc.hpp> // secdecutil::integrators::Qmc
#include <secdecutil/deep_apply.hpp> // secdecutil::deep_apply


#include "../virtual/amplitude/amplitudel1.hpp"

int main()
{
    std::cout.precision(15);
    std::cout << std::scientific;
    std::cout << "# --- Test Program Launched ---" << std::endl;

    invariants_t invariants;
    parameters_t parameters;

    std::cout << parameters << std::endl;

    invariants.es12 = 250000.00000000000;
    invariants.es23 = -206453.12071082642;
    invariants.factoutscale = invariants.es12;

    secdecutil::cuba::Divonne<integral_complex_t> integrator;
    integrator.maxeval=1e7;
    integrator.epsrel=1e-5;
    integrator.epsabs=1e-8;
    integrator.border=1e-8;

//    secdecutil::integrators::Qmc<integral_complex_t> integrator;
//    integrator.minN=10000;
//    integrator.m = 32;

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
            invariants.es12/invariants.factoutscale,invariants.es23/invariants.factoutscale,
            parameters.mH/std::sqrt(invariants.factoutscale),parameters.mT/std::sqrt(invariants.factoutscale),
        },{});

        // set real_parameters, complex_parameters, number_of_samples, deformation_parameters_maximum, deformation_parameters_minimum, deformation_parameters_decrease_factor
        sector_make_integrands_return_t sector_integrands =  amplitude_term.sector_make_integrands(
        {
            invariants.es12/invariants.factoutscale,invariants.es23/invariants.factoutscale,
            parameters.mH/std::sqrt(invariants.factoutscale),parameters.mT/std::sqrt(invariants.factoutscale),
        },{},100000,1.,1.e-5,0.9);

        auto all_sectors = std::accumulate(++sector_integrands.begin(), sector_integrands.end(), *sector_integrands.begin() ); // TODO: add type box1L::nested_series_t<box1L::integrand_t>
        integral_return_t integral = secdecutil::deep_apply( all_sectors,  integrator.integrate );
        integral_return_t integral_with_prefactor = integral_prefactor*integral;

        return evaluated_amplitude_term_t {coefficient, integral_with_prefactor};

    };

    evaluated_amplitude_t evaluated_amplitude = secdecutil::deep_apply(amplitude_l1_terms, evaluate_amplitude);

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

    std::cout << "# --- Raw Result ---" << std::endl;
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
    std::cout << std::endl;

    std::cout << "# --- Result --- " << std::endl;

    // Reference result obtained with runcard
    //    process_name=gghh
    //    process_path=virtual
    //    in=21, 21
    //    out=25, 25
    //    model=smdiag
    //    order=QCD, NONE, 2
    //    one=gs,e,gHT,gHHH
    //    zero=mU,mD,mS,mC,mB,wT,wH
    //    filter.nlo= lambda d: d.vertices(Tbar, T, H) >= 1
    //    regularisation_scheme=cdr

    // Factor 1/512 obtained from:
    // 1/8 * 1/8 (average over incoming gluon colors)
    // 1/2 * 1/2 (average over incoming gluon spins)
    // 1/2 (symmetry factor)

    integral_complex_t loop1_f1_eps0 = result.at(0).at(0).at(0).value;
    integral_complex_t loop1_f2_eps0 = result.at(1).at(0).at(0).value;
    integral_real_t me2_loop1_eps0 = std::real(loop1_f1_eps0*std::conj(loop1_f1_eps0)) + std::real(loop1_f2_eps0*std::conj(loop1_f2_eps0));
    std::cout << "GOSAM-XLOOP AMP(0): " << me2_loop1_eps0/512. << std::endl;
    std::cout << "GOSAM       AMP(0): 5.359007789014169e-01" << std::endl;
    std::cout << std::endl;

    std::cout << "# --- Fin ---" << std::endl;

}
