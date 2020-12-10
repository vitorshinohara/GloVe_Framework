from Features import paper_features
import numpy as np

def get_graph_features(g):
    extracted_features = []
    # Average Node Connectedness
    anc = paper_features.avg_conectedness(g)
    #print('ANC: {}'.format(np.isnan(anc)))
    extracted_features.append(anc)
    # Variation of Node Connectedness
    #print('VNC: {}'.format(np.isnan(vnc)))
    vnc = paper_features.variation_conectedness(g)
    extracted_features.append(vnc)
    # Page Rank
    for i, pr in enumerate(paper_features.page_rank(g)):

        #print(i + ' ' + np.isnan(pr))
        extracted_features.append(pr)
    # Number of Connected Components and Number of Nodes of the smallest connected component

    fcc, smallest = paper_features.get_number_fully_connected_components(g)
    #print('FCC: {}'.format(np.isnan(fcc)))
    #print('Smallest: {}'.format(np.isnan(smallest)))
    extracted_features.append(fcc)
    extracted_features.append(smallest)
    # Average Edge Weight
    extracted_features.append(paper_features.avg_edge_weight(g))
    # % of nodes with zero edges
    extracted_features.append(paper_features.zero_connection(g))

    return extracted_features

    # Betweenness Centrality
#    for bc in paper_features.connection_betweenness_centrality(g):
#        extracted_features.append(bc))
