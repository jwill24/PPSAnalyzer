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

from common import mass_cut, hoe_cut, acop_cut, photon_id, electron_veto, xi_cut, eta_cut, two_protons
#ROOT.gStyle.SetOptStat(0)

PI = 3.14159265358979323846
sqrts = 13000

signal = True

#photon_id = 'MVA_WP90'
#photon_id = 'cutBased_loose'
#photon_id = 'highPt'

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
        
        self.h_pro_xi_res=ROOT.TH1F('h_pro_xi_res', '#xi Relative Error', 100, 0, 0.9)
        self.h_pro_xi_diff=ROOT.TH1F('h_pro_xi_diff', '#xi Difference', 100, -0.1, 0.1)
        self.h_pro_xi_gen=ROOT.TH1F('h_pro_xi_gen', '', 100, 0, 0.25)
        self.h_pro_xi_gen_twopro=ROOT.TH1F('h_pro_xi_gen_twopro', '', 100, 0, 0.25)

        #self.h_ratio=ROOT.TH1F('h_ratio', photon_id+'ID Efficiency', len(self.v_id), 0, len(self.v_id))
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
        self.addObject( self.h_pro_xi_res )
        self.addObject( self.h_pro_xi_diff )
        self.addObject( self.h_pro_xi_gen )
        self.addObject( self.h_pro_xi_gen_twopro )

    def endJob(self):
        Module.endJob(self)

        print 'Efficiency (total):', float(self.total), '/ 94800'

        rootFile = ROOT.TFile('cutTest.root', 'RECREATE')
        #total, passing, comb_total, comb_passing = 0, 0, 0, 0
        cut_names = ['Iso Chg', 'Iso All', 'H/E', 'R_{9}', '#sigma_{i#etai#eta}']

        for i, v in enumerate(self.v_id):
            self.h_cuts_2d.GetXaxis().SetBinLabel(i+1, str(self.v_id[i][1]))
            for j, c in enumerate(cut_names):
                self.h_cuts_2d.GetYaxis().SetBinLabel(j+1, c)
                self.h_cuts_2d.SetBinContent(i+1, j+1, v[j+2])
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


    def analyze(self, event):
        photons = Collection(event, "Photon")
        #protons = Collection(event,"Proton_singleRP")
        protons = Collection(event, "Proton_multiRP")
        #lhe = Collection(event, "LHEPart")
        gen = Collection(event, "GenPart")

        
        if len(photons) < 2: return
        pho1, pho2 = photons[0], photons[1]
        pt1, pt2 = pho1.pt, pho2.pt
        if pho1.pt < 100 or pho2.pt < 100: return
        diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
        diph_mass = diph_p4.M()
        diph_rap = diph_p4.Rapidity()
        diph_pt = diph_p4.Pt()
        delta_phi = pho1.p4().DeltaPhi(pho2.p4())
        acop = 1 - abs(delta_phi)/PI
        xip = 1/13000.*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
        xim = 1/13000.*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )

        #print ''
        #print 'diph_xip:', xip, 'diph_xim:', xim

        #if not hoe_cut(pho1,pho2): return
        #if not eta_cut(pho1,pho2): return
        #if not mass_cut(diph_mass): return
        #if not photon_id(pho1,pho2): return
        #if not electron_veto(pho1,pho2): return
        #if not acop_cut(acop): return
        #if not xi_cut(xip,xim): return

        '''        
        self.total += 1

        # Fill 2D cut plots
        for v in self.v_id:
            if pt1 > v[0] and pt1< v[1]:
                if pho1.isScEtaEB:
                    if pho1.pfRelIso03_chg > 5:    v[2] += 1
                    if pho1.pfRelIso03_all > 2.75: v[3] += 1
                    if pho1.hoe > 0.05:            v[4] += 1
                    if pho1.r9 < 0.8:              v[5] += 1
                    if pho1.sieie > 0.0105:        v[6] += 1
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
                    if pho1.sieie > 0.0105:        v[6] += 1
                elif pho2.isScEtaEE:
                    if pho1.pfRelIso03_chg > 5:    v[2] += 1
                    if pho1.pfRelIso03_all > 2:    v[3] += 1
                    if pho1.hoe > 0.05:            v[4] += 1
                    if pho1.r9 < 0.8:              v[5] +=1 
                    if pho1.sieie > 0.0280:        v[6] += 1


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

        '''

        # Generated photons
        part1, part2 = gen[19], gen[20]
        if ( abs(part1.p4().Pz()-pho1.p4().Pz()) ) > ( abs(part2.p4().Pz()-pho1.p4().Pz()) ): part1, part2 = gen[20], gen[19] 
        part_p4 = ROOT.TLorentzVector( part1.p4() + part2.p4() )
        part_mass = part_p4.M()
        part_rap = part_p4.Rapidity()
        part_pt = part_p4.Pt()
        part_dphi = part1.p4().DeltaPhi(part2.p4())
        part_acop = 1 - abs(part_dphi)/PI
        part_xip = 1/13000.*( part1.pt*math.exp(part1.eta)+part2.pt*math.exp(part2.eta) )
        part_xim = 1/13000.*( part1.pt*math.exp(-1*part1.eta)+part2.pt*math.exp(-1*part2.eta) )

        #print 'gen_diph_xip:', part_xip, 'gen_diph_xim:', part_xim
        
        # Diphoton resolution plots
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

        # Generated protons
        gen_prop, gen_prom = gen[3].p4(), gen[5].p4()
        gen_xip = ( 6500.0-gen_prop.Rho() ) / 6500.0
        gen_xim = ( 6500.0-gen_prom.Rho() ) / 6500.0

        print ''
        print 'gen_xip:', gen_xip, 'gen_xim:', gen_xim

        for p in protons:
            print p.xi, 'm' if p.sector56 else 'p'

        self.h_pro_xi_gen.Fill( gen_xim ), self.h_pro_xi_gen.Fill( gen_xip )

        #print ''
        #print 'n_pro:', len(protons)
        #for p in protons: print '-' if p.sector56 else '+'#, 'xi_reco:', p.xi

        # Reconstructed protons
        if not two_protons(protons): 
            #print 'gen_xip:', gen_xip, 'gen_xim:', gen_xim
            return
        self.total += 1
        v45, v56 = [], []
        for proton in protons:
            if proton.sector45: v45.append(proton)
            elif proton.sector56: v56.append(proton)

        pro_m, pro_p = min(v45, key=lambda x:abs(x.xi-xim)), min(v56, key=lambda x:abs(x.xi-xip))
        pro_xim, pro_xip = pro_m.xi, pro_p.xi


        #print 'xim:', pro_xim, 'xip:', pro_xip, 
        #print 'gen_xip:', gen_xip, 'gen_xim:', gen_xim 
        #for p in protons:
            #print p.xi, 'm' if p.sector56 else 'p'

        # Proton plots
        
        self.h_pro_xi_res.Fill(abs(pro_xim-gen_xim)/gen_xim), self.h_pro_xi_res.Fill(abs(pro_xip-gen_xip)/gen_xip)
        self.h_pro_xi_diff.Fill(pro_xim-gen_xim), self.h_pro_xi_diff.Fill(pro_xip-gen_xip)
        self.h_pro_xi_gen_twopro.Fill( gen_xim ), self.h_pro_xi_gen_twopro.Fill( gen_xip )

        return True



preselection='HLT_DoublePhoton70'
#files=["Skims/nanoAOD_aqgc2017_Skim.root"] if signal else ["Skims/nanoAOD_ggj2017_Skim.root"]
#files=['/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PhysicsTools/NanoAOD/test/nano_mirror.root']
#files=['/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PhysicsTools/NanoAOD/test/nanoAOD_aqgc_noPU_2017postTS2.root']
#files=['/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PhysicsTools/NanoAOD/test/nano_adjustedBeam_1000.root']
#files=['/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PhysicsTools/NanoAOD/test/nano_adjustedBeam_reverse_1000.root']
#files=['/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PhysicsTools/NanoAOD/test/nano_only45.root']
files=['/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PhysicsTools/NanoAOD/test/nanoAOD_jan_1000.root']
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[SignalStudy()],noOut=True,histFileName="histOut_signal_multiRP_2017postTS2.root",histDirName="plots",maxEntries=100)
p.run()
