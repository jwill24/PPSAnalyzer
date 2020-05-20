#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

from common import Prettify

gStyle.SetOptStat(0)

color = 50
stations = [['0','45'], ['1','56'], ['3','45N'], ['23','45F'], ['103','56N'], ['123','56F']]

#aqgcFile = TFile('outputHists/histOut_resolution_aqgc.root')
#aqgcFile = TFile('histOut_signal_singleRP_2017postTS2.root')
aqgcFile = TFile('output_hists_2017postTS2.root')

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
    label.AddText( "2017 Post TS2 cond. (13 TeV)" )
    label.SetTextSize( 0.034 )
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

def plotEfficiency(var,method,numpro):
    c = Canvas('c')
    pad1 = TPad('pad1', 'pad1', 0., 0.3, 1., 1.)
    pad1.SetBottomMargin(0.005)
    pad1.SetTicks(1,1)
    pad1.Draw()
    c.cd()
    pad2 = TPad('pad2', 'pad2', 0., 0.05, 1., 0.28)
    pad2.SetTopMargin(0.005)
    pad2.SetBottomMargin(0.3)
    pad2.SetTicks(1,1)
    pad2.Draw()
    pad1.cd()
    #pad1.SetGrid(1,1)
    h_total = aqgcFile.Get('h_'+var+'_sim')
    h_total.SetTitle('')
    h_total.GetYaxis().SetTitle('Events')
    h_total.SetLineColor(ROOT.kBlue)
    h_total.GetYaxis().SetTitle('Events')
    h_total.Draw('HIST')
    h_selected = aqgcFile.Get('h_'+var+'_sim_'+numpro+'pro_'+method)
    h_selected.SetTitle('')
    h_selected.SetLineColor(ROOT.kRed)
    h_selected.Draw('HIST same')
    legend = TLegend(0.17, 0.57, 0.34, 0.77)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.038)
    if numpro == 'two': legend.AddEntry(h_selected,'Both protons reconstructed','l')
    elif numpro == 'one': legend.AddEntry(h_selected,'Proton reconstructed ('+method+'RP)','l')
    legend.AddEntry(h_total,'All events', 'l')
    legend.Draw()
    cLabel, pLabel = condLabel(), simLabel()
    cLabel.SetTextSize(0.049), pLabel.SetTextSize(0.049)
    cLabel.Draw(), pLabel.Draw()
    pad2.cd()
    pad2.SetGrid(0,1)
    h_new = h_selected.Clone('h_new')
    h_new.Sumw2()
    h_new.Divide(h_total)
    h_new.SetMarkerStyle(20)
    h_new.SetMarkerSize(0.9)
    h_new.SetLineColor(ROOT.kBlack)
    h_new.GetXaxis().SetTitle('Generated '+'#xi' if var=='xi' else 'missing mass')
    h_new.Draw('p same')
    Prettify(h_new)
    #h_new.GetXaxis().SetTitle('Generated #xi')
    h_new.GetYaxis().SetTitle('Red/Blue')
    c.SaveAs('test_efficiency_'+var+'_'+method+'.pdf')

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
    c.SaveAs('h_proton_res_'+method+'_'+string+'.pdf')
     
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



plotEfficiency('mass','multi','two')
#plotEfficiency('mass','single','two')
#plotEfficiency('xi','single','one')
#plotEfficiency('xi','multi','one')

#plotProtonResolution('singleRP','3')
#plotProtonResolution('singleRP','23')
#plotProtonResolution('singleRP','103')
#plotProtonResolution('singleRP','123')
#plotProtonResolution('multiRP','0')
#plotProtonResolution('multiRP','1')




