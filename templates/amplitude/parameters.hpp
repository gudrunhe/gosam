%=$
/*
 *
 * Defines the complete list of parameters known to GoSam
 * Written by: template.xml
 *
 */

#ifndef parameters_hpp_included
#define parameters_hpp_included

#include <iostream>
#include <iomanip>
#include "typedef.hpp"

struct parameters_t
{
    // Constants
    const real_parameter_t pi = real_parameter_t(3.141592653589793238462643383279502884197169399375105820974944592307816406286209L);
//    const real_parameter_t pi = real_parameter_t("3.141592653589793238462643383279502884197169399375105820974944592307816406286209"); // TODO - implement this multiprecision version


    // Input Parameters
    [$ @for parameters $]
    [$ @select type
    @case R $]real_parameter_t [$ $_ $] = [$real convert=float format=%24.15f $];[$
    @case C $]complex_parameter_t [$ $_ $] = {[$ real convert=float format=%24.15f $], [$ imag convert=float format=%24.15f $]};[$
    @case RP $]const real_parameter_t [$ $_ $] = [$real convert=float format=%24.15f $];[$
    @case CP $]const complex_parameter_t [$ $_ $] = {[$ real convert=float format=%24.15f $], [$ imag convert=float format=%24.15f $]};
    [$ @end @select type $][$ @end @for parameters $]

    // Derived Parameters
    [$ @for functions_resolved language=cpp $]
    [$ @select type
    @case R $]real_parameter_t [$ $_ $] = [$ expression $];[$
    @case C $]complex_parameter_t [$ $_ $] = [$ expression $];
    [$ @end @select type $][$ @end @for functions_resolved $]


    friend std::ostream& operator<< (std::ostream& os, const parameters_t& parameters)
    {
        const char separator = ' ';
        const int nameWidth = 15;
        const int numWidth = 40;

        os << "# --- PARAMETER VALUES ---" << std::endl;

        os << "# Constants" << std::endl;
        os << std::left << std::setw(nameWidth) << std::setfill(separator) << "# pi";
        os << " = ";
        os << std::left << std::setw(numWidth) << std::setfill(separator) << parameters.pi << std::endl;

        os << "# Input Parameters" << std::endl;
        [$ @for parameters $]os << std::left <<  std::setw(nameWidth) << std::setfill(separator) << "# [$ $_ $]";
        os << " = ";
        os << std::left << std::setw(numWidth) << std::setfill(separator) << parameters.[$ $_ $] << std::endl;
        [$ @end @for parameters $]

        os << "# Derived Parameters" << std::endl;
        [$ @for functions_resolved language=cpp $]os << std::left <<  std::setw(nameWidth) << std::setfill(separator) << "# [$ $_ $]";
        os << " = ";
        os << std::left << std::setw(numWidth) << std::setfill(separator) << parameters.[$ $_ $] << std::endl;
        [$ @end @for functions_resolved $]

        return os;
    };
};

#endif
