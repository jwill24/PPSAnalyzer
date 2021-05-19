# Usage: python diphotonAnalyzer.py <sample> <selection> <method>
# <sample> = data2017/data2018/gj2017/tt2018/...
# <selection = HLT/Elastic/Xi/...
# <method> = singleRP/multiRP


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

from common import open_root, get_root_obj, mass_cut, hoe_cut, acop_cut, photon_id, electron_veto, xi_cut, eta_cut, two_protons
from common import mass, rapidity, mass_err, rapidity_err, mass_matching, rap_matching, getEra, checkProton

ROOT.gROOT.ProcessLine(
"struct MyStruct {\
   Float_t     mass;\
   Float_t     rap;\
   Float_t     xim;\
   Float_t     xip;\
   Long64_t    crossingAngle;\
   Char_t      era[5];\
   Float_t     weight;\
};" );
 
from ROOT import MyStruct
mystruct = MyStruct()

PI = 3.1415926535897932643383279
lumi2016, lumi2017, lumi2018 = 9780, 37190, 55720 
rel_mass_err, rel_rap_err = 0.02, 0.074
#rel_mass_err, rel_rap_err = 0.02, 0.1 # FIXME FIXME FIXME

sample, selection, method = str( sys.argv[1] ), str( sys.argv[2] ), str( sys.argv[3] )

if '2016' in sample: year = '2016'
elif '2017' in sample: year = '2017'
elif '2018' in sample: year = '2018'

mc_file = open('/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/datasets.txt','r') 
mcs = [[n.rstrip('\n') for n in line.split(',')] for line in mc_file]
selections = [ ['HLT', 1], ['Preselection', 2], ['ReverseElastic', 2.5], ['ID', 3], ['Elastic', 4], ['Xi', 5] ]

for sel in selections:
    if selection == sel[0]: nSelect = sel[1] 

xsec, nevents = 0.0, 0.0
for mc in mcs:
    if 'data' in sample: 
        xsec, n_events = 1, 1
        data_ = True
    elif 'ALP' in sample:
        xsec, n_events = 1, 1
        data_ = False
    elif sample == mc[0]:
        xsec, n_events = float(mc[1]), float(mc[2])
        data_ = False


# TEMPORARY FOR RUNNING OVER AQGC SAMPLE FOR MATCHING PLOT FIXME FIXME FIXME FIXME FIXME FIXME
#xsec, n_events = 1, 1
#data_ = True


if data_: sample_weight = 1
else: 
    #lumi = lumi2017 if '2017' in sample else lumi2018
    if year == '2016': lumi = lumi2016
    elif year == '2017': lumi = lumi2017
    elif year == '2018': lumi = lumi2018
    sample_weight = xsec*lumi/n_events


print ''
print 'Sample:', sample, 'Weight:', sample_weight, 'Selection:', selection, 'nSelect:', nSelect
print '----------------------------------'
print ''


class DiphotonAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True

        self.count = 0

        # Get SF hists for ID and CSEV
        self.photonmapname = "EGamma_SF2D"        
        if '2016' in sample: 
            self.photon_file = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/egammaEffi.txt_EGM2D_Pho_wp90_UL16.root")
            self.csev_file = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/ScalingFactors_80X_Summer16.root")
            self.csevmapname = "Scaling_Factors_CSEV_R9 Inclusive"
        elif '2017' in sample: 
            self.photon_file = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/egammaEffi.txt_EGM2D_PHO_MVA90_UL17.root")
            self.csev_file = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/CSEV_ScaleFactors_2017.root")
            self.csevmapname = "MVA_ID"
        elif '2018' in sample:
            self.photon_file = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/2018_PhotonsMVAwp90.root")
            self.csev_file = open_root("/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/CSEV_2018.root")
            self.csevmapname = "eleVeto_SF"
        self.csev_map = get_root_obj(self.csev_file, self.csevmapname)
        self.photon_map = get_root_obj(self.photon_file, self.photonmapname)


        if nSelect == 2.5 or nSelect == 5:
            # Initialize objects for toy matching file
            self.diphoton_file = ROOT.TFile('/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/tmp/diphotonEvents_'+sample+'_'+selection+'_'+method+'.root', 'RECREATE')
            self.diphoton_tree = ROOT.TTree('tree','Tree with diphoton events')
            self.v_mass, self.v_rap, self.v_xip, self.v_xim, self.v_era, self.v_crossingAngle = array('f', []), array('f', []), array('f', []), array('f', []), array('f', []), array('f', [])
            self.diphoton_tree.Branch('mass', ROOT.AddressOf( mystruct, 'mass'), 'mass/F')
            self.diphoton_tree.Branch('rap', ROOT.AddressOf( mystruct, 'rap'), 'rap/F')
            self.diphoton_tree.Branch('xim', ROOT.AddressOf( mystruct, 'xim'), 'xim/F')
            self.diphoton_tree.Branch('xip', ROOT.AddressOf( mystruct, 'xip'), 'xip/F')
            self.diphoton_tree.Branch('crossingAngle', ROOT.AddressOf( mystruct, 'crossingAngle'), 'crossingAngle/L')
            self.diphoton_tree.Branch('era', ROOT.AddressOf( mystruct, 'era'), 'era/C')
            self.diphoton_tree.Branch('weight', ROOT.AddressOf( mystruct, 'weight'), 'weight/F')

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
        
        self.h_num_pho=ROOT.TH1F('h_num_pho', 'Number Of Photons', 8, 0, 8)
        self.h_diph_mass=ROOT.TH1F('h_diph_mass', 'Diphoton Mass', 100, 100 if nSelect<2 else 350, 2500.) # aqgc - 3000, data - 2500
        self.h_diph_rap=ROOT.TH1F('h_diph_rap', 'Diphoton Rapidity', 100, -2, 2)
        self.h_acop=ROOT.TH1F('h_acop', 'Diphoton Acoplanarity', 100, 0., 0.01 if nSelect < 4 else 0.0025) # aqgc - 0.01, data - 0.25 if nSelect < 4 else 0.01
        self.h_single_phi=ROOT.TH1F('h_single_phi', 'Single Photon #phi', 100, -6.3, 6.3)
        self.h_lead_phi=ROOT.TH1F('h_lead_phi', 'Leading Photon #phi', 100, -6.3, 6.3)
        self.h_sub_phi=ROOT.TH1F('h_sub_phi', 'Subleading Photon #phi', 100, -6.3, 6.3)
        self.h_pt_ratio=ROOT.TH1F('h_pt_ratio', 'Diphoton p_{T} Ratio', 100, 0, 2)
        self.h_single_eta=ROOT.TH1F('h_single_eta', 'Single Photon Eta', 100, -3.0, 3.0)
        self.h_lead_eta=ROOT.TH1F('h_lead_eta', 'Leading Photon Eta', 100, -3.0, 3.0)
        self.h_sub_eta=ROOT.TH1F('h_sub_eta', 'Subleading Photon Eta', 100, -3.0, 3.0)
        self.h_single_pt=ROOT.TH1F('h_single_pt', 'Single Photon pT', 100, 0.0, 750) # aqgc - 1400, data - 750
        self.h_lead_pt=ROOT.TH1F('h_lead_pt', 'Lead Photon pT', 100, 100, 750)
        self.h_sub_pt=ROOT.TH1F('h_sub_pt', 'Sublead Photon pT', 100, 100, 750)
        self.h_single_r9=ROOT.TH1F('h_single_r9', 'Single Photon R_{9}', 100, 0.5, 1) # aqgc - 0.8, data - 0.5 if nSelect < 4 else 0.8
        self.h_lead_r9=ROOT.TH1F('h_lead_r9', 'Lead Photon R_{9}', 100, 0.5, 1)
        self.h_sub_r9=ROOT.TH1F('h_sub_r9', 'Sublead Photon R_{9}', 100, 0.5, 1)
        self.h_single_hoe=ROOT.TH1F('h_single_hoe', 'Single Photon H/E', 100, 0, 1 if nSelect < 2 else 0.1)
        self.h_eb_hoe=ROOT.TH1F('h_eb_hoe', 'Lead Photon H/E', 100, 0, 1 if nSelect < 2 else 0.1)
        self.h_ee_hoe=ROOT.TH1F('h_ee_hoe', 'Sublead Photon H/E', 100, 0, 1 if nSelect < 2 else 0.1)
        self.h_single_sieie=ROOT.TH1F('h_single_sieie', 'Single Photon #sigma_{i#etai#eta}', 100, 0, 0.02)
        self.h_eb_sieie=ROOT.TH1F('h_eb_sieie', 'Lead Photon #sigma_{i#etai#eta}', 100, 0, 0.02)
        self.h_ee_sieie=ROOT.TH1F('h_ee_sieie', 'Sublead Photon #sigma_{i#etai#eta}', 100, 0, 0.02)
        self.h_single_electronVeto=ROOT.TH1F('h_single_electronVeto', 'Single Photon Electron Veto', 2, 0, 2)
        self.h_lead_electronVeto=ROOT.TH1F('h_lead_electronVeto', 'Lead Photon Electron Veto', 2, 0, 2)
        self.h_sub_electronVeto=ROOT.TH1F('h_sub_electronVeto', 'Sublead Photon Electron Veto', 2, 0, 2)
        self.h_isEEEE=ROOT.TH1F('h_isEEEE', 'EEEE', 2, 0, 2)
        self.h_xip=ROOT.TH1F('h_xip', '#xi _{#gamma#gamma}^{+}', 100, 0., 0.25)
        self.h_xim=ROOT.TH1F('h_xim', '#xi _{#gamma#gamma}^{-}', 100, 0., 0.25)
        self.h_nvtx=ROOT.TH1F('h_nvtx','Number Of Vertices', 75, 0., 75.)
        self.h_vtx_z=ROOT.TH1F('h_vtx_z', 'Vtx z position', 100,-15,15)
        self.h_fgr=ROOT.TH1F('h_fgr', 'fixedGridRho', 58, 0, 58)

        self.h_num_pro=ROOT.TH1F('h_num_pro', 'Number of Protons', 12, 0, 12)
        self.h_num_pro_45=ROOT.TH1F('h_num_pro_45', 'Number of Protons sector45', 8, 0, 8)
        self.h_num_pro_56=ROOT.TH1F('h_num_pro_56', 'Number of Protons sector56', 8, 0, 8)
        self.h_proton_side=ROOT.TH1F('h_proton_side', 'Proton side',4, 0, 4)
        self.h_detType=ROOT.TH1F('h_detType', 'PPS Detector Type', 2, 3, 5)
        self.h_pro_xip=ROOT.TH1F('h_pro_xip', 'Proton #xi ^{+}', 100, 0.00, 0.2)
        self.h_pro_xim=ROOT.TH1F('h_pro_xim', 'Proton #xi ^{-}', 100, 0.00, 0.2)
        self.h_pro_xi_45f=ROOT.TH1F('h_pro_xi_45f', 'Proton #xi 45F', 100, 0., 0.2)
        self.h_pro_xi_45n=ROOT.TH1F('h_pro_xi_45n', 'Proton #xi 45N', 100, 0., 0.2)
        self.h_pro_xi_56n=ROOT.TH1F('h_pro_xi_56n', 'Proton #xi 56N', 100, 0., 0.2)
        self.h_pro_xi_56f=ROOT.TH1F('h_pro_xi_56f', 'Proton #xi 56F', 100, 0., 0.2)
        self.h_pro_thetaY_45=ROOT.TH1F('h_pro_thetaY_45', 'Proton #theta_{y} 45', 100, -0.001, 0.001)
        self.h_pro_thetaY_56=ROOT.TH1F('h_pro_thetaY_56', 'Proton #theta_{y} 56', 100, -0.001, 0.001)
        self.h_pro_time_45=ROOT.TH1F('h_pro_time_45', 'Proton time 45', 100, -2, 2)
        self.h_pro_time_56=ROOT.TH1F('h_pro_time_56', 'Proton time 56', 100, -2, 2)
        self.h_hitmap45=ROOT.TH2F('h_hitmap45', 'sector45 hit map', 100, 0.0, 12.0, 100, -8.0, 8.0)
        self.h_hitmap56=ROOT.TH2F('h_hitmap56', 'sector56 hit map', 100, 0.0, 12.0, 100, -8.0, 8.0)

        self.gr_matching=ROOT.TGraphErrors('gr_matching')
        self.gr_matching.SetName('gr_matching')
        self.gr_numerator=ROOT.TGraphErrors('gr_numerator')
        self.gr_numerator.SetName('gr_numerator')
        self.gr_xip_matching=ROOT.TGraphErrors('gr_xip_matching')
        self.gr_xip_matching.SetName('gr_xip_matching')
        self.gr_xim_matching=ROOT.TGraphErrors('gr_xim_matching')
        self.gr_xim_matching.SetName('gr_xim_matching')


        self.addObject( self.h_num_pho ), self.addObject( self.h_diph_mass ), self.addObject( self.h_diph_rap )
        self.addObject( self.h_acop ), self.addObject( self.h_pt_ratio )
        self.addObject( self.h_single_eta ), self.addObject( self.h_lead_eta ), self.addObject( self.h_sub_eta ) 
        self.addObject( self.h_single_pt ), self.addObject( self.h_lead_pt ), self.addObject( self.h_sub_pt )
        self.addObject( self.h_single_r9 ), self.addObject( self.h_lead_r9 ), self.addObject( self.h_sub_r9 )
        self.addObject( self.h_single_hoe ), self.addObject( self.h_eb_hoe ), self.addObject( self.h_ee_hoe )
        self.addObject( self.h_single_sieie ), self.addObject( self.h_eb_sieie ), self.addObject( self.h_ee_sieie )
        self.addObject( self.h_single_electronVeto ), self.addObject( self.h_lead_electronVeto ), self.addObject( self.h_sub_electronVeto )
        self.addObject( self.h_isEEEE )
        self.addObject( self.h_xip ), self.addObject( self.h_xim )
        self.addObject( self.h_nvtx ), self.addObject( self.h_vtx_z ), self.addObject( self.h_fgr )

        if data_:
            self.addObject( self.h_num_pro ), self.addObject( self.h_num_pro_45 ), self.addObject( self.h_num_pro_56 ), 
            self.addObject( self.h_detType ), self.addObject( self.h_proton_side )
            self.addObject( self.h_pro_xip ), self.addObject( self.h_pro_xim )
            self.addObject( self.h_pro_xi_45f ), self.addObject( self.h_pro_xi_45n )
            self.addObject( self.h_pro_xi_56n ), self.addObject( self.h_pro_xi_56f )
            self.addObject( self.h_pro_thetaY_45 ), self.addObject( self.h_pro_thetaY_56 )
            self.addObject( self.gr_matching )
            self.addObject( self.gr_numerator )
            self.addObject( self.gr_xip_matching ), self.addObject( self.gr_xim_matching )
            self.addObject( self.h_hitmap45 ), self.addObject( self.h_hitmap56 )


        if not data_:
            self.mcfile = ROOT.TFile( '/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/%s/nanoAOD_%s_Skim.root' % (year,sample) )
            self.mchist = ROOT.TH1F('mchist', 'fixedGridRho', 58, 0, 58) 
            self.mctree = self.mcfile.Events
            self.mctree.Project('mchist', 'fixedGridRhoFastjetAll')
            self.mchist.Scale( 1 / self.mchist.Integral() )

            self.datafile = ROOT.TFile( '/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/dataFixedGridRho_%s.root' % year )
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

        print 'Events passing:', self.count

        if nSelect == 2.5 or nSelect == 5:
            self.diphoton_file.Write()
            self.diphoton_file.Close()

    # Get the SFs for MCs
    def efficiency(self,pt,eta_sc,r9):
        if nSelect != 2.5 and nSelect < 3: return 1.0
        bin_x = min( max( self.photon_map.GetXaxis().FindBin( eta_sc ), 1 ), self.photon_map.GetXaxis().GetNbins() )
        bin_y = min( max( self.photon_map.GetYaxis().FindBin( pt ), 1 ), self.photon_map.GetYaxis().GetNbins() )
        id_sf = self.photon_map.GetBinContent( bin_x, bin_y )
        if '2016' in sample:
            bin_x = min( max( self.csev_map.GetXaxis().FindBin( pt ), 1 ), self.csev_map.GetXaxis().GetNbins() )
            bin_y = min( max( self.csev_map.GetYaxis().FindBin( eta_sc ), 1 ), self.csev_map.GetYaxis().GetNbins() )
            csev_sf = self.csev_map.GetBinContent( bin_x, bin_y )
        elif '2017' in sample:
            if eta_sc <= 1.4442: bin_r9 = 2 if r9 > 0.94 else 3
            else: bin_r9 = 5 if r9 > 0.94 else 6
            csev_sf = self.csev_map.GetBinContent( bin_r9 ) 
        elif '2018' in sample:
            bin_x = min( max( self.csev_map.GetXaxis().FindBin( eta_sc ), 1 ), self.csev_map.GetXaxis().GetNbins() )
            bin_y = min( max( self.csev_map.GetYaxis().FindBin( pt ), 1 ), self.csev_map.GetYaxis().GetNbins() )
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


    def analyze(self, event):
        if data_ and method == 'singleRP': protons, tracks = Collection(event, "Proton_singleRP"), Collection(event, "PPSLocalTrack") # edited
        elif data_ and method == 'multiRP': protons, tracks = Collection(event, "Proton_multiRP"), Collection(event, "PPSLocalTrack") # edited
        photons = Collection(event, "Photon")
        if data_: pu_weight, vtxWeight, prefWeight, eff_pho1, eff_pho2 = 1.0, 1.0, 1.0, 1.0, 1.0
        else: 
            try: pu_weight, vtxWeight, prefWeight = event.puWeightUp, self.rhoReweight(event.Pileup_nPU), event.PrefireWeight if '2017' in sample else 1.0
            except: pu_weight, vtxWeight, prefWeight = 1.0, 1.0, 1.0
        s_weight = sample_weight*pu_weight*prefWeight

        if len(photons) < 2: return
                
        # Choose the best diphoton candidate
        acop = 999.0
        pho1, pho2 = photons[0], photons[1]
        for combo in combinations(range(0,len(photons)),2):
            p1, p2 = photons[combo[0]], photons[combo[1]]
            if p1.pt < 100.0 or p2.pt < 100.0: continue
            tmp_acop =  1.0 - abs( p1.p4().DeltaPhi(p2.p4()) ) / PI
            if tmp_acop > acop: continue
            acop = tmp_acop
            pho1, pho2 = p1, p2
            
        diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
        diph_mass = diph_p4.M()
        diph_rap = diph_p4.Rapidity()
        delta_phi = pho1.p4().DeltaPhi(pho2.p4())
        xip = 1/13000.0*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
        xim = 1/13000.0*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )
        if data_: weight = 1
        pt_thresh = 75.0 if year == '2016' else 100.0

        # Make selection cuts
        if nSelect > 1:                                   # Preselection
            if pho1.pt < pt_thresh or pho2.pt < pt_thresh: return
            if not hoe_cut(pho1,pho2): return
            if not eta_cut(pho1,pho2): return 
            if not mass_cut(diph_mass): return
        if nSelect > 2:                                   # ID
            if not photon_id(pho1,pho2): return
            if not electron_veto(pho1,pho2): return
        if nSelect == 2.5:                                # Reverse Elastic
            if acop_cut(acop): return
        if nSelect > 3:                                   # Elastic
            if not acop_cut(acop): return
        if nSelect > 4 or nSelect == 2.5:                 # Tight xi or reverse elastic
            if not xi_cut(xip,xim): return

        self.count += 1

        # Print high-mass event kinematics
        if data_: 
            if nSelect == 5 and diph_mass > 1000:
                with open('/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/events_%s.txt' % year, 'a') as f:
                    print >> f, 'R:L:E', str(event.run)+':'+str(event.luminosityBlock)+':'+str(event.event), 'npho:', len(photons), 'nvtx:', event.PV_npvs, 'vtx_z:', event.PV_z
                    print >> f, 'mass:', diph_mass, 'Acoplanarity:', acop
                    print >> f, 'pt1:', pho1.pt, 'pt2:', pho2.pt, 'eta1:', pho1.eta, 'eta2:', pho2.eta
                    print >> f, 'R9_1:', pho1.r9, 'R9_2:', pho2.r9, 'xip:', xip, 'xim:', xim
                    print >> f, 'Num protons:', len(protons)
                    if len(protons) > 0: 
                        for i in range(0,len(protons)-1): print >> f,  'proton'+str(i), 'xi:', protons[i].xi
                    print >> f, ''

        if not data_:
            eff_pho1, eff_pho2 = self.efficiency(pho1.pt,pho1.eta,pho1.r9), self.efficiency(pho2.pt,pho2.eta,pho2.r9)
            weight = s_weight * ( eff_pho1*eff_pho2 )

        # Fill diphoton tree for background estimation

        if nSelect == 2.5 or nSelect == 5: # xi and reverse FIXME FIXME FIXME change nSelect to 5 not 4
            mystruct.mass = diph_mass
            mystruct.rap = diph_rap
            mystruct.xim = xim
            mystruct.xip = xip
            mystruct.weight = weight
            if data_:
                mystruct.crossingAngle = event.LHCInfo_crossingAngle # edited from xangle
                mystruct.era = getEra(event.run)
            else: # dummy variables
                mystruct.crossingAngle = 150.0 # random crossingAngle
                mystruct.era = '2017E' if '2017' in sample else '2018D' # random eras
            self.diphoton_tree.Fill()

        # Fill single photon hists
        self.h_single_eta.Fill(pho1.eta,s_weight*eff_pho1), self.h_single_eta.Fill(pho2.eta,s_weight*eff_pho2)
        self.h_lead_eta.Fill(pho1.eta,s_weight*eff_pho1), self.h_sub_eta.Fill(pho2.eta,s_weight*eff_pho2)
        self.h_single_pt.Fill(pho1.pt,s_weight*eff_pho1), self.h_single_pt.Fill(pho2.pt,s_weight*eff_pho2)
        self.h_lead_pt.Fill(pho1.pt,s_weight*eff_pho1), self.h_sub_pt.Fill(pho2.pt,s_weight*eff_pho2)
        self.h_single_r9.Fill(pho1.r9,s_weight*eff_pho1), self.h_single_r9.Fill(pho2.r9,s_weight*eff_pho2)
        self.h_lead_r9.Fill(pho1.r9,s_weight*eff_pho1), self.h_sub_r9.Fill(pho2.r9,s_weight*eff_pho2)
        self.h_single_hoe.Fill(pho1.hoe,s_weight*eff_pho1), self.h_single_hoe.Fill(pho2.hoe,s_weight*eff_pho2)
        self.h_single_sieie.Fill(pho1.sieie,s_weight*eff_pho1), self.h_single_sieie.Fill(pho2.sieie,s_weight*eff_pho2)
        self.h_single_electronVeto.Fill(pho1.electronVeto,s_weight*eff_pho1), self.h_single_electronVeto.Fill(pho2.electronVeto,s_weight*eff_pho2) 
        self.h_lead_electronVeto.Fill(pho1.electronVeto,s_weight*eff_pho1), self.h_sub_electronVeto.Fill(pho2.electronVeto,s_weight*eff_pho2) 
        if abs(pho1.eta) <= 1.4442: self.h_eb_hoe.Fill(pho1.hoe,s_weight*eff_pho1), self.h_eb_sieie.Fill(pho1.sieie,s_weight*eff_pho1)
        else: self.h_ee_hoe.Fill(pho1.hoe,s_weight*eff_pho1), self.h_ee_sieie.Fill(pho1.sieie,s_weight*eff_pho1)
        if abs(pho2.eta) <= 1.4442: self.h_eb_hoe.Fill(pho2.hoe,s_weight*eff_pho2), self.h_eb_sieie.Fill(pho2.sieie,s_weight*eff_pho2)
        else: self.h_ee_hoe.Fill(pho2.hoe,s_weight*eff_pho2), self.h_ee_sieie.Fill(pho2.sieie,s_weight*eff_pho2)
        if abs(pho1.eta) >= 1.566: self.h_isEEEE.Fill( 1, weight )
        else: self.h_isEEEE.Fill( 0, weight )


        # Fill diphoton hists
        self.h_diph_mass.Fill(diph_mass,weight) 
        self.h_diph_rap.Fill(diph_rap,weight)
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
        v45, v56 = [], []
        for i, proton in enumerate(protons):
            v_trks = []
            for t in tracks:
                if method == 'multiRP':
                    if t.multiRPProtonIdx == i: v_trks.append(t) 
                elif method == 'singleRP':
                    if t.singleRPProtonIdx == i: v_trks.append(t)

            if not checkProton(event.run,event.LHCInfo_crossingAngle,v_trks,proton): continue #FIXME FIXME FIXME
            if proton.sector45:   v45.append(proton), self.h_pro_xip.Fill( proton.xi )
            elif proton.sector56: v56.append(proton), self.h_pro_xim.Fill( proton.xi )
            #if proton.arm == 0:   v45.append(proton), self.h_pro_xip.Fill( proton.xi ) # CMSSW version FIXME
            #elif proton.arm == 1: v56.append(proton), self.h_pro_xim.Fill( proton.xi ) # CMSSW version FIXME

            for t in v_trks: 
                if proton.sector45: self.h_hitmap45.Fill(t.x, t.y) # FIXME
                if proton.sector56: self.h_hitmap56.Fill(t.x, t.y) # FIXME
                #if proton.arm == 0: self.h_hitmap45.Fill(t.x, t.y)
                #if proton.arm == 1: self.h_hitmap56.Fill(t.x, t.y)
            if method == 'singleRP':
                self.h_detType.Fill( 0 if proton.decRPId == 3 or proton.decRPId == 103 else 1 )  # not available for multiRP
                if proton.decRPId == 23: self.h_pro_xi_45f.Fill( proton.xi )                     # not available for multiRP
                elif proton.decRPId == 3: self.h_pro_xi_45n.Fill( proton.xi )                    # not available for multiRP
                elif proton.decRPId == 103: self.h_pro_xi_56n.Fill( proton.xi )                  # not available for multiRP
                elif proton.decRPId == 123: self.h_pro_xi_56f.Fill( proton.xi )                  # not available for multiRP
                else: print 'Proton not in known det id:', proton.decDetId                       # not available for multiRP
            if method == 'multiRP':
                if proton.sector45: self.h_pro_thetaY_45.Fill(proton.thetaY), self.h_pro_time_45.Fill(proton.time) # FIXME
                else: self.h_pro_thetaY_56.Fill(proton.thetaY), self.h_pro_time_56.Fill(proton.time) #FIXME
                #if proton.arm == 0: self.h_pro_thetaY_45.Fill(proton.thetaY), self.h_pro_time_45.Fill(proton.time) 
                #else: self.h_pro_thetaY_56.Fill(proton.thetaY), self.h_pro_time_56.Fill(proton.time)
                
        self.h_num_pro_45.Fill( len(v45) ), self.h_num_pro_56.Fill( len(v56) )

        if len(v45) == 0 or len(v56) == 0: # check for two opposite-side protons
            if len(v45) == 0 and len(v56) == 0: self.h_proton_side.Fill(0)
            if len(v45) > 0 and len(v56) == 0:  self.h_proton_side.Fill(1)
            if len(v56) > 0 and len(v45) == 0:  self.h_proton_side.Fill(2)
            return
        
        self.h_proton_side.Fill(3)

        # Remove protons not within chosen xi range
        if nSelect == 5:
            for i, pro in enumerate(v45):
                if pro.xi < 0.035 or pro.xi > 0.15: del v45[i]
            for j, pro in enumerate(v56):
                if pro.xi < 0.035 or pro.xi > 0.18: del v56[j]
            
            # Cut on events without opposite-side signal protons
            if len(v45) == 0 or len(v56) == 0: return
            
        
        # Choose the diproton candidate with the best xi matching
        #pro_m = min(v56, key=lambda x:abs(x.xi-xim))
        #pro_p = min(v45, key=lambda x:abs(x.xi-xip))

        # Choose the diproton candidate with the highest xi
        pro_m = max(v56, key=lambda x:x.xi)
        pro_p = max(v45, key=lambda x:x.xi)

        # stop if the xi cut didn't work
        if nSelect == 5: 
            if pro_m.xi < 0.035 or pro_m > 0.18:
                print 'Stop everything! pro_m.xi =', pro_m.xi
                sys.exit()
            if pro_p.xi < 0.035 or pro_p > 0.15:
                print 'Stop everything! pro_p.xi =', pro_p.xi
                sys.exit()

        # Set point for matching plot
        pps_mass, pps_rap = mass(pro_m.xi,pro_p.xi), rapidity(pro_m.xi,pro_p.xi) 
        pps_mass_err, pps_rap_err = mass_err(method, pro_m, pro_p, event.run), rapidity_err(method, pro_m, pro_p, event.run)
        mass_point = (pps_mass - diph_mass) / (pps_mass_err + diph_mass*rel_mass_err) 
        rap_point = (pps_rap + diph_rap) / (pps_rap_err + rel_rap_err*abs(diph_rap))

        #print 'pps_rap:', pps_rap, 'diph_rap:', diph_rap, 'pps_rap_err:', pps_rap_err, 'diph_rap_err:', rel_rap_err*abs(diph_rap)
        #print ''
        
        # print signal event kinematics
        if abs(mass_point) < 3 and abs(rap_point) < 3:
            print 'Mass point:', mass_point, 'Rap point:', rap_point
            print 'xip:', pro_p.xi, 'xim:', pro_m.xi
            print 'pps mass err:', pps_mass_err, 'pps rap err:', pps_rap_err
            print 'diph mass:', diph_mass, 'diph_rap', diph_rap
            print 'pt1:', pho1.pt, 'pt2:', pho2.pt
        
        self.gr_matching.SetPoint( self.gr_matching.GetN(), mass_point, rap_point )
        self.gr_numerator.SetPoint( self.gr_numerator.GetN(), pps_mass - diph_mass, pps_rap + diph_rap )
        self.gr_xim_matching.SetPoint( self.gr_xim_matching.GetN(), pro_m.xi, xim )
        self.gr_xip_matching.SetPoint( self.gr_xip_matching.GetN(), pro_p.xi, xip )


        return True

preselection=""
if sample == 'data2016':
    files=[
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2016/nanoAOD_Run2016B_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2016/nanoAOD_Run2016C_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2016/nanoAOD_Run2016G_Skim.root",
    ]
elif sample == 'data2017':
    files=[
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2017/nanoAOD_Run2017B_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2017/nanoAOD_Run2017C_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2017/nanoAOD_Run2017D_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2017/nanoAOD_Run2017E_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2017/nanoAOD_Run2017F_Skim.root"
    ]
elif sample == 'data2018':
    files=[
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2018/nanoAOD_Run2018A_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2018/nanoAOD_Run2018B_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2018/nanoAOD_Run2018C_Skim.root",
        "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2018/nanoAOD_Run2018D_Skim.root",
    ]
else: 
    if '2016' in sample:
        files=["/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2016/nanoAOD_"+sample+"_Skim.root"]
    elif '2017' in sample:
        files=["/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2017/nanoAOD_"+sample+"_Skim.root"]
    elif '2018' in sample:
        files=["/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/Skims/2018/nanoAOD_"+sample+"_Skim.root"]
        
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[DiphotonAnalysis()],noOut=True,histFileName="/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/tmp/histOut_"+sample+"_"+selection+"_"+method+".root",histDirName="plots")
p.run()


