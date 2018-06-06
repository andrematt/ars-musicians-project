import networkx as nx
import demon as d
from networkx.algorithms.community import kclique as kq


g = nx.read_edgelist("data/test.csv", delimiter="\t")
k = nx.karate_club_graph()
'''
# k-clique
k=3
#g = nx.complete_graph(5)
#K5 = nx.convert_node_labels_to_integers(g,first_label=2)
#g.add_edges_from(K5.edges())
c = list(kq.k_clique_communities(g, k, cliques=None)) #no already defined cliques
print(c)
'''


dm = d.Demon(graph=g, epsilon=0.25, min_community_size=3, file_output="communities.txt")
coms = dm.execute()
