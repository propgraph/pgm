import os, sys
from collections import OrderedDict


try:
    outFileName = sys.argv[1]
except:
    print("File name required")
    exit()

args = OrderedDict([("Working_Dir", None),\
("Source_Graph_File", None),\
("Source_Attributes_File", None),\
("Target_Graph_File", None),\
("Target_Attributes_File", None),\
("Number_Target_Graph_Nodes", None),\
("Number_Target_Graph_Edges", None),\
("Number_Attributes", None),\
("Attribute_Cardinalities", None),
("Node_Probability_Threshold", None),\
("Edge_Probability_Threshold", None),\
("Augment_Label_Cardinality", None),\
("Random_Seed", None),\
("Augmentation_Type", None),\
("OpenMP", None),\
("Attributes_Input_Type", None)\
])

#print(args)




keys = list(args.keys())



for key in keys:
    val = input(str(key) + "\n")
    
    #Path Arguments
    if key == "Working_Dir" and val[len(val) - 1] != "/":
        val = val + "/"
    
    #Integer Arguments
    if key == "Number_Target_Graph_Nodes" or key == "Number_Target_Graph_Edges" or key == "Number_Attributes" or key == "Augment_Label_Cardinality" or key == "Random_Seed" or key == "OpenMP":
        while True:
            try:
                assert int(val)
                break
            except ValueError:
                print("This value must be an integer")
                val = input(str(key) + "\n")
    
    #List Arguments
    if key == "Attribute_Cardinalities":
        while True:
            try:
                tmp_val = val.strip().split(" ")
                #Check Cardinality Length
                assert len(tmp_val) == int(args["Number_Attributes"])
                #Check Cardinality Values
                validVals = True
                for i,v in enumerate(tmp_val):
                    try:
                        assert int(v)
                    except ValueError:
                        validVals = False
                        raise Exception("Invalid entry for ", i, " entry")
                        break
                #If all values are valid, move on to next attribute
                if validVals:
                   break
            except:
                print("Cardinalities don't match total number of attributes")
                val = input(str(key) + "\n")

    #Float Arguments
    if key == "Node_Probability_Threshold" or key == "Edge_Probability_Threshold":
        while True:
            try:
                assert float(val)
                break
            except:
                print("Must be float")
                val = input(str(key) + "\n")

    #String Arguments
    if key == "Augmentation_Type":
        while True:
            try:
                assert val == "Linear" or val == "Logarithmic"
                break
            except:
                val = input(str(key) + "\n")
    
    if key == "Attributes_Input_Type":
        include = True
        while True:
            try:
                assert val == "Node_Id_Implicit"
                break
            except:
                response = input("Would you like to include this parameter (y/n)?")
                include = response == "y"
                if include:
                    val = input(str(key) + "\n")
                    continue
                else:
                    break
        if not include:
            del args[key]
            break

    args[key] = val

keys = list(args.keys())
outFP = open(outFileName,"w")
for key in keys:
    outFP.write(key + " "+ str(args[key]) + "\n")
