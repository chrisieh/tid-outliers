import argparse
from root_numpy import root2array
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="root ntuple")
    parser.add_argument("variable", help="variable to check")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    
    data = root2array(args.filename, "CollectionTree",
                      branches=[args.variable, "weight"])
    var = data[args.variable]
    weight = data["weight"]
    
    # Sort 
    sorted_args = np.argsort(var)
    var = var[sorted_args]
    weight = weight[sorted_args]

    min = var.min()
    max = var.max()
    mean = np.average(var, weights=weight)
    rms = np.sqrt(np.average(np.power(var - mean, 2), weights=weight))

    cdf = np.cumsum(weight)
    cdf /= cdf[-1]

    def quantile(q):
        return var[np.argmax(cdf > q)]

    out = [args.variable, args.filename, min, max, mean, rms, quantile(0.0025), quantile(0.9975), quantile(0.005), quantile(0.995), quantile(0.01), quantile(0.99), quantile(0.02), quantile(0.98)]
    print("\t".join([str(x) for x in out]))
