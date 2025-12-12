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

import subprocess
import sys
sys.path.append('../')

import objectives.LowQ2GlobalResolution as lqg
import objectives.LowQ2LocalResolution as lql

# test 0: generate inputs -----------------------------------------------------

# input file names for convenience
ifSim = "backward.e10ele.edm4hep.root"
ifRec = "backward.e10ele.edm4eic.root"

subprocess.run(["../scripts/generate-input.sh", ifSim, ifRec])

# test 0: run objectives ------------------------------------------------------

# output file names for convenience
ofGloRes  = "test_globa_reso.root"
ofLocRes1 = "test_local1_reso.root"
ofLocRes2 = "test_local2_reso.root"

# test global resolution
glo_reso = lqg.CalculateMomReso(ifRec, ofGloRes)

# test local resolutions
lo1_reso = lql.CalculateMomReso(ifSim, ifRec, ofLocRes1, 1)
lo2_reso = lql.CalculateMomReso(ifSim, ifRec, ofLocRes2, 2)

print(f"[1] Ran objectives:")
print(f"  -- global p resolution   = {glo_reso}")
print(f"  -- m1 local p resolution = {lo1_reso}")
print(f"  -- m2 local p resolution = {lo2_reso}")

# test 1: extract objectives --------------------------------------------------

# extract global resolution
glo_reso_txt = None
with open(ofGloRes.replace(".root", ".txt")) as oglo:
    glo_reso_txt = float(oglo.read().splitlines()[0])

# extract local resolutions
lo1_reso_txt = None
with open(ofLocRes1.replace(".root", ".txt")) as oloc1:
    lo1_reso_txt = float(oloc1.read().splitlines()[0])

lo2_reso_txt = None
with open(ofLocRes2.replace(".root", ".txt")) as oloc2:
    lo2_reso_txt = float(oloc2.read().splitlines()[0])

print(f"[2] Extracted objectives:")
print(f"  -- global p resolution   = {glo_reso_txt}, type = {type(glo_reso_txt)}")
print(f"  -- m1 local p resolution = {lo1_reso_txt}, type = {type(lo1_reso_txt)}")
print(f"  -- m2 local p resolution = {lo2_reso_txt}, type = {type(lo2_reso_txt)}")

# end =========================================================================
