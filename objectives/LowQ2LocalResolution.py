#!/usr/bin/env python3
# =============================================================================
## @file   LowQ2LocalResolution.py
#  @author Derek Anderson
#  @date   10.06.2025
# -----------------------------------------------------------------------------
## @brief Script to compute momentum resolution for a
#    specified tagger
#
#  Usage if executed directly:
#    ./LowQ2RecoResolution.py \
#        -i <input file> \
#        -o <output file> \
#        -t <tagger>
# =============================================================================

import argparse as ap
import numpy as np
import ROOT
import sys

from podio.reading import get_reader

# default arguments
IFileDefault = "root://dtn-eic.jlab.org//volatile/eic/EPIC/RECO/25.07.0/epic_craterlake/SINGLE/e-/5GeV/45to135deg/e-_5GeV_45to135deg.0099.eicrecon.edm4eic.root"
OFileDefault = "test_reso.root"
TagDefault   = 1

def CalculateMomReso(
    ifile = IFileDefault, 
    ofile = OFileDefault,
    tag = TagDefault
):
    """CalculateMomReso

    A function to calculate momentum resolution for a 
    specified tagger.

    Args:
      ifile: input file name
      ofile: output file name
      tag:   tagger to use
    Returns:
      calculated resolution
    """

    # set up histograms, etc. -------------------------------------------------

    # set axis title accordingly 
    axis = ";(p_{tag" + f"{tag}" + "} - p^{e}_{mag}) / p^{e}_{mag}"

    # create histogram from extracting resolution
    hres = ROOT.TH1D("hMomRes", axis, 50, -2., 3.)
    hres.Sumw2()

    # event loop --------------------------------------------------------------

    # loop through all events
    reader = get_reader(ifile)
    for iframe, frame in enumerate(reader.get("events")):

        # grab relevant collections
        maghits = frame.get("BackwardsBeamlineHits")  # FIXME this might be in npsim output...
        taghits = None
        match tag:
            case 1:
                taghits = frame.get("TaggerTrackerM1LocalTracks")
            case 2:
                taghits = frame.get("TaggerTrackerM2LocalTracks")
            case _:
                raise ValueError("Unkown tagger specified!")

        # calculate momentum of e- leaving beamline magnets
        emag  = maghits[4]
        pmag2 = emag.getMomentum().x**2 + emag.getMomentum().y**2 + emag.getMomentum().z**2
        pmag  = np.sqrt(pmag2)

        # now compare against tagger hits
        for hit in taghits:

            # calculate momentum of tagger hit
            ptag2 = hit.getMomentum().x**2 + hit.getMomentum().y**2 + hit.getMomentum().z**2
            ptag  = np.sqrt(ptag2)

            # and now compute resolution
            pres = (ptag - pmag) / pmag
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
    parser.add_argument(
        "-t",
        "--tagger",
        help = "Tagger to use",
        nargs = '?',
        const = TagDefault,
        default = TagDefault,
        type = int
    )

    # grab arguments
    args = parser.parse_args()

    # run analysis
    CalculateMomReso(args.input, args.output, args.tagger)

# end =========================================================================
