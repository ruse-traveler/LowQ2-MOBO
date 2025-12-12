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

out_sim=$1
out_rec=$2

npsim --compactFile $DETECTOR_PATH/epic_ip6_extended.xml --enableG4GPS --steeringFile ../steering/electron/backward.e10ele.py --outputFile $out_sim

eicrecon -Ppodio:output_file=$out_rec $out_sim

# end ===========================================
