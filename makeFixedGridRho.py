#!/usr/bin/env python                                                                                                                                                                                                                                  import os, sys
import glob
import tqdm
import ROOT as r
from ROOT import gROOT
r.PyConfig.IgnoreCommandLineOptions = True

year = '2017'
files = glob.glob('Skims/%s/nanoAOD_Run*_Skim.root' % year)

h = r.TH1F('h', '', 58, 0.0, 58.0)

for f in files:
    print 'Working on file %s' % f
    tf = r.TFile(f)
    entries = tf.Get('Events').GetEntries()
    denom = round(entries/100);
    with tqdm.tqdm(total=100, leave=True) as pbar:
        for i, event in enumerate(tf.Events):
            h.Fill(event.fixedGridRhoFastjetAll)
            if i%denom == 0: pbar.update(1)
            if i == 1000: break
    pbar.close()
    print ''

outputFile = r.TFile('dataFixedGridRho_%s.root' % year, 'RECREATE')
outputFile.cd()
h.Write()
outputFile.Close()


