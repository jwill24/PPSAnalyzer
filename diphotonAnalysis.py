# Things To Do
#   1. Implement proton errors when available

#!/usr/bin/env python
import os, sys, re
from itertools import combinations
import numpy as np
from array import array
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeightProducer, puWeight_2017

ROOT.gROOT.ProcessLine(
"struct MyStruct {\
   Float_t     mass;\
   Float_t     rap;\
   Float_t     xim;\
   Float_t     xip;\
   Long64_t    xangle;\
   Char_t      era[5];\
};" );
 
from ROOT import MyStruct
mystruct = MyStruct()

PI = 3.14159265358979323846
sqrts = 13000
lumi = 37200 # 2017 data
rel_mass_err = 0.02
rel_rap_err = 0.074
rel_xi_err = 0.08

sample = str( sys.argv[1] )
selection = str( sys.argv[2] )

mcs = [ ['ggj2017', 134.3, 3883535],['g+j2017',873.7,79243357],['qcd2017',117500,20622034],['wg2017',191.1,25918966],['zg2017',55.47,30490034],['tt2017',725.5,154280331],['aqgc2017',3.86e-5,300000],
        ['ggj2018', 118.0, 3760030],['g+j2018',875.4,10205533],['qcd2018',117200,10895375],['wg2018',191.6,27933663],['zg2018',55.48,13946364],['tt2018',749.9,304627424] ]
selections = [ ['HLT', 1], ['Preselection', 2], ['ReverseElastic', 2.5], ['ID', 3], ['Elastic', 4], ['Xi', 5] ]

for sel in selections:
    if selection == sel[0]: nSelect = sel[1] 

for mc in mcs:
    if 'data' in sample: 
        xsec, n_events = 1, 1
        data_ = True
    elif sample == mc[0]:
        xsec, n_events = mc[1], mc[2]
        data_ = False

if data_: sample_weight = 1
else: sample_weight = xsec*lumi/n_events

print ''
print 'Sample:', sample, 'Selection:', selection, 'nSelect:', nSelect
print '----------------------------------'
print ''

class DiphotonAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True

        # Get SF hists for ID and CSEV
        self.photonmapname = "EGamma_SF2D"        
        if '2017' in sample: 
            self.photon_file = self.open_root("2017_PhotonsMVAwp90.root")
            self.csev_file = self.open_root("CSEV_ScaleFactors_2017.root")
            self.csevmapname = "MVA_ID"
        elif '2018' in sample:
            self.photon_file = self.open_root("2018_PhotonsMVAwp90.root")
            self.csev_file = self.open_root("CSEV_2018.root")
            self.csevmapname = "eleVeto_SF"
        self.csev_map = self.get_root_obj(self.csev_file, self.csevmapname)
        self.photon_map = self.get_root_obj(self.photon_file, self.photonmapname)

        # Initialize objects for toy matching file
        self.diphoton_file = ROOT.TFile('diphotonEvents.root', 'RECREATE')
        self.diphoton_tree = ROOT.TTree('tree','Tree with diphoton events')
        self.v_mass, self.v_rap, self.v_xip, self.v_xim, self.v_era, self.v_xangle = array('f', []), array('f', []), array('f', []), array('f', []), array('f', []), array('f', [])
        self.diphoton_tree.Branch('mass', ROOT.AddressOf( mystruct, 'mass'), 'mass/F')
        self.diphoton_tree.Branch('rap', ROOT.AddressOf( mystruct, 'rap'), 'rap/F')
        self.diphoton_tree.Branch('xim', ROOT.AddressOf( mystruct, 'xim'), 'xim/F')
        self.diphoton_tree.Branch('xip', ROOT.AddressOf( mystruct, 'xip'), 'xip/F')
        self.diphoton_tree.Branch('xangle', ROOT.AddressOf( mystruct, 'xangle'), 'xangle/L')
        self.diphoton_tree.Branch('era', ROOT.AddressOf( mystruct, 'era'), 'era/C')
        

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
        
        self.h_num_pho=ROOT.TH1F('h_num_pho', 'Number Of Photons', 10, 0, 8)
        self.h_diph_mass=ROOT.TH1F('h_diph_mass', 'Diphoton Mass', 100, 100 if nSelect==1 else 350, 2500.) # aqgc - 3000, data - 2500
        self.h_acop=ROOT.TH1F('h_acop', 'Diphoton Acoplanarity', 100, 0., 0.25 if nSelect < 4 else 0.01) # aqgc - 0.01, data - 0.25 if nSelect < 4 else 0.01
        self.h_pt_ratio=ROOT.TH1F('h_pt_ratio', 'Diphoton p_{T} Ratio', 100, 0, 2)
        self.h_single_eta=ROOT.TH1F('h_single_eta', 'Single Photon Eta', 100, -3.0, 3.0)
        self.h_lead_eta=ROOT.TH1F('h_lead_eta', 'Leading Photon Eta', 100, -3.0, 3.0)
        self.h_sub_eta=ROOT.TH1F('h_sub_eta', 'Subleading Photon Eta', 100, -3.0, 3.0)
        self.h_single_pt=ROOT.TH1F('h_single_pt', 'Single Photon pT', 100, 100, 750) # aqgc - 1400, data - 750
        self.h_lead_pt=ROOT.TH1F('h_lead_pt', 'Lead Photon pT', 100, 100, 750)
        self.h_sub_pt=ROOT.TH1F('h_sub_pt', 'Sublead Photon pT', 100, 100, 750)
        self.h_single_r9=ROOT.TH1F('h_single_r9', 'Single Photon R_{9}', 100, 0.5 if nSelect < 4 else 0.8, 1) # aqgc - 0.8, data - 0.5 if nSelect < 4 else 0.8
        self.h_lead_r9=ROOT.TH1F('h_lead_r9', 'Lead Photon R_{9}', 100, 0.5 if nSelect < 4 else 0.8, 1)
        self.h_sub_r9=ROOT.TH1F('h_sub_r9', 'Sublead Photon R_{9}', 100, 0.5 if nSelect < 4 else 0.8, 1)
        self.h_single_hoe=ROOT.TH1F('h_single_hoe', 'Single Photon H/E', 100, 0, 1)
        self.h_eb_hoe=ROOT.TH1F('h_eb_hoe', 'Lead Photon H/E', 100, 0, 1 if nSelect == 1 else 0.1)
        self.h_ee_hoe=ROOT.TH1F('h_ee_hoe', 'Sublead Photon H/E', 100, 0, 1 if nSelect == 1 else 0.1)
        self.h_single_sieie=ROOT.TH1F('h_single_sieie', 'Single Photon #sigma_{i#etai#eta}', 100, 0, 0.1)
        self.h_eb_sieie=ROOT.TH1F('h_eb_sieie', 'Lead Photon #sigma_{i#etai#eta}', 100, 0, 0.1)
        self.h_ee_sieie=ROOT.TH1F('h_ee_sieie', 'Sublead Photon #sigma_{i#etai#eta}', 100, 0, 0.1)
        self.h_single_electronVeto=ROOT.TH1F('h_single_electronVeto', 'Single Photon Electron Veto', 2, 0, 1)
        self.h_lead_electronVeto=ROOT.TH1F('h_lead_electronVeto', 'Lead Photon Electron Veto', 2, 0, 1)
        self.h_sub_electronVeto=ROOT.TH1F('h_sub_electronVeto', 'Sublead Photon Electron Veto', 2, 0, 1)
        self.h_xip=ROOT.TH1F('h_xip', '#xi _{#gamma#gamma}^{+}', 100, 0., 0.25)
        self.h_xim=ROOT.TH1F('h_xim', '#xi _{#gamma#gamma}^{-}', 100, 0., 0.25)
        self.h_nvtx=ROOT.TH1F('h_nvtx','Number Of Vertices', 75, 0., 75.)
        self.h_vtx_z=ROOT.TH1F('h_vtx_z', 'Vtx z position', 100,-15,15)
        self.h_fgr=ROOT.TH1F('h_fgr', 'fixedGridRho', 100, 0, 58)

        self.h_num_pro=ROOT.TH1F('h_num_pro', 'Number of Protons', 15, 0, 15)
        self.h_detType=ROOT.TH1F('h_detType', 'PPS Detector Type', 2, 3, 4)
        self.h_pro_xip=ROOT.TH1F('h_pro_xip', 'Proton #xi ^{+}', 100, 0.01, 0.25)
        self.h_pro_xim=ROOT.TH1F('h_pro_xim', 'Proton #xi ^{-}', 100, 0.01, 0.25)
        self.h_pro_xi_45f=ROOT.TH1F('h_pro_xi_45f', 'Proton #xi 45F', 100, 0., 0.25)
        self.h_pro_xi_45n=ROOT.TH1F('h_pro_xi_45n', 'Proton #xi 45N', 100, 0., 0.25)
        self.h_pro_xi_56n=ROOT.TH1F('h_pro_xi_56n', 'Proton #xi 56N', 100, 0., 0.25)
        self.h_pro_xi_56f=ROOT.TH1F('h_pro_xi_56f', 'Proton #xi 56F', 100, 0., 0.25)

        self.gr_matching=ROOT.TGraphErrors('gr_matching')
        self.gr_matching.SetName('gr_matching')
        self.gr_xip_matching=ROOT.TGraphErrors('gr_xip_matching')
        self.gr_xip_matching.SetName('gr_xip_matching')
        self.gr_xim_matching=ROOT.TGraphErrors('gr_xim_matching')
        self.gr_xim_matching.SetName('gr_xim_matching')

        self.addObject( self.h_num_pho ), self.addObject( self.h_diph_mass ), self.addObject( self.h_acop ), self.addObject( self.h_pt_ratio )
        self.addObject( self.h_single_eta ), self.addObject( self.h_lead_eta ), self.addObject( self.h_sub_eta ) 
        self.addObject( self.h_single_pt ), self.addObject( self.h_lead_pt ), self.addObject( self.h_sub_pt )
        self.addObject( self.h_single_r9 ), self.addObject( self.h_lead_r9 ), self.addObject( self.h_sub_r9 )
        self.addObject( self.h_single_hoe ), self.addObject( self.h_eb_hoe ), self.addObject( self.h_ee_hoe )
        self.addObject( self.h_single_sieie ), self.addObject( self.h_eb_sieie ), self.addObject( self.h_ee_sieie )
        self.addObject( self.h_single_electronVeto ), self.addObject( self.h_lead_electronVeto ), self.addObject( self.h_sub_electronVeto )
        self.addObject( self.h_xip ), self.addObject( self.h_xim )
        self.addObject( self.h_nvtx ), self.addObject( self.h_vtx_z ), self.addObject( self.h_fgr )

        if data_:
            self.addObject( self.h_num_pro ), self.addObject( self.h_detType )
            self.addObject( self.h_pro_xip ), self.addObject( self.h_pro_xim )
            self.addObject( self.h_pro_xi_45f ), self.addObject( self.h_pro_xi_45n )
            self.addObject( self.h_pro_xi_56n ), self.addObject( self.h_pro_xi_56f )
            self.addObject( self.gr_matching )
            self.addObject( self.gr_xip_matching ), self.addObject( self.gr_xim_matching )


        if not data_:
            self.mcfile = ROOT.TFile( 'Skims/nanoAOD_'+sample+'_Skim.root' )
            self.mchist = ROOT.TH1F('mchist', 'fixedGridRho', 100, 0, 58)
            self.mctree = self.mcfile.Events
            self.mctree.Project('mchist', 'fixedGridRhoFastjetAll')
            self.mchist.Scale( 1 / self.mchist.Integral() )

            if '2017' in sample: self.datafile = ROOT.TFile( 'dataFixedGridRho_2017.root' )
            elif '2018' in sample: self.datafile = ROOT.TFile( 'dataFixedGridRho_2018.root' )
            self.datahist = self.datafile.Get('h')
            self.datahist.Scale( 1 / self.datahist.Integral() )

            if self.mchist.GetNbinsX() != self.datahist.GetNbinsX():
                raise ValueError('data and mc histograms must have the same number of bins')
            if self.mchist.GetXaxis().GetXmin() != self.datahist.GetXaxis().GetXmin():
                raise ValueError('data and mc histograms must have the same xmin')
            if self.mchist.GetXaxis().GetXmax() != self.datahist.GetXaxis().GetXmax():
                raise ValueError('data and mc histograms must have the same xmax')

    def endJob(self):
        Module.endJob(self)
        
        self.diphoton_file.Write()
        self.diphoton_file.Close()


    # Apply mass cut
    def mass_cut(self,diph_mass):
        if diph_mass > 350: return True
        else: return False

    # Apply hoe cut
    def hoe_cut(self,pho1,pho2):
        if pho1.hoe >= 0.8 and pho2.hoe >= 0.8: return True
        else: return False

    # Apply acoplanarity cut
    def acop_cut(self,acop):
        if acop < 0.005: return True
        else: return False

    # Apply photon ID
    def photon_id(self,pho1,pho2):
        if pho1.mvaID_WP90 == 1 and pho2.mvaID_WP90 == 1: return True # loose MVA ID
        else: return False
        return True

    # Apply electron veto
    def electron_veto(self,pho1,pho2):
        if pho1.electronVeto == 1 and pho2.electronVeto == 1: return True
        else: return False

    # Tight xi cut
    def xi_cut(self,xip,xim):
        if xip < 0.015 or xip > 0.2: return False
        if xim < 0.015 or xim > 0.2: return False
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

    # Apply hoe cut
    def hoe_cut(self,pho1,pho2):
        if pho1.isScEtaEB and pho1.hoe > 0.082: return False
        if pho1.isScEtaEE and pho1.hoe > 0.075: return False
        if pho2.isScEtaEB and pho2.hoe > 0.082: return False
        if pho2.isScEtaEE and pho2.hoe > 0.075: return False
        return True 
        
    # Get the SFs for MCs
    def efficiency(self,pt,eta_sc,r9):
        if nSelect != 2.5 and nSelect < 3: return 1
        bin_x = min( max( self.photon_map.GetXaxis().FindBin( eta_sc ), 1 ), self.photon_map.GetXaxis().GetNbins() )
        bin_y = min( max( self.photon_map.GetYaxis().FindBin( pt ), 1 ), self.photon_map.GetYaxis().GetNbins() )
        id_sf = self.photon_map.GetBinContent( bin_x, bin_y )
        if '2017' in sample:
            if eta_sc <= 1.4442: bin_r9 = 2 if r9 > 0.94 else 3
            else: bin_r9 = 5 if r9 > 0.94 else 6
            csev_sf = self.csev_map.GetBinContent( bin_r9 ) 
        elif '2018' in sample:
            bin_x = min( max( self.csev_map.GetXaxis().FindBin( eta_sc ), 1 ), self.photon_map.GetXaxis().GetNbins() )
            bin_y = min( max( self.csev_map.GetYaxis().FindBin( pt ), 1 ), self.photon_map.GetYaxis().GetNbins() )
            csev_sf = self.csev_map.GetBinContent( bin_x, bin_y )
        return id_sf*csev_sf 

    # Use the fixedGridRho for reweighting
    def rhoReweight(self,nPU):
        bin = self.datahist.FindBin(nPU)
        if bin<1 or bin>self.datahist.GetNbinsX():
            w = 0
        else:
            data = self.datahist.GetBinContent(bin)
            mc = self.mchist.GetBinContent(bin)
            if mc !=0.0:
                w = data/mc
            else:
                w = 1 
        return w

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

    def mass(self,xi1,xi2):
        if xi1 < 0 or xi2 < 0: 
            print '---> Weird. Negtative xi value. xi1:', xi1, 'xi2:', xi2
            return -1
        else: return sqrts*math.sqrt(xi1*xi2)

    def rapidity(self,xi1,xi2):
        if xi1 < 0 or xi2 < 0: return -999
        else: return 0.5*math.log(xi1/xi2)

    def mass_err(self,pro1,pro2):
        return self.mass(pro1.xi,pro2.xi) * self.rapidity_err(pro1,pro2)
        
    def rapidity_err(self,pro1,pro2):
        xi1_err, xi2_err = pro1.xi*rel_xi_err, pro2.xi*rel_xi_err
        return 0.5 * math.sqrt( pow(xi1_err/pro1.xi,2) + pow(xi2_err/pro2.xi,2) )

    def mass_matching(self,mp):
        if abs(mp) <= 3: return True
        else: return False

    def rap_matching(self,rp):
        if abs(rp) <= 3: return True
        else: return False

    def getEra(self,run):
        if run > 297023 and run < 299330: return '2017B'
        elif run > 299359 and run < 302045: return '2017C'
        elif run > 302111 and run < 302679: return '2017D'
        elif run > 303708 and run < 304798: return '2017E'
        elif run > 305016 and run < 306462: return '2017F'
        elif run > 305016 and run < 306462: return '2018A'
        elif run > 305016 and run < 306462: return '2018B'
        elif run > 305016 and run < 306462: return '2018C'
        elif run > 305016 and run < 306462: return '2018D'
        else: return 'none'

    def analyze(self, event):
        if data_: protons = Collection(event, "Proton_singleRP")
        #if data_: protons = Collection(event, "Proton_multiRP")
        photons = Collection(event, "Photon")
        if data_: pu_weight, vtxWeight, eff_pho1, eff_pho2 = 1, 1, 1, 1
        else: pu_weight, vtxWeight = event.puWeightUp, self.rhoReweight(event.Pileup_nPU)
        s_weight = sample_weight*pu_weight
        
        if len(photons) < 2: return
                
        # Choose the best diphoton candidate
        acop = 999
        pho1, pho2 = photons[0], photons[1]
        for combo in combinations(range(0,len(photons)),2):
            p1, p2 = photons[combo[0]], photons[combo[1]]
            if p1.pt < 75 or p2.pt < 75: return
            tmp_acop =  1 - abs( p1.p4().DeltaPhi(p2.p4()) ) / PI
            if tmp_acop > acop: continue
            acop = tmp_acop
            pho1, pho2 = p1, p2
            
        diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
        diph_mass = diph_p4.M()
        diph_rap = diph_p4.Rapidity()
        delta_phi = pho1.p4().DeltaPhi(pho2.p4())
        xip = 1/13000.*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
        xim = 1/13000.*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )
        if data_: weight = 1

        # Make selection cuts
        if nSelect > 1: # Preselection
            if not self.eta_cut(pho1,pho2): return
            if pho1.pt < 100 or pho2.pt < 100: return
            if not self.mass_cut(diph_mass): return
            if not self.hoe_cut(pho1,pho2): return
        if nSelect > 2: # ID
            if not self.photon_id(pho1,pho2): return
            if not self.electron_veto(pho1,pho2): return
        if nSelect == 2.5: 
            if acop < 0.005: return
        if nSelect > 3: # Elastic
            if not self.acop_cut(acop): return
        if nSelect > 4 or nSelect == 2.5: # Tight xi or reverse elastic
            if not self.xi_cut(xip,xim): return

        # Print high-mass event kinematics
        if data_ and diph_mass > 1700:
            with open('events.txt', 'a') as f:
                print >> f, 'R:L:E', str(event.run)+':'+str(event.luminosityBlock)+':'+str(event.event), 'npho:', len(photons), 'nvtx:', event.PV_npvs, 'vtx_z:', event.PV_z
                print >> f, 'mass:', diph_mass, 'Acoplanarity:', acop
                print >> f, 'pt1:', pho1.pt, 'pt2:', pho2.pt, 'eta1:', pho1.eta, 'eta2:', pho2.eta
                print >> f, 'R9_1:', pho1.r9, 'R9_2:', pho2.r9, 'xip:', xip, 'xim:', xim
                print >> f, 'Num protons:', len(protons)
                if len(protons) > 0: 
                    for i in range(0,len(protons)-1): print >> f,  'proton'+str(i), 'xi:', protons[i].xi
                print >> f, ''

        # Fill diphoton tree for background estimation
        if data_: 
            if nSelect == 2.5 or nSelect == 5: # tight xi selection 
                mystruct.mass = diph_mass
                mystruct.rap = diph_rap
                mystruct.xim = xim
                mystruct.xip = xip
                mystruct.xangle = event.LHCInfo_xangle
                mystruct.era = self.getEra(event.run)
                self.diphoton_tree.Fill()

        if not data_:
            eff_pho1 = self.efficiency(pho1.pt,pho1.eta,pho1.r9)
            eff_pho2 = self.efficiency(pho2.pt,pho2.eta,pho2.r9)
            weight = s_weight * ( eff_pho1*eff_pho2 )

        # Fill single photon hists
        self.h_single_eta.Fill(pho1.eta,s_weight*eff_pho1),                   self.h_single_eta.Fill(pho2.eta,s_weight*eff_pho2)
        self.h_lead_eta.Fill(pho1.eta,s_weight*eff_pho1),                     self.h_sub_eta.Fill(pho2.eta,s_weight*eff_pho2)
        self.h_single_pt.Fill(pho1.pt,s_weight*eff_pho1),                     self.h_single_pt.Fill(pho2.pt,s_weight*eff_pho2)
        self.h_lead_pt.Fill(pho1.pt,s_weight*eff_pho1),                       self.h_sub_pt.Fill(pho2.pt,s_weight*eff_pho2)
        self.h_single_r9.Fill(pho1.r9,s_weight*eff_pho1),                     self.h_single_r9.Fill(pho2.r9,s_weight*eff_pho2)
        self.h_lead_r9.Fill(pho1.r9,s_weight*eff_pho1),                       self.h_sub_r9.Fill(pho2.r9,s_weight*eff_pho2)
        self.h_single_hoe.Fill(pho1.hoe,s_weight*eff_pho1),                   self.h_single_hoe.Fill(pho2.hoe,s_weight*eff_pho2)
        self.h_single_sieie.Fill(pho1.sieie,s_weight*eff_pho1),               self.h_single_sieie.Fill(pho2.sieie,s_weight*eff_pho2)
        self.h_single_electronVeto.Fill(pho1.electronVeto,s_weight*eff_pho1), self.h_single_electronVeto.Fill(pho2.electronVeto,s_weight*eff_pho2) 
        self.h_lead_electronVeto.Fill(pho1.electronVeto,s_weight*eff_pho1),   self.h_sub_electronVeto.Fill(pho2.electronVeto,s_weight*eff_pho2) 
        if pho1.isScEtaEB: self.h_eb_hoe.Fill(pho1.hoe,s_weight*eff_pho1), self.h_eb_sieie.Fill(pho1.sieie,s_weight*eff_pho1)
        else: self.h_ee_hoe.Fill(pho1.hoe,s_weight*eff_pho1), self.h_ee_sieie.Fill(pho1.sieie,s_weight*eff_pho1)
        if pho2.isScEtaEB: self.h_eb_hoe.Fill(pho2.hoe,s_weight*eff_pho2), self.h_eb_sieie.Fill(pho2.sieie,s_weight*eff_pho2)
        else: self.h_ee_hoe.Fill(pho2.hoe,s_weight*eff_pho2), self.h_ee_sieie.Fill(pho2.sieie,s_weight*eff_pho2)

        # Fill diphoton hists
        self.h_diph_mass.Fill(diph_mass,weight) 
        self.h_acop.Fill(acop,weight) 
        self.h_pt_ratio.Fill(pho1.pt/pho2.pt, weight)
        self.h_xip.Fill(xip,weight), self.h_xim.Fill(xim,weight)

        # Fill event hists
        self.h_num_pho.Fill( len(photons), s_weight)
        self.h_nvtx.Fill(event.PV_npvs,s_weight) 
        self.h_vtx_z.Fill(event.PV_z,s_weight)
        self.h_fgr.Fill(event.fixedGridRhoFastjetAll,s_weight)


        # Fill proton hists 
        if not data_: return 
        self.h_num_pro.Fill( len(protons) )
        for proton in protons:
            self.h_detType.Fill( proton.protonRPType )                       # not available for multiRP
            if proton.sector45: self.h_pro_xip.Fill( proton.xi )
            elif proton.sector56: self.h_pro_xim.Fill( proton.xi ) 
            if proton.decDetId == 3: self.h_pro_xi_45f.Fill( proton.xi )     # not available for multiRP
            elif proton.decDetId == 23: self.h_pro_xi_45n.Fill( proton.xi )  # not available for multiRP
            elif proton.decDetId == 103: self.h_pro_xi_56n.Fill( proton.xi ) # not available for multiRP
            elif proton.decDetId == 123: self.h_pro_xi_56f.Fill( proton.xi ) # not available for multiRP
            else: print 'Proton not in known det id:', proton.decDetId       # not available for multiRP

        # Choose the best diproton candidate
        if not self.two_protons(protons): return
        v45, v56 = [], []
        for proton in protons:
            if proton.sector45: v45.append(proton)
            elif proton.sector56: v56.append(proton)

        pro_m = min(v45, key=lambda x:abs(x.xi-xim))
        pro_p = min(v56, key=lambda x:abs(x.xi-xip))


        # SetPoint for matching plot
        pps_mass, pps_rap = self.mass(pro_m.xi,pro_p.xi), self.rapidity(pro_m.xi,pro_p.xi)
        pps_mass_err, pps_rap_err = self.mass_err(pro_m, pro_p), self.rapidity_err(pro_m, pro_p)
        mass_point = (pps_mass - diph_mass) / (pps_mass_err + diph_mass*rel_mass_err) 
        rap_point = (pps_rap - diph_rap) / (pps_rap_err + rel_rap_err*diph_rap)
        self.gr_matching.SetPoint( self.gr_matching.GetN(), mass_point, rap_point )
        self.gr_xim_matching.SetPoint( self.gr_xim_matching.GetN(), pro_m.xi, xim )
        self.gr_xip_matching.SetPoint( self.gr_xip_matching.GetN(), pro_p.xi, xip )


        return True

preselection=""
if sample == 'data2017':
    files=[
        "Skims/nanoAOD_Run2017B_Skim.root",
        "Skims/nanoAOD_Run2017C_Skim.root",
        "Skims/nanoAOD_Run2017D_Skim.root",
        "Skims/nanoAOD_Run2017E_Skim.root",
        "Skims/nanoAOD_Run2017F_Skim.root"
    ]
elif sample == 'data2018':
    files=[
        "Skims/nanoAOD_Run2018A_Skim.root",
        "Skims/nanoAOD_Run2018B_Skim.root",
        "Skims/nanoAOD_Run2018C_Skim.root",
        "Skims/nanoAOD_Run2018D_Skim.root",
    ]
else: 
    files=[
        "Skims/nanoAOD_"+sample+"_Skim.root"
    ]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[DiphotonAnalysis()],noOut=True,histFileName="histOut_"+sample+"_"+selection+".root",histDirName="plots")
p.run()


