import networkx as nx
import csv as csv

def loadGraph():
# Read data from disk and generate graph
#
    g = nx.Graph()

# Define the object data
#
    def personObj():
        person = dict({
            'birth_date': 1000,  # default values
            'start_date': 1000,
            'city': [],
            'genre': [],
            'label': []
        })
        return person

# Read csv line by line and assign to dict entry
#
    csv_read = csv.reader(open("data/test.csv"), delimiter='\t')
    for row in csv_read:

        row_dict = personObj()

        birth_date = row[2]
        row_dict['birth_date'] = birth_date

        start_date = row[3]
        row_dict['start_date'] = start_date

        city_splitted = row[4].split('|')
        for n in city_splitted:
            row_dict['city'].append(n)

        genre_splitted = row[5].split('|')
        for n in genre_splitted:
            row_dict['genre'].append(n)

        label_splitted = row[6].split('|')
        for n in label_splitted:
            row_dict['label'].append(n)

        g.add_node(row[0], data=row_dict)

        if (g.has_node(row[1])):
            g.add_edge(row[0], row[1])
        else:
            g.add_node(row[1], data=personObj())
            g.add_edge(row[0], row[1])

    return g