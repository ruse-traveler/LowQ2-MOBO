from DDSim.DD4hepSimulation import DD4hepSimulation

SIM = DD4hepSimulation()

SIM.inputFiles     = "root://dtn-eic.jlab.org//volatile/eic/EPIC/EVGEN/DIS/pythia6.428-1.0/NC/noRad/ep/10x130/q2_1to10/pythia6.428-1.0_NC_noRad_ep_10x130_q2_1to10_ab.hepmc3.tree.root"
SIM.numberOfEvents = 1000
