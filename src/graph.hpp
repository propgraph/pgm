//
//  graph.hpp
//  pgm-Cpp
//

#ifndef graph_hpp
#define graph_hpp

#include <iostream>
#include <tuple>
#include <set>
#include <map>
#include <array>
#include <string>

#include "options.hpp"
#include "distributions.hpp"
#include "utils.hpp"

class graph{

public:
    
    graph(options* );
    ~graph();
    
    void processInputPropertyGraph();
    void outputTargetPropertyGraph();
    
private:
    
    //Member variables
    options* pOpt; //Pointer to options object
    ul lAttribC, lDegreeMin, lDegreeMax; //Total attribute cardinality (product of all cardinalities)
    int numCores;
    
    typedef std::tuple<unsigned,unsigned> edge;
    
    std::set<ul> nodesSrc; //No duplicates allowed
    std::set<edge> edgesSrc; //No duplicates allowed
    
    std::vector<ul> vDegree;
    
    std::map<ul, std::vector<ul> > mSrcNodeAttr,mTarNodeAttr, mCatToNodeList;
    std::map<ul, ul> mSrcNodeAttrDec, mSrcNodeDegree, mCatCounts;
    
    std::vector<edge> vEdgesTar;
    
    distributions* Pl;
    distributions* Pc;
    
    //Member functions

    //Process input property graph
    void readEdgeList(std::string); //Read in edge list
    void readAttribs(std::string); // Read in attributes
    void printBasicStats(); //Some basic graph stats
    void constructDistributions();
    
    //Basic helper functions
    void addNode(ul);
    void addEdge(ul, ul);
    
    //Pl an Pc distributions
    void createNodeCategoryDistribution(); //Create node category distribution (Pl)
    void createEdgeCategoryDistribution(); //Create edge category distribution (Pc)
    
    //Target graph creation
    void createTargetNodes();
    void createTargetEdges();
    
    //Writing the target graph
    void writeTargetEdgeList(std::string);
    void writeTargetNodeAttributes(std::string);
    
    //Label Augmentation
    void augmentNodeLabels();
    
};

#endif /* graph_hpp */
