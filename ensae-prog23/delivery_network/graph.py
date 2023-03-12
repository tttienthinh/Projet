import graphviz
from math import log2


# in the following, we refer to the complexity found here for the use of basic functions : https://www.python.org
class Graph:
    def __init__(self, nodes=[]):  # complexity : O(len(nodes))
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.tree = None
        self.power_2puiss = None

    def __str__(self):  # complexity : O(nb_edges)
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def add_edge(self, node1, node2, power_min, dist=1):  # complexity : O(1)
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
        """
        complexité à vérifier
        """
        # complexity : O(nb_edges log(nb_edges) + nb_node)
        power_dict = {node: None for node in self.nodes}
        power_dict[src] = 0
        path = {node: [] for node in self.nodes}
        path[src] = [src]
        dist_dict = {node: None for node in self.nodes}
        dist_dict[src] = 0
        pile = [(0, src)]
        while pile:  # Djikstras on dist
            """in this part we use the Djikstra algorithm on the dist with the condition on power
            It is like removing all edges with too big power required
            """
            node_dist, node = min(pile)
            pile.remove((node_dist, node))
            if node == dest:  # Test if reached dest
                return path[dest]
            for end_node in self.graph[node]:
                end_node, power_between, dist_between = end_node
                if power_between <= power:  # Test if has enough power
                    if power_dict[end_node] is None or dist_between + dist_dict[node] < dist_dict[
                        end_node]:  # Test if found a better dist
                        power_dict[end_node] = max(power_between, power_dict[node])
                        dist_dict[end_node] = dist_between + dist_dict[node]
                        path[end_node] = path[node] + [end_node]
                        pile.append((dist_dict[end_node], end_node))
        return None

    def connected_components(self):  # complexity : O(nb_edges) everytime
        """Return all the connected components of a graph in a list of list (for example the function 
        executed on the graph generated by network.01 will return [[1,2,3], [4,5,6,7]])"""
        components_list = []
        node_visited = {node: False for node in self.nodes}

        def find_component(node):  # complexity : O(nb_node^2) in the worst case (if the graph is full)
            # O(1) in the best case (if the node is not connected to anny other node)
            """Return all the accessible node from the input node as a list"""
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

    def connected_components_set(self):  # complexity : the same as connected_components()
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(maap(frozenset, self.connected_components()))

    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        # complexity : à vérifier
        """
        The indication in the instruction recommend to use 
        self.get_path_with_power with a dichotomy research thus doing it nlog(n) times ending with O(nlog(n)(nb_edges log(nb_edges)))

        We think that modifying Djikstra with the condition 
            max(power_between, power_dict[node]) < power_dict[node]
            rather than dist_between + dist_dict[node] < dist_dict[end_node]
        can end up with the same result 

        And it will be better in complexity because executing Djikstra ending with O(nb_edges log(nb_edges))
        """
        power_dict = {node: None for node in self.nodes}
        power_dict[src] = 0
        path = {node: [] for node in self.nodes}
        path[src] = [src]
        pile = [(0, src)]
        while pile != []:  # Djikstras on max power
            """in this part we use the principle of Djikstra algorithm
            """
            node_power, node = min(pile)
            pile.remove((node_power, node))
            if node == dest:  # Test if reached dest
                return path[dest], node_power
            for end_node in self.graph[node]:
                end_node, power_between, _ = end_node
                if power_dict[end_node] is None or max(power_between, power_dict[node]) < power_dict[
                    end_node]:  # Test if found a better power
                    power_dict[end_node] = max(power_between, power_dict[node])
                    path[end_node] = path[node] + [end_node]
                    pile.append((power_dict[end_node], end_node))

        return None, None

    def to_graphviz(self, comment="Graphe", view=True):  # we do not calculate the complexity because we did'nt find the
        # complexity of graphviz functions
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
        """
        The complexity is O(nb_edges * (log(nb_edges) + nb_nodes))
        """
        A = Graph(self.nodes)
        vertices_list = []  # this is a list of all the vertices
        already_added = {node: [] for node in self.nodes}
        for node1 in self.nodes:
            for node2, power, dist in self.graph[node1]:
                if (node2, power, dist) not in already_added[node1]:  # making sure each vertices is only appears once
                    vertices_list.append((power, dist, node1, node2))
                    already_added[node1].append((node2, power, dist))
                    already_added[node2].append((node1, power, dist))
        vertices_list.sort()  # we sort them O(nb_edges * log(n_edges))

        root = {node: node for node in self.nodes} # represent the union find
        def union(node1, node2):  # In the very worst case O(nb_nodes)
            # making a compression
            root[find(node1)] = find(node2)

        def find(node):  # In the very worst case O(nb_nodes)
            if node != root[node]:
                root[node] = find(root[node]) # making a compression
            return root[node]

        i = 0
        while A.nb_edges < self.nb_nodes-1 and i < len(vertices_list):  # creating the tree in the worst case repeating
            # nb_edges
            power, dist, node1, node2 = vertices_list[i]
            i += 1
            if (find(node1) != find(node2)):  # Otherwise, it is a cycle
                A.add_edge(node1, node2, power, dist)
                union(node1, node2)
        return A

    def oriented_tree(self):
        """
        The complexity is O(nb_nodes) we are visiting every nodes only once
        """
        # This function can only be applied to trees (You can execute kruskal before executing this one)

        # We will choose the root of our tree as the node with the greatest number of neighbour
        root = self.nodes[0]
        max_neighbour = len(self.graph[root])
        for node in self.nodes[1:]:
            if len(self.graph[root]) > max_neighbour:
                root = node
                max_neighbour = len(self.graph[node])

        # defining the unique tree from root
        self.tree = {node: (node, 0, 0) for node in self.nodes}
        self.power_2puiss = {node: [] for node in self.nodes}

        def tree(ancestor, node, level):
            for child in self.graph[node]:
                child, power_min, dist = child
                if child != ancestor[-2]:
                    power = power_min
                    for i in range(int(log2(level))):
                        dist = int(2**i)
                        ancestor_dist = ancestor[-dist]
                        self.power_2puiss[child].append((ancestor_dist, power))
                        power = max(power, self.power_2puiss[ancestor_dist][i][1])
                    dist = int(2**int(log2(level)))
                    self.power_2puiss[child].append((ancestor[-dist], power))
                    # the father of the child and the level to reach root
                    self.tree[child] = (node, level, power_min)
                    tree(ancestor+[child], child, level + 1)
        tree([None, root], root, 1)

    # execute it only on a tree or the algorithm won't finish
    # this function allow to compute the height of each node given a root, it's a simple graph recursive exploration
    # it also return a dict with the father of each node and the power min of the edges linking theim,
    # the dict need to be initialized with the value of root at None
    def calc_height_tree(self, root, ancestor=None, rank=0, dict=False):  # complexity : O(nb_node)
        if len(self.graph[root]) == 1 and rank != 0:
            return {root: rank}, dict
        else:
            result = {root: rank}
            for suc in self.graph[root]:
                if suc[0] != ancestor:
                    if dict:
                        dict[suc[0]] = [(root, suc[1])]
                    result.update(self.calc_height_tree(suc[0], rank=rank + 1, ancestor=root, dict=dict)[0])
        return result, dict

    # given a tree and a dict that contain the father of each node and the power of the edge linking theim,
    # it compute the minimal power necessary to go from each node to all its 2**i predecessor
    def calc_pred_log(self, dist):
        modifying = True
        i = 0
        while modifying:
            modifying = False
            for keys in dist.keys():
                if len(dist[keys]) >= i+1:
                    departure = dist[keys][i]
                    if departure is not None:
                        intermediary = dist[departure][i][0]
                        if len(dist[intermediary]) >= i+1:
                            if dist[intermediary][i] is not None:
                                dist[keys].append((dist[intermediary][0], max(dist[intermediary][0], departure[1])))
                                modifying = True
                        else:
                            dist[keys].append(None)




    def kruskal_min_power(self, src, dest):
        """
        The complexity in the worst case is O(nb_nodes)
        But if we have choosen the best root in self.oriented_tree() it can be O(log(nb_nodes)) in average
        """
        # This fonction can only be applied to trees (You can execute kruskal before executing this one)
        if self.tree is None:
            self.oriented_tree()

        # We will go from src and dest to root
        def goto_root(node1, node2):  # node1 = src, node2 = dest
            dad1, level1, power1 = self.tree[node1]
            dad2, level2, power2 = self.tree[node2]
            if level1 == level2:
                if node1 == node2:
                    return [node1, node2], 0
                path, power3 = goto_root(dad1, dad2)
                return [node1] + path + [node2], max(power1, power2, power3)
            if level1 > level2:
                path, power3 = goto_root(dad1, node2)
                return [node1] + path, max(power1, power3)
            if level1 < level2:
                path, power3 = goto_root(node1, dad2)
                return path + [node2], max(power2, power3)
            print("Error in goto_root")

        return goto_root(src, dest)
    
    def kruskal_2puiss_min_power(self, src, dest):
        """
        The complexity in the worst case is O(nb_nodes)
        But if we have choosen the best root in self.oriented_tree() it can be O(log(nb_nodes)) in average
        """
        # This fonction can only be applied to trees (You can execute kruskal before executing this one)
        if self.tree is None:
            self.oriented_tree()

        # We will go from src and dest to root
        def goto_root(node1, node2):  # node1 = src, node2 = dest
            dad1, level1, power1 = self.tree[node1]
            dad2, level2, power2 = self.tree[node2]
            if level1 > level2: # Just to sort them
                return goto_root(node2, node1)
            if level1 < level2:
                i = int(log2(level2-level1))
                ancestor_i, puissance_i = self.power_2puiss[node2][i]
                power3 = goto_root(node1, ancestor_i)
                return max(puissance_i, power3)
            if level1 == level2:
                if node1 == node2:
                    return 0
                if dad1 == dad2:
                    return max(power1, power2)
                for i in range(int(log2(level1)+1)):
                    if self.power_2puiss[node1][i][0] == self.power_2puiss[node2][i][0]:
                        ancestor1_i, power1_i = self.power_2puiss[node1][i-1]
                        ancestor2_i, power2_i = self.power_2puiss[node2][i-1]
                        return max(power1_i, power2_i, goto_root(ancestor1_i, ancestor2_i))
                    dist = int(log2(level1))
                    ancestor1_i, power1_i = self.power_2puiss[node1][dist]
                    ancestor2_i, power2_i = self.power_2puiss[node2][dist]
                    return max(power1_i, power2_i, goto_root(ancestor1_i, ancestor2_i))
            print("Error in goto_root")

        return goto_root(src, dest)


def graph_from_file(filename):  # complexity : O(number of line)
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
            listint = [float(x) if '.' in x else int(x) for x in listline]
            return listint

        n, m = readline_to_listint()
        nodes = [i for i in range(1, n + 1)]
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
