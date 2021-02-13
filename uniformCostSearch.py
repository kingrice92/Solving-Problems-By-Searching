#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 21:57:08 2021

@author: Neil Rice
"""
import graph as g
import queue as q

def uniformCostSearch(graph):
    # This is the Uniform-cost search. In this algorithm, nodes are evaluated 
    # based on the lowest path cost.
    
    # Initialize priority queue (frontier). Will be ordered by path cost (g).
    pq = q.PriorityQueue()
    
    # Add starting node to the priority queue.
    pq.put((0,graph.start.vertexID))
    
    # Empty set for storing explored nodes.
    explored = set()
    
    # Initialize variable to keep track of the size of the priority queue.
    maxQ = 0
    
    # As long as there are nodes in the priority queue, keep exploring.
    while pq:
        
        # Update the max queue variable as the queue grows.
        if len(pq.queue) > maxQ:
            maxQ = len(pq.queue)
            
        # Remove and return the node with the lowest path cost (g) from the queue.
        pathCost, node = pq.get()
        if node not in explored:
            explored.add(node)
            
            # Once the node returned from the priority queue matches the goal
            # destination node of the search problem, the search is complete.
            if node == graph.destination.vertexID:
                # Print the results of the algorithm to the console.
                print('Shortest path: ' + str(pathCost))
                print('Nodes explored: ' + str(explored))
                print('Number of nodes explored: ' + str(len(explored)))
                print('Maximum queue size: ' + str(maxQ))
                return
            
            for iNode in range(len(graph.edgeList)):
                # Since the edge objects are defined in terms of source node, 
                # destination node, and distance, and all edges are only defined 
                # once, we must account for that with the following if/elif statement. 
                 
                if (graph.edgeList[iNode].source.vertexID==node and 
                    graph.edgeList[iNode].destination.vertexID not in explored):
                    # If the present node matches a source node in edgeList, 
                    # and the destination node for that same edge object has not 
                    # yet been explored, add the destination node and its path-cost
                    # to the priority queue.
                    nextVertex = graph.edgeList[iNode].destination.vertexID
                    newPathCost = pathCost + graph.edgeList[iNode].distance
                    pq.put((newPathCost, nextVertex))
                    
                elif (graph.edgeList[iNode].destination.vertexID==node and 
                      graph.edgeList[iNode].source.vertexID not in explored):
                    # If the present node matches a destination node in edgeList, 
                    # and the source node for that same edge object has not 
                    # yet been explored, add the source node and its path-cost
                    # to the priority queue.
                    nextVertex = graph.edgeList[iNode].source.vertexID
                    newPathCost = pathCost + graph.edgeList[iNode].distance
                    pq.put((newPathCost, nextVertex))
                         
if __name__ == '__main__':
    
    path = 'p1_graph.txt'
    G = g.Graph(path)
    uniformCostSearch(G)