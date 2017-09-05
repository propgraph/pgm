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
    print ss.entropy(pLD)
    print ss.entropy(eProp)
    
    #print "Sum of edge proportions : "
    #print np.sum(eProp)
    #print eProp
    
        
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
    
    #Print statistics
    print
    
    print "Number of nodes in the given graph : ",len(G1.nodes())
    print "Number of nodes in the generated graph : ",len(G2.nodes())
    
    print
    
    print "Number of edges in the given graph : ",len(G1.edges())
    print "Number of edges in the generated graph : ",len(G2.edges())
    
    print
    
    print "Is the original graph connected : ", nx.is_connected(G1)
    print "Is the generated graph connected : ", nx.is_connected(G2)
    
    print
    
    #print "Diameter of the original graph : ", nx.diameter(G1)
    #print "Diameter of the generated graph : ", nx.diameter(G2)
    
    print
    #print "Avg. CC of the original graph : ", nx.average_clustering(G1)
    #print "Avg. CC of the generated graph : ", nx.average_clustering(G2)    
    
    #Degree distribution comparison
        
    deg1 = np.array(nx.degree(G1).values())
    deg2 = np.array(nx.degree(G2).values())
    y1 = pg.getCCDF(deg1)
    y2 = pg.getCCDF(deg2)
    jsd = pg.findJSDiv(deg1,deg2,100)
    print "JS Divergence : ",jsd
    
    c1 = [0,0,0]
    c2 = [1,0.6,0.0]
    
    plt.figure()
    plt.plot(range(len(y1)),y1,color= c1,linewidth = 6,linestyle="--",label = "Given graph")
    plt.plot(range(len(y2)),y2,color= c2,linewidth = 6,linestyle="--",label = "Expanded graph")
    #plt.yscale('log')
    #plt.xscale('log')    
    
    ax=plt.gca()
  
    #ax.fill_between(range(y1.shape[0]), 0, y1, facecolor=c1, interpolate=True, alpha=0.2)
    #ax.fill_between(range(y2.shape[0]), 0, y2, facecolor=c2, interpolate=True, alpha=0.2)        
    
    ax.xaxis.set_tick_params(labelsize=48)
    ax.yaxis.set_tick_params(labelsize=48)  
    
    #ax.xaxis.set_major_formatter(ScalarFormatter())
    #ax.set_xticks([10,20,50,100,200,500,1000])
    #plt.xlim([1,1600]) 
    #plt.ylim([0.0001,1.00])
    
    plt.xlabel("Degree",fontsize = 54)
    plt.ylabel("CCDF Value",fontsize = 54)
    plt.legend(fontsize = 50, loc = "upper right")
    plt.grid()
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.show()
        
if __name__ == "__main__" :
    

    
    #Regenerating the graph
       
    np.random.seed(0) #Seed
    expFactor = 2
       
    #Role based graph where given labels explain connectivity
    
    fG = "./datasets/graph-role.edges"  #Graph file
    fL = "./datasets/graph-role-labels.txt"     #Labels file
    cmmntStr = "role-based graph"

    print
    print ("Expansion of the graph for the test case : "+cmmntStr)
    simulateExpandedGraph(fL, fG, expFactor, cmmntStr)
    
        
    #PA based graph where given labels do not fully explain connectivity
    fG = "./datasets/graph-pa.edges"  #Graph file
    fL = "./datasets/graph-pa-labels.txt"     #Labels file
    cmmntStr = "PA graph"    
    
    print
    print ("Expansion of the graph for the test case : "+cmmntStr)
    simulateExpandedGraph(fL, fG, expFactor, cmmntStr)
    
    #Regeneration with augmented labels
    cmmntStr = "PA graph augmented"
    
    print
    print ("Expansion of the graph for the test case : "+cmmntStr)
    simulateExpandedGraph(fL, fG, expFactor, cmmntStr,True, 3)    
                  
    #Facebook graph
    fG = "./datasets/facebook.edges"  #Graph file
    fL = "./datasets/facebook-labels.txt"     #Labels file
    cmmntStr = "Facebook graph"

    print
    print ("Expansion of the graph for the test case : "+cmmntStr)
    simulateExpandedGraph(fL, fG, expFactor, cmmntStr,True, 3)    