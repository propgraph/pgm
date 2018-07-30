//
//  distributions.cpp
//  pgm-Cpp
//


#include <iostream>
#include "distributions.hpp"

distributions::distributions(){
    
    generator.seed(0);
}

distributions::distributions(unsigned int seed){

    generator.seed(seed);
}

distributions::distributions(const distributions* tDist, unsigned int seed)
{
    generator.seed(seed);
    vCategories = tDist->vCategories;
    vDistribution = tDist->vDistribution;
}

distributions::~distributions(){
    
}

void distributions::setDataAndOptions(const std::vector<ul> & tmpData, ul lSize, double dThresh) {
    
    vData = tmpData;
    lCatSize = lSize;
    pThresh = dThresh;
    
}

void distributions::constructDist(){
    
    ul numEntries = vData.size();
    std::vector<double> vCounts(lCatSize,0.0);
    
    for (size_t idx = 0; idx < numEntries; ++idx){
        vCounts[vData[idx]] += 1.00;
    }
    
    std::cout << "Computing the multinomial distribution entries." << std::endl;
    
    for (size_t idx = 0; idx < lCatSize; ++idx){
        
        double prob = vCounts[idx]/((double) numEntries);
        if (prob >= pThresh) {
            vCategories.push_back(idx);
            vDistribution.push_back(prob);
        }
    }

}

const std::vector<ul>& distributions::generateSamples(ul nSamples){
    
    vSamples.resize(nSamples);
    std::discrete_distribution<ul> distribution(vDistribution.begin(),vDistribution.end());
    
    for (size_t idx = 0; idx < nSamples; ++idx){
        ul sample = vCategories[distribution(generator)];
        //std::cout << "Sample # " << idx << " : " << sample << std::endl;
        vSamples[idx] = sample;
    }
    return vSamples;
}

const ul distributions::generateUniformRandomInt(ul lMax){
    
    std::uniform_int_distribution<ul> distribution(0,lMax);
    return distribution(generator);
}
