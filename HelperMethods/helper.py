import string
import numpy as np

def _write_output(data_arr, outputPath):
    erase_file_content = open(outputPath, 'w')
    erase_file_content.close()

    with open(outputPath, 'a') as f:
        for element in data_arr:
            f.write(element + '\n')

# Define functions for lyric processing
def process_lyric(lyric, stopwords):
    lyric = str(lyric)
    data = lyric.replace('\n', ' ').replace(string.punctuation, '')\
            .replace(',','').replace('.', '').lower().split(' ')
    data = [dt for dt in data if dt not in stopwords]
    return data

def make_word_vector(txt, embedding_dict):
    word_vectors = []
    for w in txt:
        if w.lower() in embedding_dict:
            word_vectors.append(embedding_dict[w.lower()])
    return word_vectors

def skip_signal(word_vectors):
    sig = []
    for i in range(len(word_vectors)-1):
        sig.append (np.sum( (word_vectors[i+1] - word_vectors[i]) **2 ) )
    arr_sig = np.array(sig)
    return arr_sig

# Functions for dataset processing
def process_line(line, stop_words, text_index):
    data = []
    data = process_lyric(line[text_index].encode('utf-8'), stop_words)
    return data
