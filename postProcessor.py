#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

pufile_data2017="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-goldenJSON-13tev-2018-99bins_withVar.root" % os.environ['CMSSW_BASE']
pufile_mc2017="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileup2017.root" % os.environ['CMSSW_BASE']
puWeight_2017 = lambda : puWeightProducer(pufile_mc2017,pufile_data2017,"pu_mc","pileup",verbose=False, doSysVar=True)
puAutoWeight_2017 = lambda : puWeightProducer("auto",pufile_data2017,"pu_mc","pileup",verbose=False)


fnames=[
'nanoAOD_files/aqgc_nanoAOD2017.root'
]

p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","",[puWeight_2017()],provenance=True,haddFileName="nanoAOD_aqgc2017_Skim.root")
p.run()
