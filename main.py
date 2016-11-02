import argparse
import ROOT

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="root ntuple")
    parser.add_argument("variable", help="variable to check")
    return parser.parse_args()

if __name__ == "__main__":
    print("Entering main")
    args = get_args()
    
    # Check exist
    infile = ROOT.TFile(args.filename, "READ")
    tree = ROOT.TTree()
    infile.GetObject("CollectionTree", tree)

    minimum = tree.GetMinimum(args.variable)
    maximum = tree.GetMaximum(args.variable)
    hist = ROOT.TH1F("hist", "hist", 200, minimum, maximum)
    tree.Draw("{0} >> hist".format(args.variable))

    mean = hist.GetMean()
    rms = hist.GetRMS()

    print("{0}, {1}".format(minimum, maximum))
    print("{0}, {1}".format(mean, rms))
