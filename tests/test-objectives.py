# =============================================================================
## @file   test-objectives.py
#  @author Derek Anderson
#  @date   08.29.2025
# -----------------------------------------------------------------------------
## @Driver script to test run objective
#    methods
#
#  TODO convert to use pytest
# =============================================================================

import sys
sys.path.append('../')

import objectives.LowQ2GlobalResolution as lqg

# test 0: run objectives ------------------------------------------------------

# output file names for convenience
ofGloRes = "test_globa_reso.root"

# test global resolution
glo_reso = lqg.CalcaulateMomReso(
    "root://dtn-eic.jlab.org//volatile/eic/EPIC/RECO/25.07.0/epic_craterlake/SINGLE/e-/5GeV/45to135deg/e-_5GeV_45to135deg.0099.eicrecon.edm4eic.root",
    ofGloRes
)

print(f"[0] Ran objectives:")
print(f"  -- global p resolution = {glo_reso}")

# test 1: extract objectives --------------------------------------------------

# extract global resolution
glo_reso_txt = None
with open(ofGloRes.replace(".root", ".txt")) as oglo:
    glo_reso_txt = float(oglo.read().splitlines()[0])

print(f"[1] Extracted objectives:")
print(f"  -- global p resolution = {glo_reso_test}, type = {type(glo_reso_txt)}")

# end =========================================================================
