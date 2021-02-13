#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 21:35:44 2021

@author: Neil Rice
"""
import graph as g
import queue as q
import math as m

def calculateHeuristicFunction(nextLocation, destinationLocation):
    # This is the heuristic function that is used in the A* algorithm. 
    # This heuristic (h) approximates the euclidean distance between a node and 
    # the goal node. Since this is the straight-line distance between the two 
    # nodes, it cannot be an overestimate and therefore is an admissable 
    # heuristic. Additionally, this heuristic also satisfies the triangle 
    # inequality, and therefore it is consistent as well.
   
    # Convert the square IDs of the two nodes into strings so that the row and 
    # column indices can be easily determined.
    nextLocation = str(nextLocation)
    destinationLocation = str(destinationLocation)
    
    # If the location strings (square IDs) have only one character, its square 
    # ID belongs to the first row of the 10x10 square grid.
    if len(nextLocation) > 1:
        # Otherwise, the first character gives the column number and the 
        # second character gives the row number.
        nodeColumn = int(nextLocation[1])
        nodeRow = int(nextLocation[0])
    else: 
        nodeColumn = int(nextLocation)
        nodeRow = 0
    
    if len(destinationLocation) > 1:
        destinationColumn = int(destinationLocation[1])
        destinationRow = int(destinationLocation[0])
    else: 
        destinationColumn = int(destinationLocation)
        destinationRow = 0
    
    # The nodes of the graph are located inside 100x100 size unit squares. 
    # Therefore, the difference in row and column numbers need to be multiplied 
    # by 100 to get the x and y distances between the nodes. Furthermore, an 
    # additional space is subtracted to account for the fact that two vertices 
    # in adjacent squares can be arbitrarily close to each other. Thus the
    # heuristic provided is a lower bound on the cost to reach the destination.
    if not abs(destinationRow - nodeRow) == 0:
        yDistance = (abs(destinationRow - nodeRow) - 1)*100
    else:
        yDistance = 0
                
    if not abs(destinationColumn - nodeColumn) == 0:
        xDistance = (abs(destinationColumn - nodeColumn) - 1)*100
    else:
        xDistance = 0
    
    # Get the distance between the nodes by using the pythagorean theorem.
    estimatedDistance = m.sqrt(xDistance**2 + yDistance**2)
    return estimatedDistance

def aStarSearch(graph):
    # This is the A* search algorithm. A node (n) is evaluated by combining 
    # the cost to reach the node (g) and the cost to reach the goal from the 
    # node (h): f(n) = g(n) + h(n). The result is the estimated cost of the 
    # cheapest solution through n.
    
    # Initialize priority queue (frontier). This will be ordered by estimated cost (f).
    pq = q.PriorityQueue()
    
    # Add starting node to the priority queue.
    pq.put((0,0,graph.start.vertexID))
    
    # Empty set for storing explored nodes.
    explored = set()
    
    # Set a variable for the destination location.
    destinationLocation = graph.destination.squareID
    
    # Initialize variable to keep track of the size of the priority queue.
    maxQ = 0
    
    # As long as there are nodes in the priority queue, keep exploring.
    while pq:
       
        # Update the max queue variable as the queue grows.
        if len(pq.queue) > maxQ:
            maxQ = len(pq.queue)
            
        # Remove and return the node with the lowest etimated cost (f) from the queue.
        estimatedCost, costSoFar, node = pq.get()
        if node not in explored:
            explored.add(node)
            # Once the node returned from the priority queue matches the goal
            # destination node of the search problem, the search is complete.
            if node == graph.destination.vertexID:
                # Print the results of the algorithm to the console.
                print('Shortest path: ' + str(costSoFar))
                print('Nodes explored: ' + str(explored))
                print('Number of nodes explored: ' + str(len(explored)))
                print('Maximum queue size: ' + str(maxQ))
                return
            
            for iNode in range(len(graph.edgeList)):
                # Since the edge objects are defined in terms of source node, 
                # destination node, and distance, and all edges are only defined 
                # once, we must account for that with the following if/elif statement. 
                
                if (graph.edgeList[iNode].source.vertexID == node and 
                    graph.edgeList[iNode].destination.vertexID not in explored):
                    # If the present node matches a source node in edgeList, 
                    # and the destination node for that same edge object has not 
                    # yet been explored, add the destination node, its path cost, 
                    # and the estimated cost to reach the final destination node
                    # to the priority queue.
                    newPathCost = costSoFar + graph.edgeList[iNode].distance
                    nextVertex = graph.edgeList[iNode].destination.vertexID
                    nextLocation = graph.edgeList[iNode].destination.squareID
                    
                    estimatedDistance = calculateHeuristicFunction(nextLocation, 
                        destinationLocation)
                    
                    newEstimatedCost = newPathCost + estimatedDistance
                    pq.put((newEstimatedCost, newPathCost, nextVertex))
                    
                elif (graph.edgeList[iNode].destination.vertexID == node and 
                          graph.edgeList[iNode].source.vertexID not in explored):
                    
                    # If the present node matches a destination node in edgeList, 
                    # and the source node for that same edge object has not 
                    # yet been explored, add the source node, its path cost, 
                    # and the estimated cost to reach the final destination node
                    # to the priority queue.
                    newPathCost = costSoFar + graph.edgeList[iNode].distance
                    nextVertex = graph.edgeList[iNode].source.vertexID
                    nextLocation = graph.edgeList[iNode].source.squareID
                    estimatedDistance = calculateHeuristicFunction(nextLocation, 
                        destinationLocation)
                    
                    newEstimatedCost = newPathCost + estimatedDistance
                    pq.put((newEstimatedCost, newPathCost, nextVertex))
                                
if __name__ == '__main__':
    
    path = 'p1_graph.txt'
    G = g.Graph(path)
    aStarSearch(G)