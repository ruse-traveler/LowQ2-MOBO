# =============================================================================
## @file   test-eic-tools.py
#  @author Derek Anderson
#  @date   09.02.2025
# -----------------------------------------------------------------------------
## @brief A small script to test various features
#    of the EICMOBOTestTools module.
#
#  TODO convert to use pytest
# =============================================================================

import pprint
import sys
sys.path.append('../')

import EICMOBOTestTools as emt



# (0) Test ConfigParser -------------------------------------------------------

# these should work
tag1H = emt.GetParameter("tagger1_height", "../configuration/parameters.config")
tag2W = emt.GetParameter("tagger2_width", "../configuration/parameters.config")
tag1Z = {
    "element"    : "value",
    "path"       : ".//constant[@name='Tagger1_Layer_1_Z']",
    "default"    : "3.0",
    "units"      : "mm",
    "lower"      : "1.0",
    "upper"      : "102.0",
    "compact"    : "compact/far_backward/taggers.xml",
    "stage"      : "sim",
    "value_type" : "float",
    "param_type" : "range"
}

# grab variables
path1H, type1H, units1H = emt.GetPathElementAndUnits(tag1H)
path2W, type2W, units2W = emt.GetPathElementAndUnits(tag2W)
path1Z, type1Z, units1Z = emt.GetPathElementAndUnits(tag1Z)

print(f"[0][tagger1_height] path = {path1H}, type = {type1H}, units = {units1H}")
print(f"[0][tagger2_width] path = {path2W}, type = {type2W}, units = {units2W}")
print(f"[0][tagger1_layer1_z] path = {tag1Z}, type = {type1Z}, units = {units1Z}")

try:
    tag2H = emt.GetParameter("tgager2_hieght", "parameters.config")
except:
    print(f"[0][tagger2_height] exception raised!")
finally:
    print(f"[0][tagger2_height] typo generated error as expected!")

# (1) Test GeometryEditor -----------------------------------------------------

# create a geometry editor
geditor = emt.GeometryEditor("../configuration/run.config")

# edit a couple parameters in one compact file
geditor.EditCompact(tag1Z, 5.0, "test1A")
geditor.EditCompact(tag1H, 147.5, "test1A")
geditor.EditCompact(tag2W, 156.3, "test1A")
print(f"[1][test A] set values of tagger 1 layer 1 z, tagger 1 height, tagger 2 width to 5.0 mm, 147.5 mm, 156.3 mm respectively")

# now create a config files associated with
# compact; the 2nd line should leave the
# config file unmodified
configA = geditor.EditConfig(tag1H, "test1A")
configA = geditor.EditConfig(tag2W, "test1A")
print(f"[1][Test A] config file {configA} created")

# grab/make additional parameters for
# next test
tag2H = emt.GetParameter("tagger2_height", "../configuration/parameters.config")
tag2Z = {
    "element"    : "value",
    "path"       : ".//constant[@name='Tagger2_Layer_2_Z']",
    "default"    : "103.0",
    "units"      : "mm",
    "lower"      : "53",
    "upper"      : "153.0",
    "compact"    : "compact/far_backward/taggers.xml",
    "stage"      : "sim",
    "value_type" : "float",
    "param_type" : "range"
}
bicLG = {
    "element"    : "value",
    "path"       : ".//constant[@name='EcalBarrel_LightGuide_length']",
    "default"    : "5.0",
    "units"      : "cm",
    "lower"      : "1.0",
    "upper"      : "9.0",
    "compact"    : "compact/ecal/bic/bic.xml",
    "stage"      : "sim",
    "value_type" : "float",
    "param_type" : "range"
}

# apply edits to compact files
geditor.EditCompact(tag2H, 152.9, "test1B")
geditor.EditCompact(tag2Z, 112.3, "test1B")
geditor.EditCompact(bicLG, 7.0, "test1B")
print(f"[1][Test B] set tagger 2 height to 152.9 mm, tagger 2 layer 2 z to 112.3 mm, and BIC light guide length to 7.0 cm")

# and then recursively edit all
# related files
geditor.EditRelatedFiles(tag2H, "test1B")
geditor.EditRelatedFiles(tag2Z, "test1B")
geditor.EditRelatedFiles(bicLG, "test1B")
print(f"[1][test B] recursively edited all files associated with tagger 2 height and BIC light guide")

# (2) Test generators  --------------------------------------------------------

# create a sim generator and parse enviroment
# config for easy use
simgen = emt.SimGenerator("../configuration/run.config")
enviro = emt.ReadJsonFile("../configuration/run.config")
intest = "single_electron"
inputs = enviro["sim_input"][intest]

# try to create a simulation command
dosimA = simgen.MakeCommand("test2A", intest, inputs["location"], "backward.e10ele.py", inputs["type"])
dosimB = simgen.MakeCommand("test2B", intest, inputs["location"], "backward.e10ele.py", inputs["type"])
print(f"[2][Test A] Created commands to do simulation:")
print(f"  {dosimA}")
print(f"  {dosimB}")

# grab just the config names from
# our previous test
conPathA, conFileA = emt.SplitPathAndFile(configA)
conFileA = conFileA.replace(".xml", "")

# now try to create a simulation driver script
runsimA = simgen.MakeScript("test2A", intest, "backward.e10ele.py", conFileA, dosimA)
runsimB = simgen.MakeScript("test2B", intest, "backward.e10ele.py", conFileA, dosimB)
print(f"[2][Test B] created driver scripts for simulation:")
print(f"  {runsimA}")
print(f"  {runsimB}")

# create a rec generator
recgen = emt.RecGenerator("../configuration/run.config")

# try to create a reco command
dorecA = recgen.MakeCommand("test2A", intest, "backward.e10ele.py")
dorecB = recgen.MakeCommand("test2B", intest, "backward.e10ele.py")
print(f"[2][Test C] Created commands to do reconstruction:")
print(f"  {dorecA}")
print(f"  {dorecB}")

# and now try to create a reconstruction driver script
runrecA = recgen.MakeScript("test2A", intest, "backward.e10ele.py", conFileA, dorecA)
runrecB = recgen.MakeScript("test2B", intest, "backward.e10ele.py", conFileA, dorecB)
print(f"[2][Test D] Created driver scripts for reconstruction:")
print(f"  {runrecA}")
print(f"  {runrecB}")

# create an ana generator
anagen = emt.AnaGenerator("../configuration/run.config", "../configuration/objectives.config")

# recreate output names for input to
# test ana generator
steeTag = emt.ConvertSteeringToTag("backward.e10ele.py")
simOutA = emt.MakeOutName("test2A", intest, steeTag, "sim")
simOutB = emt.MakeOutName("test2B", intest, steeTag, "sim")
recOutA = emt.MakeOutName("test2A", intest, steeTag, "rec")
recOutB = emt.MakeOutName("test2B", intest, steeTag, "rec")
simDirA = enviro["out_path"] + "/test2A/" + simOutA
simDirB = enviro["out_path"] + "/test2B/" + simOutB
recDirA = enviro["out_path"] + "/test2A/" + recOutA
recDirB = enviro["out_path"] + "/test2B/" + recOutB

# try to create an analysis command
doanaA, ofileA = anagen.MakeCommand("test2A", intest, "TaggerOneResolution", simDirA, recDirA)
doanaB, ofileB = anagen.MakeCommand("test2B", intest, "TaggerOneResolution", simDirB, recDirB)
print(f"[2][Test E] Created commands to do analysis")
print(f"  (A) command = {doanaA}")
print(f"      output  = {ofileA}")
print(f"  (B) command = {doanaB}")
print(f"      output  = {ofileB}")

# and finally try to create an analysis script
runanaA = anagen.MakeScript("test2A", intest, "TaggerOneResolution", doanaA)
runanaB = anagen.MakeScript("test2B", intest, "TaggerOneResolution", doanaB)
print(f"[2][Test F] Created driver scripts for analysis")
print(f"  {runanaA}")
print(f"  {runanaB}")

# (3) Test trial manager ------------------------------------------------------

# create a trial manager
triman = emt.TrialManager("../configuration/run.config",
                          "../configuration/parameters.config",
                          "../configuration/objectives.config",
                          "test3")

# create new parameters to test
nupar3 = {
    "tagger1_width"  : 157.0,
    "tagger1_height" : 234.0,
    "tagger2_width"  : 143.0,
    "tagger2_height" : 178.0
}

# make run script
dorun3, ofiles3 = triman.MakeTrialScript(nupar3)
print(f"[3] Created driver script for entire trial:")
print(f"  script  = {dorun3}")
print(f"  outputs =")
pprint.pprint(ofiles3)

# end =========================================================================
