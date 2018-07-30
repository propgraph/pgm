//
//  options.hpp
//  pgm-Cpp
//

#ifndef options_hpp
#define options_hpp

#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>

#include "utils.hpp"

class options{
  
public:
    
    options(std::string);
    ~options();
    
    void readOptionsFile();
    const std::string getWorkingDir() const;
    const std::string getSourceGraphFile() const;
    const std::string getSourceAttribsFile() const;
    const std::string getTargetAttribsFile() const;
    const ul getNumAttribs() const;
    const std::vector<ul>& getAttribCardinalities() const;
    const ul getTotalAttributeCardinality() const;
    const double getNodeProbThreshold() const;
    const double getEdgeProbThreshold() const;
    const std::string getTargetGraphFile() const;
    const ul getNumTargetGraphNodes() const;
    const ul getNumTargetGraphEdges() const;
    const ul getRandomSeed() const;
    const ul getAugLabelCardinality() const;
    const int getNumberOfCores() const;
    const std::string getAugmentationType() const;
    const bool isAttributeInputExplicit() const;
    const bool isAugment() const;
    const bool isOpenMPCores() const;
    
   
private:
    
    std::string sOptionsFile, sWorkingDir, sSourceGraphFile, sTargetGraphFile, sSrcAttribsFile, sTarAttribsFile;
    std::string sAugmentType, sAttributeInputType;
    ul nAttribs, lAttribC, lNumTarGraphNodes, lNumTarGraphEdges, lRandSeed, lAugLabelC;
    std::vector<ul> vAttribCardinality;
    double dNodeProbThresh, dEdgeProbThresh;
    int numCores;
    bool bAugment, bOpenMPCores, bAttributeExplicit;
    
};

#endif /* options_hpp */
