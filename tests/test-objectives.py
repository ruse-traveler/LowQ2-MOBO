# =============================================================================
## @file   test-objectives.py
#  @author Derek Anderson
#  @date   08.29.2025
# -----------------------------------------------------------------------------
## @Driver script to test run objective
#    methods
#
#  TODO convert to use pytest
#  TODO update to be better for Low-Q2
# =============================================================================

import sys
sys.path.append('../')

import objectives.LowQ2RecoResolution as eres

# test resolution calculation on electrons
ele_reso = eres.CalculateReso(
    ifile = "root://dtn-eic.jlab.org//volatile/eic/EPIC/RECO/25.07.0/epic_craterlake/SINGLE/e-/5GeV/45to135deg/e-_5GeV_45to135deg.0099.eicrecon.edm4eic.root",
    ofile = "test_reso.ele.root",
    pdg   = 11
)

print(f"Ran objectives:")
print(f"  -- e- resolution = {ele_reso}")

# end =========================================================================
