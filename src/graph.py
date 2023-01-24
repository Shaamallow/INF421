# Use lib networkx and matplotlib to display graph 

import networkx as nx
import matplotlib.pyplot as plt
import os 

# DOC :
#[LINK](https://networkx.org/documentation/stable/tutorial.html)


class Node:

    def __init__ (self, ID, parent=None):
        self.ID = ID
        if parent == None:
            self.parent = self
        else:
            self.parent = parent
    
    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()

        return self.parent

    def union(self, node):
        root1 = self.find()
        root2 = node.find()
        root1.parent = root2
    
    def __str__(self):
        return 'Node ' + str(self.ID)

# Define an Edge Class 
class Edge():

    def __init__(self, a : Node, b : Node, weight=None, color=None):
        self.a = a
        self.b = b
        self.weight = weight
        self.color = color

    def __str__(self):
        return 'Edge : ' + str(self.a) + ' - ' + str(self.b) + ' | weight : ' + str(self.weight) + ' | color : ' + str(self.color)

  
# Define a Graph Class for vizualisation 
class GraphVisualization:
   
    def __init__(self):
        # Graph Object from networkx
        self.G = nx.Graph()
          
        # List of edges
        self.edges = []

        # Union Find Structure for nodes
        self.nodes = []

    # add a single Node to the graph and update Union Find Structure
    def addNode(self, nodeA : Node):
        """
        Add a sigle node to the graph
        """
        # Add node to the graph
        self.G.add_node(nodeA.ID)
        # Update Union Find Structure
        self.nodes.append(nodeA)
          
    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a : Node, b : Node, weight=None, color= None):
        """
        Add an edge to the graph
        Create a new edge if not already exist
        Automatically add Nodes if necessary
        """

        # Add edge to the graph
        self.G.add_edge(a.ID,b.ID)

        # Add edge to the list
        self.edges.append(Edge(a,b,weight,color))
    
        # Add 2 Nodes with no parenting
            # Check if the node already exist

        # REMOVE AUTO ADDING NODES TO GRAPH => Too long to compute
        # ADD NODES TO GRAPH BEFORE ADDING EDGES
        """ a_in = False
        b_in = False
        i = 0
        for node in self.nodes:

            print(str(i) + '/' + str(len(self.nodes)))

            if node.ID == a.ID:
                a_in = True
            if node.ID == b.ID:
                b_in = True
            i+=1

        if not a_in:
            self.nodes.append(a)
        if not b_in:
            self.nodes.append(b) """
          
    # visualize function draws the graph with matplotlib
    def visualize(self):
        nx.draw_networkx(self.G)
        plt.show()

    # Return all nodes of the graph
    def getNodes(self):
        """
        Return all nodes of the graph
        """
        return self.G.nodes()

    # Method to get the MST of the graph
    def Kruskal(self):
        """
        Return the MST of the graph
        """
        
        # Sort edges by weight
        self.edges.sort(key=lambda x: x.weight)

        # Create a new Graph
        MST = GraphVisualization()

        # Add Nodes
        for node in self.nodes:
            MST.addNode(node)

        # Add Edges
        for edge in self.edges:
            if edge.a.find() != edge.b.find():
                MST.addEdge(edge.a, edge.b, edge.weight, edge.color)
                edge.a.union(edge.b)

        return MST

# --- Open File and create Graph ---

def file2Graph(path):
    """
    Return a graph from a file
    """

    # Open test file 
    file = open(path, 'r')
    lines = file.readlines()

    entry = []
    for line in lines:
        entry.append(line.strip().split())

    # Close file
    file.close()

    # Get Number of Nodes and Edges (n,m)
    n = int(entry[0][0])
    m = int(entry[0][1])

    # remove first line
    entry.pop(0)

    # Create Graph
    Graph = GraphVisualization()

    # Add Nodes
    for i in range(n):
        Graph.addNode(Node(i+1))

    # Add Edges
    for i in range(m):
        Node_a = int(entry[i][0])
        Node_b = int(entry[i][1])
        weight = int(entry[i][2])
        a = Graph.nodes[Node_a-1]
        b = Graph.nodes[Node_b-1]
        Graph.addEdge(a,b,weight)

    return Graph

# RUN TEST on  ./tests/tests/itinerariesX.in
# with X from 0 to 9
path = 'tests/tests/itineraries.'

ID = 4
print('Test ' + str(ID))
Graph = file2Graph(path + str(ID) + '.in')
#Graph.visualize()
MST = Graph.Kruskal()
MST.visualize()

# Can't visualise graph 2 to 9 => too big, more than 100 000 Nodes...