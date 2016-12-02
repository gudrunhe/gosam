#define _USE_MATH_DEFINES
#include <math.h> // M_PI
#include <iostream>
#include <secdecutil/deep_apply.hpp> // secdecutil::deep_apply

#include "amplitudel1.hpp"

int main()
{
    std::cout << "---- Test Program Launched ----" << std::endl;

    invariants_t invariants;
    parameters_t parameters;

    invariants.es12 = 90000;
    invariants.es23 = -62500;

    parameters.mH = 125.;
    parameters.mT = 173.;
    parameters.mW = 1.;

    parameters.e = 1.;
    parameters.gHHH = -3./2.*pow(parameters.mH,2)/parameters.mW; // g = 1
    parameters.gHT = -1./2.*parameters.mT/parameters.mW; // g = 1


    // We will convert our conventions to those of Glover, i.e... by "gauge1", "gauge2" we mean exactly the quantities given in Nuclear Physics B309 (1988) 282-294 Eq(7-9)
    // pi^2/(2pi)^D missing for each integral => multiply our result by 1./(16.*pow(M_PI,2))
    // glover factors out 1/(8.*mW^2) => multiply our result by 8.*pow(parameters.mW,2),
    // glover factors out \alpha_s \alpha_w = gs^2/(4pi) g^2/(4pi) => multiply our result by 16.*pow(M_PI,2) for gs = g = 1
    // apparently our amplitude convention differs by (-1) compared to glover => multiply our result by (-1)
    // we return the coefficient of c1 = Tr[t^a t^b] = TF * \delta^{AB} but glover gives the coeff of \delta^{AB} => multiply our result by TF = 1/2
    std::complex<double> prefactor = 1./(16.*pow(M_PI,2)) * 8.*pow(parameters.mW,2) * 16.*pow(M_PI,2) * (-1.) * 1/2.;

    // Evaluates coefficient function with numerical invariants and physical parameters
    std::function<coeff_return_t(coeff_func_t)> evaluate_coefficient =
    [invariants, parameters] (coeff_func_t coeff_func)
    {
        return coeff_func(invariants, parameters);
    };

    std::cout << " -- Printing Coefficients --" << std::endl;

    secdecutil::Series<std::complex<double>> gauge1 = {0,2, {0.,0.,0.}, true, "eps"};
    secdecutil::Series<std::complex<double>> gauge2 = {0,2, {0.,0.,0.}, true, "eps"};

    for (auto term : amplitude_l1_terms )
    {

        integral_coeffs_t coeff = term.coefficient;

        // Evaluated coefficient is a vector<vector<Series<double>>
        auto evaluated_coefficient = secdecutil::deep_apply(coeff, evaluate_coefficient);

        auto& projector1 = evaluated_coefficient.at(0);
        auto& projector2 = evaluated_coefficient.at(1);

        for (auto color_coefficient : projector1 )
        {
            gauge1 += prefactor * color_coefficient;
            std::cout << prefactor * color_coefficient << std::endl;
        }

        for (auto color_coefficient : projector2 )
        {
            gauge2 += prefactor * color_coefficient;
            std::cout << prefactor * color_coefficient << std::endl;
        }

    }

    std::cout << "gauge1: " << gauge1 << std::endl;
    std::cout << "gauge2: " << gauge2 << std::endl;
    std::cout << "gauge1+gauge2: " << gauge1 + gauge2 << std::endl;
    
    std::cout << "---- Fin ----" << std::endl;
    
}
