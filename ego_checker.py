import networkx as nx
import csv_loader
import similarity_checker
from networkx.generators import ego_graph

# Read data from disk and generate graph
#
crawled = csv_loader.loadGraph()
betweenness = open('data/betweenness.txt', 'r').read()
closeness = open('data/closeness.txt', 'r').read()
degree=open('data/degree.txt', 'r').read()

test = eval(betweenness)
coms_list=[]

for i in range(150):
    #print("extractiong ego of: ", test[i][0])
    ego = ego_graph(crawled, test[i][0], radius=1, center=True)
    #print("ego exctracted: ", tuple(ego))
    coms_list.append(tuple(ego))
    sorted_by_labels = (similarity_checker.comm_comparer(coms_list, crawled))
    total_count = 0
    #print(sorted_by_labels)
    for j in sorted_by_labels:
        total_count += j[1]['genre']
    #print("iteration: ", i)
    #print(total_count)
    print(total_count / (i+1))
