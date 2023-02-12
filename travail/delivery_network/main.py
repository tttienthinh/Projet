from graph import Graph, graph_from_file
import graphviz

data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)

dot = graphviz.Digraph(comment='The Round Table')
dot.node('A', 'King Arthur')  # doctest: +NO_EXE
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')


dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')
print(dot.source)
dot.render('doctest-output/round-table.gv', view=True)