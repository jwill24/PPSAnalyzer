#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

pufile_data2017="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-goldenJSON-13tev-2018-99bins_withVar.root" % os.environ['CMSSW_BASE']
pufile_mc2017="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileup2017.root" % os.environ['CMSSW_BASE']
#puWeight_2017 = lambda : puWeightProducer(pufile_mc2017,pufile_data2017,"pu_mc","pileup",verbose=False, doSysVar=True)
puAutoWeight_2017 = lambda : puWeightProducer("auto",pufile_data2017,"pu_mc","pileup",verbose=False)


fnames=[
'nanoAOD_files/8C87296C-EDBD-3846-A764-F8CC2456EE8C.root',
'nanoAOD_files/BDED178E-505B-A347-81F5-952F2FD802E6.root',
'nanoAOD_files/C72862D4-6954-F243-9963-7B2AC3CBCE1D.root'
]

p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","",[puAutoWeight_2017()],provenance=True,haddFileName="nanoAOD_ggj_Skim_test2.root")
p.run()
