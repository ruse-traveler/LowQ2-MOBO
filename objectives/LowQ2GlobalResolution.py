#!/usr/bin/env python3
# =============================================================================
## @file   LowQ2GlobalResolution.py
#  @author Derek Anderson
#  @date   12.10.2025
# -----------------------------------------------------------------------------
## @brief Script to compute momentum resolution for
#    particles reconstructed by the Low-Q2 tagger(s).
#
#  Usage if executed directly:
#    ./LowQ2RecoResolution.py -i <input file> -o <output file>
# =============================================================================

import argparse as ap
import numpy as np
import ROOT
import sys

from podio.reading import get_reader

# default arguments
IFileDefault = "../backward.e10ele.edm4eic.root"
OFileDefault = "test_global_reso.root"

def CalculateMomReso(
    ifile = IFileDefault, 
    ofile = OFileDefault
):
    """CalculateMomReso

    A function to calculate momentum resolution for a 
    particles reconstructed by the Low-Q2 tagger(s).

    Args:
      ifile: input file name
      ofile: output file name
    Returns:
      calculated resolution
    """

    # set up histograms, etc. -------------------------------------------------

    # create histogram from extracting resolution
    hres = ROOT.TH1D("hMomRes", ";(p_{rec} - p_{sim}^{e}) / p_{sim}^{e}", 50, -2., 3.)
    hres.Sumw2()

    # event loop --------------------------------------------------------------

    # loop through all events
    reader = get_reader(ifile)
    for iframe, frame in enumerate(reader.get("events")):

        # grab relevant collections
        mcpars  = frame.get("MCParticles")
        recpars = frame.get("TaggerTrackerReconstructedParticles")

        # find scattered e- in MCParticles
        electron = None
        for par in mcpars:
            isElec  = par.getPDG() == 11
            isFinal = par.getGeneratorStatus() == 1
            if isElec and isFinal:
                electron = par
                break

        # calculate momentum of scattered electron
        pele2 = electron.getMomentum().x**2 + electron.getMomentum().y**2 + electron.getMomentum().z**2
        pele  = np.sqrt(pele2)

        # now compare against reconstructed particles
        for par in recpars:

            # calculate momentum of reconstructed particle
            ptag2 = par.getMomentum().x**2 + par.getMomentum().y**2 + par.getMomentum().z**2
            ptag  = np.sqrt(ptag2)

            # and now compute resolution
            pres = (ptag - pele) / pele
            hres.Fill(pres)

    # resolution calculation --------------------------------------------------

    # fit spectrum with a gaussian to extract peak 
    fres = ROOT.TF1("fMomRes", "gaus(0)", -0.5, 0.5)
    fres.SetParameter(0, hres.Integral())
    fres.SetParameter(1, hres.GetMean())
    fres.SetParameter(2, hres.GetRMS())
    hres.Fit(fres, "r")

    # wrap up script ----------------------------------------------------------

    # save objects
    with ROOT.TFile(ofile, "recreate") as out:
        out.WriteObject(hres, "hMomRes")
        out.WriteObject(fres, "fMomRes")
        out.Close()

    # grab objective and other info
    reso = fres.GetParameter(2)
    eres = fres.GetParError(2)
    mean = fres.GetParameter(1)
    emea = fres.GetParError(1)

    # write them out to a text file for extraction later
    otext = ofile.replace(".root", ".txt")
    with open(otext, 'w') as out:
        out.write(f"{reso}\n")
        out.write(f"{eres}\n")
        out.write(f"{mean}\n")
        out.write(f"{emea}")

    # and return calculated resolution
    return fres.GetParameter(2)

# main ========================================================================

if __name__ == "__main__":

    # set up argments
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help = "Input file",
        nargs = '?',
        const = IFileDefault,
        default = IFileDefault,
        type = str
    )
    parser.add_argument(
        "-o",
        "--output",
        help = "Output file",
        nargs = '?',
        const = OFileDefault,
        default = OFileDefault,
        type = str
    )

    # grab arguments
    args = parser.parse_args()

    # run analysis
    CalculateMomReso(args.input, args.output)

# end =========================================================================
