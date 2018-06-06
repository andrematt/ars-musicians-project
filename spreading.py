import networkx as nx
import csv_loader
import ndlib.models.epidemics.SIModel as si
import ndlib.models.epidemics.SISModel as sis
import ndlib.models.epidemics.SIRModel as sir
import ndlib.models.epidemics.ThresholdModel as th
import ndlib.models.ModelConfig as mc
import json
from ndlib.utils import multi_runs
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from bokeh.plotting import figure, output_file, show

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

# Modify this parameters for customize the initial status of experiment
#
config = mc.Configuration()
toUse = 'crawled'  # assign to crawled, er, ba
toSim = 'TH'  # assign to SI, SIS, SIR, TH
initial_infected = 0.008  # fraction of nodes infected initially both for random or selected nodes situation
beta = 0.05  # infection rate for SI, SIS, SIR
lamb = 0.01  # recovery rate for SIS
gamma = 0.01  # probability of removal for SIR
selectedInitialInfected = 1  # 1 select top or bottom fraction of nodes, 0 use a random fraction of nodes
direction = 1  # 1 for select nodes in top-down direction, 0 for bottom-up (use with selectedInitialInfected)
threshold = 0.01  # threshold for TH model


############################################


# Set the graph to use
#
if toUse == 'crawled':
    graphInUse = crawled
elif toUse == 'er':
    graphInUse = er
elif toUse == 'ba':
    graphInUse = ba

# Configure the infected nodes (number of nodes derived from initial_infected parameter)
#
if selectedInitialInfected == 1:

    nodesToTake = round(nodes*initial_infected)  # size of initial infection
    print(nodesToTake)
    infected_nodes = []
    topDegrees = []
    lowDegrees = []

    # Find the top and bottom fraction of nodes in the graph in use
    #
    sortedByDegree = sorted(graphInUse.degree, key=lambda x: x[1], reverse=True)  # each element is a tuple (name, value)

    for i in range(nodesToTake):
        topDegrees.append(sortedByDegree[i][0])

    for l in range(nodesToTake):
        lowDegrees.append(sortedByDegree[nodes-l-1][0]) # takes nodes from the end of array

    # Assign top or bottom degree nodes to infection_set
    #
    if direction == 1:
        infected_nodes = topDegrees
    elif direction == 0:
        infected_nodes = lowDegrees
    #infected_nodes=('Polo Hofer')
    print(sortedByDegree)
    print (infected_nodes)

# config a SI propagation
#
if toSim=='SI':
    model = si.SIModel(graphInUse)
    config.add_model_parameter('beta', beta)
    if selectedInitialInfected == 1:
        config.add_model_initial_configuration("Infected", infected_nodes)
    else:
        config.add_model_parameter("percentage_infected", initial_infected)


# Config a SIS propagation
#
if toSim=='SIS':
    model = sis.SISModel(graphInUse)
    config.add_model_parameter('beta', beta)
    config.add_model_parameter('lambda', lamb)
    if selectedInitialInfected == 1:
        config.add_model_initial_configuration("Infected", infected_nodes)
    else:
        config.add_model_parameter("percentage_infected", initial_infected)



# Config a SIR propagation
#
if toSim=='SIR':
    model = sir.SIRModel(graphInUse)
    config.add_model_parameter('beta', beta)
    config.add_model_parameter('gamma', gamma)
    if selectedInitialInfected == 1:
        config.add_model_initial_configuration("Infected", infected_nodes)
    else:
        config.add_model_parameter("percentage_infected", initial_infected)

# Config spreading via Threshold model
#
if toSim=='TH':
    model = th.ThresholdModel(graphInUse)
    if selectedInitialInfected == 1:
        print ('uso infetti')
        config.add_model_initial_configuration("Infected", infected_nodes)
    else:
        config.add_model_parameter("percentage_infected", initial_infected)
    for i in graphInUse.nodes():  # Setting node parameters
        config.add_node_configuration("threshold", i, threshold)


# Assign config and exec simulation
#
model.set_initial_status(config)
toRun = model
trends = multi_runs(toRun, execution_number=4, iteration_number=100,  nprocesses=4)
iterations = model.iteration_bunch(100, node_status=False) #node status?

#print and visualize results
#
res = json.dumps(iterations)
print(res)
viz = DiffusionTrend(toRun, trends)
p = viz.plot(width=700, height=700)

show(p)
