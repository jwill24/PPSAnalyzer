#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import PrefCorr

fnames=[
'nanoAOD_test_file.root'
]

# 2017 MC
p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[puAutoWeight_2017(),PrefCorr()],provenance=True,haddFileName="nanoAOD_2017_withLPC_Skim.root")
# 2017 Data
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[],provenance=True,haddFileName="nanoAOD_Run2017C_noLPC_Skim.root")
# 2018 MC
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[puAutoWeight_2018()],provenance=True,haddFileName="nanoAOD_zg2018_Skim.root")
# 2018 Data
#p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","keep_drop.txt",[],provenance=True,haddFileName="nanoAOD_dataRun2018A_Skim.root")

p.run()
