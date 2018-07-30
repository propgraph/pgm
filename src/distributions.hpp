//
//  distributions.hpp
//  pgm-Cpp
//

#ifndef distributions_hpp
#define distributions_hpp

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <random>

#include "options.hpp"
#include "utils.hpp"

class distributions{
  
public:
    
    distributions();
    distributions(unsigned int);
    distributions(const distributions*,unsigned int);
    ~distributions();
    
    void setDataAndOptions(const std::vector<ul>&, ul, double);
    void constructDist();
    const std::vector<ul>& generateSamples(ul);
    const ul generateUniformRandomInt(ul);

    
    
private:
    
    std::mt19937 generator;
    ul lCatSize;
    double pThresh;
    
    std::vector<ul> vData;
    std::vector<ul> vCategories;
    std::vector<double> vDistribution;
    std::vector<ul> vSamples;
    
    
};

#endif /* distributions_hpp */
