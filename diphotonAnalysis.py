# Things To Do
#  1. Add photon errors 
#  2. Add proton errors
#  3. Choose one diproton candidate per event
#  4. Verify SFs
#  5. Verify PU weight

#!/usr/bin/env python
import os, sys, re
from itertools import combinations
import numpy as np
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer, puWeight_2017

PI = 3.14159265358979323846
sqrts = 13000
lumi = 37200

data_ = False
sample = 'ggj'

mcs = [ ['ggj', 138.5, 4000000],['g+j',873.7,80000000],['qcd',117500,4000000],['wg',191.1,6300000],['zg',55.47,30000000], ['aqgc',3.86e-5,300000] ]

for mc in mcs:
    if sample == mc[0]:
        xsec = mc[1]
        n_events = mc[2]

sample_weight = xsec*lumi/n_events

class DiphotonAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True
        #self.n_passing = 0
        self.photonmapname = "EGamma_SF2D"
        self.photon_file = self.open_root("2017_PhotonsMVAwp90.root")
        self.photon_map = self.get_root_obj(self.photon_file, self.photonmapname)

    def open_root(self, path):
        r_file = ROOT.TFile.Open(path)
        if not r_file.__nonzero__() or not r_file.IsOpen(): raise NameError('File ' + path + ' not open')
        return r_file

    def get_root_obj(self, root_file, obj_name):
        r_obj = root_file.Get(obj_name)
        if not r_obj.__nonzero__(): raise NameError('Root Object ' + obj_name + ' not found')
        return r_obj
        
    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
        
        self.h_diph_mass=ROOT.TH1F('h_diph_mass', 'Diphoton Mass', 100, 350., 2500.)
        self.h_acop=ROOT.TH1F('h_acop', 'Diphoton Acoplanarity', 100, 0., 0.25)
        self.h_single_eta=ROOT.TH1F('h_single_eta', 'Single Photon Eta', 100, -3.0, 3.0)
        self.h_single_pt=ROOT.TH1F('h_single_pt', 'Single Photon pT', 100, 0., 750.0)
        self.h_xip=ROOT.TH1F('h_xip', '#xi _{#gamma#gamma}^{+}', 100, 0., 0.25)
        self.h_xim=ROOT.TH1F('h_xim', '#xi _{#gamma#gamma}^{-}', 100, 0., 0.25)
        self.h_nvtx=ROOT.TH1F('h_nvtx','Number Of Vertices', 75, 0., 75.)
        self.gr_matching=ROOT.TGraph()
        self.gr_matching.SetName('gr_matching')
        self.addObject( self.h_diph_mass )
        self.addObject( self.h_acop )
        self.addObject( self.h_single_eta )
        self.addObject( self.h_single_pt )        
        self.addObject( self.h_xip )
        self.addObject( self.h_xim )
        self.addObject( self.h_nvtx )
        self.addObject( self.gr_matching )

    def endJob(self):
        Module.endJob(self)
        #print ''
        #print ''
        #print 'Events:', self.n_passing
        #print ''
        #print ''

    # Apply mass cut
    def mass_cut(self,diph_mass):
        if diph_mass > 350: return True
        else: return False

    # Apply acoplanarity cut
    def acop_cut(self,acop):
        if acop < 0.005: return True
        else: return False

    # Apply photon ID
    def photon_id(self,pho1,pho2):
        if pho1.mvaID_WP90 == 1 and pho2.mvaID_WP90 == 1: return True         # loose MVA ID
        #if pho1.mvaID_WP80 == 1 and pho2.mvaID_WP80 == 1: return True        # tight MVA ID
        #if pho1.cutBasedBitmap >= 1 and pho2.cutBasedBitmap >= 1: return True # loose cutBased ID
        #if pho1.cutBasedBitmap >= 3 and pho2.cutBasedBitmap >= 3: return True # medium cutBased ID
        #if pho1.cutBasedBitmap >= 7 and pho2.cutBasedBitmap >= 7: return True # tight cutBased ID
        else: return False
        return True

    # Apply electron veto
    def electron_veto(self,pho1,pho2):
        if pho1.electronVeto == 1 and pho2.electronVeto == 1: return True
        else: return False

    # Apply eta veto
    def eta_cut(self,pho1,pho2):
        if abs(pho1.eta) > 2.5 or abs(pho2.eta) > 2.5: return False # Out of fiducial range
        if pho1.isScEtaEE and pho2.isScEtaEE: return False          # EEEE events
        if pho1.eta > 1.4442 and pho1.eta < 1.566: return False     # transition region
        if pho1.eta < -1.442 and pho1.eta > -1.566: return False    # transition region
        if pho2.eta > 1.4442 and pho2.eta < 1.566: return False     # transition region
        if pho2.eta < -1.442 and pho2.eta > -1.566: return False    # transition region
        return True

    # Get the SFs for MCs
    def efficiency(self,pt,eta_sc):
        bin_x = min( max( self.photon_map.GetXaxis().FindBin( eta_sc ), 1 ), self.photon_map.GetXaxis().GetNbins() )
        bin_y = min( max( self.photon_map.GetYaxis().FindBin( pt ), 1 ), self.photon_map.GetYaxis().GetNbins() )
        return self.photon_map.GetBinContent( bin_x, bin_y )

    # Check for two opposite-side protons
    def two_protons(self,protons):
        if len(protons) >= 2:
            proton_45 = proton_56 = False
            for proton in protons:
                if proton.sector45 == 1: proton_45 = True
                elif proton.sector56 == 1: proton_56 = True
            if proton_45 and proton_56: return True
            else: return False 
        else: return False
        #return True

    def mass_matching(self,diph_mass,pro1,pro2):
        mass = sqrts*math.sqrt(pro1.xi*pro2.xi)
        #error = 0.5 * math.sqrt( math.pow(pro1.xiError/pro1.xi,2) + math.pow(pro2.xiError/pro2.xi,2) )
        error = mass*0.2
        if diph_mass > (mass - error) and diph_mass < (mass + error): return True
        else: return False
        
    def rap_matching(self,diph_rap,pro1,pro2):
        rap = 0.5*math.log(pro1.xi/pro2.xi)
        if rap > (diph_rap - 0.2) and rap < (diph_rap + 0.2): return True
        else: return False

    def analyze(self, event):
        if data_: protons = Collection(event, "Proton_singleRP")
        photons = Collection(event, "Photon")
        pu_weight = event.puWeight
        #print 'pu_weight:', pu_weight

        #if self.two_protons(protons):

        it = 0
        
        for combo in combinations(range(0,len(photons)),2):
            pho1, pho2 = photons[combo[0]], photons[combo[1]]
            if pho1.pt < 75 or pho2.pt < 75: continue
            diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
            diph_mass = diph_p4.M()
            diph_rap = diph_p4.Rapidity()
            delta_phi = pho1.p4().DeltaPhi(pho2.p4())
            acop = 1 - abs(delta_phi)/PI
            xip = 1/13000.*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
            xim = 1/13000.*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )
            if data_: 
                weight = 1
            else: 
                s_weight = pu_weight*sample_weight

            #if self.photon_id(pho1,pho2):
                #if self.electron_veto(pho1,pho2):
                    #if self.mass_cut(diph_mass):
                        #if self.eta_cut(pho1,pho2):
                            #if self.acop_cut(acop):
                                #if xip <= 0.2 and xip >= 0.015:
                                    #if xim <= 0.2 and xim >= 0.015:
                                        #if it == 0:
                                            #self.n_passing += 1
                                            #it += 1
                                            #continue
                                        #else: continue

            # Make selection cuts
            if \
               self.photon_id(pho1,pho2) and \
               self.electron_veto(pho1,pho2) and \
               self.eta_cut(pho1,pho2) and \
               self.mass_cut(diph_mass): #and \
               #self.acop_cut(acop):
                
                if not data_:
                    eff_pho1 = self.efficiency(pho1.pt,pho1.eta)
                    eff_pho2 = self.efficiency(pho2.pt,pho2.eta)
                    weight = s_weight * ( eff_pho1*eff_pho2 )

                #for combo in combinations(range(0,len(protons)),2):
                    #pro1, pro2 = protons[combo[0]], protons[combo[1]]
                    #if pro1.sector45 == pro2.sector45: continue
                    
                    # SetPoint for matching plot
                    #self.gr_matching.SetPoint( self.gr_matching.GetN(),\
                        #sqrts*math.sqrt(pro1.xi*pro2.xi) / diph_mass,\
                        #0.5*math.log(pro1.xi/pro2.xi) - diph_rap )

                    #if self.mass_matching(diph_mass,pro1,pro2) and self.rap_matching(diph_rap,pro1,pro2):
                        #print "Passing cuts!"
                        #print "R:L:E", str(event.run)+":"+str(event.luminosityBlock)+":"+str(event.event)
                        #print "Diphoton mass:", diph_mass
                        #print "Diphoton rapidity:", diph_rap
                        #print "Acoplanarity:", acop
                        #print "Pho1 pT:", pho1.pt, "Pho2 pT:", pho2.pt
                        #print "Pho1 eta:", pho1.eta, "Pho2 eta:", pho2.eta
                        #print "xi1:", pro1.xi, "xi2:", pro2.xi
                        #print "Diproton mass:", sqrts*math.sqrt(pro1.xi*pro2.xi)
                        #print "Diproton rapidity:", 0.5*math.log(pro1.xi/pro2.xi)
                        #print "" 
                                
                # Ploting
                self.h_diph_mass.Fill(diph_mass,weight)
                self.h_acop.Fill(acop,weight)
                self.h_single_eta.Fill(pho1.eta,weight), self.h_single_eta.Fill(pho2.eta,weight)
                self.h_single_pt.Fill(pho1.pt,weight), self.h_single_pt.Fill(pho2.pt,weight)
                self.h_xip.Fill(xip,weight), self.h_xim.Fill(xim,weight)
                self.h_nvtx.Fill(event.PV_npvs,weight) 

        
        return True

preselection=""
files=[
#"nanoAOD_Run2017B_Skim.root",
#"nanoAOD_Run2017C_Skim.root",
#"nanoAOD_Run2017D_Skim.root",
#"nanoAOD_Run2017E_Skim.root",
#"nanoAOD_Run2017F_Skim.root"

"nanoAOD_ggj_Skim_test.root"
#"nanoAOD_GGJ2017_Skim.root"
#"nanoAOD_gj_2017_Skim.root"
#"nanoAOD_qcd_2017_Skim.root"
#"nanoAOD_wg_2017_Skim.root"
#"nanoAOD_zg_2017_Skim.root"

#"nanoAOD_aqgc_Skim.root"
]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[DiphotonAnalysis()],noOut=True,histFileName="histOut_ggj_inelastic_test.root",histDirName="plots")
p.run()


