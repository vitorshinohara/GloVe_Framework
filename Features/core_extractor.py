import numpy as np
import scipy.stats as st
import scipy
import string
import json

from Utils import glovedict
from Features.spatial_features_extractor import get_spatial_features
from Features.temporal_features_extractor import get_temporal_features
from Features.graph_features_extractor import get_graph_features
from HelperMethods.helper import make_word_vector, process_line, process_lyric, skip_signal
from Features import paper_features


def process_dataset(args):

    idxs = args[0]
    avg_distance = args[1]
    opt = args[2]

    filename = opt.input

    gloved = glovedict.glove_dict(opt.glove_embedding_path)

    with open(opt.stop_words_path, 'r') as myfile:
        stop_words=set(myfile.read().replace('\n', '')\
                .replace(string.punctuation,'').lower().split(' '))

    dataset_lines = open(opt.input, 'r').readlines()
    dataset = np.array([json.loads(line) for line in dataset_lines])
    dataset = dataset[idxs]

    out_batch = []

    for row in dataset:
        data = process_line(row, stop_words, opt.text_column)
        if len(data) < 5:
            continue

        wordvec = make_word_vector(data, gloved)
        wordarr = np.array(wordvec)
        signal = skip_signal(wordvec)


        if len(signal) > 5:

            g, c = paper_features.make_graph_networkx(scipy.spatial.distance_matrix(wordarr, wordarr),'mst_mod', avg_distance)

            out_row = row
            features_output = []
            features_output.extend(get_spatial_features(wordarr))
            features_output.extend(get_temporal_features(wordarr))
            features_output.extend(get_graph_features(g))
            out_row['features'] = features_output

            #try:
            #    out_row.append(paper_features.mean_eigenvector(g))
            #    out_row.append(paper_features.std_eigenvector(g))
            #except:
            #    continue

            # RMS
            #out_row.append(np.sqrt(np.mean((scipy.spatial.distance_matrix(wordarr, wordarr)-c)**2)).tolist())

            out_batch.append(json.dumps(out_row))


    return out_batch
