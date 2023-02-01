# Use lib networkx and matplotlib to display graph

import networkx as nx
import matplotlib.pyplot as plt
from math import log2

# DOC :
# [LINK](https://networkx.org/documentation/stable/tutorial.html)


class Node:

    def __init__(self, ID, parent=None):
        """
        Node Object
        - ID : ID of the node
        - parent : Parent of the node in the Union Find Structure
        - ancestor : List of the ancestor in the Union Find as power of 2
            : [2^0 th = parent, 2^1 = parent of parent, 2^2, ...] while last element is the root of the tree
        """

        self.ID = ID
        if parent is None:
            self.parent = self
        else:
            self.parent = parent
        self.depth = 0

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

    def __eq__(self, obj):
        """
        Overriding the default Equals behavior
        Compare ID of Nodes
            - Doesn't compare parents (Union Find Structure)
        """

        return self.ID == obj.ID

# Define an Edge Class


class Edge():

    def __init__(self, a: Node, b: Node, weight=None, color=None):
        self.a = a
        self.b = b
        self.weight = weight
        self.color = color

    def __str__(self):
        return 'Edge : ' + str(self.a) + ' - ' + str(self.b) + ' | weight : ' + str(self.weight) + ' | color : ' + str(self.color)

    def __eq__(self, obj):
        """
        Overriding the default Equals behavior
        Compare ID of Nodes
            - if weights, also compares
            - Doesn't compare colors of edges

        Depends on the Node method __eq__
        """

        nodes_eq = (self.a == obj.a and self.b == obj.b) or (
            self.a == obj.b and self.b == obj.a)
        weights_eq = (self.weight == obj.weight) or (
            self.weight is None) or (obj.weight is None)
        # colors_eq = (self.color == obj.color) or (self.color == None) or (obj.color == None)

        return nodes_eq and weights_eq  # and colors_eq


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
    def addNode(self, nodeA: Node):
        """
        Add a sigle node to the graph
        """
        # Add node to the graph
        self.G.add_node(nodeA.ID)
        # Update Union Find Structure
        self.nodes.append(nodeA)

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a: Node, b: Node, weight=None, color=None):
        """
        Add an edge to the graph
        Create a new edge if not already exist
        Automatically add Nodes if necessary
        """

        # Add edge to the graph
        self.G.add_edge(a.ID, b.ID, weight=weight, color=color)

        # Add edge to the list
        self.edges.append(Edge(a, b, weight, color))

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

    # Return neighbors of a node
    def getNeighbors(self, nodeA: Node):
        """
        Gives the neighbors of a node


        ## Input :
        - Node object

        ## Output :
        - List of Node objects
        """
        L: list[Node] = []
        # Iter over all edges
        for edge in self.edges:
            if edge.a == nodeA:
                L.append(edge.b)
            elif edge.b == nodeA:
                L.append(edge.a)

        return L

    # Method to get the MST of the graph
    # TODO : Compute properly the MST with the Union Find Structure instead of updating it with BFS algorithm afterward...
    def Kruskal(self):
        """
        Return the MST of the graph

        ## Output :
        - GraphVisualization object : MST of the graph
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

    # DFS Algorithm
    def itineraries_v1(self, nodeA: Node, nodeB: Node):
        """
        Return the path between 2 nodes

        ## Input :
        - nodeA : Start Node
        - nodeB : End Node

        ## Output :
        - List of Node objects
        - Integer : Maximum weight of the path
        """

        # USE DFS ALGORITHM
        # ITERATIVE VERSION
        # PATH-TRACKING VERSION

        # Create a stack
        stack = []

        # Create a list of visited nodes
        visited = []

        # Add the start node to the stack
        stack.append(nodeA)

        nodeA.parent = nodeA

        while len(stack) > 0:
            # Current node
            node = stack.pop()

            # Add node to visited list
            visited.append(node)

            # check if node is the end node
            if node == nodeB:
                # compute path from nodeB to nodeA by reading parenting
                path = []
                max_weight = 0
                weight = 0
                while node != nodeA:
                    path.append(node.ID)
                    node = node.parent
                    # get weight of the edge between node and node.parent
                    if node.parent != node:
                        data = self.G.get_edge_data(node.ID, node.parent.ID)
                        weight = data['weight']
                    if weight > max_weight:
                        max_weight = weight
                path.append(nodeA.ID)
                path.reverse()
                return path, max_weight

            # Get neighbors of the node
            neighbors = self.getNeighbors(node)

            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbor.parent = node
                    stack.append(neighbor)

    def LCA(self, nodeA: Node, nodeB: Node):
        """
        Return the LCA (Lowest Common Ancestor) of 2 nodes

        ## Input :
        - nodeA : Start Node
        - nodeB : End Node

        ## Output :
        - Node object
        - Integer : Maximum weight of the path
        """

        max_weight = 0

        # if depthA > depthB, swap nodes
        if nodeA.depth > nodeB.depth:
            nodeA, nodeB = nodeB, nodeA

        # get the difference in depth
        diff = nodeB.depth - nodeA.depth

        # move the deeper node up the tree
        while diff > 0:

            # get weight of the edge between node and node.parent
            if nodeB.parent != nodeB:
                data = self.G.get_edge_data(nodeB.ID, nodeB.parent.ID)
                weight = data['weight']
                if weight > max_weight:
                    max_weight = weight

            nodeB = nodeB.parent
            diff -= 1

        # now both nodes are at the same depth
        # move both nodes up the tree until they are the same
        while nodeA != nodeB:

            # get weight of the edge between node and node.parent
            if nodeA.parent != nodeA:
                data = self.G.get_edge_data(nodeA.ID, nodeA.parent.ID)
                weight = data['weight']
                if weight > max_weight:
                    max_weight = weight

            if nodeB.parent != nodeB:
                data = self.G.get_edge_data(nodeB.ID, nodeB.parent.ID)
                weight = data['weight']
                if weight > max_weight:
                    max_weight = weight

            nodeA = nodeA.parent
            nodeB = nodeB.parent

        # return the LCA
        return nodeA, max_weight

    # Auxiliary function for LCA

    def ancestor(self, nodeA: Node, n: int):
        """
        Preprocessing : Compute the ancestor of each node at distance 2^n from nodeA
        Ancestor is the 2^n_th parent of the Node going up the tree
        If the distance is too long, the ancestor is the root of the tree

        ## Input :
        - nodeA : Start Node
        - n : Distance (as a power of 2) => distance = 2^n

        ## Output :
        - Node Object
        - maximum noise level of the path
        """
        # sparse matrix of ancestors
        # node.ancestor[n] = ancestor of node at distance 2^n

        pass

    def BFS(self, nodeA: Node):
        """
        Use BFS algorithm to compute the parenting of each node from the Tree
        Kruskal should have done it but it's not working properly...

        ## Input :
        - nodeA : Root of the tree

        ## Output :
        - Graph object
        """
        # Create a queue
        queue = []

        # Create a list of visited nodes
        visited = []

        # Add the start node to the queue
        queue.append(nodeA)

        nodeA.parent = nodeA

        while len(queue) > 0:
            # Current node
            node = queue.pop(0)

            # Add node to visited list
            visited.append(node)

            # Get neighbors of the node
            neighbors = self.getNeighbors(node)

            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbor.parent = node
                    neighbor.depth = node.depth + 1
                    queue.append(neighbor)

        # Update the ancestor list of each node according to the size of the tree
        for node in self.nodes:
            node.ancestor = [None] * int(log2(len(self.nodes)))


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
        Graph.addNode(Node(i + 1))

    # Add Edges
    for i in range(m):
        Node_a = int(entry[i][0])
        Node_b = int(entry[i][1])
        weight = int(entry[i][2])
        a = Graph.nodes[Node_a - 1]
        b = Graph.nodes[Node_b - 1]
        Graph.addEdge(a, b, weight)

    return Graph


def file2Querries(path):
    """
    Return List of querries from a file
    """
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

    # Remove from 1st line to m+1 as they are edges
    entry = entry[m + 1:]
    # Number of queries
    e = int(entry[0][0])
    entry.pop(0)
    # Get ID of Nodes
    entry = [list(map(int, i)) for i in entry]
    return (n, m, e, entry)

# Can't visualise graph 2 to 9 => too big, more than 100 000 Nodes...

# --- Display Both Graphs and MST ---


def compareGraphs(Graph, **kwargs):
    """
    ## Input :
    - Graph : GraphVisualization object
    - display_MST : Boolean (default False)
    - display_weights : Boolean (default False)
    - display_weights_MST : Boolean (default False)
    - same_pos : Boolean (default False)

    ## Output:
    - Visualize both the Graph and the Minimum Spanning Tree
    """

    # Get arguments
    display_MST = kwargs.get('display_MST', False)
    display_weights = kwargs.get('display_weights', False)
    display_weights_MST = kwargs.get('display_weights_MST', False)
    same_pos = kwargs.get('same_pos', False)

    if display_MST:
        # Create a new Graph visualization object corresponding to the MST of the Graph
        MST = Graph.Kruskal()

    # -- Caracteristics of the Graph --

    # Position of the nodes
    # get the position of the nodes once and for all

    pos = nx.spring_layout(Graph.G)

    # Edges of the Graph
    # weights

    edge_labels = {}
    if display_weights:
        edge_labels = nx.get_edge_attributes(Graph.G, 'weight')

    edge_labels_MST = {}
    if display_weights_MST:
        edge_labels_MST = nx.get_edge_attributes(MST.G, 'weight')

    # Visualize
    plt.figure(1)
    nx.draw_networkx(Graph.G, pos=pos)
    nx.draw_networkx_edge_labels(Graph.G, pos, edge_labels)

    if display_MST:
        plt.figure(2)
        if not (same_pos):
            pos = nx.spring_layout(MST.G)
        nx.draw_networkx(MST.G, node_color='r', edge_color='r', pos=pos)
        nx.draw_networkx_edge_labels(Graph.G, pos, edge_labels_MST)

    plt.show()

# --- GET INPUT ---


def getGraph():
    # RUN TEST on  ./tests/tests/itinerariesX.in
    # with X from 0 to 9
    path = 'tests/tests/itineraries.'
    ID = 1
    print('Open Graph  ' + str(ID))
    Graph = file2Graph(path + str(ID) + '.in')
    return Graph


def getQueries():
    # RUN TEST on  ./tests/tests/itinerariesX.in
    # with X from 0 to 9
    path = 'tests/tests/itineraries.'
    ID = 1
    print('Getting Queries From Test  ' + str(ID))
    queries = file2Querries(path + str(ID) + '.in')
    return queries
# --- Tests ---


def test1():
    E1 = Edge(Node(1), Node(2))
    E2 = Edge(Node(1), Node(2), 2)
    E3 = Edge(Node(2), Node(1))

    print(E1 == E2)
    print(E1 == E3)
    print(E2 == E3)


def test2(Graph):
    """
    Display MST
    """
    MST = Graph.Kruskal()
    print(MST.nodes[0].find())
    MST.visualize()


def test3(Graph):
    """
    Display Graph and MST
    """
    print("Display Graph and MST")
    compareGraphs(Graph, display_MST=True, display_weights=True,
                  display_weights_MST=True, same_pos=False)


def test4(Graph):
    print("Test Neighbors")
    nodeA = Graph.nodes[0]
    for element in Graph.getNeighbors(nodeA):
        print(element)


def test5(Graph):
    print("Test DFS")
    nodeA = Graph.nodes[0]
    nodeB = Graph.nodes[17]
    MST = Graph.Kruskal()
    pathway = MST.itineraries_v1(nodeA, nodeB)
    print(pathway)
    MST.visualize()


def test6(Graph, queries: list):

    print("Test Itineraries")
    queries = queries[3]
    MST = Graph.Kruskal()
    for query in queries:
        nodeA = Graph.nodes[query[0] - 1]
        nodeB = Graph.nodes[query[1] - 1]
        pathway = MST.itineraries_v1(nodeA, nodeB)
        print('Pathway from ', str(nodeA.ID),
              ' to ', str(nodeB.ID), ' : ', end='')
        print(pathway)


def test7(Graph):
    print("Test BFS")
    MST = Graph.Kruskal()
    nodeA = Graph.nodes[0]
    MST.BFS(nodeA)
    for node in MST.nodes:
        print(node, ' : Depth =', node.depth, ' : ', end='')
        pointeur = node
        for i in range(node.depth):
            pointeur = pointeur.parent
            print(pointeur, ', ', end=' ')
        print()
    MST.visualize()


def test8(Graph):
    print("LCA")
    MST = Graph.Kruskal()
    # Update the depth of the nodes
    MST.BFS(MST.nodes[0])
    for nodeA in MST.nodes:
        for nodeB in MST.nodes:
            common_ancestor = MST.LCA(nodeA, nodeB)
            print('Common Ancestor : ', nodeA, ' - ',
                  nodeB, ': ', common_ancestor[0], ' - ', common_ancestor[1])
    MST.visualize()


def test9(Graph):
    MST = Graph.Kruskal()
    MST.BFS(MST.nodes[0])
    nodeA = MST.nodes[18]
    nodeB = MST.nodes[12]
    common_ancestor = MST.LCA(nodeA, nodeB)
    print('Common Ancestor : ', nodeA, ' - ', nodeB, ': ', common_ancestor)


if __name__ == "__main__":

    G = getGraph()
    queries = getQueries()
    test8(G)
    G = getGraph()
    test6(G, queries)
    # test3(G)
