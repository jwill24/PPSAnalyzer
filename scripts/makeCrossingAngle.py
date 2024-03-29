#!/usr/bin/env python                                                                                                                                                                                                                                  import os, sys
import glob
import tqdm
import ROOT as r
from ROOT import gROOT
r.PyConfig.IgnoreCommandLineOptions = True

year = '2018'
#files = glob.glob('../Skims/%s/nanoAOD_Run*_Skim.root' % year)
files = glob.glob('../Skims/%s/nanoAOD_Run2018C_Skim.root' % year)

print(files)

hxang = r.TH1F('hxang', '', 42, 120, 162)

for f in files:
    print 'Working on file %s' % f
    tf = r.TFile(f)
    entries = tf.Get('Events').GetEntries()
    denom = round(entries/100);
    with tqdm.tqdm(total=100, leave=True) as pbar:
        for i, event in enumerate(tf.Events):
            hxang.Fill(event.LHCInfo_crossingAngle)
            if i%denom == 0: pbar.update(1)
    pbar.close()
    print ''

outputFile = r.TFile('CrossingAngles%s.root' % year, 'RECREATE')
outputFile.cd()
hxang.Write()
outputFile.Close()


