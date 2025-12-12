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
ISimDefault = "../backward.e10ele.edm4hep.root"
IRecDefault = "../backward.e10ele.edm4eic.root"
OutDefault  = "test_local_reso.root"
TagDefault  = 1

def CalculateMomReso(
    sfile = ISimDefault,
    rfile = IRecDefault,
    ofile = OutDefault,
    tag = TagDefault
):
    """CalculateMomReso

    A function to calculate momentum resolution for a 
    specified tagger.

    Args:
      sfile: input sim file name
      rfile: input rec file name
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

    # open inputs with podio readers
    sreader  = get_reader(sfile)
    rreader  = get_reader(rfile)
    nsframes = len(sreader.get("events"))
    nrframes = len(rreader.get("events"))
    if nsframes != nrframes:
        raise RuntimeError(f"The no. of sim frames ({nsframes}) isn't the same as the no. of reco frames ({nrframes})!")
        return

    # iterate through frames
    sframes = sreader.get("events")
    rframes = rreader.get("events")
    for iframe in range(nsframes):

        # grab sim and reco frames
        sframe = sframes[iframe]
        rframe = rframes[iframe]

        # grab relevant collections
        maghits = sframe.get("BackwardsBeamlineHits")
        tagtrks = None
        match tag:
            case 1:
                tagtrks = rframe.get("TaggerTrackerM1LocalTracks")
            case 2:
                tagtrks = rframe.get("TaggerTrackerM2LocalTracks")
            case _:
                raise ValueError("Unkown tagger specified!")

        # calculate momentum of e- leaving beamline magnets
        emag  = maghits[4]
        pmag2 = emag.getMomentum().x**2 + emag.getMomentum().y**2 + emag.getMomentum().z**2
        pmag  = np.sqrt(pmag2)

        # now compare against tagger hits
        for trk in tagtrks:

            # calculate momentum of tagger track
            ptag2 = trk.getMomentum().x**2 + trk.getMomentum().y**2 + trk.getMomentum().z**2
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

    # grab objective and other info
    #   - FIXME the local track momenta is *very* different from
    #     the electron momentum, so just use abs value of mean
    #     and RMS of %-diff for now
    #reso = fres.GetParameter(2)
    #eres = fres.GetParError(2)
    #mean = fres.GetParameter(1)
    #emea = fres.GetParError(1)
    reso = hres.GetRMS()
    eres = hres.GetRMSError()
    mean = np.abs(hres.GetMean())
    emea = np.abs(hres.GetMeanError())

    # write them out to a text file for extraction later
    otext = ofile.replace(".root", ".txt")
    with open(otext, 'w') as out:
        out.write(f"{reso}\n")
        out.write(f"{eres}\n")
        out.write(f"{mean}\n")
        out.write(f"{emea}")

    # and return calculated resolution
    return reso

# main ========================================================================

if __name__ == "__main__":

    # set up argments
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sim",
        help = "Input simulation file",
        nargs = '?',
        const = ISimDefault,
        default = ISimDefault,
        type = str
    )
    parser.add_argument(
        "-r",
        "--reco",
        help = "Input reconstruction file",
        nargs = '?',
        const = IRecDefault,
        default = IRecDefault,
        type = str
    )
    parser.add_argument(
        "-o",
        "--output",
        help = "Output file",
        nargs = '?',
        const = OutDefault,
        default = OutDefault,
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
    CalculateMomReso(args.sim, args.reco, args.output, args.tagger)

# end =========================================================================
