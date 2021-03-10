import numpy as np
import scipy.stats as st
import scipy
import string
import json
import logging
import multiprocessing
from Utils import glovedict
from Features.spatial_features_extractor import get_spatial_features
from Features.temporal_features_extractor import get_temporal_features
from Features.graph_features_extractor import get_graph_features
from HelperMethods.helper import make_word_vector, process_line, process_lyric, skip_signal
from Features import paper_features

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(process)s %(levelname)s %(message)s',
    filename='results.log',
    filemode='a'
)

def process_features(dataset, stop_words, text_column, gloved, avg_distance):

    for row_idx, row in enumerate(dataset):
        data = process_line(row, stop_words, text_column)
        if len(data) < 5:
            continue

        wordvec = make_word_vector(data, gloved)
        wordarr = np.array(wordvec)
        signal = skip_signal(wordvec)


        if len(signal) > 5 and len(signal) < 4000:

            try:
                g, c = paper_features.make_graph_networkx(scipy.spatial.distance_matrix(wordarr, wordarr),'mst_mod', avg_distance)
            except Exception as e:           
                continue

            out_row = row
            features_output = []

            for spatial_feature in get_spatial_features(wordarr):
                features_output.append(spatial_feature)
            
            temporal_features = get_temporal_features(wordarr)

            # Multiple try catchs to enhance memory usage
            try:
                for temporal_feature in temporal_features:
                    features_output.append(temporal_feature)

            except Exception as e:
                with multiprocessing.Lock():
                    logging.error(e)                
                continue

            try:
                graph_features = get_graph_features(g)
            except Exception as e:
                with multiprocessing.Lock():
                    logging.error(e)                
                continue
            
            try:
                for graph_feature in graph_features:
                    features_output.append(graph_feature)
            except Exception as e:
                with multiprocessing.Lock():
                    logging.error(e)                
                continue
            
            
            out_row['features'] = features_output

            #try:
            #    out_row.append(paper_features.mean_eigenvector(g))
            #    out_row.append(paper_features.std_eigenvector(g))
            #except:
            #    continue

            # RMS
            #out_row.append(np.sqrt(np.mean((scipy.spatial.distance_matrix(wordarr, wordarr)-c)**2)).tolist())

            #out_batch.append(json.dumps(out_row))

            yield json.dumps(out_row)

def process_dataset(args):

    idxs = args[0]
    avg_distance = args[1]
    opt = args[2]

    filename = opt.input

    gloved = glovedict.glove_dict(opt.glove_embedding_path)

    with open(opt.stop_words_path, 'r', encoding="utf8") as myfile:
        stop_words=set(myfile.read().replace('\n', '')\
                .replace(string.punctuation,'').lower().split(' '))

    dataset_lines = open(opt.input, 'r', encoding="utf8").readlines()
    dataset = np.array([json.loads(line) for line in dataset_lines])
    dataset = dataset[idxs]

    features = process_features(dataset, stop_words, opt.text_column, gloved, avg_distance)

    for idx, feature in enumerate(features):
        with multiprocessing.Lock():
            logging.info("{}/{}".format(idx + 1, len(dataset)) )
            with open('output/features.csv', 'a') as f:
                f.write(feature)
                f.write('\n')


    return True
