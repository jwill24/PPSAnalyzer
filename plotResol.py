#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)

color = 50

aqgcFile = TFile('outputHists/histOut_resolution_aqgc.root')

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
    label = TPaveText( 0.63, 0.9, 0.8, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "2017 PU cond. (13 TeV)" )
    label.SetTextSize( 0.034 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label

def simLabel():
    label = TPaveText( 0.12, 0.9, 0.2, 0.92, 'NB NDC' )
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









