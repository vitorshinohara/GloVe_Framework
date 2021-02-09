
import numpy as np
import string

def glove_dict(path):
    d = dict()
    f = open(path, "r", encoding="utf8")
    for line in f.readlines():
        tokens = line.split(" ")
        vector = [float(k) for k in tokens[1:]]
        d[tokens[0]] = np.array( vector )
    f.close()
    return d

if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    d = glove_dict(sys.argv[1])
    t1 = time.time()

    print("Finished reading glove dataset")
    print("Time: ", t1-t0, " seconds")
    print("Total words: ", len(d.keys()))

