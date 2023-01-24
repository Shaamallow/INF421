# Use lib networkx and matplotlib to display graph 

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# DOC :
#[LINK](https://networkx.org/documentation/stable/tutorial.html)


# Define a Node Class for Union Find Structure
class Node:

    def __init__ (self, ID, parent=None):
        self.ID = ID
        if parent == None:
            self.parent = self
        else:
            self.parent = parent
    
    

    def find(self):
        if self.parent != self :
            self.parent = self.parent.find()

        return self.parent

    def union(self, node):
        root1 = self.find()
        root2 = node.find()
        root1.parent = root2
    
    def __str__(self):
        return 'Node ' + str(self.ID)

# Define a Graph Class for vizualisation 

class GraphVisualization:
   
    def __init__(self):
        # Graph Object from networkx
        self.G = nx.Graph()
          
        # List of edges
        self.edges = []

        # Union Find Structure for nodes
        self.nodes = []
          
    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a : Node, b : Node, weight=None, color= None):

        # Add edge to the graph
        self.G.add_edge(a.ID,b.ID)

        # Add edge to the list
        self.edges.append(Edge(a,b,weight,color))
    
        # Add 2 Nodes with no parenting
            # Check if the node already exist
        a_in = False
        b_in = False
        for node in self.nodes:
            if node.ID == a.ID:
                a_in = True
            if node.ID == b.ID:
                b_in = True

        if not a_in:
            self.nodes.append(a)
        if not b_in:
            self.nodes.append(b)
          
    # visualize function draws the graph with matplotlib
    def visualize(self):
        nx.draw_networkx(self.G)
        plt.show()

    # add a single Node to the graph and update Union Find Structure
    def addNode(self, node : Node):
        """
        Add a single node to the graph
        """

        self.G.add_node(node.ID)
        # Update Union Find Structure
        self.nodes.append(node)

    # Return all nodes of the graph
    def getNodes(self):
        """
        Return all nodes of the graph
        """
        return self.G.nodes()

    def getNeighbors(self, node : Node) :
        """
        Return all node neighbors of a node
        """
        res = []
        for x in self.edges :
            if x.a.ID == node.ID :
                res.append(x.b)
        return res

    def getEdge(self, a : Node, b : Node) :
        """
        Return the edge between a and b
        """
        for x in self.edges :
            if x.a.ID == a.ID and x.b.ID == b.ID or x.a.ID == b.ID and x.b.ID == a.ID :
                return x

    def getNode(self, Id) :
        """
        Return the node with the ID Id
        """
        for x in self.nodes :
            if x.ID == Id :
                return x






class Edge():

    def __init__(self, a : Node, b : Node, weight=None, color=None):
        self.a = a
        self.b = b
        self.weight = weight
        self.color = color

    def __str__(self):
        return 'Edge : ' + str(self.a) + ' - ' + str(self.b) + ' | weight : ' + str(self.weight) + ' | color : ' + str(self.color)

"""
# Driver code
Graph = GraphVisualization()
Graph.addEdge(0, 2)
Graph.addNode(5)
Graph.addNode(6)
Graph.addEdge(5, 6)
Graph.visualize()

print(Graph.getNodes())
for element in Graph.nodes:
    print(element)

for element in Graph.edges:
    print(element)

NodeA = Node(0)
NodeB = Node(1)
NodeC = Node(2)
NodeD = Node(3)

NodeA.union(NodeB)
print(NodeA.find().ID)
NodeB.union(NodeC)
NodeD.union(NodeC)

print(NodeB.find().ID)
print(NodeC.find().ID)
NodeC.union(NodeD)
print(NodeD.find().ID)
"""

def kruskal(graph):
    """
    Kruskal's algorithm
    """
    # Sort edges by weight
    li = sorted(graph.edges, key=lambda x: x.weight)
    # Initialize MST
    MST = GraphVisualization()
    # Iterate over edges
    for edge in li :
        # Check if the edge create a cycle
        if edge.a.find() != edge.b.find():
            # Add edge to the MST
            MST.addEdge(edge.a, edge.b, edge.weight, edge.color)
            # Update Union Find Structure
            edge.a.union(edge.b)
    return MST

def openGraph(file, color = None) :
    """
    Create a graph from a file
    """
    graph = GraphVisualization()
    
    f = open(file, 'r')
    j = 0
    for lines in f :
        if j == 0 :
            data = lines.split()
            n,m = int(data[0]), int(data[1])
            for i in range(n) :
                graph.addNode(Node(i+1))
        elif j <= m :
            data = lines.split()
            graph.addEdge(graph.nodes[int(data[0])-1], graph.nodes[int(data[1])-1], weight = int(data[2]), color = color)
        else :
            break
        j += 1
    f.close()
    return graph


(kruskal(openGraph(r'C:\Users\marti\Downloads\tests\tests\itineraries.0.in'))).visualize()

def task_v1(graph, u : Node, v : Node) :
    """
    Return the most pleasant path between u and v
    """
    if u == v :
        return [u]
    MST = kruskal(graph)
    # Find the path between u and v
    path = [[] for i in range(len(MST.nodes))]
    neighbors = []
    flag = False
    for n in MST.getNeighbors(u) :
        neighbors.append(n)
        path[n.ID-1].append(u)
        path[n.ID - 1].append(n)
    while not flag and len(neighbors) > 0 :
        nod = neighbors.pop(0)
        for n in MST.getNeighbors(nod) :
            if n not in path[nod.ID-1] :
                neighbors.append(n)
                path[n.ID-1] = path[nod.ID-1] + [n]
            if n == v :
                flag = True
                break
            
    return  path[v.ID-1] 


grap = openGraph(r'C:\Users\marti\Downloads\tests\tests\itineraries.0.in')
print([grap.nodes[i].ID for i in range(len(grap.nodes))])
it = task_v1(grap, grap.getNode(2), grap.getNode(9))
for i in it :
    print(i.ID)
r"""

def itineraries_v1(file, file_results) :
    graph = openGraph(file)
    tree = kruskal(graph)
    f = open(file, 'r')
    j = 0
    queries = []
    for lines in f :
        if j == 0 :
            data = lines.split()
            n,m = int(data[0]), int(data[1])
        j += 1
        if j > m + 2 :
            data = lines.split()
            queries.append((data[0], data[1]))
    f.close()

    res = open(file_results, 'w')
    for i in queries :
        print(i[0], i[1])
        print(tree.getNode(int(i[0])).ID, tree.getNode(int(i[1])).ID)
        answer = task_v1(tree, tree.getNode(int(i[0])), tree.getNode(int(i[1])))
        max = tree.getEdge(answer[0], answer[1]).weight
        for i in range(2, len(answer)) :
            max = max(max, tree.getEdge(answer[i-1], answer[i]).weight)
        res.write(str(max) + '\n')
    res.close()

itineraries_v1(r'C:\Users\marti\Downloads\tests\tests\itineraries.0.in', r'C:\Users\marti\Documents\travail\.X\projet info\itineraries.out.txt)')

        
        
"""