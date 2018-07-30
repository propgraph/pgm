//
//  utils.cpp
//  pgm-Cpp
//


#include "utils.hpp"

namespace utils
{
    //Helper function definitions
    ul convertToDecimal(std::vector<ul> aVec, std::vector<ul> baseVec, ul nL){
        
        ul decAttr = aVec[0];
        for (size_t idx = 1; idx < nL; ++idx){
            decAttr *= baseVec[idx];
            decAttr += aVec[idx];
        }
        
        return decAttr;
    }
    
    std::vector<ul> convertToTuple(ul decAttr, std::vector<ul> baseVec,ul nL){
        
        std::vector<ul> aVec(nL,0);
        std::ldiv_t dv{};
        ul num = decAttr;
        
        for (size_t idx = nL; idx > 0; idx--){
            
            dv = std::ldiv(num,baseVec[idx-1]);
            aVec[idx-1] = dv.rem;
            num = dv.quot;
        }
        return aVec;
    }
    
    std::vector<double> computeQuartiles(std::vector<ul> vVec){
        
        
        //First sort
        
        std::vector<double> vQuart{0.0,0.25,0.5,0.75,1.0};
        std::vector<double> vQuartValues(0.0,vQuart.size());
        ul n  = vVec.size();
        
        for (size_t idx = 0; idx < vQuart.size(); ++idx) {
            
                double id = (n - 1) * vQuart[idx];
                double lo = floor(id);
                double hi = ceil(id);
                double qs = vVec[lo];
                double h  = (id - lo);
        
                double qVal = (1.0 - h) * qs + h * vVec[hi];
            
                vQuartValues.push_back(qVal);
        }
        
        return vQuartValues;
    }
}

