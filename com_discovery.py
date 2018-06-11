import networkx as nx
import demon as d
import csv_loader
import similarity_checker
from networkx.algorithms.community import kclique as kq

# Read data from disk and generate graph
#
crawled = csv_loader.loadGraph()

# Benchmark graph
#
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

dm = d.Demon(graph=crawled, epsilon=0.25, min_community_size=3)
coms = dm.execute()
print(similarity_checker.comm_comparer(coms, crawled))

