//
//  main.cpp
//  pgm-Cpp
//


#include <iostream>
#include <string>
#include <cstdlib>

#include "graph.hpp"
#include "options.hpp"


int main(int argc, const char * argv[]) {
    
    //Source files

    std::string sOptFile;
    //std::string sOptFile = "/Users/visw924/Desktop/Projects/T-APM/pgm-Cpp/data/options-sample.txt";
    
    //Get the input filenames
    
    if (argc < 2){
        std::cerr << "Not enough program arguments." << std::endl;
        exit(EXIT_FAILURE);
    }
    else{   sOptFile = std::string(argv[1]); }
        
    options* Options = new options(sOptFile);
    Options->readOptionsFile();
    
    graph* Graph = new graph(Options);
    Graph->processInputPropertyGraph();
    Graph->outputTargetPropertyGraph();
    
    delete Options;
    delete Graph;
    
    return 0;
}
