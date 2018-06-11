import networkx as nx

# Generate an internal label similarity index via label_check
#
def comm_comparer(array_of_coms, graph):
    for com in array_of_coms:
        print("comm internal similarity:")
        print("nodes: ", com)
        subgraph_com = graph.subgraph(com)
        data_com = nx.get_node_attributes(subgraph_com, 'data')
        print("city index: ", label_check(data_com, 'city'))
        print("label index: ", label_check(data_com, 'label'))
        print("genre index: ", label_check(data_com, 'genre'))

# Compute a "repetition index" inside a community (the ratio between the total number of labels and
# the count of different labels)
#
def label_check(comm, label):
    total = []
    different = set()
    for key, value in comm.items():
        elements = value[label]
        for element in elements:
            if element != '':
                different.add(element)
                total.append(element)
    #print('different: ', different)
    #print('total: ', total)
    if (len(different)==0):
        return 0
    else:
        return(len(total)/len(different))
        #return(len(total)-len(different))/len(different)  # result > 1 means more than an half of labels are repeated
