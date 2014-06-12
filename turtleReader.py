import logging
from rdflib import Graph
from scipy.sparse import *
from scipy import *
import imp
import ConfigParser

"""
Turtle reader to parse a turtle file into a
n*n*m Matrix where 
n = number of distinct resources
m = number of predicates
to use the rescal algorithm for computing the tensor factorization
on the m n*n slices

todo: implement a threshhold function and and turtle return for possible new triples
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
#print allData

#fill in allData to have 1's in every cell representing an existing triple
for s,p,o in graph:
    if("http" in o):
        allData[predicatesList.index(p),resourcesList.index(s),resourcesList.index(o)] = 1

print allData

#build single slices of the tensor
sliceCollection = list()
for i in range(len(predicatesList)):
    sliceCollection.append(csr_matrix(allData[i]))

#call rescal
A, R, fit, itr, exectimes = rescal.als(sliceCollection,2)
print R
print A
print fit
print itr
