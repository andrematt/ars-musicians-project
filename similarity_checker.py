import networkx as nx


# Generate an internal label similarity index via label_check or jaccard_label_check
#
def comm_comparer(array_of_coms, graph):
    comm_dict = {}
    for com in array_of_coms:
        subgraph_com = graph.subgraph(com)
        data_com = nx.get_node_attributes(subgraph_com, 'data')
        city_value = jaccard_label_check(data_com, 'city')  # change in jaccard_label_check or label_check
        label_value = jaccard_label_check(data_com, 'label') # change in jaccard_label_check or label_check
        genre_value = jaccard_label_check(data_com, 'genre') # change in jaccard_label_check or label_check
        if city_value is None:
            city_value = 0
        if genre_value is None:
            genre_value = 0
        if label_value is None:
            label_value = 0
        total = (city_value + label_value + genre_value) / 3
        data_dict = {}
        #data_dict['data']= dict([('total', total), ('city', city_value), ('label', label_value), ('genre', genre_value)])
        comm_dict[com]={'total': total, 'city': city_value, 'label': label_value, 'genre': genre_value}
    sorted_comm_dict = sorted(comm_dict.items(), key=lambda x: x[1]['total'], reverse=True)
    return sorted_comm_dict

# Compute a "repetition index" inside a community (ratio between the count of different labels and the label total)
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
    if len(different)!=0:
        return(len(different)/len(total))

# Jaccard similarity index
# test
def jaccard_label_check(comm, label):
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

    if len(different)!=0:
        '''
        intersection = len(list(set(total).intersection(different)))
        union = (len(total) + len(different)) - intersection
        return float(intersection / union)
        '''
        inter = set(total).intersection(different)
        return float(len(inter)) / (len(total) + len(different) - len(inter))