import numpy as np
from scipy.spatial import distance
import networkx as nx
from networkx.algorithms.centrality import betweenness_centrality
from networkx import minimum_spanning_tree
#import matplotlib.pyplot as plt


def get_max_distance(D):
    g = nx.from_numpy_matrix(D)
    g = minimum_spanning_tree(g)

    D = nx.to_numpy_matrix(g)
    return np.max(D)


def make_graph_networkx(D, graph_generator, avg_distance_th):

    if graph_generator == 'mst':
        g = nx.from_numpy_matrix(D)
        g = minimum_spanning_tree(g)

    elif graph_generator == 'mst_mod':
        c = D * (D < avg_distance_th)
        g = nx.from_numpy_matrix(c)
        return g, c

    return g

def _angle(arr1, arr2):
    norm1 = np.sqrt (np.sum (arr1 **2 ) )
    norm2 = np.sqrt (np.sum (arr2 **2 ) )

    if (norm1*norm2) == 0 or (np.sum(arr1 * arr2) <= 0):
        return 0

    dotprod = np.sqrt( np.sum(arr1 * arr2) ) / (norm1*norm2)
    angle = np.arccos(dotprod)
    return angle

# Spatial Distribution Based Features
def centroid_location(D):
    return np.mean(D, axis=0)

def span_volume(D):
    m1 = np.max(D, axis=0)
    m2 = np.min(D, axis=0)

    G = D.shape[1]
    dg = np.sqrt( np.sum((m1-m2)**2) )
    exponent = (1/G) * np.sum( np.log10(dg) )
    V = 10 ** exponent
    return V

def dispersion_semantic_word_dimensions(D):
    dispersion_measurement = np.std(D, axis=0)
    mean = np.mean(dispersion_measurement)
    std = np.std(dispersion_measurement)
    return mean, std

def maximun_semantic_span(D):
    max_dist = 0
    for i in range(0, len(D)-1):
        for j in range(i+1, len(D)):
            this_dist = np.sqrt (np.sum( (D[i,:]-D[j,:])**2 ))
            max_dist = max(this_dist, max_dist)
    return max_dist

def semantic_span_imbalance(D):
    raise NotImplementedError

# Temporal Structure Based Features
def avg_step_size(D):
    stepSizes = []
    for x in range(0, len(D)-1):
        for j in range(x+1, len(D)):
            stepSizes.append(distance.euclidean(D[x], D[j]))
    return np.mean(stepSizes)

def variation_step_size(D):
    stepSizes = []
    for x in range(0, len(D)-1):
        for j in range(x+1, len(D)):
            stepSizes.append(distance.euclidean(D[x], D[j]))
    return np.std(stepSizes), np.max(stepSizes), np.min(stepSizes), np.max(stepSizes) - np.min(stepSizes)

def avg_adjacent_edge_angles(D):
    vectors = np.diff(D, axis=0)
    angles = np.array([ _angle(D[i,:], D[i+1,:]) for i in range(len(D)-1)])
    return np.mean(angles)

def mean_adjacent_edge_angle_increment(D):
    vectors = np.diff(D, axis=0)
    angles = np.array([ _angle(D[i,:], D[i+1,:]) for i in range(len(D)-1)])
    return np.mean(np.diff(angles))

# Feature Descriptor for Graph Topology
def avg_conectedness(g):
    conectdness = [g.degree(v) for v in g]
    return np.mean(conectdness)/float(len(conectdness))

def variation_conectedness(g):
    conectdness = [g.degree(v) for v in g]
    return np.std(conectdness)/float(len(conectdness))

def topological_balance_conectedness(g):
    raise NotImplementedError

def page_rank(g):
    page_rank = [v for v in nx.pagerank(g)]
    return np.mean(page_rank)/float(nx.number_of_nodes(g)), np.std(page_rank)/float(nx.number_of_nodes(g))

def connection_betweenness_centrality(g):
    bc_dict = betweenness_centrality(g)
    bc_arr = [ bc_dict[i] for i in bc_dict.keys() ]
    return np.mean(bc_arr)/float(len(bc_arr)), np.std(bc_arr)/float(len(bc_arr))

def mean_eigenvector(g):
    center = nx.eigenvector_centrality(g, max_iter=350)
    eigen_values = [center[node] for node in center]
    return np.mean(eigen_values)

def std_eigenvector(g):
    center = nx.eigenvector_centrality(g, max_iter=350)
    eigen_values = [center[node] for node in center]
    return np.std(eigen_values)

def get_number_fully_connected_components(g):
    smallest_subgraph = 999

    number_fully_connected_components = 0
    subgraphs = nx.connected_component_subgraphs(g)

    for subgraph in subgraphs:
        number_fully_connected_components += 1

        if len(subgraph) > 1:
            smallest_subgraph = len(subgraph) if len(subgraph) < smallest_subgraph else smallest_subgraph

    return number_fully_connected_components, smallest_subgraph/float(len(g))

def avg_edge_weight(g):
    matrix = nx.to_numpy_matrix(g)
    return np.mean(matrix)

def zero_connection(g):
    count_zero = 0
    for v in g.degree:
        if v[1] == 0:
            count_zero += 1
    return count_zero/float(len(g))
