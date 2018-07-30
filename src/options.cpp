//
//  options.cpp
//  pgm-Cpp
//

#include <fstream>
#include <cassert>

#include "options.hpp"

options::options(std::string sFile){
    
    sOptionsFile = sFile;
    bAugment = false;
    bOpenMPCores = false;
    bAttributeExplicit = true;
    
}

options::~options(){
    
    
}

void options::readOptionsFile(){
    
    std::fstream oFile(sOptionsFile, std::ios_base::in);
    if (oFile.good()){
        
        std::string sOption;
        while (oFile >> sOption)
        {
            if (sOption.compare("Working_Dir") == 0)      {   oFile >> sWorkingDir;   }
            if (sOption.compare("Source_Graph_File") == 0)       {   oFile >> sSourceGraphFile;   }
            if (sOption.compare("Target_Graph_File") == 0)       {   oFile >> sTargetGraphFile;   }
            if (sOption.compare("Source_Attributes_File") == 0)      {   oFile >> sSrcAttribsFile;   }
            if (sOption.compare("Target_Attributes_File") == 0)      {   oFile >> sTarAttribsFile;   }
            if (sOption.compare("Node_Probability_Threshold") == 0) {   oFile >> dNodeProbThresh; }
            if (sOption.compare("Edge_Probability_Threshold") == 0) {   oFile >> dEdgeProbThresh; }
            if (sOption.compare("Number_Attributes") == 0)    {   oFile >> nAttribs;   }
            if (sOption.compare("Number_Target_Graph_Nodes") == 0)    {   oFile >> lNumTarGraphNodes;   }
            if (sOption.compare("Number_Target_Graph_Edges") == 0)    {   oFile >> lNumTarGraphEdges;   }
            if (sOption.compare("Random_Seed") == 0)    {   oFile >> lRandSeed;   }
            if (sOption.compare("Augmentation_Type") == 0) { oFile >> sAugmentType; }
            if (sOption.compare("Attributes_Input_Type") == 0)  {
                oFile >> sAttributeInputType;
                if (sAttributeInputType.compare("Node_Id_Implicit") == 0) bAttributeExplicit = false;
            }
            if (sOption.compare("OpenMP") == 0)    {
                oFile >> numCores;
                if (numCores > 0) bOpenMPCores = true;
            }
            if (sOption.compare("Augment_Label_Cardinality") == 0) {
                
                oFile >> lAugLabelC;
                if (lAugLabelC > 10 ) {
                    std::cout << "Current limit of the augmented label cardinality is 10." << std::endl;
                    std::cout << "Setting Augment_Label_Cardinality to 10." << std::endl;
                    lAugLabelC = 10;
                }
                
                if (lAugLabelC >= 2){
                    bAugment = true;
                }
            }
            
            if (sOption.compare("Attribute_Cardinalities") == 0) {

                unsigned tmp = 0;
                lAttribC = 1;
                
                //Using whitespace to separate attribute cardinalities
                for (size_t idx = 0; idx < (nAttribs); ++idx){
                    oFile >> tmp;
                    vAttribCardinality.push_back(tmp);
                    lAttribC *= tmp;
                }
            }
            
        }
        
        sSourceGraphFile = sWorkingDir + sSourceGraphFile;
        sTargetGraphFile = sWorkingDir + sTargetGraphFile;
        sSrcAttribsFile = sWorkingDir + sSrcAttribsFile;
        sTarAttribsFile = sWorkingDir + sTarAttribsFile;
        
        std::cout << "Program options : " << std::endl;
        std::cout << "Working directory : " << sWorkingDir << std::endl;
        std::cout << "Source graph edgelist file : " << sSourceGraphFile << std::endl;
        std::cout << "Target graph edgelist file : " << sTargetGraphFile << std::endl;
        std::cout << "Source node attributes file : " << sSrcAttribsFile << std::endl;
        std::cout << "Target node attributes file : " << sTarAttribsFile << std::endl;
        std::cout << "Number of node attributes : " << nAttribs << std::endl;
        std::cout << "Attribute cardinalities : ";
        for (size_t idx = 0; idx < vAttribCardinality.size(); ++idx){ std::cout << vAttribCardinality[idx] << " ";}
        std::cout << "Total attribute cardinality : " << lAttribC << std::endl;
        std::cout << "Node probability threshold : " << dNodeProbThresh << std::endl;
        std::cout << "Edge probability threshold : " << dEdgeProbThresh << std::endl;
        std::cout << "#Nodes in the target graph : " << lNumTarGraphNodes << std::endl;
        std::cout << "#Edges in the target graph : " << lNumTarGraphEdges << std::endl;
        std::cout << "Random seed : " << lRandSeed << std::endl;
        std::cout << "Augmentation type : " << sAugmentType << std::endl;
        std::cout << "Augmented Label Cardinality : " << lAugLabelC << std::endl;
        std::cout << std::endl;
        
    }
    else {
        
        std::cerr << "Unable to read from the options file. Please check." << std::endl;
        exit(EXIT_FAILURE);
    }
}

const std::string options::getWorkingDir() const {
    
    return sWorkingDir;
}

const std::string options::getSourceGraphFile() const {

    return sSourceGraphFile;
}

const std::string options::getTargetGraphFile() const {
    
    return sTargetGraphFile;
}

const std::string options::getSourceAttribsFile() const {

    return sSrcAttribsFile;
}

const std::string options::getTargetAttribsFile() const {
    
    return sTarAttribsFile;
}

const std::string options::getAugmentationType() const {
    
    return sAugmentType;
}

const ul options::getNumAttribs() const{
    
    return nAttribs;
}

const std::vector<ul>& options::getAttribCardinalities() const {
    
    return vAttribCardinality;
}

const ul options::getTotalAttributeCardinality() const {
    
    return lAttribC;
}

const ul options::getNumTargetGraphNodes() const {
    
    return lNumTarGraphNodes;
}

const ul options::getNumTargetGraphEdges() const {
    
    return lNumTarGraphEdges;
}

const ul options::getRandomSeed() const {
    
    return lRandSeed;
}

const int options::getNumberOfCores() const {
    
    return numCores;
}

const ul options::getAugLabelCardinality() const {
    
    return lAugLabelC;
}

const double options::getNodeProbThreshold() const {
    
    return dNodeProbThresh;
}

const double options::getEdgeProbThreshold() const{
    
    return dEdgeProbThresh;
}

const bool options::isAttributeInputExplicit() const {
    
    return bAttributeExplicit;
}

const bool options::isAugment() const {
    
    return bAugment;
}

const bool options::isOpenMPCores() const {
    
    return bOpenMPCores;
}
