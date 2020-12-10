import numpy as np

def calculate_meaning(words, distance_array, gloved):
    centroid = []
    for word in words:
        try:
            semantic_value = gloved[word]
            projection = np.inner(semantic_value, distance_array)/len(distance_array)
            centroid.append(projection)
        except:
            pass
    return centroid
