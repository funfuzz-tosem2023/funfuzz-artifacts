import networkit as nk
from networkit.centrality import KatzCentrality

"""
Generate exemplified call graph
"""

G = nk.Graph(n=10, directed=True)
# Add edge with reversed direction
G.addEdge(1, 0)
G.addEdge(2, 0)
G.addEdge(3, 1)
G.addEdge(4, 1)
G.addEdge(5, 1)
G.addEdge(5, 2)
G.addEdge(6, 3)
G.addEdge(7, 4)
G.addEdge(8, 4)
G.addEdge(9, 5)

# Influence analysis
katz = KatzCentrality(G=G, alpha=0.5)
katz.run()
print([round(score, 2) for score in katz.scores()])

katz = KatzCentrality(G=G)
katz.run()
print([round(score, 2) for score in katz.scores()])
#                       0,    1,    2,    3,    4,    5,    6,    7,    8,    9
# \alpha = 0.5,     [0.66, 0.63, 0.21, 0.14, 0.27, 0.14, 0.02, 0.02, 0.02, 0.02]
# \alpha = default, [0.59, 0.65, 0.23, 0.18, 0.32, 0.18, 0.04, 0.04, 0.04, 0.04]
