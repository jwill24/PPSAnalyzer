# To Do List
#   1. Change cuts to be consistent with diphotonAnalysis.py

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

#ROOT.gStyle.SetOptStat(0)

PI = 3.14159265358979323846
sqrts = 13000

signal = False

#photon_id = 'MVA_WP90'
#photon_id = 'cutBased_loose'
photon_id = 'highPt'

class SignalStudy(Module):
    def __init__(self):
        self.writeHistFile=True
        '''
        self.v_id = [[100,200,0,0],
                [200,400,0,0],
                [400,600,0,0],
                [600,800,0,0],
                [800,1000,0,0],
                [1000,1200,0,0],
                [1200,1400,0,0]]

        self.v_id = [[100,200,0,0],
                [200,300,0,0],
                [300,400,0,0],
                [400,500,0,0],
                [500,600,0,0],
                [600,700,0,0],
                [700,800,0,0],
                [800,900,0,0],
                [900,1000,0,0],
                [1000,1100,0,0],
                [1100,1200,0,0],
                [1200,1300,0,0],
                [1300,1400,0,0]]
        '''
        self.v_id = [[100,200,0,0,0,0,0],
                [200,300,0,0,0,0,0],
                [300,400,0,0,0,0,0],
                [400,500,0,0,0,0,0],
                [500,600,0,0,0,0,0],
                [600,700,0,0,0,0,0],
                [700,800,0,0,0,0,0],
                [800,900,0,0,0,0,0],
                [900,1000,0,0,0,0,0],
                [1000,1100,0,0,0,0,0],
                [1100,1200,0,0,0,0,0],
                [1200,1300,0,0,0,0,0],
                [1300,1400,0,0,0,0,0]]

        self.total = 0

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
        
        self.h_ratio=ROOT.TH1F('h_ratio', photon_id+'ID Efficiency', len(self.v_id), 0, len(self.v_id))
        self.h_cuts_2d=ROOT.TH2F('h_cuts_2d', '', len(self.v_id), 0, len(self.v_id), 5, 0, 5)

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

        rootFile = ROOT.TFile('cutTest.root', 'RECREATE')
        #total, passing, comb_total, comb_passing = 0, 0, 0, 0
        cut_names = ['Iso Chg', 'Iso All', 'H/E', 'R_{9}', '#sigma_{i#etai#ta}']

        for i, v in enumerate(self.v_id):
            '''
            total = float(v[2])
            passing = float(v[3])
            comb_total += total
            comb_passing += passing
            try: ratio = 100*passing/total
            except: ratio = 0
            if signal: self.h_ratio.SetBinContent(i+1, ratio)
            else: self.h_ratio.SetBinContent(i+1, 100-ratio)
            self.h_ratio.GetXaxis().SetBinLabel(i+1, str(self.v_id[i][1]))
            print 'i:', i, 'bin:', v[1], 'efficiency:', ratio
            '''
            self.h_cuts_2d.GetXaxis().SetBinLabel(i+1, str(self.v_id[i][1]))
            for j, c in enumerate(cut_names):
                self.h_cuts_2d.GetYaxis().SetBinLabel(j+1, c)
                self.h_cuts_2d.SetBinContent(i+1, j+1, v[j+2])
            

        #print ''
        #print 'Signal' if signal else 'Background', 'ID:', photon_id, 'Total:', comb_total, 'Passing:', comb_passing
        #print ''
        '''
        self.h_ratio.SetLineColor(ROOT.kWhite)
        self.h_ratio.GetXaxis().SetTitleOffset(1.3)
        self.h_ratio.GetYaxis().SetTitleOffset(1.5)
        
        g_ratio = ROOT.TGraph(self.h_ratio)
        g_ratio.SetMarkerSize(0.7)
        g_ratio.SetMarkerStyle(20)
                
        x = self.h_ratio.GetXaxis()
        x.SetTitleSize(20)
        x.SetTitleFont(43)
        x.SetLabelFont(43)
        x.SetLabelSize(15)
        x.SetTitle('p_{T}^{#gamma}')
        y = self.h_ratio.GetYaxis()
        y.SetTitle('Efficiency %')
        y.SetTitleSize(20)
        y.SetTitleFont(43)
        y.SetLabelFont(43)
        y.SetLabelSize(20)
        y.SetRangeUser(40,100) if signal else y.SetRangeUser(0,105)
        
        self.h_ratio.Write()
        g_ratio.Write()
        '''
        self.h_cuts_2d.Draw('colz')
        self.h_cuts_2d.Write()
        rootFile.Close()
        
    # Apply photon ID
    def photon_id(self,pho1,pho2):
        if '90' in photon_id:
            if pho1.mvaID_WP90 == 1 and pho2.mvaID_WP90 == 1: return True 
            else: return False
        elif '80' in photon_id:
            if pho1.mvaID_WP80 == 1 and pho2.mvaID_WP80 == 1: return True
            else: return False
        elif 'loose' in photon_id:
            if pho1.cutBasedBitmap >= 1 and pho2.cutBasedBitmap >= 1: return True
            else: return False
        elif 'medium' in photon_id:
            if pho1.cutBasedBitmap >= 3 and pho2.cutBasedBitmap >= 3: return True
            else: return False
        elif 'tight' in photon_id:
            if pho1.cutBasedBitmap >= 7 and pho2.cutBasedBitmap >= 7: return True
            else: return False
        elif 'highPt' in photon_id:
            return self.highPtID(pho1,pho2)


    # Apply high pT photon ID (AN2018_234)
    def highPtID(self,pho1,pho2):
        if pho1.isScEtaEB:
            if pho1.pfRelIso03_chg > 5: return False
            if pho1.pfRelIso03_all > 2.75: return False
            if pho1.hoe > 0.05: return False
            if pho1.r9 < 0.8: return False
            if pho1.sieie > 0.0112: return False # FIXME
        elif pho1.isScEtaEE:
            if pho1.pfRelIso03_chg > 5: return False
            if pho1.pfRelIso03_all > 2: return False
            if pho1.hoe > 0.05: return False
            if pho1.r9 < 0.8: return False
            if pho1.sieie > 0.0280: return False # FIXME
        if pho2.isScEtaEB:
            if pho1.pfRelIso03_chg > 5: return False
            if pho1.pfRelIso03_all > 2.75: return False
            if pho1.hoe > 0.05: return False
            if pho1.r9 < 0.8: return False
            if pho1.sieie > 0.0112: return False # FIXME
        elif pho2.isScEtaEE:
            if pho1.pfRelIso03_chg > 5: return False
            if pho1.pfRelIso03_all > 2: return False
            if pho1.hoe > 0.05: return False
            if pho1.r9 < 0.8: return False
            if pho1.sieie > 0.0280: return False # FIXME
        return True

    # Apply eta veto
    def eta_cut(self,pho1,pho2):
        if abs(pho1.eta) > 2.5 or abs(pho2.eta) > 2.5: return False # Out of fiducial range
        #if pho1.isScEtaEE and pho2.isScEtaEE: return False          # EEEE events
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
        
        '''
        for combo in combinations(range(0,len(photons)),2):
            pho1, pho2 = photons[combo[0]], photons[combo[1]]
            if pho1.pt < 100 or pho2.pt < 100: continue
            diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
            diph_mass = diph_p4.M()
            diph_rap = diph_p4.Rapidity()
            diph_pt = diph_p4.Pt()
            delta_phi = pho1.p4().DeltaPhi(pho2.p4())
            acop = 1 - abs(delta_phi)/PI
            xip = 1/13000.*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
            xim = 1/13000.*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )
        '''

        if len(photons) < 2: return
        pho1, pho2 = photons[0], photons[1]
        pt1, pt2 = pho1.pt, pho2.pt
        if pho1.pt < 100 or pho2.pt < 100: return
        diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
        diph_mass = diph_p4.M()

        if not self.eta_cut(pho1,pho2): return
        if not self.mass_cut(diph_mass): return
        
        self.total += 1

        # Fill 2D cut plots
        for v in self.v_id:
            if pt1 > v[0] and pt1< v[1]:
                if pho1.isScEtaEB:
                    if pho1.pfRelIso03_chg > 5:    v[2] += 1
                    if pho1.pfRelIso03_all > 2.75: v[3] += 1
                    if pho1.hoe > 0.05:            v[4] += 1
                    if pho1.r9 < 0.8:              v[5] += 1
                    if pho1.sieie > 0.0112:        v[6] += 1
                elif pho1.isScEtaEE:
                    if pho1.pfRelIso03_chg > 5:    v[2] += 1
                    if pho1.pfRelIso03_all > 2:    v[3] += 1
                    if pho1.hoe > 0.05:            v[4] += 1
                    if pho1.r9 < 0.8:              v[5] += 1
                    if pho1.sieie > 0.0280:        v[6] += 1
            if pt2> v[0] and pt2 < v[1]:
                if pho2.isScEtaEB:
                    if pho1.pfRelIso03_chg > 5:    v[2] += 1
                    if pho1.pfRelIso03_all > 2.75: v[3] += 1
                    if pho1.hoe > 0.05:            v[4] += 1
                    if pho1.r9 < 0.8:              v[5] += 1
                    if pho1.sieie > 0.0112:        v[6] += 1
                elif pho2.isScEtaEE:
                    if pho1.pfRelIso03_chg > 5:    v[2] += 1
                    if pho1.pfRelIso03_all > 2:    v[3] += 1
                    if pho1.hoe > 0.05:            v[4] += 1
                    if pho1.r9 < 0.8:              v[5] +=1 
                    if pho1.sieie > 0.0280:        v[6] += 1

        '''
        # Increment total for pT bins
        for v in self.v_id:
            if pt1 > v[0] and pt1 < v[1]: v[2] += 1
            if pt2 > v[0] and pt2 < v[1]: v[2] += 1

        if not self.photon_id(pho1,pho2): return
        if not self.electron_veto(pho1,pho2): return
        #if not self.acop_cut(acop): continue
        

        #Increment passing for pT bins
        for v in self.v_id:
            if pt1 > v[0] and pt1 < v[1]: v[3] += 1
            if pt2 > v[0] and pt2 < v[1]: v[3] += 1
            

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
        '''

        return True



preselection=''
files=["Skims/nanoAOD_aqgc2017_Skim.root"] if signal else ["Skims/nanoAOD_ggj2017_Skim.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[SignalStudy()],noOut=True,histFileName="histOut_study.root",histDirName="plots")
p.run()
