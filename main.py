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
    weight = weight[sort_args]

    min = var.min()
    max = var.max()
    mean = np.average(var, weights=weight)
    rms = np.sqrt(np.average(np.power(var - mean, 2), weights=weight))

    cdf = np.cumsum(weight)
    cdf /= cdf[-1]

    def quantile(q):
        return var[np.argmax(cdf > q)]

    print("Statistics for {} in {}".format(args.variable, args.filename))
    print("min: {}\tmax: {}".format(min, max))
    print("mean: {}\trms: {}".format(mean, rms))
    print("0.25% {}\t99.75%: {}".format(quantile(0.0025), quantile(0.9975)))
    print("0.5%: {}\t99.5%: {}".format(quantile(0.005), quantile(0.995)))
    print("1%: {}\t99%: {}".format(quantile(0.01), quantile(0.99)))
    print("2%: {}\t98%: {}".format(quantile(0.02), quantile(0.98)))

