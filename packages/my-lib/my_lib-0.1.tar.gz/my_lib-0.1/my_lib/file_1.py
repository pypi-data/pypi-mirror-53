import numpy as np
def average(*args):
    return np.average(args)

def double(*args):
    args = np.array(args)
    return args*2 