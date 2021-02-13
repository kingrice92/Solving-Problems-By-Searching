#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 21:36:01 2021

@author: Neil Rice
"""
import pandas as pd 

class Graph():
    # This is a graph class that holds all of the required information given 
    # by the problem statement. This includes the list of nodes, edges, and 
    # start and end points.
    def __init__(self, filename):
        self.nodeList = []
        self.edgeList = []
        self.parseInputData(filename)
       
    def parseInputData(self, filename):
        # This is a function for extracting the required information from the
        # p1_graph.txt file and sorting it into th relevant data structures.
        
        # Create a pandas dataframe for the input data file
        df = pd.read_csv(filename, header=None, names=range(3))
        # Extract the node, edge, and endpoint data and sort them into tables.
        table_names = ['# Vertices', '# Edges', '# Source and Dest']
        groups = df[0].isin(table_names).cumsum()
        tables = {group.iloc[0,0]: group.iloc[1:] for i,group in df.groupby(groups)}

        # Clean up node and edge tables.
        nodes = tables['# Vertices']
        nodes = nodes.drop([2], axis=1)
        nodes = nodes.drop(nodes.index[0])
        nodes.columns = ['Vertex ID', 'Square ID']
        nodes = nodes.reset_index(drop=True)
        nodes['Vertex ID'] = nodes['Vertex ID'].astype('int')
        nodes['Square ID'] = nodes['Square ID'].astype('int')

        edges = tables['# Edges']
        edges = edges.drop(edges.index[0])
        edges.columns = ['From', 'To', 'Distance']
        edges = edges.reset_index(drop=True)
        edges['From'] = edges['From'].astype('int')
        edges['To'] = edges['To'].astype('int')
        edges['Distance'] = edges['Distance'].astype('int')

        endPoints = tables['# Source and Dest']
        
        # Use node and edge tables to assign attributes to the graph object.
        self.start = int(endPoints.iloc[0][1])
        self.destination = int(endPoints.iloc[1][1])
        self.getNodeList(nodes)
        self.getEdgeList(edges)
        
        
    def getNodeList(self, nodes):
        # Create Node objects for each vertex in the input file.
        for idx, row in nodes.iterrows():
            if row['Vertex ID'] == self.start:
                self.start = self.Node(row['Vertex ID'], row['Square ID'])
            elif row['Vertex ID'] == self.destination:
                self.destination = self.Node(row['Vertex ID'], row['Square ID'])
            
            self.nodeList.append(self.Node(row['Vertex ID'], row['Square ID']))
    
    def getEdgeList(self, edges):
        # Create Edge objects for each edge in the input file.
        for idx, row in edges.iterrows():
            
            findSource = True
            findDestination = True
            nodeCount = 0
            while findSource or findDestination:
                if self.nodeList[nodeCount].vertexID==row['From']:
                    source = self.nodeList[nodeCount]
                    findSource = False
                elif self.nodeList[nodeCount].vertexID==row['To']:
                    destination = self.nodeList[nodeCount]
                    findDestination = False
                    
                nodeCount = nodeCount + 1
                
            self.edgeList.append(self.Edge(source, destination, row['Distance']))
        
    class Node():
        # This is a node class for storing the vertex and square IDs of each 
        # node of the graph. 
        def __init__(self, vertexID, squareID):
            self.vertexID = vertexID
            self.squareID = squareID
        
    class Edge():
        # This is a edge class for storing the source and destination nodes, as
        # well as the distance between them for each edge in the graph.
        def __init__(self, source, destination, distance):
            self.source = source
            self.destination = destination
            self.distance = distance