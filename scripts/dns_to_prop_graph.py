import collections
import numpy as np
import os, sys
import pandas as pd
import argparse
import statistics
from threading import Thread, Lock

#Checks to see if an edge is valid
def update_edge(key,value,property_map):
    #No Cycles (ie staying on one node)
    if key == value:
        return False
    
    prop_keys = list(property_map.keys())
    #Check to see if value is already a key
    if value in prop_keys:
        #Check to see if key is a value in list for value (ie cycle)
        if key in property_map[value]:
            return False


    # Check to see if node is a new node that hasn't been evaluated
    if key not in list(prop_keys):
        property_map[key] = []
    property_map[key].append(value)
    return True

#Updates a property for a given node
def update_property(key, value, property_map):
    if key not in list(property_map.keys()):
        property_map[key] = []
    
    property_map[key].append(value)
    return

#Creates ID's for the individual nodes. Node ID's could be written to a file
#But that currently isn't implemented
def set_id(node_id_map, node_str):
    if node_str not in list(node_id_map.keys()):
        node_id_map[node_str] = len(node_id_map)

#Creates edges between nodes
def createEdges(src_map, node_id_map):
    edge_dict = dict()
    keys = list(src_map.keys())
    for key in keys:
        edge_dict[int(node_id_map[key])] = []
        for elem in src_map[key]:
            edge_dict[int(node_id_map[key])].append(int(node_id_map[elem]))
    return edge_dict


#Function takes in a property(src_map) and generates a label for each node based on that property
def createLabels(src_map, node_id_map):
    node_ids = list(node_id_map.values())
    node_keys = list(node_id_map.keys())

    label_dict = dict.fromkeys(node_ids)   
    src_keys = list(src_map.keys())  

    threads = []
    lock = Lock()
    numActiveThreads = 0

    for i,node_key in enumerate(node_keys):
        t = Thread(target=setLabels,args=(node_key, node_id_map, src_keys, src_map, label_dict,lock))
        threads.append(t)
        t.start()
        numActiveThreads += 1
        if numActiveThreads == 500:
            for j in reversed(range(numActiveThreads)):
                threads[i-j].join()
            numActiveThreads = 0


    for i in range(len(threads) - numActiveThreads,len(threads)):
        threads[i].join()

    discretizeData(label_dict)
    return label_dict

#This function sets a label for a property for each node
def setLabels(node_key, node_id_map, src_keys, src_map, label_dict,lock):
    label_dict[node_id_map[node_key]] = 0
    if node_key in src_keys:
        for val in src_map[node_key]:
            lock.acquire()
            label_dict[node_id_map[node_key]] += val
            lock.release()


#Since data is not categorical, it must be discretized. Discretizes data to create label
def discretizeData(labels):
    keys = list(labels.keys())
    values = list(labels.values())
    med = statistics.median(values)

    threads = []
    lock = Lock()
    numActiveThreads = 0       

    for i,key in enumerate(keys):
        t = Thread(target=discretizeThread,args=(key,labels,med,lock))
        threads.append(t)
        t.start()
        numActiveThreads += 1
        if numActiveThreads == 500:
            for j in reversed(range(numActiveThreads)):
                threads[i-j].join()
            numActiveThreads = 0
    for i in range(len(threads)-numActiveThreads,len(threads)):
        threads[i].join()

#Discretizes property for an individual node
def discretizeThread(key, labels, med,lock):
    lock.acquire()    
    labels[key] = 1 if labels[key] > med else 0
    lock.release()


#Main Function. Reads input file, generates edges and labels and
#Writes output to OutDir
def processData(outDir, fieldIndex, fP):
    sep = ','
    node_id_map = dict()
    edges = {}
    src_times = {}
    res_times = {}
    totalEdges = 0

    #Read and Parse input file
    while True:
        line = fP.readline()
        if line == '':
            break
        totalEdges += 1
        line = line.strip().replace(" ", "")
        tokens = line.split(sep)
        src = tokens[fieldIndex['src']]
        res = tokens[fieldIndex['res']]
        time = int(tokens[fieldIndex['time']])
        
        if not update_edge(src, res,edges):
            continue

        update_property(src,time,src_times)
        update_property(res,time,res_times)
        set_id(node_id_map,src)
        set_id(node_id_map, res)

    fP.close()
    #Dictionary of edges
    edge_dict = createEdges(edges, node_id_map)
    src_time_dict = createLabels(src_times, node_id_map)
    res_time_dict = createLabels(res_times, node_id_map)

    edge_keys = list(edge_dict.keys())
    src_time_keys = list(src_time_dict.keys())
    res_time_keys = list(res_time_dict.keys())
    node_ids = list(node_id_map.values())

    print("Total Nodes:\t", len(node_ids))
    print("Total Edges:\t", totalEdges)

    edgeFile = open(outDir + ".edges","w")
    labelFile = open(outDir + '-labels.txt',"w")
    for key in node_ids:
        edge_list = []
        if key in edge_keys:
            edge_list = edge_dict[key]
            for i in range(len(edge_list)):
                edgeFile.write(str(key) + "\t" + str(edge_list[i]) + "\n")
        labelFile.write(str(src_time_dict[key]) + "\t" + str(res_time_dict[key]) + "\n")


#Creates Filed Index based on input
def createFieldIndex(path):
    fieldIndex = {"src": None, "res": None, "time": None}
    header = ""
    sep = ","
    fp = open(path, "r")
    while header == "":
        header = fp.readline()
   
    tokens = []
    for h in header.strip().split(sep):
        if h == '':
            continue
        tokens.append(h.strip())
    
    fieldIndex = getIndex(fieldIndex, tokens)
    status, invalidCol = checkFieldIndex(fieldIndex)
    if status:
        return fieldIndex,fp
    else:
        print("Error. Cannot find column corresponding to " + str(invalidCol))


#Creates index for each header element in file
def getIndex(fieldIndex, header):
    keys = list(fieldIndex.keys())
    for i,col in enumerate(header):
        if col in keys:
            fieldIndex[col] = i
    return fieldIndex

#Checks that src, header and res have values
def checkFieldIndex(fieldIndex):
  keys = list(fieldIndex.keys())
  for key in keys:
    if fieldIndex[key] == None and key != None:
      return False, key
  return True,None

def driver():
    parser = argparse.ArgumentParser()
    parser.add_argument('inPath')
    parser.add_argument('outPath')
    args = parser.parse_args()

    path = args.inPath
    outDir = args.outPath
    fieldIndex, filePointer = createFieldIndex(path)

    fileName = os.path.split(path)[1]
    outDir = outDir + fileName if outDir[len(outDir) - 1] == "/" else outDir + "/" + fileName

    processData(outDir, fieldIndex, filePointer)



if __name__ == '__main__':
    driver()