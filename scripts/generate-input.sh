#!/bin/bash
# ===============================================
# @file    generate-input.sh
# @authors Derek Anderson
# @date    12.11.2025
# -----------------------------------------------
# Runs npsim and eicrecon to generate
# inputs for testing objective scripts.
#
# Usage:
#   ./generate-input.sh
# ===============================================

# single electron -------------------------------

npsim --compactFile $DETECTOR_PATH/epic_ip6_extended.xml --enableG4GPS --steeringFile ./steering/electron/backward.e10ele.py --outputFile backward.e10ele.edm4hep.root

eicrecon -Ppodio:output_file=backward.e10ele.edm4eic.root backward.e10ele.edm4hep.root

# end ===========================================
