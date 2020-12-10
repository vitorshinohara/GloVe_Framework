import json
import string
import numpy as np
import scipy

from Utils import glovedict
from Features import paper_features
from HelperMethods.helper import make_word_vector, process_line, process_lyric, skip_signal

def get_avg_distance_matrix_lyrics(args):
    idxs = args[0]
    opt = args[1]

    distance_matrix_lyrics = []
    dataset_lines = open(opt.input, 'r').readlines()
    dataset = np.array([json.loads(line) for line in dataset_lines])
    dataset = dataset[idxs]

    gloved = glovedict.glove_dict(opt.glove_embedding_path)


    with open(opt.stop_words_path, 'r') as myfile:
        stop_words=set(myfile.read().replace('\n', '')\
                .replace(string.punctuation,'').lower().split(' '))

        for row in dataset:
            data = process_line(row, stop_words, opt.text_column)
            if len(data) < 5:
                continue

            wordvec = make_word_vector(data, gloved)
            wordarr = np.array(wordvec)
            signal = skip_signal(wordvec)

            if len(signal) > 5:
                distance_matrix_lyrics.append(paper_features.get_max_distance(scipy.spatial.distance_matrix(wordarr, wordarr)))


    if distance_matrix_lyrics == []:
        return []

    return [np.mean(distance_matrix_lyrics)]
