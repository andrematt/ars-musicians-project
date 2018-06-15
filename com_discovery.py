import networkx as nx
import demon as d
import csv_loader
import similarity_checker
import community as com
import pquality
import matplotlib.pyplot as plt
from networkx.algorithms.community import kclique as kq
from networkx.algorithms.community import label_propagation as label
from networkx.algorithms.community.centrality import girvan_newman as gn

# Read data from disk and enerate graph
#
crawled = csv_loader.loadGraph()

# Benchmark graph
#
karate = nx.karate_club_graph()

coms=[]
'''
# k-clique
#
k=3
coms = list(kq.k_clique_communities(crawled, k, cliques=None)) #no already defined cliques
print(type(coms))
'''


'''
#Demon
#
dm = d.Demon(graph=crawled, epsilon=0.01, min_community_size=3)
coms = dm.execute()
'''

'''
# Label propagation
#
coms_generator=label.label_propagation_communities(crawled)
for com in coms_generator:
    coms.append(frozenset(com))
'''

'''
# Grivan-Newman
# (loads for ages)
#coms=[]
#coms_generator = gn(crawled)
#for com in coms_generator:
#    coms.append(frozenset(com))
'''


# Louvain
# (loads for ages)
coms=[]
partition = com.best_partition(crawled)
for com in set(partition.values()) :
    list_nodes = [nodes for nodes in partition.keys()]
    #print(list_nodes)
    coms.append(frozenset(list_nodes))

#print(coms)



scores = pquality.pquality_summary(crawled, coms)
print(scores['Indexes'])
print(scores['Modularity'])
sorted_by_labels=(similarity_checker.comm_comparer(coms, crawled))
comm_count = 0
total_count = 0
for i in sorted_by_labels:
    total_count+=i[1]['total']
    comm_count +=1

print(total_count)
print(comm_count)
print("avg label index: ", total_count/comm_count)

print("sorted by labels: ", sorted_by_labels)
