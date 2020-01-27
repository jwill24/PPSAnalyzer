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

PI = 3.14159265358979323846
sqrts = 13000
lumi = 37200


class ResolutionStudy(Module):
    def __init__(self):
        self.writeHistFile=True

        self.h_mass_res=ROOT.TH1F('h_mass_res', 'Diphoton Mass Resolution', 100, -0.1, 0.1)
        self.h_rap_diff=ROOT.TH1F('h_rap_diff', 'Diphoton Rapidity Resolution', 100, -0.3, 0.3)
        self.h_pt_res=ROOT.TH1F('h_pt_res', 'Single #gamma p_{T} Resolution', 100, -0.25, 0.25)
        self.h_phi_diff=ROOT.TH1F('h_phi_diff', 'Single Photon #phi Resolution', 100, -0.01, 0.01)
        self.h_dphi_diff=ROOT.TH1F('h_dphi_diff', '#Delta#phi Resolution', 100, -0.01, 0.01)
        self.h_eta_res=ROOT.TH1F('h_eta_res', '#eta Resolution', 100, -0.25, 0.25) 
        self.h_eta_diff=ROOT.TH1F('h_eta_diff', '#eta Resolution', 100, -0.25, 0.25) 
        self.h_ratio_diff=ROOT.TH1F('h_ratio_diff', 'Diphoton p_{T} Ratio Resolution', 100, -0.25, 0.25)
        self.h_diphpt_diff=ROOT.TH1F('h_diphpt_diff', 'Diphoton pT Resolution', 100, 0, 20)
        self.h_xi_res=ROOT.TH1F('h_xi_res', 'Single Photon #xi Resolution', 100, -0.25,0.25)
        self.h_logxi_diff=ROOT.TH1F('h_logxi_diff', 'log(1/#xi) Difference', 100, -0.25,0.25)

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        self.addObject( self.h_mass_res )
        self.addObject( self.h_rap_diff )
        self.addObject( self.h_pt_res )
        self.addObject( self.h_phi_diff )
        self.addObject( self.h_dphi_diff )
        self.addObject( self.h_eta_res )
        self.addObject( self.h_eta_diff )
        self.addObject( self.h_ratio_diff )
        self.addObject( self.h_diphpt_diff )
        self.addObject( self.h_xi_res )
        self.addObject( self.h_logxi_diff )

    def endJob(self):
        Module.endJob(self)

        print ''
        print 'Mass RMS:', self.h_mass_res.GetRMS()
        print 'Rapidity RMS:', self.h_rap_diff.GetRMS()
        print 'Phi RMS:', self.h_phi_diff.GetRMS()
        print 'Delta Phi RMS:', self.h_dphi_diff.GetRMS()
        print 'pT ratio RMS:', self.h_ratio_diff.GetRMS()
        print 'xi RMS:', self.h_xi_res.GetRMS()
        print ''

    # Apply photon ID
    def photon_id(self,pho1,pho2):
        if pho1.mvaID_WP90 == 1 and pho2.mvaID_WP90 == 1: return True 
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

    # Apply mass cut
    def mass_cut(self,diph_mass):
        if diph_mass > 350: return True
        else: return False

    # Apply electron veto
    def electron_veto(self,pho1,pho2):
        if pho1.electronVeto == 1 and pho2.electronVeto == 1: return True
        else: return False
    
    # Apply acoplanarity cut
    def acop_cut(self,acop):
        if acop < 0.005: return True
        else: return False

    def analyze(self, event):
        photons = Collection(event, "Photon")
        lhe = Collection(event, "LHEPart")
        
        for combo in combinations(range(0,len(photons)),2):
            pho1, pho2 = photons[combo[0]], photons[combo[1]]
            if pho1.pt < 75 or pho2.pt < 75: continue
            diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
            diph_mass = diph_p4.M()
            diph_rap = diph_p4.Rapidity()
            diph_pt = diph_p4.Pt()
            delta_phi = pho1.p4().DeltaPhi(pho2.p4())
            acop = 1 - abs(delta_phi)/PI
            xip = 1/13000.*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
            xim = 1/13000.*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )
            
            if not self.photon_id(pho1,pho2): continue
            if not self.eta_cut(pho1,pho2): continue
            if not self.mass_cut(diph_mass): continue
            if not self.electron_veto(pho1,pho2): continue
            if not self.acop_cut(acop): continue
            

            part1, part2 = lhe[2], lhe[3]
            if ( abs(part1.p4().Pz()-pho1.p4().Pz()) ) > ( abs(part2.p4().Pz()-pho1.p4().Pz()) ): part1, part2 = lhe[3], lhe[2] 
            part_p4 = ROOT.TLorentzVector( part1.p4() + part2.p4() )
            part_mass = part_p4.M()
            part_rap = part_p4.Rapidity()
            part_pt = part_p4.Pt()
            part_dphi = part1.p4().DeltaPhi(part2.p4())
            part_acop = 1 - abs(part_dphi)/PI
            part_xip = 1/13000.*( part1.pt*math.exp(part1.eta)+part2.pt*math.exp(part2.eta) )
            part_xim = 1/13000.*( part1.pt*math.exp(-1*part1.eta)+part2.pt*math.exp(-1*part2.eta) )

            self.h_mass_res.Fill( (diph_mass-part_mass)/part_mass )
            self.h_rap_diff.Fill( (diph_rap-part_rap) )
            self.h_pt_res.Fill( (pho1.pt-part1.pt)/part1.pt )
            self.h_pt_res.Fill( (pho2.pt-part2.pt)/part2.pt )
            self.h_phi_diff.Fill( (pho1.phi-part1.phi) )
            self.h_phi_diff.Fill( (pho2.phi-part2.phi) )
            self.h_dphi_diff.Fill( (delta_phi-part_dphi) )
            self.h_eta_res.Fill( (pho1.eta-part1.eta)/part1.eta )
            self.h_eta_res.Fill( (pho2.eta-part2.eta)/part2.eta )
            self.h_eta_diff.Fill( (pho1.eta-part1.eta) )
            self.h_eta_diff.Fill( (pho2.eta-part2.eta) )
            self.h_ratio_diff.Fill( ((pho1.pt/pho2.pt)-(part1.pt/part2.pt)) )
            self.h_diphpt_diff.Fill( (diph_pt-part_pt) )
            self.h_xi_res.Fill( (xip-part_xip)/part_xip )
            self.h_xi_res.Fill( (xim-part_xim)/part_xim )
            self.h_logxi_diff.Fill( math.log(1/xip)-math.log(1/part_xip) )
            self.h_logxi_diff.Fill( math.log(1/xim)-math.log(1/part_xim) )

        return True



preselection=''
files=["Skims/nanoAOD_aqgc2017_Skim.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[ResolutionStudy()],noOut=True,histFileName="histOut_resolution_aqgc.root",histDirName="plots")
p.run()
