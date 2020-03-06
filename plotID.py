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

'''
def makeIDPlot(name, xTitle, rbin, log):
    c = Canvas('c')
    c.cd()
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
'''

def graph(id_name, color, leg):
    rootFile = TFile('identification/'+id_name+'_output.root')
    g = rootFile.Get('Graph_from_h_ratio')
    g.SetMarkerSize(0.7)
    g.SetMarkerStyle(24)
    g.SetMarkerColor(color)

    leg.AddEntry(g,id_name,'lep')
    return g, leg


c = Canvas('c')
IDs = ['MVA_WP90', 'highPt']
colors = [ROOT.kRed, ROOT.kBlue]

c.cd() 
rootFile = TFile('identification/MVA_WP90_output.root')
h = rootFile.Get('h_ratio')
h.SetTitle('')
h.Draw('HIST')

leg = TLegend(0.45, 0.2, 0.55, 0.3)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.032)

for i,ID in enumerate(IDs):
    print 'ID:', ID
    g, leg = graph(ID, colors[i], leg)
    g.Draw('p e2 same')
    
sLabel, cLabel = simLabel(), condLabel()
sLabel.Draw(), cLabel.Draw()

leg.Draw()

c.SaveAs('multiplot_id.png')
