import logging
from rdflib import Graph
from scipy.sparse import *
from scipy import *
import numpy as np
import imp
import ConfigParser

"""
Turtle reader to parse a turtle file into a
n*n*m Matrix where 
n = number of distinct resources
m = number of predicates
to use the rescal algorithm for computing the tensor factorization
on the m n*n slices

#todo: write turtle result into file, or make it accessible to java
"""
#read configs
config = ConfigParser.ConfigParser()
config.read("config.ini")

#load rescal algorithm
rescal = imp.load_source('rescal',config.get("paths","pathToRescal"))

#set logging to basic
logging.basicConfig()

graph = Graph()
#parsing ttl file into data structure
graph.parse(config.get("paths","pathToTurtleFile"),format='n3')


resources = set()
predicates = set()

#calculate number of distinct resources and predicates by collecting them
for s, p, o in graph:
#if the object is a literal, ignore this triple
    if("http" in o):
        resources.add(s)
        resources.add(o)
        predicates.add(p)

resourcesList = list()
predicatesList = list()

#build iterable,indexalbe lists
for r in resources:
    resourcesList.append(r)
for p in predicates:
    predicatesList.append(p)

#build empty n*n*m matrix 
allData = zeros((size(predicatesList),size(resourcesList),size(resourcesList)))

#fill in allData to have 1's in every cell representing an existing triple
for s,p,o in graph:
    if("http" in o):
        allData[predicatesList.index(p),resourcesList.index(s),resourcesList.index(o)] = 1

#build single slices of the tensor
sliceCollection = list()
for i in range(len(predicatesList)):
    sliceCollection.append(csr_matrix(allData[i]))

#call rescal
A, R, fit, itr, exectimes = rescal.als(sliceCollection,2)

#collect rescal result for every slice
rescalResults = list()
for i in range(len(predicatesList)):
    rescalResults.append(A.dot(R[i]).dot(A.T))

#build new graph to put found triples
# for some reason namespace binding is not even needed
newGraph = Graph()


slicenumber=0
i=0
j=0

for slice in rescalResults:
    for line in slice:
        for element in line:
            if allData[slicenumber][i][j] != 1:
                if rescalResults[slicenumber][i][j] >= config.get("paths","threshhold"):
                    newGraph.add( (predicatesList[slicenumber],resourcesList[i],resourcesList[j]) )
            j = j+1
        j=0
        i = i+1
    slicenumber = slicenumber+1
    i=0

print newGraph.serialize(format='turtle')

