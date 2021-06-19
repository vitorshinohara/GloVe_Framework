import json
import string
import numpy as np
import scipy
from scipy.spatial import minkowski_distance
import logging

import multiprocessing

from Utils import glovedict
from Features import paper_features
from HelperMethods.helper import make_word_vector, process_line, process_lyric, skip_signal


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(process)s] %(message)s',
    filename='results.log',
    filemode='a'
)

def get_avg_distance_matrix_lyrics(args):

    idxs = args[0]
    opt = args[1]

    distance_matrix_lyrics = []
    
    file_dataset = open(opt.input, 'r', encoding='utf-8')
    dataset_lines = file_dataset.readlines()
    file_dataset.close()

    dataset = np.array([json.loads(line) for line in dataset_lines])
    dataset = dataset[idxs]

    gloved = glovedict.glove_dict(opt.glove_embedding_path)

    with open(opt.stop_words_path, 'r', encoding="utf8") as file:
        stop_words=set(file.read().replace('\n', '').replace(string.punctuation,'').lower().split(' '))
    
    for row_idx_debug, row in enumerate(dataset):
        data = process_line(row, stop_words, opt.text_column)
        
        if len(data) < 5:
            continue

        wordvec = make_word_vector(data, gloved)
        wordarr = np.array(wordvec)
        signal = skip_signal(wordvec)
        
	
        if len(signal) > 5 and len(signal) < 1000:
                logging.debug("Start to process {}/{} -> Lenght: {}".format(row_idx_debug, len(dataset), len(data)))
                try:
                    distance_matrix_lyrics.append(paper_features.get_max_distance(scipy.spatial.distance_matrix(wordarr, wordarr)))
                except Exception as e:
                    with multiprocessing.Lock():
                            logging.debug("{}/{} {}".format(row_idx_debug, len(dataset), e) )
                    continue
                    
        
        with multiprocessing.Lock():
                logging.debug("Finished processing {}/{} -> Length: {}".format(row_idx_debug, len(dataset), len(data)) )


    if(distance_matrix_lyrics == []):
        return []

    return [np.mean(distance_matrix_lyrics)]

def our_distance_matrix(x):
    x = np.asarray(x)
    m, k = x.shape

    result = np.empty((m,m),dtype=float)  # FIXME: figure out the best dtype

    for j in range(m):
        result[:,j] = minkowski_distance(x,x[j])

    return result