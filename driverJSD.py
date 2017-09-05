import numpy as np
import propgraph as pg
import networkx as nx
import matplotlib.pyplot as plt
import sys
import time
import scipy.stats as ss
from matplotlib.ticker import ScalarFormatter


def simulateExpandedGraph(fileL, fileG, eF, commentStr, augFlag = False, nLA = None):
    
    #Estimation part from given 
    
    eL = pg.readEdges(fileG)
    G1 = nx.Graph()
    G1.add_edges_from(eL)   
    
    
    nND, nLD, vLD = pg.readLabels(fileL)

    if(augFlag):
        print "Augmenting ", nLA, " additional labels."
        nLD = nLD + nLA
        vLD = pg.augmentDegreeBasedLabels(G1,vLD,nLA)
        
    
    pLD = pg.computeLabelDist(vLD,nLD,nND)
    pED, eProp = pg.computeEdgeProbabilities(fileG,nND,nLD,vLD,pLD)
        
    start = time.time()
  
    #Expand from the estimated distribution
    nNE = int(np.floor(eF*nND))
    vLE = pg.generateLabels(nNE,nLD,pLD)
    nE = int(eF*len(eL)*(1+0.1*np.log(eF)))
    eLE = pg.generateEdgesScalable(nNE,nE,nLD,vLE,eProp)
    
   
    end = time.time()
    print "Time taken to generate the expanded graph and labels : ", (end-start), " seconds"



    G2 = nx.Graph()
    G2.add_edges_from(eLE) 
    
    print
        
    print "Number of nodes in the given graph : ",len(G1.nodes())
    print "Number of nodes in the generated graph : ",len(G2.nodes())
    
    print
    
    print "Number of edges in the given graph : ",len(G1.edges())
    print "Number of edges in the generated graph : ",len(G2.edges())
    
    print    
        
    deg1 = np.array(nx.degree(G1).values())
    deg2 = np.array(nx.degree(G2).values())
    y1 = pg.getCCDF(deg1)
    y2 = pg.getCCDF(deg2)
    jsd = pg.findJSDiv(deg1,deg2,100)
    
    return jsd
        
if __name__ == "__main__" :
    

    
    #Regenerating the graph
       
    np.random.seed(0) #Seed
    expFactor = 1
       
    fG = "./datasets/graph-pa.edges"  #Graph file
    fL = "./datasets/graph-pa-labels.txt"     #Labels file
    cmmntStr = "PA graph"
    nGraphs = 2
    jsdValues = np.zeros((nGraphs))
    
    for idx in range(nGraphs):
    
        jsdValues[idx] = simulateExpandedGraph(fL, fG, expFactor, cmmntStr,True, idx)
    
    print jsdValues
    
    #plt.plot(np.power(2,range(nGraphs)),jsdValues,color= 'r',linewidth = 6,linestyle="--")
    #plt.plot(np.power(2,range(nGraphs)),jsdValues,color= 'r',linewidth = 8,linestyle= "None", marker='o', ms=18)
    #ax=plt.gca()
    
    #ax.xaxis.set_tick_params(labelsize=42)
    #ax.yaxis.set_tick_params(labelsize=42) 
    #plt.xlabel("Number of augmented categories",fontsize = 54)
    #plt.ylabel("Jensen-Shannon Divergence",fontsize = 54)
    #plt.grid()
    #plt.gcf().subplots_adjust(bottom=0.15)
    #plt.show()     
                  
    