#!/usr/bin/env python3

import sys
import logging

log = logging.getLogger(__name__)

from math import inf
import copy #For use of copy/deepcopy
from adjlist import AdjacencyList
from math import inf

def warshall(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Warshall's
    algorithm.

    Pre: adjlist is not empty.
    '''
    nodeSize = adjlist.node_cardinality() #Number of nodes
    matrix = [[None]*nodeSize]*nodeSize #Matrix for end result
    tmpMatrix = copy.deepcopy(adjlist.adjacency_matrix()) #Temporary matrix for calculations of algorithm

    #Warshall
    for k in range(nodeSize):
      for i in range(nodeSize):
        if k == i:
          tmpMatrix[k][i] = 0
        for j in range(nodeSize):
          tmpMatrix[i][j] = min(tmpMatrix[i][j], (tmpMatrix[i][k] + tmpMatrix[k][j]))

    #Swaps int/inf to True/False
    for i in range(nodeSize):
      matrix[i] = [False if x == inf else True for x in tmpMatrix[i]]

    return matrix


def floyd(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Floyd's algorithm.

    Pre: adjlist is not empty.
    '''

    nodeSize = adjlist.node_cardinality()
    matrix = adjlist.adjacency_matrix() #Initiates matrix with adjecency matrix

    #Deepcopy as to make sure that no values are distorted
    tmpMatrix = copy.deepcopy(matrix)

    for k in range(nodeSize):
      for i in range(nodeSize):
        if k == i:
          tmpMatrix[k][i] = 0
        for j in range(nodeSize):
          tmpMatrix[i][j] = min(tmpMatrix[i][j], (tmpMatrix[i][k] + tmpMatrix[k][j]))
          


    return tmpMatrix

def dijkstra(adjlist, start_node):
    '''
    Returns the result of running Dijkstra's algorithm as two N-length lists:
    1) distance d: here, d[i] contains the minimal cost to go from the node
    named `start_node` to the i:th node in the adjacency list.
    2) edges e: here, e[i] contains the node name that the i:th node's shortest
    path originated from.

    If the index i refers to the start node, set the associated values to None.

    Pre: start_node is a member of adjlist.

    === Example ===
    Suppose that we have the following adjacency matrix:

      a b c
    -+-----
    a|* 1 2
    b|* * 2
    c|* * *

    For start node "a", the expected output would then be:

    d: [ None, 1, 2]
    e: [ None, 'a', 'a' ]
    '''
    d = [None] * adjlist.node_cardinality()
    e = [None] * adjlist.node_cardinality()

    q = []# tmp queue to sort and pick node for loop
    s = []# Values that pop from q are added here to contain order of nodes and replicated for d and e

    #Initates values
    loadAndInit(adjlist, q, start_node)

    #MAIN LOOP
    while len(q) != 0:
      q.sort(key=lambda node: node.info()[0])
      u = q.pop(0)

      s.append(u)
      #Fetches all edges from current node - Tries to relax them if v has not been visited
      for edge in u.getListOfEdges(): #Gets all edges and loops through them with help of DST
        v = adjlist.getNode(edge.dst())    #Doesn't really improve bigO... but searches and finds correct node from graph
        #Relaxes edge if v is not visited
        if v in q: 
          relax(v, u, edge.weight()) #Alters v.key value if actual weight from u to v is lower


    #Based on s array, sets values on correct spot in d and e arrays.
    s.sort(key=lambda node: node.name())
    for index, node in enumerate(s):
      if node.info()[0] == 0: #Special case for startnode
        d[index] = None
        e[index] = None
      else:
        d[index] = node.info()[0]
        e[index] = node.info()[1]

    return d, e

#Relax function that compares an edge dst info with (src info + weight) - Swaps values if src combination is lower
def relax(v, u, weight):
  '''
  Pre: v and u are nodes and weight is an integer
  Post: Alters info of v if (u.info + weight) is lower can current v.info
  '''
  if v.info()[0] > u.info()[0] + weight:
    v.set_info([(u.info()[0] + weight), u.name()])


#Initation function for algorithms that use an array of nodes

def loadAndInit(adjNode, targetList, start_node):
  '''
  Pre: adjNode = root to graph, targetList = list of nodes, start_node = value of startnode
  Post: targetList is an array of all nodes in graph, start_node in array has special value of 0 instead of inf for startnode detection
  Post: All nodes in array have info updates with correct values
  '''
  targetList.extend(adjNode.getListOfNodes())
  for node in (targetList):
    if node.name() == start_node:
      node.set_info([0, None, None])
    else:
      node.set_info([inf, None, None])

def prim(adjlist, start_node):
    '''
    Returns the result of running Prim's algorithm as two N-length lists:
    1) lowcost l: here, l[i] contains the weight of the cheapest edge to connect
    the i:th node to the minimal spanning tree that started at `start_node`.
    2) closest c: here, c[i] contains the node name that the i:th node's
    cheapest edge orignated from. 

    If the index i refers to the start node, set the associated values to None.

    Pre: adjlist is setup as an undirected graph and start_node is a member.

    === Example ===
    Suppose that we have the following adjacency matrix:

      a b c
    -+-----
    a|* 1 3
    b|1 * 1
    c|3 1 *

    For start node "a", the expected output would then be:

    l: [ None, 1, 1]
    c: [ None, 'a', 'b' ]
    '''
    l = [None] * adjlist.node_cardinality() #Lowcost, weights
    c = [None] * adjlist.node_cardinality() #Closest, parents
    q = [] #Tmpqueue to hold nodes

    #Inits all arrays and values with None, 0 and Inf etc
    loadAndInit(adjlist, q, start_node)

    while len(q) != 0:
      q.sort(key=lambda node: node.info()[0]) #Sorts to pop the node with the smalles key
      u = q.pop(0)
      for edge in (u.getListOfEdges()):
        dstNode = adjlist.getNode(edge.dst()) #Gets real node based on edge.dst
        if dstNode in q and edge.weight() < dstNode.info()[0]:
          dstNode.set_info([edge.weight(), u.name()]) #Sets new values if dstNode is contained in q and the key is lager than weight

    #Adds values from node.info to correct place in l and c
    for index, node in enumerate(adjlist.getListOfNodes()):
      if node.info()[0] == 0:
        l[index] = None
        c[index] = None
      else:
        l[index] = node.info()[0]
        c[index] = node.info()[1]

    return l, c



if __name__ == "__main__":
    logging.critical("module contains no main")
    sys.exit(1)