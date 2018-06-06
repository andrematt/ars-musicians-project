import networkx as nx
import matplotlib.pyplot as plt
import csv_loader
import operator

# Read data from disk and generate graph
#
crawled = csv_loader.loadGraph()

# Generate ER and BA model graphs with same stats as crawled graph
#
nodes = crawled.number_of_nodes()
links = float(crawled.number_of_edges())
erProb = 2*links/(nodes*nodes-1)
baLinks = round(links/nodes) #è giusto?
er = nx.erdos_renyi_graph(nodes, erProb)
ba = nx.barabasi_albert_graph(nodes, baLinks)

toUse = 'crawled'  # assign to crawled, er, ba
toDraw = '0'  # 0 nothing, 1 degree dist, 2 graph

############################################

# Set the graph to use
#
if toUse == 'crawled':
    graphInUse = crawled
elif toUse == 'er':
    graphInUse = er
elif toUse == 'ba':
    graphInUse = ba


# Extract basic measures
#
nodes = graphInUse.number_of_nodes()
links = float(graphInUse.number_of_edges())
self = graphInUse.number_of_selfloops()
directed = graphInUse.is_directed()
components = nx.number_connected_components(graphInUse)
comps = list(nx.connected_components(graphInUse))
totalCompsSize = 0
for i in comps:
    totalCompsSize += (len(i))
largest_comp = max(comps, key=lambda coll: len(coll))
closeness_c = nx.closeness_centrality(graphInUse) # Return a dictionary
sorted_closeness = sorted(closeness_c.items(), key=operator.itemgetter(1), reverse=True) # Dictionary have .key, .value and .items for the couple
betweenness_c = nx.betweenness_centrality(graphInUse)
sorted_betweenness = sorted(betweenness_c.items(), key=operator.itemgetter(1), reverse=True)
density = nx.density(graphInUse)
avg_cc = nx.average_clustering(graphInUse)
highest = sorted(graphInUse.degree, key=lambda x: x[1], reverse=True)
diameter = 0
#avg_shortest = nx.average_shortest_path_length(graphInUse)  # Not defined on crawled graph, because it is not connected
diameter = nx.diameter(graphInUse.subgraph(largest_comp))  # Works with test dataset, with complete data load for ages


# Print basic measures
#
print("nodes:", nodes)
print("links:", links)
print("self-loops:", self)
print("is directed:", directed)
print("components:", components)
print ("largest component: ", largest_comp)
print("size of largest component:", (len(largest_comp)))
print ("avg components size: ", totalCompsSize/components)
print ("highest degree node: ", highest[0])
print("density:", density)
print ("average clustering: ", avg_cc)
print("diameter: ", diameter)
print("sorted closeness: ", sorted_closeness)  # TODO vedere il rapporto tra alta betweennees e semantica?
print("sorted betweenness: ", sorted_betweenness)
#print("average shortest path length", avg_shortest)


# Draw degree distibution plot or graph
#
if (toDraw!=0):
    if toDraw == '1':
        hist = nx.degree_histogram(graphInUse)
        plt.plot(range(0, len(hist)), hist, ".")
        plt.title("Degree Distribution")
        plt.xlabel("Degree")
        plt.ylabel("#Nodes")
        plt.loglog()
    elif toDraw == '2':
        nx.draw(graphInUse, with_labels=True)
    plt.show()
