import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys

def getCCDF(data):
    
    data_dist = np.bincount(data)
    data_ccdf = 1-(data_dist.cumsum(0)/float(data_dist.sum()))
    
    return data_ccdf


if __name__ == "__main__":
    
    #Purpose : Compare source and the genersted output target graph in terms of basic stats including degree distribution
    #Usage : python compare_datasets.py "example_name"; For example python compare_datasets.py role
        
    #prefix is the name of the dataset (pa or role in the case of two examples)
    prefix = sys.argv[1]
    
    base_dir = "../data/"+prefix+"/"
    src = base_dir + prefix + ".edges"
    tar = base_dir + prefix + "-op.edges"
    
    #Recommended to be set to True for power-law type graphs to ensure better visualization
    logScale = False
    if ((prefix == "pa")):
        logScale = True
    
    G_src = nx.read_edgelist(src)
    G_tar = nx.read_edgelist(tar)
    
    deg_src = [tup[1] for tup in G_src.degree(nx.nodes(G_src))]
    deg_tar = [tup[1] for tup in G_tar.degree(nx.nodes(G_tar))]    
    
    print "Number of nodes and edges (SRC) : ", nx.number_of_nodes(G_src), " ", nx.number_of_edges(G_src)
    print "Number of nodes and edges (TAR) : ", nx.number_of_nodes(G_tar), " ", nx.number_of_edges(G_tar)
    print "Max degree (SRC) ", max(deg_src), "Min degree (SRC) ", min(deg_src), "Avg. degree (SRC) ", np.mean(deg_src)
    print "Max degree (TAR) ", max(deg_tar), "Min degree (TAR) ", min(deg_tar), "Avg. degree (TAR) ", np.mean(deg_tar)    
    print "Clustering coefficient (SRC) : ", nx.average_clustering(G_src)
    print "Clustering coefficient (TAR) : ", nx.average_clustering(G_tar)

    y_src = getCCDF(deg_src)
    y_tar = getCCDF(deg_tar) 
    

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.figure()
    plt.plot(range(len(y_src)),y_src,color= 'k',linewidth = 8,label = "Given graph")
    plt.plot(range(len(y_tar)),y_tar,color= 'r',linewidth = 8,linestyle="--",label = "Simulated graph")   
    if (logScale == True):
        
        plt.yscale('log')
        plt.xscale('log')          
        plt.xlim([15,500]) 

    ax = plt.gca()
    ax.xaxis.set_tick_params(labelsize=42)
    ax.yaxis.set_tick_params(labelsize=42)      
    
    plt.xlabel("Degree",fontsize = 44)
    plt.ylabel("CCDF Value",fontsize = 44)
    plt.legend(fontsize = 36, loc = "lower left")
    plt.grid()
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.show()
    #plt.savefig("comparison.png")    