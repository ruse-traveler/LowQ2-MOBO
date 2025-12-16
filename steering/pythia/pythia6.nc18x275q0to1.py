from DDSim.DD4hepSimulation import DD4hepSimulation
from g4units import m

SIM = DD4hepSimulation()

SIM.runType          = "run"
SIM.physics.rangecut = 100.0*m

SIM.inputFiles     = "root://dtn-eic.jlab.org//volatile/eic/EPIC/EVGEN/SIDIS/pythia6-eic/1.0.0/18x275/q2_0to1/pythia_ep_noradcor_18x275_q2_0.000000001_1.0_run1.ab.hepmc3.tree.root"
SIM.numberOfEvents = 100000
