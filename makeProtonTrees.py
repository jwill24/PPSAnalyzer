#!/usr/bin/env python
import os, sys, re
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class MakeProtonTrees(Module):

    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
 
    def endJob(self):
        Module.endJob(self)

    def analyze(self, event):
    

        return True

preselection=''
files=['Skims/nanoAOD_Run2017B_Skim.root']
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[MakeProtonTrees()],noOut=True,histFileName='test.root',histDirName="plots",maxEntries=5)
p.run()
