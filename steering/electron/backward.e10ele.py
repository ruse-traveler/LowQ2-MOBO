from DDSim.DD4hepSimulation import DD4hepSimulation
from g4units import m

SIM = DD4hepSimulation()

SIM.runType          = "run"
SIM.physics.rangecut = 100.0*m

# NOTE num events set in macro file
