#   To Do List
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
from PhysicsTools.NanoAODTools.postprocessing.modules.common.hepmcDump import *

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

        self.total, self.passing_hp, self.passing_wp90, self.passing_wp80, self.passing_l, self.passing_m, self.passing_t = 0, 0, 0, 0, 0, 0, 0

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

        #print 'Efficiency (total):', float(self.total), '/ 94800'
        print 'High pT ID:', float(self.passing_hp)/float(self.total)
        print 'MVA WP90 ID:', float(self.passing_wp90)/float(self.total)
        print 'MVA WP80 ID:', float(self.passing_wp80)/float(self.total)
        print 'Loose ID:', float(self.passing_l)/float(self.total)
        print 'Medium ID:', float(self.passing_m)/float(self.total)
        print 'Tight ID:', float(self.passing_t)/float(self.total)
        
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
    def highPtID(self,pho1,pho2,rho):
        for pho in (pho1,pho2):
            if pho.isScEtaEB:
                corPhoIso = 2.5 + pho.photonIso - rho*0.14 - 0.0045*pho.pt
                if corPhoIso > 2.75: return False
                if pho.see > (0.0112 if pho.isSeedSaturated else 0.0105): return False
            elif pho.isScEtaEE:
                corPhoIso = 2.5 + pho.photonIso - rho*0.22 - 0.003*pho.pt
                if corPhoIso > 2.00: return False
                if pho.see > (0.0300 if pho.isSeedSaturated else 0.0280): return False
            if pho.chargedHadronIso > 5: return False
            if pho.hoe > 0.05: return False
            if pho.r9 < 0.8: return False
        return True



    def analyze(self, event):
        photons = Collection(event, "Photon")
        #protons = Collection(event,"Proton_singleRP")
        #protons = Collection(event, "Proton_multiRP")
        #lhe = Collection(event, "LHEPart")
        #gen = Collection(event, "GenPart")

        '''
        for i, g in enumerate(gen):
            print 'i:', i, 'pdgId:', g.pdgId, 'status:', g.status
        return
        
        if event.HLT_DoublePhoton70 == 0:
            print 'Not passing HLT'
            return
        '''

        if len(photons) < 2: 
            print 'Not 2 reconstructed photons'
            return

        self.total += 1
        pho1, pho2 = photons[0], photons[1]
        if self.highPtID(pho1,pho2,event.fixedGridRhoFastjetAll): self.passing_hp += 1
        if pho1.mvaID_WP90 == 1 and pho2.mvaID_WP90 == 1: self.passing_wp90 += 1 
        if pho1.mvaID_WP80 == 1 and pho2.mvaID_WP80 == 1: self.passing_wp80 += 1
        if pho1.cutBasedBitmap >= 1 and pho2.cutBasedBitmap >= 1: self.passing_l += 1
        if pho1.cutBasedBitmap >= 3 and pho2.cutBasedBitmap >= 3: self.passing_m += 1
        if pho1.cutBasedBitmap >= 7 and pho2.cutBasedBitmap >= 7: self.passing_t += 1




        '''
        pt1, pt2 = pho1.pt, pho2.pt
        if pho1.pt < 100 or pho2.pt < 100: 
            print 'Not passing pT cut'
            return

        diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
        diph_mass = diph_p4.M()
        diph_rap = diph_p4.Rapidity()
        diph_pt = diph_p4.Pt()
        delta_phi = pho1.p4().DeltaPhi(pho2.p4())
        acop = 1 - abs(delta_phi)/PI
        xip = 1/13000.*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
        xim = 1/13000.*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )


        # Generated photons
        part1, part2 = gen[2], gen[3] #gen[19], gen[20]
        if ( abs(part1.p4().Pz()-pho1.p4().Pz()) ) > ( abs(part2.p4().Pz()-pho1.p4().Pz()) ): part1, part2 = gen[3], gen[2]  #gen[20], gen[19] 
        part_p4 = ROOT.TLorentzVector( part1.p4() + part2.p4() )
        part_mass = part_p4.M()
        part_rap = part_p4.Rapidity()
        part_pt = part_p4.Pt()
        part_dphi = part1.p4().DeltaPhi(part2.p4())
        part_acop = 1 - abs(part_dphi)/PI
        part_xip = 1/13000.*( part1.pt*math.exp(part1.eta)+part2.pt*math.exp(part2.eta) )
        part_xim = 1/13000.*( part1.pt*math.exp(-1*part1.eta)+part2.pt*math.exp(-1*part2.eta) )

        
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
        gen_prop, gen_prom = gen[0].p4(), gen[1].p4() #gen[3].p4(), gen[5].p4()
        gen_xip = ( 6500.0-gen_prop.Rho() ) / 6500.0
        gen_xim = ( 6500.0-gen_prom.Rho() ) / 6500.0

        print ''
        #print 'xi_simu_p:', gen_xip, 'eta:', gen[3].eta, 'mass:', gen[3].mass, 'phi:', gen[3].phi, 'pt:', gen[3].pt 
        #print 'xi_simu_m:', gen_xim, 'eta:', gen[5].eta, 'mass:', gen[5].mass, 'phi:', gen[5].phi, 'pt:', gen[5].pt

        print 'xi_simu_p:', gen_xip, 'px:', gen_prop.Px(), 'py:', gen_prop.Py(), 'pz:', gen_prop.Pz(), 'E:', gen_prop.E()  
        print 'xi_simu_m:', gen_xim, 'px:', gen_prom.Px(), 'py:', gen_prom.Py(), 'pz:', gen_prom.Pz(), 'E:', gen_prom.E()

        #print 'Rho_p:', gen_prop.Rho(), 'Rho_m:', gen_prom.Rho()
        #print 'E_p:', gen_prop.E(), 'E_m:', gen_prom.E()
        #print 'Mag_p:', gen_prop.Mag(), 'Mag_m:', gen_prom.Mag()
        #print 'P_p:', gen_prop.P(), 'P_m:', gen_prom.P()

        for p in protons: 
            if p.sector45: print 'xi_reco_p:', p.xi
            if p.sector56: print 'xi_reco_m:', p.xi

        self.h_pro_xi_gen.Fill( gen_xim ), self.h_pro_xi_gen.Fill( gen_xip )


        # Reconstructed protons
        if not two_protons(protons): return
        self.total += 1
        v45, v56 = [], []
        for proton in protons:
            if proton.sector45: v45.append(proton)
            elif proton.sector56: v56.append(proton)

        pro_m, pro_p = min(v45, key=lambda x:abs(x.xi-xim)), min(v56, key=lambda x:abs(x.xi-xip))
        pro_xim, pro_xip = pro_m.xi, pro_p.xi


        # Proton plots        
        self.h_pro_xi_res.Fill(abs(pro_xim-gen_xim)/gen_xim), self.h_pro_xi_res.Fill(abs(pro_xip-gen_xip)/gen_xip)
        self.h_pro_xi_diff.Fill(pro_xim-gen_xim), self.h_pro_xi_diff.Fill(pro_xip-gen_xip)
        self.h_pro_xi_gen_twopro.Fill( gen_xim ), self.h_pro_xi_gen_twopro.Fill( gen_xip )
        '''

        return True



preselection=''
files=['/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/nanoAOD_aqgc2017_Skim.root']
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[hepmcDump(),SignalStudy()],noOut=True,histFileName="histOut_aqgc2017_study.root",histDirName="plots")
p.run()
