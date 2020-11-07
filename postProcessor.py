#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import PrefCorr

fnames=[

]

# 2016 Data
p=PostProcessor(".",fnames,"HLT_DoublePhoton60 == 1","keep_drop.txt",[],provenance=True,haddFileName="nanoAOD_Run2016B_Skim.root")

# 2017 MC
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[puAutoWeight_2017(),PrefCorr()],provenance=True,haddFileName="nanoAOD_aqgc2017_Skim.root")

# 2017 Data
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[],provenance=True,haddFileName="nanoAOD_Run2017F_Skim.root")

# 2018 MC
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[puAutoWeight_2018()],provenance=True,haddFileName="nanoAOD_ggj2018_Skim.root")

# 2018 Data
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[],provenance=True,haddFileName="nanoAOD_Run2018A_Skim.root")

p.run()
