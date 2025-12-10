from DDSim.DD4hepSimulation import DD4hepSimulation
from g4units import m

SIM = DD4hepSimulation()
SIM.enableG4GPS

SIM.runType          = "run"
SIM.macroFile        = "./backward.e18ele.py"
SIM.physics.rangeCut = 100.0*m

# NOTE num events set in macro file
