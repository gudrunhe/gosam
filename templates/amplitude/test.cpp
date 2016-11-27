#include <iostream>
#include <secdecutil/deep_apply.hpp> // secdecutil::deep_apply

#include "amplitudel1.hpp"

int main()
{
    std::cout << "---- Test Program Launched ----" << std::endl;

    invariants_t invariants;
    parameters_t parameters;

    invariants.es12 = -1.;
    invariants.es23 = 2.;

    // Evaluates coefficient function with numerical invariants and physical parameters
    std::function<coeff_return_t(coeff_func_t)> evaluate_coefficient =
    [invariants, parameters] (coeff_func_t coeff_func)
    {
        return coeff_func(invariants, parameters);
    };

    std::cout << " -- Printing Coefficients --" << std::endl;

    for (auto term : amplitude_l1_terms )
    {

        integral_coeffs_t coeff = term.coefficient;

        // Evaluated coefficient is a vector<vector<Series<double>>
        auto evaluated_coefficient = secdecutil::deep_apply(coeff, evaluate_coefficient);

        for (auto projector_coefficient : evaluated_coefficient )
            for (auto color_coefficient : projector_coefficient )
                std::cout << color_coefficient << std::endl;

    };

    std::cout << "---- Fin ----" << std::endl;
    
}
