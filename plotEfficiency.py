#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from common import open_root, get_root_obj, mass_cut, hoe_cut, acop_cut, photon_id, electron_veto, xi_cut, eta_cut
from common import mass, rapidity, mass_err, rapidity_err, mass_matching, rap_matching

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, TGraphErrors
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)

PI = 3.141592653589793
years = ['2017']
s_years = '+'.join(years)
# year, events, zeta1, zeta2, xsec_bare, xsec
samples = [['2017',300000,10e-14,10e-14,5.0e-3,3.8595147826276311e-5]]
v_passing = []
pots_accept = [['45N',0.02],['45F',0.02],['56N',0.02],['56F',0.02]] #FIXME


class plotEfficiency(Module):
    def __init__(self):
        self.writeHistFile=True

        self.passing_2016, self.passing_2017, self.passing_2018 = 0, 0, 0
        self.total_2016, self.total_2017, self.total_2018 = 0, 0, 0

        self.gr_acc = ROOT.TGraph2D()
        self.gr_eff = ROOT.TGraph2D()

        # Get SF hists for ID and CSEV
        self.photonmapname = "EGamma_SF2D"

        self.photon_file_16 = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/egammaEffi.txt_EGM2D_Pho_wp90_UL16.root")
        self.csev_file_16 = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/CSEV_SummaryPlot_UL16_preVFP.root")
        
        self.photon_file_17 = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/egammaEffi.txt_EGM2D_PHO_MVA90_UL17.root")
        self.csev_file_17 = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/CSEV_SummaryPlot_UL17.root")
        
        self.photon_file_18 = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/egammaEffi.txt_EGM2D_Pho_wp90.root_UL18.root")
        self.csev_file_18 = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/CSEV_SummaryPlot_UL18.root")

        self.csevmapname = "MVAID/SF_CSEV_MVAID"

        self.csev_map_16 = get_root_obj(self.csev_file_16, self.csevmapname)
        self.photon_map_16 = get_root_obj(self.photon_file_16, self.photonmapname)

        self.csev_map_17 = get_root_obj(self.csev_file_17, self.csevmapname)
        self.photon_map_17 = get_root_obj(self.photon_file_17, self.photonmapname)

        self.csev_map_18 = get_root_obj(self.csev_file_18, self.csevmapname)
        self.photon_map_18 = get_root_obj(self.photon_file_18, self.photonmapname)


    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        self.addObject( self.gr_acc )
        self.addObject( self.gr_eff )

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.fileName = inputFile.GetName()

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def endJob(self):
        Module.endJob(self)
        
        print 'Passing 2016:', self.passing_2016
        print 'Efficiency 2016:', float(self.passing_2016)/float(self.total_2016)

        print 'Passing 2017:', self.passing_2017
        print 'Efficiency 2017:', float(self.passing_2017)/float(self.total_2017)

        print 'Passing 2018:', self.passing_2018
        print 'Efficiency 2018:', float(self.passing_2018)/float(self.total_2018)


        for s in samples:
            self.gr_acc.SetPoint( self.gr_acc.GetN(), s[2]*1.0e12, s[3]*1.0e12, float(s[5])/float(s[4]) )

    
    # Get the SFs for MCs
    def efficiency(self,year,pt,eta_sc,r9):
        
        #if nSelect != 2.5 and nSelect < 3: return 1.0

        if year == '2016':
            bin_x = min( max( self.photon_map_16.GetXaxis().FindBin( eta_sc ), 1 ), self.photon_map_16.GetXaxis().GetNbins() )
            bin_y = min( max( self.photon_map_16.GetYaxis().FindBin( pt ), 1 ), self.photon_map_16.GetYaxis().GetNbins() )
            id_sf = self.photon_map_16.GetBinContent( bin_x, bin_y )
            #id_sf -= self.photon_map_16.GetBinError( bin_x, bin_y )

            if abs(eta_sc) <= 1.4442: bin_r9 = 2 if r9 > 0.94 else 3
            else: bin_r9 = 5 if r9 > 0.94 else 6
            csev_sf = self.csev_map_16.GetBinContent( bin_r9 )

        elif year == '2017':
            bin_x = min( max( self.photon_map_17.GetXaxis().FindBin( eta_sc ), 1 ), self.photon_map_17.GetXaxis().GetNbins() )
            bin_y = min( max( self.photon_map_17.GetYaxis().FindBin( pt ), 1 ), self.photon_map_17.GetYaxis().GetNbins() )
            id_sf = self.photon_map_17.GetBinContent( bin_x, bin_y )
            #id_sf -= self.photon_map_17.GetBinError( bin_x, bin_y )

            if abs(eta_sc) <= 1.4442: bin_r9 = 2 if r9 > 0.94 else 3
            else: bin_r9 = 5 if r9 > 0.94 else 6
            csev_sf = self.csev_map_17.GetBinContent( bin_r9 )

        elif year == '2018':
            bin_x = min( max( self.photon_map_18.GetXaxis().FindBin( eta_sc ), 1 ), self.photon_map_18.GetXaxis().GetNbins() )
            bin_y = min( max( self.photon_map_18.GetYaxis().FindBin( pt ), 1 ), self.photon_map_18.GetYaxis().GetNbins() )
            id_sf = self.photon_map_18.GetBinContent( bin_x, bin_y )
            #id_sf -= self.photon_map_18.GetBinError( bin_x, bin_y )


            if abs(eta_sc) <= 1.4442: bin_r9 = 2 if r9 > 0.94 else 3
            else: bin_r9 = 5 if r9 > 0.94 else 6
            csev_sf = self.csev_map_18.GetBinContent( bin_r9 )

        return id_sf*csev_sf


    def analyze(self, event):
        photons = Collection(event, "Photon")
        if len(photons) < 2: return

        # Choose the best diphoton candidate
        acop = 999.0
        pho1, pho2 = photons[0], photons[1]
        for combo in combinations(range(0,len(photons)),2):
            p1, p2 = photons[combo[0]], photons[combo[1]]
            if p1.pt < 100.0 or p2.pt <100.0: continue
            tmp_acop =  1.0 - abs( p1.p4().DeltaPhi(p2.p4()) ) / PI
            if tmp_acop > acop: continue
            acop = tmp_acop
            pho1, pho2 = p1, p2


        # Calculate diphoton variables
        diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
        diph_mass = diph_p4.M()
        diph_rap = diph_p4.Rapidity()
        delta_phi = pho1.p4().DeltaPhi(pho2.p4())
        xip = 1/13000.0*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
        xim = 1/13000.0*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )
        pt_thresh = 100.0 if '2016' in self.fileName else 100.0
        
        # Make selection cuts
        if pho1.pt < pt_thresh or pho2.pt < pt_thresh: return

        if '2016' in self.fileName: 
            self.total_2016 += 1
            year = '2016'
        elif '2017' in self.fileName: 
            self.total_2017 += 1
            year = '2017'
        elif '2018' in self.fileName: 
            self.total_2018 += 1
            year = '2018'

        if not hoe_cut(pho1,pho2): return
        if not eta_cut(pho1,pho2): return
        if not mass_cut(diph_mass): return
        if not photon_id(pho1,pho2): return
        if not electron_veto(pho1,pho2): return
        if not acop_cut(acop): return
        if not xi_cut(xip,xim): return



        eff_pho1, eff_pho2 = self.efficiency(year,pho1.pt,pho1.eta,pho1.r9), self.efficiency(year,pho2.pt,pho2.eta,pho2.r9)
        w = eff_pho1 * eff_pho2

        if '2016' in self.fileName: self.passing_2016 += w #1
        elif '2017' in self.fileName: self.passing_2017 += w #1
        elif '2018' in self.fileName: self.passing_2018 += w #1
        
        return True


preselection=''
files=[
    #'Skims/2016/nanoAOD_aqgc2016_e-13_e-13_Skim.root',
    #'Skims/2017/nanoAOD_aqgc2017_5e-13_0_Skim.root',
    #'Skims/2018/nanoAOD_aqgc2018_e-13_e-13_Skim.root',

    'Skims/2016/nanoAOD_alp2016_fe-1_m500_Skim.root',
    'Skims/2017/nanoAOD_alp2017_fe-1_m500_Skim.root',
    'Skims/2018/nanoAOD_alp2018_fe-1_m500_Skim.root',

    #'Skims/2016/nanoAOD_LbL2016_SM_Skim.root',
    #'Skims/2017/nanoAOD_LbL2017_SM_Skim.root',
    #'Skims/2018/nanoAOD_LbL2018_SM_Skim.root'
]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[plotEfficiency()],noOut=True,histFileName="histOut_efficiency.root",histDirName="plots")
p.run()



