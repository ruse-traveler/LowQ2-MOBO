# =============================================================================
## @file   RunObjectives.py
#  @author Derek Anderson
#  @date   11.24.2025
# -----------------------------------------------------------------------------
## @brief Simple wrapper for deploying the
#    trial manager.
# =============================================================================

import argparse
import datetime
import os
import re
import subprocess

import EICMOBOTestTools as emt 

def RunObjectives(tag = None, **kwargs):
    """RunObjectives

    Runs trial (simulation, reconstruction,
    and all analyses) for provided set of
    updated parameters.

    Args:
      tag:    tag associated with trial
      kwargs: any keyword arguments (e.g. parameterization)
    Returns:
      dictionary of objectives and their values
    """

    # extract path to script being run currently
    main_path, main_file = emt.SplitPathAndFile(
        os.path.realpath(__file__)
    )

    # determine paths to config files
    #   -- FIXME this is brittle!
    run_path = main_path + "/../configuration/run.config"
    par_path = main_path + "/../configuration/parameters.config"
    obj_path = main_path + "/../configuration/objectives.config"

    # create trial manager
    trial = emt.TrialManager(run_path,
                             par_path,
                             obj_path,
                             tag)

    # create and run script
    oFiles = trial.DoTrial(kwargs)

    # extract relevant objectives
    #   --> (should be 1st line in associated
    #       text files)
    objectives = dict()
    for obj, file in oFiles.items():
        oTxt = file.replace(".root", ".txt")
        oVal = None
        with open(oTxt, 'r') as out:
            oDat = out.readlines()
            oVal = float(oDat[0])
        objectives[obj] = oVal

    # return dictionary of objectives
    return objectives

# main ========================================================================

if __name__ == "__main__":

    # parse keyword arguments
    #   -- TODO automate adding parameters to parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", "--tag", help = "Trial tag", type = str, default = None)
    parser.add_argument("--tagger1_width", "--tagger1_width", help = "Width of tagger 1 discs", type = float)
    parser.add_argument("--tagger1_height", "--tagger1_height", help = "Height of tagger 1 discs", type = float)
    parser.add_argument("--tagger2_width", "--tagger2_width", help = "Width of tagger 2 discs", type = float)
    parser.add_argument("--tagger2_height", "--tagger2_height", help = "Height of tagger 2 discs", type = float)

    # grab arguments & create dictionary
    # of parameters
    #   -- TODO this can also be automated
    args   = parser.parse_args()
    params = {
        "tagger1_width"  : args.tagger1_width,
        "tagger1_height" : args.tagger1_height,
        "tagger2_width"  : args.tagger2_width,
        "tagger2_height" : args.tagger2_height
    }

    # run objective
    RunObjectives(args.tag, **params)

# end ===========================================================================
