from Features import paper_features
import numpy as np

def get_graph_features(g):
    extracted_features = []
    # Average Node Connectedness
    anc = paper_features.avg_conectedness(g)
    yield anc
    # Variation of Node Connectedness
    vnc = paper_features.variation_conectedness(g)
    yield vnc
    # Page Rank
    for i, pr in enumerate(paper_features.page_rank(g)):
        yield pr

    # Number of Connected Components and Number of Nodes of the smallest connected component
    fcc, smallest = paper_features.get_number_fully_connected_components(g)
    yield fcc
    yield smallest
    # Average Edge Weight
    yield paper_features.avg_edge_weight(g)
    # % of nodes with zero edges
    yield paper_features.zero_connection(g)

    # Betweenness Centrality
#    for bc in paper_features.connection_betweenness_centrality(g):
#        yield (bc))
