#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import PrefCorr

fnames=[
'/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PhysicsTools/NanoAOD/test/testing_tt.root'
]

# 2017 MC
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[puAutoWeight_2017(),PrefCorr()],provenance=True,haddFileName="nanoAOD_2017_withLPC_Skim.root")
# 2017 Data
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[],provenance=True,haddFileName="nanoAOD_Run2017C_noLPC_Skim.root")
# 2018 MC
p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[puAutoWeight_2018()],provenance=True,haddFileName="nanoAOD_tt2018_test_Skim.root")
# 2018 Data
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[],provenance=True,haddFileName="nanoAOD_dataTest_Skim.root")

p.run()
