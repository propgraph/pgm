//
//  utils.hpp
//  pgm-Cpp


#ifndef utils_hpp
#define utils_hpp

#include <iostream>
#include <vector>
#include <cmath>

typedef unsigned long ul;

namespace utils
{
    //Helper function declarations
    ul convertToDecimal(std::vector<ul>, std::vector<ul>, ul);
    std::vector<ul> convertToTuple(ul, std::vector<ul>, ul);
    std::vector<double> computeQuartiles(std::vector<ul>);
}

#endif /* utils_hpp */
