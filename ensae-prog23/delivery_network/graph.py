import graphviz
import sys

class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        sys.setrecursionlimit(max(self.nb_nodes*10, 1_000))
    

    def __str__(self): # complexity : O(nb_edges)
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items(): #je pense que c'est faux car
                output += f"{source}-->{destination}\n"
        return output
    
        
    def add_edge(self, node1, node2, power_min, dist=1): # complexity : O(1)
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        self.nb_edges += 1
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
    

    def get_path_with_power(self, src, dest, power): 
        # complexity : O(nb_nodes + nb_edges log(nb_edges)) in worst case
        # O(nb_nodes) in best case
        """
        We first search if src and dest are in the same connected_component 
        to restrain the set of node where we have to search 
        We can now lower the space complexity of power_dict and dist_dict
        """
        connected = self.connected_components_set()
        component = set()
        for elt in connected:
            if src in elt:
                if dest in elt:
                    component = elt
                    pass
                else:
                    return None

        power_dict = {node:None for node in component}
        power_dict[src] = 0
        path = {node:[] for node in component}
        path[src] = [src]
        dist_dict = {node:None for node in component}
        dist_dict[src] = 0
        pile = [(0, src)]
        while pile != []: # Djikstras on dist
            """in this part we use the Djikstra algorithm on the dist with the condition on power
            It is like removing all edges with too big power required
            """
            node_dist, node = min(pile)
            pile.remove((node_dist, node))
            if node == dest: # Test if reached dest
                return path[dest]
            for end_node in self.graph[node]:
                end_node, power_between, dist_between = end_node
                if power_between <= power: # Test if has enough power
                    if power_dict[end_node] is None or dist_between + dist_dict[node] < dist_dict[end_node]: # Test if found a better dist
                        power_dict[end_node] = max(power_between, power_dict[node])
                        dist_dict[end_node] = dist_between + dist_dict[node]
                        path[end_node] = path[node] + [end_node]
                        pile.append((dist_dict[end_node], end_node))
        return None
        
        
    def connected_components(self): # complexity : O(nb_node) everytime
        """Return all the connected components of a graph in a list of list (for example the function 
        executed on the graph generated by network.01 will return [[1,2,3], [4,5,6,7]])"""
        components_list = []
        node_visited = {node: False for node in self.nodes}
        
        def find_component(node): # complexity : O(nb_node) in the worst case (if the graph is conex)
            """Return all the accesible node from the input node as a list"""
            for end_node in self.graph[node]:
                end_node = end_node[0]
                if not node_visited[end_node]:
                    node_visited[end_node] = True
                    # changing it rather than returning the component prevent from stack overflow
                    # Segmentation fault (core dumped) for big graph
                    components_list[-1].append(end_node)
                    find_component(end_node)

        for node in self.nodes:
            if not node_visited[node]:
                components_list.append([node])
                find_component(node)
        
        return components_list



    def connected_components_set(self): # complexity : the same as connected_components()
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        # complexity : O(nb_nodes + nb_edges log(nb_edges)) in worst case O(nb_nodes) in best case
        """
        The indication in the instruction recommend to use 
        self.get_path_with_power with a dichotomy research thus doing it nlog(n) times ending with O(nlog(n)(nb_nodes + nb_edges log(nb_edges)))

        We think that modifying Djikstra with the condition 
            max(power_between, power_dict[node]) < power_dict[node]
            rather than dist_between + dist_dict[node] < dist_dict[end_node]
        can end up with the same result 

        And it will be better in complexity because executing Djikstra ending with O(nb_nodes + nb_edges log(nb_edges))
        """
        connected = self.connected_components_set()
        component = set()
        for elt in connected:
            if src in elt:
                if dest in elt:
                    component = elt
                    pass
                else:
                    return None

        power_dict = {node:None for node in component}
        power_dict[src] = 0
        path = {node:[] for node in component}
        path[src] = [src]
        pile = [(0, src)]
        while pile != []: # Djikstras on max power
            """in this part we use the principle of Djikstra algorithm
            """
            node_power, node = min(pile)
            pile.remove((node_power, node))
            if node == dest: # Test if reached dest
                return path[dest], node_power
            for end_node in self.graph[node]:
                end_node, power_between, _ = end_node
                if power_dict[end_node] is None or max(power_between, power_dict[node]) < power_dict[end_node]: # Test if found a better power
                    power_dict[end_node] = max(power_between, power_dict[node])
                    path[end_node] = path[node] + [end_node]
                    pile.append((power_dict[end_node], end_node))
                    
        return None, None

    def to_graphviz(self, comment="Graphe", view=True):
        dot = graphviz.Graph(comment=comment)
        for node in self.nodes:
            dot.node(f"{node}", str(node))
        for source, destinations in self.graph.items():
            for destination, power, dist in destinations:
                if source < destination:
                    # Le premier nombre est la puissance le deuxième est la distance
                    dot.edge(str(source), str(destination), label=f'{power}, {dist}')
        dot.render(filename=f'doctest-output/{comment}.gv', cleanup=True, view=view)

    def kruskal(self):
        root = {node:node for node in self.nodes}
        A = Graph(self.nodes)
        vertices_list = [] # this is a list of all the vertices
        already_added = {node:[] for node in self.nodes}
        for node1 in self.nodes:
            for node2, power, dist in self.graph[node1]:
                if node2 not in already_added[node1]: # making sure each vertices is only appears once
                    vertices_list.append((power, dist, node1, node2))
                    already_added[node1].append(node2)
                    already_added[node2].append(node1)
        vertices_list.sort() # we sort them

        def union(node1, node2):
            if node1 == root[node1]: # Merging this root to node2
                root[node1] = node2
                return node2
            if node2 == root[node2]: # Merging this root to node1
                root[node2] = node1
                return node1
            # searching for a root
            root_node = union(root[node1], root[node2])
            # making a compression
            root[node1] = root_node
            root[node2] = root_node
            return root_node
            
        def search(node):
            if node==root[node]:
                return node
            # making a compression
            root_node = search(root[node])
            root[node] = root_node
            return root_node

        visited_nodes = {node: False for node in self.nodes}
        nb_visited = 0
        i = 0
        while nb_visited < self.nb_nodes and i < len(vertices_list): # creating the tree
            power, dist, node1, node2 = vertices_list[i]
            i += 1
            if (search(node1) != search(node2)): # Otherwise it is a cycle
                A.add_edge(node1, node2, power, dist)
                union(node1, node2)
                if not visited_nodes[node1]:
                    visited_nodes[node1] = True
                    nb_visited += 1
                if not visited_nodes[node2]:
                    visited_nodes[node2] = True
                    nb_visited += 1
        return A



def graph_from_file(filename): # complexity : O(number of line)
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename) as file:
        def readline_to_listint():
            """
            Read the next line of file, and return this line as a list of integer
            
            Outputs: 
            -----------
            listint: list
                A list of integer [node1, node2, power_min, (dist)].
            """
            listline = file.readline().split()
            listint = [float(x) if '.' in x else int(x) for x in listline ]
            return listint

        n, m = readline_to_listint()
        nodes = [i for i in range(1, n+1)]
        G = Graph(nodes)
        for _ in range(m):
            args = readline_to_listint()
            G.add_edge(*args) 
            # Grace à l'étoilé, on prend en compte dist qui peut, ou non être présent
    return G


if __name__ == "__main__":
    g = graph_from_file("input/network.04.in")
    g.connected_components()
    g.graph
    g.get_path_with_power(1, 2, 10)
    g.to_graphviz()

