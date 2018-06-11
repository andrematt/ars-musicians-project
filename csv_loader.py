import networkx as nx
import csv as csv
import datetime as dt


def loadGraph():
# Read data from disk and generate graph
#

    #reference_datetime = dt.datetime.strptime('1975-01-01', '%Y-%m-%d')
    default_datetime = dt.datetime.strptime('1000-01-01', '%Y-%m-%d')
    g = nx.Graph()

# Define the object data
#
    def personObj():
        person = dict({
            'birth_date': default_datetime,  # default values
            'start_date': 1000,
            'city': [],
            'genre': [],
            'label': []
        })
        return person

# Read csv line by line and assign to dict entry
#

    csv_read = csv.reader(open("data/mergetsv.csv", encoding="utf8"), delimiter='\t')
    print(type(csv_read))
    for row in csv_read:

        row_dict = personObj()

        birth_date = (row[2])
        try:
            mydate = dt.datetime.strptime(birth_date, '%Y-%m-%d')
            # print (mydate)
            row_dict['birth_date'] = mydate
        except ValueError:
            print ('wrong format! ', birth_date)


        start_date = row[3]
        row_dict['start_date'] = start_date # to int

        city_splitted = row[4].split('|')
        for n in city_splitted:
            row_dict['city'].append(n)

        genre_splitted = row[5].split('|')
        for n in genre_splitted:
            row_dict['genre'].append(n)

        label_splitted = row[6].split('|')
        for n in label_splitted:
            row_dict['label'].append(n)

        # if (row_dict['birth_date']>reference_datetime):  #birthdate filter
        g.add_node(row[0], data=row_dict)

        if (g.has_node(row[1])):  # if the linked node exists, just add the link
            g.add_edge(row[0], row[1])
        else:
            g.add_node(row[1], data=personObj())  # otherwise create the node with default values
            g.add_edge(row[0], row[1])  # then add the link

    return g
