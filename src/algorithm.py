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
    
    nodeSize = adjlist.node_cardinality()
    matrix = [None]*nodeSize

    #Deepcopy as to make sure that no values are distorted
    tmpMatrix = copy.deepcopy(floyd(adjlist))
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

    q = []# *adjlist.node_cardinality() #Iniates list to use index
    s = []# * adjlist.node_cardinality() #Initiates list to use index

    loadAndInit(adjlist, q, start_node, d, e)

    #MAIN LOOP
    while len(q) != 0:
      q.sort(key=lambda node: node.info()[0])
      u = q.pop(0)
      s.append(u)
      #Hämta ut alla nodes som u har edges mot
      for edge in u.getListOfEdges(): #Gets all edges and loops through them with help of DST
        print(f"Running from node: {u.name()}")
        v = adjlist.getNode(edge.dst())    #Doesn't really improve bigO... but searches and finds correct node from graph
        relax(v, u, edge.weight()) #Alters v.key value if actual weight from u to v is lower



    # 1. Sortera S
    # 2. Sätt in rätt värde på rätt plats
    s.sort(key=lambda node: node.name())
    for index, node in enumerate(s):
      if node.info()[0] == 0:
        d[index] = None
        e[index] = None
      else:
        d[index] = node.info()[0]
        e[index] = node.info()[1]

    return d, e

def relax(v, u, weight):
  if v.info()[0] > u.info()[0] + weight:
    v.set_info([(u.info()[0] + weight), u.name()])

def loadAndInit(adjNode, targetList, start_node, distanceList, edgeList):
  targetList.extend(adjNode.getListOfNodes())
  for index, node in enumerate(targetList):
    print(node.name())
    distanceList[index] = None
    edgeList[index] = None
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
    vArr = [] #Contains all nodes in graph
    eArr = [] #Contains list with all actual edges that can be added in current tree

    #Add all nodevalues to list and initiates info as False
    for index, node in enumerate(adjlist.getListOfNodes()):
      tmpNode = AdjacencyList(node.name(), False)
      tmpNode.set_edges(node.edges())
      vArr.append(tmpNode)
      if vArr[index].name() == start_node:
        vArr[index].set_info(True) #Sets info to true to imply that start_node is member of MST
        eArr.extend(vArr[index].edges().list(vArr[index].name())) #Adds edges from startnode

      
    while len(eArr) != 0:  #Ändra till whileloop
      minEdgeIndex = extractMin(eArr) # Hämtar ut minsta edge bland tillagda
      minEdgeDST = eArr[extractMin(eArr)][1] #Gets dst of least value

      for index, node in enumerate(vArr):
        if node.name() == minEdgeDST and node.info() is False:
          node.set_info(True)
          l[vArr.index(node)] = eArr[minEdgeIndex][2] #Adds weight value to l array
          c[vArr.index(node)] = eArr[minEdgeIndex][0] #Adds parent name to c array
          eArr.extend(node.edges().list(node.name())) #Extends new edges from found node to eArr
          eArr.remove(eArr[minEdgeIndex]) #Removes edge from eArr

        elif node.name() == minEdgeDST and node.info() is True:
          eArr.remove(eArr[minEdgeIndex])
          #Ta bort edge


    #Kan ändra index vid lägg till l+c för att snygga till. Använd enumerate
    #Borde kunna fixa till init-loopen, fixa. Behöver inte använda tmp-värden
    return l, c



#Pre: Requires eList to not be empty, and be a 2d-list
#Post: Returns index in eList with lowest weight
def extractMin(eList):
  minVal = sys.maxsize
  smallest_index = -1
  for i in range(len(eList)):
    if eList[i][2] < minVal:
      minVal = eList[i][2]
      smallest_index = i
  
  return smallest_index


def cleanup(somelist):
  returnList = [y for y in somelist if y != inf]
  return returnList
      


if __name__ == "__main__":
    logging.critical("module contains no main")
    sys.exit(1)