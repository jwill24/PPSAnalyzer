#!/usr/bin/env python  
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)

#color = ROOT.kGreen-9
#color = ROOT.kTeal+8
color = 212
weight = 3.86e-5*37200/300000

signalFile = TFile('outputHists/2017/histOut_signal_2017.root')

def Canvas(name):
    c = TCanvas(name,'c',750,600)
    return c

def selectionLabel(text):
    label = TPaveText( 0.11, 0.9, 0.18, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( text )
    label.SetTextSize( 0.035 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
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
    #label = TPaveText( 0.11, 0.9, 0.2, 0.92, 'NB NDC' )
    label = TPaveText( 0.8, 0.79, 0.87, 0.86, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    #label.SetTextAlign(11)
    label.SetTextAlign(31)
    #label.AddText( "#font[62]{CMS} #font[52]{Simulation}" )
    label.AddText( "#font[62]{CMS}" )
    label.AddText( "#scale[0.75]{#font[52]{Simulation}}" )
    label.SetTextSize(0.045)
    #label.SetTextFont( 52 )
    label.SetTextColor( 1 )
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

def makeSignalPlot(name, xTitle, rbin, log):
    c = Canvas('c')
    c.cd()
    if log: c.SetLogy()
    h = signalFile.Get('plots/' + name)
    h.SetTitle('')
    h.SetYTitle('Events')
    h.SetXTitle(xTitle)
    #h.Scale(1/weight)
    h.Rebin(rbin)
    h.SetFillColor(color)
    h.SetLineColor(color)
    h.SetMaximum( h.GetMaximum()*1.2 )
    h.Draw('HIST')
    sLabel, cLabel, selLabel = simLabel(), condLabel(), selectionLabel('FPMC, BSM #gamma#gamma#rightarrow#gamma#gamma pred.')
    sLabel.Draw(), cLabel.Draw(), selLabel.Draw()
    c.SaveAs('plots/signal/'+name+'_signal.png')


#makeSignalPlot('h_diph_mass', 'm_{#gamma#gamma} (GeV)', 1, False)
#makeSignalPlot('h_single_eta', '#eta^{#gamma}', 1, False)
#makeSignalPlot('h_single_pt', 'p_{T}^{#gamma} (GeV)', 1, False)
#makeSignalPlot('h_acop', '1- |#Delta #phi|/#pi', 1, True)

makeSignalPlot('h_single_r9', 'R_{9}', 1, True)
makeSignalPlot('h_eb_hoe', 'EB H/E', 1, True)
makeSignalPlot('h_ee_hoe', 'EE H/E', 1, True)
makeSignalPlot('h_eb_sieie', 'EB #sigma_{i#etai#eta}', 1, True)
makeSignalPlot('h_ee_sieie', 'EE #sigma_{i#etai#eta}', 1, True)
