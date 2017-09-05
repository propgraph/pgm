import numpy as np
import itertools as it
import scipy.stats as ss
import networkx as nx
import re

def generateLabels(nNodes,nLabels,pLabels):
    
    print "Generating labels from the given label distribution ", "for ",nNodes," vertices." 
    vertLabels = np.zeros((nNodes,nLabels),dtype=int)
    # All possible label assignments
    allTuplesLabels = list(it.product([0,1],repeat=(nLabels)))
        
    for idx in range(nNodes):
        
        vertLabel = list(np.random.multinomial(1, pLabels))
        thisLabel = vertLabel.index(1)
        
        #Get the binary equivalent of this label 
        vertLabels[idx,:] = allTuplesLabels[thisLabel]
   
    return vertLabels

def generateEdges(nNodes,nLabels,vLabels,pEdge,thinningFactor):
    
    print "Generating edges based on joint with label distribution."
    
    edgeList = []
    allTuplesLabels = list(it.product([0,1],repeat=(2*nLabels)))
    
    for idx in range(nNodes):
        for jdx in range(idx+1,nNodes):    
            
            twoLabels = list(vLabels[idx]) + list(vLabels[jdx])
            twoLabelsIndex = allTuplesLabels.index(tuple(twoLabels))
            
            prob = pEdge[twoLabelsIndex]
            
            #Sample undirected edge
            if (np.random.random() < thinningFactor*prob):
                edgeList.append(tuple((idx,jdx)))             
                   
    return edgeList

def generateEdgesScalable(nNodes,nEdges,nLabels,vLabels,eProp):
    
    print "Bucketing the vertices based on their attributes."
    nBucket = bucketVertices(nNodes,vLabels,nLabels)
    #print nBucket
    
    edgeList = []
    allTuplesLabels = list(it.product([0,1],repeat=(2*nLabels)))
    print "Sampling the edges from the joint distribution : "
    for idx in range(nEdges):
        
        #print
        #print
        #print "Edge number : ", idx
        #print
        #Get the bucket in which the edge falls
        bList = list(np.random.multinomial(1,eProp))
        eBucket = bList.index(1)
                
        #Compute the two node label indices
        eLIdx = bin(eBucket)[2:]
        eLIdxFill = eLIdx.zfill(2*nLabels)
        #print eLIdx
        #print eLIdxFill        
        
        
        n1LIdx = int(eLIdxFill[:nLabels],2)
        #print n1LIdx
        n2LIdx = int(eLIdxFill[nLabels:],2)
        #print n2LIdx
        
        #Now sample these two vertices at random from the bucket IDs
        #print len(nBucket[n1LIdx])
        #print len(nBucket[n2LIdx])
        
        if((len(nBucket[n1LIdx]) == 0) or (len(nBucket[n2LIdx]) == 0)):
            continue
                
        n1Idx = np.random.randint(len(nBucket[n1LIdx]))
        n1 = (nBucket[n1LIdx])[n1Idx]
        
        n2Idx = np.random.randint(len(nBucket[n2LIdx]))
        n2 = (nBucket[n2LIdx])[n2Idx]
        
        if (n1 == n2):
            edgeList.append(tuple((n1,n2)))
        else:
            edgeList.append(tuple((min(n1,n2),max(n1,n2))))
        
    return edgeList

def bucketVertices(nNodes,vL,nL):
    
    bVert = {}
    allTuplesLabels = list(it.product([0,1],repeat=(nL)))
    totTuples = len(allTuplesLabels)

    for idx in range(totTuples):
        bVert[idx] = []
    
    for idx in range(nNodes):
        labelIndex = allTuplesLabels.index(tuple(vL[idx,:]))
        (bVert[labelIndex]).append(idx)
    
    return bVert

def getFreq(data):
    
    data_dist = np.bincount(data)
    data_freq = data_dist/float(data_dist.sum())
    
    return data_freq

def getCDF(data):
    
    data_dist = np.bincount(data)
    data_cdf = data_dist.cumsum()/float(data_dist.sum())
    
    return data_cdf

def getCCDF(data):
    
    data_dist = np.bincount(data)
    data_ccdf = 1-(data_dist.cumsum(0)/float(data_dist.sum()))
    
    return data_ccdf

def findJSDiv(l1,l2,nBins):
    
    bin_edges = np.linspace(min(min(l1),min(l2)),max(max(l1),max(l2)),(nBins+1),endpoint=True)
    
    l1hist = np.histogram(l1,bin_edges)[0]
    l1dist = l1hist/float(l1hist.sum())
    
    l2hist = np.histogram(l2,bin_edges)[0]
    l2dist = l2hist/float(l2hist.sum())    
    
    mdist = (l1dist+l2dist)/2.0
    
    jsd = 0.5*(ss.entropy(l1dist,mdist)+ss.entropy(l2dist,mdist))
    
    return jsd

def writeLabels(nNodes,vLabels,labelFile):
    
    print "Writng labels to ", labelFile
    f= open(labelFile,'w')
    
    for idx in range(nNodes):
        thisLabel = list(vLabels[idx,:])
        
        f.write(str(idx) + "\t")
        
        for label in thisLabel:
            f.write(str(label)+"\t")

        f.write("\n")
        
    f.close()

def writeEdges(edges,graphFile):
    
    print "Writing edges to ",graphFile
    
    f = open(graphFile,'w')

    for edge in edges:
        f.write(str(edge[0]) + "\t" + str(edge[1]))
        f.write("\n")

    f.close()

def readEdges(graphFile):
    
    print "Reading edges from ",graphFile
    
    f = open(graphFile,'r')
    lines = f.readlines()
    eList = []
    
    for edge in lines:
        node1 = int(edge.split()[0])
        node2 = int(edge.split()[1])
        
        eList.append((node1,node2))

    f.close()
    
    return eList
    
def readLabels(labelFile):
    
    print "Reading labels from ", labelFile
    
    f = open(labelFile)
    lines = f.readlines()
    nNodes = len(lines)
    
    nLabels = len(getLabels(lines[0]))
    vertLabels = np.zeros((nNodes,nLabels),dtype=int) 
    count = 0
    
    for line in lines:
        
        vertLabels[count,:] = getLabels(lines[count])
        count = count+1
    
    return(nNodes, nLabels, vertLabels)

def getLabels(lineStr):
    
    labels = []
    newlineFlag = False
    
    if "\n" in lineStr:
        lineStr = lineStr[:-1]  
        newlineFlag = True

    labels = lineStr.split("\t")
    
    if (newlineFlag):
        labels = labels[:-1]
    
    idLabels = map(int,labels)
    boolLabels = idLabels[1:]
        
    return boolLabels

def computeLabelDist(vLabels,nLabels, nNodes):
    
    print "Computing label distribution over ", nNodes, "vertices."
    allTuplesLabels = list(it.product([0,1],repeat=(nLabels)))
    countLabels = np.zeros(np.power(2,nLabels))
    
    for idx in range(nNodes):
        
        labelIndex = allTuplesLabels.index(tuple(vLabels[idx,:]))
        countLabels[labelIndex] = countLabels[labelIndex] + 1
    
    pLabels = countLabels/float(nNodes)
    
    return pLabels

def computeEdgeProbabilities(graphFile,nNodes,nLabels,vLabels,pLabels):
    
    print "Computing edge probabilities from the vertex labels and the edge-list."
    
    f = open(graphFile)
    
    lines = f.readlines()
    nEdges = len(lines)
    
    src = np.zeros(nEdges,dtype=int)
    dest = np.zeros(nEdges,dtype=int)
    count = 0
    
    for line in lines:
        
        nodes = getSrcDest(line)
        src[count] = nodes[0]
        dest[count] = nodes[1]
        
        count = count + 1

    allTuplesLabels = list(it.product([0,1],repeat=nLabels))
    allTuplesTwoLabels = list(it.product([0,1],repeat=(2*nLabels)))
    countTwoLabels = np.zeros(np.power(2,2*nLabels))   
    pEdge = np.zeros(np.power(2,2*nLabels)) 
    edgeProp = np.zeros(np.power(2,2*nLabels))

    for idx in range(nEdges):
        
        twoLabels = list(vLabels[src[idx]]) + list(vLabels[dest[idx]])
        twoLabelsIndex = allTuplesTwoLabels.index(tuple(twoLabels))        
       
        countTwoLabels[twoLabelsIndex] = countTwoLabels[twoLabelsIndex] + 1
    
    #Actual probabilities
    for idx in range(np.power(2,2*nLabels)):
        
        twoLabels = allTuplesTwoLabels[idx]

        label1 = twoLabels[0:nLabels]
        label2 = twoLabels[nLabels:(2*nLabels)]
        
        index1 = allTuplesLabels.index(tuple(label1)) 
        index2 = allTuplesLabels.index(tuple(label2))
        
        possibleCounts = pLabels[index1]*pLabels[index2]*(nNodes*(nNodes-1)/float(2.0))
                        
        if (possibleCounts != 0):
            pEdge[idx] = countTwoLabels[idx]/float(possibleCounts)
        else:
            pEdge[idx] = 0.0
            
        edgeProp[idx] = countTwoLabels[idx]/nEdges
        
    
    #Make pEdge symmetric
    pEdge = makeProbSymmetric(pEdge,nLabels)
    edgeProp = makeProbSymmetric(edgeProp,nLabels)
    
    return (pEdge, edgeProp)

def makeProbSymmetric(pMat, nLabels):
    
    temp1 = np.reshape(pMat,(np.power(2,nLabels),np.power(2,nLabels)))
    temp2 = np.transpose(temp1)
    temp3 = (temp1+temp2)/2.0
    
    pMat = np.reshape(temp3,np.power(2,2*nLabels))
    
    return pMat
    
               
def getSrcDest(lineStr):
    
    newlineFlag = False
        
    if "\n" in lineStr:
        lineStr = lineStr[:-1]  
        newlineFlag = True

    nodes = lineStr.split()
    nodes = map(int,nodes)
    
    return nodes

def compareDistributions(p1,p2,typeDist):
    
    err = 0.0
    if (typeDist == 1):
        rel = np.abs(p1-p2)
        err = np.linalg.norm(rel)/np.linalg.norm(p1)
        
    elif (typeDist == 2):
        
        #Normalize to probability distributions if already not
        pN1 = p1/float(np.sum(p1))
        pN2 = p2/float(np.sum(p2))
        
        err = ss.entropy(p1,p2)
        
    return err
    
def createTopologyBA(nVal,mVal,sVal):
    
    G = nx.barabasi_albert_graph(nVal,mVal,sVal)
    return G.edges()

def augmentDegreeBasedLabels(G,vLabel,nAug):
    
       
    nIntervals = np.power(2,nAug)
    nNodes = vLabel.shape[0]
    
    #G = nx.Graph()
    #G.add_edges_from(eList)
    deg = nx.degree(G).values()
    
    minDeg = min(deg)
    maxDeg = max(deg)
    
   
    logSpacing = (np.log(maxDeg)-np.log(minDeg))/float(nIntervals)
    newLabels = np.zeros((nNodes,nAug),dtype=int)
    
    for idx in range(nNodes):
        thisDeg = deg[idx]
        degBin = int(np.floor((np.log(thisDeg) - np.log(minDeg))/logSpacing))
        
        thisLabel = np.zeros(nAug,dtype=int)
        binDegLabel = bin(degBin)[2:].zfill(nAug)

        for jdx in range(nAug):
            thisLabel[nAug-jdx-1] = int(binDegLabel[-1-jdx])        
  
        newLabels[idx,:] = thisLabel
        
    
    vAllLabels = np.concatenate((vLabel,newLabels),axis=1)

    return vAllLabels    
    
        
        
    
    