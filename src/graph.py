# Use lib networkx and matplotlib to display graph 

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# DOC :
#[LINK](https://networkx.org/documentation/stable/tutorial.html)
  
# Define a Graph Class for vizualisation 

class GraphVisualization:
   
    def __init__(self):
          
        # visual is a list which stores all 
        # the set of edges that constitutes a
        # graph
        self.visual = []
          
    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b, weight) :
        self.visual.append(a, b , 'weight' = weight)
          
    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
  
# Driver code
G = GraphVisualization()
G.addEdge(0, 2, 1)
G.addEdge(1, 2, 1)
G.addEdge(1, 3, 3)
G.addEdge(5, 3, 3)
G.addEdge(3, 4, 2)
G.addEdge(1, 0, 5)
G.visualize()

set = [i for i in range(G.number_of_nodes())]

def union(a, b):
    x = find(a)
    y = find(b)
    set[y] = x

def find(a) :
    if set[a] == a:
        return a
    else:
        set[a] = find(set[a])
        return set[a]

def minimum_spanning_tree(G):
    edges = sorted(G.edges(), key = lambda x: x['weight'])
    res = []
    n = 0
    for e in edges :
        if find(e[0]) != find(e[1]) :
            union(e[0], e[1])
            res.append(e)
            n+=1
        elif n > G.number_of_nodes() :
            break
    return res