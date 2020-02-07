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
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/160BBBD6-645E-FE4E-BB4C-4A657C8BCD11.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/23AE3FB4-D814-E544-85B8-7B001BBA8416.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/6844D099-CC6F-7940-8455-23185E0308C8.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/687DB9BB-82D1-2C49-B967-B2508D237ADA.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/80455F65-985C-AA4D-A6FC-0EB1B55C2303.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/8D625D30-C72D-0747-B45F-FDDFC7ABE4A2.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/9A5C1FCA-43DD-B244-B58A-9D277A8A4698.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/F902413C-35DF-624C-9ECC-C5B4F8BDBF08.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/250000/09E97185-D9B7-5846-BC6F-7D4DB0B5403E.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/250000/B4642F0E-7FFC-1D46-93E3-11B59C616558.root',
'/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/mc/RunIIFall17NanoAODv5/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/250000/C541F35D-DB04-C448-8687-75737F0FF800.root'
]

p=PostProcessor(".",fnames,"HLT_DoublePhoton70 == 1","",[puAutoWeight_2017()],provenance=True,haddFileName="nanoAOD_tt2017_Skim.root")
p.run()
