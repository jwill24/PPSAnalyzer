#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F, TH1D
from ROOT import gROOT, gStyle

from common import Prettify

gStyle.SetOptStat(0)

era = '2018'

color = 50
stations = [['0','45'], ['1','56'], ['3','45N'], ['23','45F'], ['103','56N'], ['123','56F']]

#aqgcFile = TFile('outputHists/histOut_resolution_aqgc.root')
#aqgcFile = TFile('histOut_signal_singleRP_2017postTS2.root')

f = TFile('outputHists/directSimulation/output_hists_%s.root' % era)
f_eff = TFile('outputHists/directSimulation/output_hists_%s_withWeights.root' % era)

def Canvas(name):
    c = TCanvas(name,'c',750,600)
    return c

def selectionLabel(text):
    label = TPaveText( 0.1, 0.9, 0.18, 0.92, 'NB NDC' ) 
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( text )
    label.SetTextSize( 0.048 )
    label.SetTextAlign(11)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def condLabel():
    label = TPaveText( 0.57, 0.9, 0.73, 0.93, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "%s cond. (13 TeV)" % era )
    label.SetTextSize( 0.034 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label

def descriptionLabel():
    label = TPaveText( 0.73, 0.65, 0.81, 0.8, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "Elastic #gamma#gamma#rightarrow#gamma#gamma" )
    label.AddText( "FPMC BSM pred." )
    label.AddText( "#sigma_{bd} = 30 #murads" )
    label.SetTextSize( 0.032 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label


def simLabel():
    label = TPaveText( 0.10, 0.9, 0.18, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.SetTextAlign(11)
    label.AddText( "#font[62]{CMS} #font[52]{Simulation}" )
    label.SetTextSize(0.035)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def makeStats(mean,rms):
    label = TPaveText( 0.25, 0.7, 0.3, 0.8, 'NB NDC' )
    label.SetTextSize( 0.035 )
    label.SetTextFont( 42 )
    label.SetFillStyle( 0 )
    label.SetLineWidth( 0 )
    label.AddText( 'Mean = ' + str(mean) )
    label.AddText( 'RMS = ' + str(rms) )
    return label

def addText():
    label = TPaveText( 0.7, 0.7, 0.75, 0.8, 'NB NDC' )
    label.SetTextSize( 0.04 )
    label.SetTextFont( 42 )
    label.SetFillStyle( 0 )
    label.SetLineWidth( 0 )
    label.AddText( "Elastic #gamma#gamma#rightarrow#gamma#gamma" )
    label.AddText( "FPMC, BSM pred." )
    return label

def plotRes(variable, symbol, h):
    c = Canvas('c')
    c.SetTicks(1,1)
    c.SetLeftMargin(0.12)
    h.SetTitle('')
    h.SetXTitle('('+symbol+'_{reco} - '+symbol+'_{gen})/'+symbol+'_{gen}')
    h.GetXaxis().SetTitleOffset(1.2)
    h.GetXaxis().SetLimits(-0.25,0.25)
    h.SetYTitle('Events')
    h.SetFillColorAlpha(color,0.0001)
    h.SetLineColor(color)
    h.Draw()
    mean, rms = round(h.GetMean(),3), round(h.GetRMS(),4)
    statsLabel = makeStats(mean,rms)
    sampleText, cLabel, pLabel = addText(), condLabel(), simLabel()
    sampleText.Draw(), cLabel.Draw(), pLabel.Draw(), statsLabel.Draw()
    c.SaveAs('plots/resolution/'+variable + '_resolution.png')

def plotDiff(variable, symbol, h):
    c = Canvas('c')
    c.SetTicks(1,1)
    c.SetLeftMargin(0.12)
    h.SetTitle('')
    h.SetXTitle(symbol+'_{reco} - '+symbol+'_{gen}')
    h.GetXaxis().SetTitleOffset(1.2)
    h.GetXaxis().SetLimits(-0.25,0.25)
    h.SetYTitle('Events')
    h.SetFillColorAlpha(color,0.0001)
    h.SetLineColor(color)
    h.Draw()
    mean, rms = round(h.GetMean(),3), round(h.GetRMS(),4)
    statsLabel = makeStats(mean,rms)
    sampleText, cLabel, pLabel = addText(), condLabel(), simLabel()
    sampleText.Draw(), cLabel.Draw(), pLabel.Draw(), statsLabel.Draw()
    c.SaveAs('plots/resolution/'+variable + '_difference.png')

#def plotEfficiency(var,method,numpro):
def plotEA(h_selected,h_total,label_selected,label_total,fileOut):
    c = Canvas('c')
    pad1 = TPad('pad1', 'pad1', 0., 0.3, 1., 1.)
    pad1.SetBottomMargin(0.005)
    pad1.SetTicks(1,1)
    pad1.SetGrid(1,1)
    pad1.Draw()
    c.cd()
    pad2 = TPad('pad2', 'pad2', 0., 0.05, 1., 0.29)
    pad2.SetTopMargin(0.005)
    pad2.SetBottomMargin(0.3)
    pad2.SetTicks(1,1)
    pad2.Draw()
    pad1.cd()
    h_total.SetTitle('')
    h_total.GetYaxis().SetTitle('Events')
    h_total.SetLineColor(ROOT.kBlue)
    h_total.SetFillColorAlpha(ROOT.kBlue,0.2)
    h_total.Draw('HIST')
    h_selected.SetTitle('')
    h_selected.SetLineColor(ROOT.kRed)
    h_selected.SetFillColorAlpha(ROOT.kRed,0.2)
    h_selected.Draw('HIST same')
    legend = TLegend(0.12, 0.61, 0.28, 0.8)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.031)
    legend.AddEntry(h_selected,label_selected, 'f')
    legend.AddEntry(h_total,label_total, 'f')
    legend.Draw()
    cLabel, pLabel, dLabel = condLabel(), simLabel(), descriptionLabel()
    cLabel.SetTextSize(0.049), pLabel.SetTextSize(0.049)
    cLabel.Draw(), pLabel.Draw(), dLabel.Draw()
    pad2.cd()
    pad2.SetGrid(0,1)
    h_new = h_selected.Clone('h_new')
    h_new.Sumw2()
    h_new.Divide(h_total)
    h_new.SetMarkerStyle(20)
    h_new.SetMarkerSize(0.9)
    h_new.SetLineColor(ROOT.kBlack)
    h_new.GetXaxis().SetTitle('#xi' if 'xi' in fileOut else 'missing mass')
    h_new.SetMinimum(-0.01), h_new.SetMaximum(1.05)
    h_new.Draw('p same')
    Prettify(h_new)
    #h_new.GetXaxis().SetTitle('Generated #xi')
    h_new.GetYaxis().SetTitle('Red/Blue')
    c.SaveAs(fileOut)

def plotProtonResolution(method,subdir):
    c = Canvas('c')
    c.SetTicks(1,1)
    for s in stations:
        if subdir == s[0]: string = s[1]
    h = aqgcFile.Get(method+'/'+subdir+'/h_de_xi')
    if method == 'singleRP': h.GetXaxis().SetLimits(-0.1,0.1)
    elif method == 'multiRP': h.GetXaxis().SetLimits(-0.01,0.01)
    h.SetTitle('')
    h.GetYaxis().SetTitle('Events')
    h.GetXaxis().SetTitle('#xi_{reco} - #xi_{gen} '+string)
    h.GetXaxis().SetTitleOffset(1.2)
    h.SetLineColor(208)
    h.SetFillColorAlpha(208,0.6)
    h.Draw('HIST')
    cLabel, pLabel = condLabel(), simLabel()
    #cLabel.SetTextSize(0.049), pLabel.SetTextSize(0.049)
    cLabel.Draw(), pLabel.Draw()
    mean, rms = round(h.GetMean(),3), round(h.GetRMS(),4)
    statsLabel = makeStats(mean,rms)
    statsLabel.Draw()
    c.SaveAs('plots/h_proton_res_%s_%s.pdf' % (method,string))

def plotXiReco():
    c0 = Canvas('c0')
    c1 = Canvas('c1')
    c.SetTicks(1,1)
    h0 = f_eff.Get('multirp/0/h_xi_reco_vs_xi_simu')
    h1 = f_eff.Get('multirp/1/h_xi_reco_vs_xi_simu')
    cLabel, pLabel = condLabel(), simLabel()
    c0.cd()
    h1.Draw('colz')
    cLabel.Draw(), pLabel.Draw()
    c0.SaveAs('plots/h2_xi_recoVsim_arm0_2017preTS2')
    c1.cd()
    h2.Draw('colz')
    cLabel.Draw(), pLabel.Draw()
    c1.SaveAs('plots/h2_xi_recoVsim_arm1_2017preTS2')
    
    
     
# -----------------------------------------
'''
h_mass_res = aqgcFile.Get('plots/h_mass_res')
plotRes('mass', 'm', h_mass_res)

h_xi_res = aqgcFile.Get('plots/h_xi_res')
plotRes('xi', '#xi', h_xi_res)

h_pt_res = aqgcFile.Get('plots/h_pt_res')
plotRes('pt', 'p_{T}', h_pt_res)

h_eta_res = aqgcFile.Get('plots/h_eta_res')
plotRes('eta', '#eta', h_eta_res)

h_rap_diff = aqgcFile.Get('plots/h_rap_diff')
plotDiff('rap', 'y', h_rap_diff)

h_phi_diff = aqgcFile.Get('plots/h_phi_diff')
plotDiff('phi', '#phi', h_phi_diff)

h_dphi_diff = aqgcFile.Get('plots/h_dphi_diff')
plotDiff('dphi', '#Delta#phi', h_dphi_diff)

h_eta_diff = aqgcFile.Get('plots/h_eta_diff')
plotDiff('eta', '#eta', h_eta_diff)

h_ratio_diff = aqgcFile.Get('plots/h_ratio_diff')
plotDiff('ratio', 'p_{T}^{1}/p_{T}^{2}', h_ratio_diff)

h_diphpt_diff = aqgcFile.Get('plots/h_diphpt_diff')
plotDiff('diphpt', 'p_{T}^{#gamma#gamma}', h_diphpt_diff)

h_logxi_diff = aqgcFile.Get('plots/h_logxi_diff')
plotDiff('logxi', 'log(1/#xi)', h_logxi_diff)
'''

h_xi_sim_total = f.Get('h_xi_sim')
h_xi_sim_single = f.Get('h_xi_sim_twopro_single')
h_xi_sim_multi = f.Get('h_xi_sim_twopro_multi')

h_mass_sim_total = f.Get('h_mass_sim')
h_mass_sim_single = f.Get('h_mass_sim_twopro_single')
h_mass_sim_multi = f.Get('h_mass_sim_twopro_multi')

h_xi_reco_total = TH1D('h_xi_reco_total', '', 100, 0.0, 0.3)
h_xi_reco_eff = TH1D('h_xi_reco_eff', '', 100, 0.0, 0.3)
h_xi_reco_total.Add( f.Get('multirp/0/h_xi_reco') )
h_xi_reco_total.Add( f.Get('multirp/1/h_xi_reco') )
h_xi_reco_eff.Add ( f_eff.Get('multirp/0/h_xi_reco') )
h_xi_reco_eff.Add ( f_eff.Get('multirp/1/h_xi_reco') )

h_mass_reco_total = f.Get('h_mass_reco')
h_mass_reco_eff = f_eff.Get('h_mass_reco')


plotXiReco()

plotEA(h_xi_sim_single, h_xi_sim_total, 'Both singleRP reconstructed', 'All events', 'pds_xi_singleRP_acceptance.pdf')
plotEA(h_xi_sim_multi, h_xi_sim_total, 'Both multiRP reconstructed', 'All events', 'pds_xi_multiRP_acceptance.pdf')
plotEA(h_mass_sim_single, h_mass_sim_total, 'Both singleRP reconstructed', 'All events', 'pds_mass_singleRP_acceptance.pdf')
plotEA(h_mass_sim_multi, h_mass_sim_total, 'Both multiRP reconstructed', 'All events', 'pds_mass_multiRP_acceptance.pdf')

plotEA(h_xi_reco_eff, h_xi_reco_total, 'multiRP with efficiencies', 'multiRP', 'pds_xi_efficiency.pdf')
plotEA(h_mass_reco_eff, h_mass_reco_total, 'multiRP with efficiencies', 'multiRP', 'pds_mass_efficiency.pdf')



plotEA(h_xi_reco_eff, h_xi_sim_total, 'multiRP reco with efficiencies', 'simulated', 'pds_xi_eXA_%s.pdf' % era)
plotEA(h_mass_reco_eff, h_mass_sim_total, 'multiRP reco with efficiencies', 'simulated', 'pds_mass_eXA_%s.pdf' % era)







