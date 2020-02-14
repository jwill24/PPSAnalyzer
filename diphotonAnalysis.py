# Things To Do
#   1. Implement proton errors when available

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
rel_mass_err = 0.02
rel_rap_err = 0.074
rel_xi_err = 0.08

sample = str( sys.argv[1] )

mcs = [ ['ggj', 138.5, 4000000],['g+j',873.7,80000000],['qcd',117500,4000000],['wg',191.1,6300000],['zg',55.47,30000000], ['tt',494.9,8026103], ['aqgc',3.86e-5,300000] ]

for mc in mcs:
    if sample == 'data': 
        xsec, n_events = 1, 1
        data_ = True
    elif sample == mc[0]:
        xsec, n_events = mc[1], mc[2]
        data_ = False

if data_: sample_weight = 1
else: sample_weight = xsec*lumi/n_events

class DiphotonAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True
        self.n_passing = 0
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
        
        self.h_num_pho=ROOT.TH1F('h_num_pho', 'Number Of Photons', 10, 0, 10)
        self.h_diph_mass=ROOT.TH1F('h_diph_mass', 'Diphoton Mass', 100, 350., 2500.)
        self.h_acop=ROOT.TH1F('h_acop', 'Diphoton Acoplanarity', 100, 0., 0.25)
        self.h_single_eta=ROOT.TH1F('h_single_eta', 'Single Photon Eta', 100, -3.0, 3.0)
        self.h_lead_eta=ROOT.TH1F('h_lead_eta', 'Leading Photon Eta', 100, -3.0, 3.0)
        self.h_sub_eta=ROOT.TH1F('h_sub_eta', 'Subleading Photon Eta', 100, -3.0, 3.0)
        self.h_single_pt=ROOT.TH1F('h_single_pt', 'Single Photon pT', 100, 0., 750.0)
        self.h_lead_pt=ROOT.TH1F('h_lead_pt', 'Lead Photon pT', 100, 0., 750.0)
        self.h_sub_pt=ROOT.TH1F('h_sub_pt', 'Sublead Photon pT', 100, 0., 750.0)
        self.h_single_r9=ROOT.TH1F('h_single_r9', 'Single Photon R_{9}', 100, 0.5, 1)
        self.h_lead_r9=ROOT.TH1F('h_lead_r9', 'Lead Photon R_{9}', 100, 0.5, 1)
        self.h_sub_r9=ROOT.TH1F('h_sub_r9', 'Sublead Photon R_{9}', 100, 0.5, 1)
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

        self.addObject( self.h_num_pho )
        self.addObject( self.h_diph_mass )
        self.addObject( self.h_acop )
        self.addObject( self.h_single_eta )
        self.addObject( self.h_lead_eta )
        self.addObject( self.h_sub_eta )
        self.addObject( self.h_single_pt )        
        self.addObject( self.h_lead_pt )        
        self.addObject( self.h_sub_pt )        
        self.addObject( self.h_single_r9 )
        self.addObject( self.h_lead_r9 )
        self.addObject( self.h_sub_r9 )
        self.addObject( self.h_xip )
        self.addObject( self.h_xim )
        self.addObject( self.h_pro_xi_45f )
        self.addObject( self.h_pro_xi_45n )
        self.addObject( self.h_pro_xi_56n )
        self.addObject( self.h_pro_xi_56f )
        self.addObject( self.h_nvtx )
        self.addObject( self.h_vtx_z )
        self.addObject( self.h_fgr )

        if data_:
            self.addObject( self.h_num_pro )
            self.addObject( self.h_detType )
            self.addObject( self.h_pro_xip )
            self.addObject( self.h_pro_xim )
            self.addObject( self.gr_matching )


        if not data_:
            self.mcfile = ROOT.TFile( 'Skims/nanoAOD_'+sample+'2017_Skim.root' )
            self.mchist = ROOT.TH1F('mchist', 'fixedGridRho', 100, 0, 58)
            self.mctree = self.mcfile.Events
            self.mctree.Project('mchist', 'fixedGridRhoFastjetAll')
            self.mchist.Scale( 1 / self.mchist.Integral() )

            self.datafile = ROOT.TFile( 'dataFixedGridRho.root' )
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
        #print ''
        #print ''
        #print 'Events (at least 1 EB photon):', self.n_passing
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

    # Tight xi cut
    def xi_cut(self,xip,xim):
        if xip < 0.015 or xip > 0.2: return False
        if xim < 0.015 or xim > 0.2: return False
        return True

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
    '''
    def mass_matching(self,diph_mass,pro1,pro2):
        m = self.mass(pro1.xi,pro2.xi)
        error = self.mass_err(pro1,pro2)
        if diph_mass > (m - error) and diph_mass < (m + error): return True
        else: return False
            
    def rap_matching(self,diph_rap,pro1,pro2):
        rap = self.rapidity(pro1.xi,pro2.xi)
        #error = 0.2
        error = self.rapidity_err(pro1,pro2)
        if rap > (diph_rap - error) and rap < (diph_rap + error): return True
        else: return False
    '''

    def mass_matching(self,mp):
        if abs(mp) <= 3: return True
        else: return False

    def rap_matching(self,rp):
        if abs(rp) <= 3: return True
        else: return False

    def analyze(self, event):
        if data_: protons = Collection(event, "Proton_singleRP")
        photons = Collection(event, "Photon")
        if data_: pu_weight, vtxWeight, eff_pho1, eff_pho2 = 1, 1, 1, 1
        else: pu_weight, vtxWeight = event.puWeightUp, self.rhoReweight(event.Pileup_nPU)
        s_weight = sample_weight*pu_weight
        
        if len(photons) < 2: return
        
        # Choose the best diphoton candidate
        #it = 0
        acop = 999
        pho1, pho2 = photons[0], photons[1]
        for combo in combinations(range(0,len(photons)),2):
            p1, p2 = photons[combo[0]], photons[combo[1]]
            if p1.pt < 75 or p2.pt < 75: return
            tmp_acop =  1 - abs( p1.p4().DeltaPhi(p2.p4()) ) / PI
            if tmp_acop > acop: continue #FIXME
            acop = tmp_acop
            pho1, pho2 = p1, p2
        
        if pho1.pt < 75 or pho2.pt < 75: return
        diph_p4 = ROOT.TLorentzVector( pho1.p4() + pho2.p4() )
        diph_mass = diph_p4.M()
        diph_rap = diph_p4.Rapidity()
        delta_phi = pho1.p4().DeltaPhi(pho2.p4())
        xip = 1/13000.*( pho1.pt*math.exp(pho1.eta)+pho2.pt*math.exp(pho2.eta) )
        xim = 1/13000.*( pho1.pt*math.exp(-1*pho1.eta)+pho2.pt*math.exp(-1*pho2.eta) )
        if data_: weight = 1
        #else: s_weight = sample_weight*vtxWeight#*pu_weight


        #if p1.isScEtaEE and p2.isScEtaEE: continue
        #if pho1.isScEtaEB and pho2.isScEtaEB:
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
                                        #return
                                    #else: return


        # Make selection cuts
        #if pho1.isScEtaEB and pho1.hoe > 0.04596: continue # loose hoe cut
        #if pho1.isScEtaEE and pho1.hoe > 0.05900: continue # loose hoe cut
        #if pho2.isScEtaEB and pho2.hoe > 0.04596: continue # loose hoe cut
        #if pho2.isScEtaEE and pho2.hoe > 0.05900: continue # loose hoe cut
        
        #if pho1.r9 < 0.85 or pho2.r9 < 0.85: return 
        #if not self.eta_cut(pho1,pho2): return
        #if not self.mass_cut(diph_mass): return
        #if not self.photon_id(pho1,pho2): return
        #if not self.electron_veto(pho1,pho2): return
        #if not self.acop_cut(acop): return
        #if not self.xi_cut(xip,xim): return

        if data_ and diph_mass > 1800:
            with open('events.txt', 'w') as f:
                print >> f, 'R:L:E', str(event.run)+':'+str(event.luminosityBlock)+':'+str(event.event), 'mass:', diph_mass, 'Acoplanarity:', acop
                print >> f, 'Num protons:', len(protons)
        
        if not data_:
            eff_pho1 = self.efficiency(pho1.pt,pho1.eta)
            eff_pho2 = self.efficiency(pho2.pt,pho2.eta)
            weight = s_weight * ( eff_pho1*eff_pho2 )

        # Fill single photon hists
        self.h_single_eta.Fill(pho1.eta,s_weight*eff_pho1), self.h_single_eta.Fill(pho2.eta,s_weight*eff_pho2)
        self.h_lead_eta.Fill(pho1.eta,s_weight*eff_pho1),   self.h_sub_eta.Fill(pho2.eta,s_weight*eff_pho2)
        self.h_single_pt.Fill(pho1.pt,s_weight*eff_pho1),   self.h_single_pt.Fill(pho2.pt,s_weight*eff_pho2)
        self.h_lead_pt.Fill(pho1.pt,s_weight*eff_pho1),     self.h_sub_pt.Fill(pho2.pt,s_weight*eff_pho2)
        self.h_single_r9.Fill(pho1.r9,s_weight*eff_pho1),   self.h_single_r9.Fill(pho2.r9,s_weight*eff_pho2)
        self.h_lead_r9.Fill(pho1.r9,s_weight*eff_pho1),     self.h_sub_r9.Fill(pho2.r9,s_weight*eff_pho2)

        # Fill diphoton hists
        self.h_diph_mass.Fill(diph_mass,weight)
        self.h_acop.Fill(acop,weight)
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
            self.h_detType.Fill( proton.protonRPType )
            if proton.sector45: self.h_pro_xim.Fill( proton.xi )
            elif proton.sector56: self.h_pro_xip.Fill( proton.xi ) 
            if proton.decDetId == 3: self.h_pro_xi_45f.Fill( proton.xi )
            elif proton.decDetId == 23: self.h_pro_xi_45n.Fill( proton.xi )
            elif proton.decDetId == 103: self.h_pro_xi_56n.Fill( proton.xi )
            elif proton.decDetId == 123: self.h_pro_xi_56f.Fill( proton.xi )
            else: print 'Proton not in known det id:', proton.decDetId

        # Choose the best diproton candidate
        pps_dist = 999
        if not self.two_protons(protons): return
        pro1, pro2 = protons[0], protons[1]
        for combo in combinations(range(0,len(protons)),2):
            pr1, pr2 = protons[combo[0]], protons[combo[1]]
            if pr1.sector45 == pr2.sector45: continue
            if pr1.sector56 == pr2.sector56: continue
            tmp_frac, tmp_diff = self.mass(pr1.xi,pr2.xi)/diph_mass, self.rapidity(pr1.xi,pr2.xi)-diph_rap
            tmp_dist = math.sqrt( pow(tmp_frac,2) + pow(tmp_diff,2) )
            if tmp_dist < pps_dist:
                pps_dist = tmp_dist
                pro1, pro2 = pr1, pr2

        # SetPoint for matching plot
        pps_mass, pps_rap = self.mass(pro1.xi,pro2.xi), self.rapidity(pro1.xi,pro2.xi)
        pps_mass_err, pps_rap_err = self.mass_err(pro1, pro2), self.rapidity_err(pro1, pro2)
        mass_point = (pps_mass - diph_mass) / (pps_mass_err + diph_mass*rel_mass_err) 
        rap_point = (pps_rap - diph_rap) / (pps_rap_err + rel_rap_err*diph_rap)
        self.gr_matching.SetPoint( self.gr_matching.GetN(), mass_point, rap_point )
        #self.gr_matching.SetPoint( self.gr_matching.GetN(),\
            #pps_mass / diph_mass,\
            #pps_rap - diph_rap )
        #self.gr_matching.SetPointError( self.gr_matching.GetN()-1,\
            #(pps_mass/diph_mass) * math.sqrt( pow(pps_mass_err/pps_mass,2) + pow(rel_mass_err,2) ),\
            #pps_rap_err + rel_rap_err*diph_rap )

        #print ''
        #print 'PPS relative errors --->', 'xi1:', str(round(pro1.xiError*100 / pro1.xi,2)) + '%', 'xi2:', str(round(pro2.xiError*100 / pro2.xi,2)) + '%'
        #print 'PPS mass:', pps_mass, 'PPS mass error:', pps_mass_err
        #print 'xi1:', pro1.xi, 'xi1 error:', pro1.xiError, 'xi2:', pro2.xi, 'xi2 error:', pro2.xiError
        #print ''
        
        #print ''
        #print 'PPS mass:', pps_mass, 'CMS mass:', diph_mass
        #print 'PPS rap:', pps_rap, 'CMS rap:', diph_rap
        #print 'Mass point:', mass_point, 'Rap point:', rap_point
        #print ''

        #if self.mass_matching(diph_mass,pro1,pro2) and self.rap_matching(diph_rap,pro1,pro2):
        '''
        if self.mass_matching(mass_point) and self.rap_matching(rap_point):
            print ""
            print "Passing cuts!"
            print "R:L:E", str(event.run)+":"+str(event.luminosityBlock)+":"+str(event.event)
            print "Diphoton mass:", diph_mass
            print "Diphoton rapidity:", diph_rap
            print "Acoplanarity:", acop
            print "Pho1 pT:", pho1.pt, "Pho2 pT:", pho2.pt
            print "Pho1 eta:", pho1.eta, "Pho2 eta:", pho2.eta
            print "xi1:", pro1.xi, "xi2:", pro2.xi
            print "Diproton mass:", sqrts*math.sqrt(pro1.xi*pro2.xi)
            print "Diproton rapidity:", 0.5*math.log(pro1.xi/pro2.xi)
            print "" 
           '''                     
        
        return True

preselection=""
if sample == 'data' : 
    files=[
        "Skims/nanoAOD_Run2017B_Skim.root",
        "Skims/nanoAOD_Run2017C_Skim.root",
        "Skims/nanoAOD_Run2017D_Skim.root",
        "Skims/nanoAOD_Run2017E_Skim.root",
        "Skims/nanoAOD_Run2017F_Skim.root"
    ]
else: 
    files=[
        "Skims/nanoAOD_"+sample+"2017_Skim.root"
    ]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[DiphotonAnalysis()],noOut=True,histFileName="histOut_"+sample+"_HLTpuUp_2017.root",histDirName="plots")
p.run()


