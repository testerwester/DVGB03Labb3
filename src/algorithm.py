#!/usr/bin/env python3

import sys
import logging

log = logging.getLogger(__name__)

from math import inf
from adjlist import AdjacencyList

def warshall(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Warshall's
    algorithm.

    Pre: adjlist is not empty.
    '''
    log.info("TODO: warshall()")
    return [[]]

def floyd(adjlist):
    '''
    Returns an NxN matrix that contains the result of running Floyd's algorithm.

    Pre: adjlist is not empty.
    '''
    log.info("TODO: floyd()")
    return [[]]

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
    d = []
    e = []

    q = []# *adjlist.node_cardinality() #Iniates list to use index
    s = []# * adjlist.node_cardinality() #Initiates list to use index
    
    #Get all nodes
    q.extend(adjlist.getListOfNodes())

    #Initiate nodes - can be moved to function 
    for node in q:
      node.set_info([inf, None])
      if node.name() == start_node:
        tmpNode = node
        tmpNode.set_info([0, None])

    #MAIN LOOP

    #Sort list and pop- can be moved to function
    while len(q) != 0:
      q.sort(key=lambda node: node.info()[0], reverse=False)
      for index, node in enumerate(q):
        print(f"{index}: {node.name()}")
      u = q.pop(0)
      s.append(u)
      print(f"Chosen node is: {u.name()}") #DEBUG
      print(u.info()[0])

      #Hämta ut alla nodes som u har edges mot
      # 1. Hämta alla edges
      for edge in u.getListOfEdges():
        print("Trying") #DEBUG
        print(adjlist.getNode(edge.dst()).name()) #Doesn't really improve bigO...
        v = adjlist.getNode(edge.dst())    #Doesn't really improve bigO...
        #RELAX
        if v.info()[0] > u.info()[0] + edge.weight():
          print("Changing values") #DEBUG
          v.set_info([(u.info()[0] + edge.weight()), u.name()])



    # 1. Sortera S
    # 2. Sätt in rätt värde på rätt plats
    s.sort(key=lambda node: node.name()[0], reverse=False)
    for index, node in enumerate(s):
      if node.info()[0] == 0:
        print(f"Setting None to node: {node.name()} at count {index}")
        d.insert(index, None)
        e.insert(index, None)
      else:
        d.insert(index, node.info()[0])
        e.insert(index, node.info()[1])

    print(d)
    print(e)

    return d, e

def addToSortedList(list, node):
  sortedList = list
  return sortedList

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