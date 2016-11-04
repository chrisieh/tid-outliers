from __future__ import division
import argparse
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="root ntuple")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mode1p", action="store_true")
    group.add_argument("--mode3p", action="store_true")
    return parser.parse_args()

vardict = {"centFrac": "TauJets.centFrac",
           "etOverPtLeadTrk": "TauJets.etOverPtLeadTrk",
           "innerTrkAvgDist": "TauJets.innerTrkAvgDist",
           "absipSigLeadTrk": "TauJets.absipSigLeadTrk",
           "SumPtTrkFrac": "TauJets.SumPtTrkFrac",
           "ChPiEMEOverCaloEME": "TauJets.ChPiEMEOverCaloEME",
           "EMPOverTrkSysP": "TauJets.EMPOverTrkSysP",
           "ptRatioEflowApprox": "TauJets.ptRatioEflowApprox",
           "mEflowApprox": "TauJets.mEflowApprox",
           "dRmax": "TauJets.dRmax",
           "trFlightPathSig": "TauJets.trFlightPathSig",
           "massTrkSys": "TauJets.massTrkSys"}

mode1p = ["centFrac", "etOverPtLeadTrk", "innerTrkAvgDist", "absipSigLeadTrk",
          "SumPtTrkFrac", "ChPiEMEOverCaloEME", "EMPOverTrkSysP",
          "ptRatioEflowApprox", "mEflowApprox"]

mode3p = ["centFrac", "etOverPtLeadTrk", "innerTrkAvgDist", "dRmax",
          "trFlightPathSig", "massTrkSys", "ChPiEMEOverCaloEME",
          "EMPOverTrkSysP", "ptRatioEflowApprox", "mEflowApprox"]

def in_range(x, a, b):
    return np.logical_and(x > a, x < b)

cuts = {"centFrac": lambda x: in_range(x, 0.0, 1.1),
        "etOverPtLeadTrk": lambda x: in_range(x, 0.0, 40.0),
        "innerTrkAvgDist": lambda x: in_range(x, 0.0, 0.4),
        "dRmax": lambda x: in_range(x, 0.0, 0.4),
        "trFlightPathSig": lambda x: in_range(x, -10.0, 50.0),
        "massTrkSys": lambda x: in_range(x, 0.0, 25000.0),
        "absipSigLeadTrk": lambda x: in_range(x, -1e-6, 40.0),
        "SumPtTrkFrac": lambda x: in_range(x, -1e-6, 1.0),
        "ChPiEMEOverCaloEME": lambda x: in_range(x, -5.0, 5.0),
        "EMPOverTrkSysP": lambda x: in_range(x, 0.0, 50.0),
        "ptRatioEflowApprox": lambda x: in_range(x, 0.0, 5.0),
        "mEflowApprox": lambda x: in_range(x, 0.0, 25000.0)}

if __name__ == "__main__":
    args = get_args()

    if args.mode1p:
        mode = mode1p
    else:
        mode = mode3p
    
    from root_numpy import root2array
    data = root2array(args.filename, "CollectionTree",
                      branches=[vardict[var] for var in mode] + ["weight"])
    
    # Get rid of default value
    if args.mode3p:
        c = data[vardict["trFlightPathSig"]] > -1000
        data = data[c]

    # Apply cuts
    pass_cuts = np.ones(shape=data.shape, dtype=bool)
    for var in mode:
        pass_cuts = np.logical_and(pass_cuts, cuts[var](data[vardict[var]]))
    fail_cuts = np.invert(pass_cuts)
    
    num_pass = np.count_nonzero(pass_cuts)
    total = len(pass_cuts)
    eff = num_pass / total
    print("Number of events passed: {}".format(num_pass))
    print("Total number of events: {}".format(total))
    print("Cut efficiency: {}".format(eff))

    from root_numpy import array2root
    array2root(data[fail_cuts],
               args.filename.replace(".root", "_outliers.root"),
               treename="CollectionTree", mode="recreate")
