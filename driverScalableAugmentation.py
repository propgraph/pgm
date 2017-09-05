import numpy as np
import propgraph as pg
import networkx as nx
import matplotlib.pyplot as plt
import sys
import time
import scipy.stats as ss
from matplotlib.ticker import ScalarFormatter
from matplotlib import ticker


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
    
    return (deg1,deg2)

        
if __name__ == "__main__" :
    
    #PA based graph where given labels do not fully explain connectivity
    fG = "./datasets/facebook.edges"  #Graph file
    fL = "./datasets/facebook-labels.txt"     #Labels file
    cmmntStr = "Facebook graph" 
    
    #Regenerating the graph
       
    np.random.seed(11) #Seed
    expFactor = 1
  
   
    #Regeneration with augmented labels
    cmmntStr = "Facebook graph augmented"
    
    print
    print ("Expansion of the graph for the test case : "+cmmntStr)
    
    deg1,deg23 = simulateExpandedGraph(fL, fG, expFactor,cmmntStr,True, 4)
    deg1,deg22 = simulateExpandedGraph(fL, fG, expFactor,cmmntStr,True, 2)
    deg1,deg21 = simulateExpandedGraph(fL, fG, expFactor,cmmntStr,True, 1)
    deg1,deg20 = simulateExpandedGraph(fL, fG, expFactor,cmmntStr)
  
   
    j20 = pg.findJSDiv(deg1,deg20,100)
    j21 = pg.findJSDiv(deg1,deg21,100)
    j22 = pg.findJSDiv(deg1,deg22,100)
    j23 = pg.findJSDiv(deg1,deg23,100)
    
    y1 = pg.getCCDF(deg1)
    y20 = pg.getCCDF(deg20)
    y21 = pg.getCCDF(deg21)
    y22 = pg.getCCDF(deg22)
    y23 = pg.getCCDF(deg23)
    
    #y1 = np.sort(deg1)[::-1]
    #y20 = np.sort(deg20)[::-1]
    #y21 = np.sort(deg21)[::-1]
    #y22 = np.sort(deg22)[::-1]
    #y23 = np.sort(deg23)[::-1]    
    
    labelStr20 = "$n_a$ = 0, " + "JSD = " + str(round(j20,3))
    labelStr21 = "$n_a$ = 2, " + "JSD = " + str(round(j21,3))
    labelStr22 = "$n_a$ = 4, " + "JSD = " + str(round(j22,3))
    labelStr23 = "$n_a$ = 8, " + "JSD = " + str(round(j23,3))
    
    print labelStr20
    print labelStr21
    print labelStr22
    print labelStr23
    
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.figure()
    plt.plot(range(len(y1)),y1,color= 'k',linewidth = 8,label = "Given graph")
    plt.plot(range(len(y20)),y20,color= 'r',linewidth = 8,linestyle="--",label = labelStr20)
    plt.plot(range(len(y21)),y21,color= 'g',linewidth = 8,linestyle="--",label = labelStr21)
    plt.plot(range(len(y22)),y22,color= 'b',linewidth = 8,linestyle="--",label = labelStr22)
    plt.plot(range(len(y23)),y23,color= 'm',linewidth = 8,linestyle="--",label = labelStr23)
    
    plt.yscale('log')
    plt.xscale('log')  
    
    ax=plt.gca()

    ax.xaxis.set_tick_params(labelsize=42)
    ax.yaxis.set_tick_params(labelsize=42)  

    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.set_xticks([10,20,50,100,200,500,1000])
    plt.xlim([1,1200]) 
    plt.ylim([0.0001,1.00])

    plt.xlabel("Degree",fontsize = 54)
    plt.ylabel("CCDF Value",fontsize = 54)
    plt.legend(fontsize = 44, loc = "lower left")
    plt.grid()
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.show()                 
    