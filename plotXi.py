#!/usr/bin/env python                                                                                                                                                                                                                                                          
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)

def Canvas(name):
    c = TCanvas(name,'c',750,600)
    return c
def prelimLabel():
    label = TPaveText( 0.2, 0.9, 0.27, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.SetTextAlign(31)
    label.AddText( "#font[62]{CMS} #font[52]{Preliminary}" )
    label.SetTextSize(0.03)
    label.SetTextColor( 1 )
    return label
def lumiLabel():
    label = TPaveText( 0.72, 0.9, 0.8, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "37.19 fb^{-1} (13 TeV)" )
    label.SetTextSize( 0.03 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label

reverseFile = TFile('outputHists/2017/histOut_data_ReverseElastic_2017.root')
xiFile = TFile('outputHists/2017/histOut_data_Xi_2017.root')

h_rev_xim = reverseFile.Get('plots/h_xim')
h_rev_xip = reverseFile.Get('plots/h_xip')
h_xi_xim = xiFile.Get('plots/h_xim')
h_xi_xip = xiFile.Get('plots/h_xip')

c1 = Canvas('c1')
c1.cd()
h_rev_xim.Scale( 1/h_rev_xim.GetEntries() )
h_rev_xim.Rebin(4)
h_rev_xim.SetLineColor(ROOT.kRed)
h_rev_xim.SetFillStyle(0)
h_rev_xim.SetTitle('')
h_rev_xim.GetXaxis().SetTitle('#xi -')
h_rev_xim.GetXaxis().SetLimits(0,0.2)
h_rev_xim.Draw('HIST')
h_xi_xim.Rebin(4)
h_xi_xim.Scale( 1/h_xi_xim.GetEntries() )
h_xi_xim.SetLineColor(ROOT.kBlue)
h_xi_xim.SetFillStyle(0)
h_xi_xim.Draw('HIST same')
legend = TLegend(0.65,0.65,0.75,0.8)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.038)
legend.AddEntry(h_rev_xim, 'Reverse Elastic', 'l')
legend.AddEntry(h_xi_xim, 'Tight #xi', 'l')
legend.Draw()
pLabel, lLabel = prelimLabel(), lumiLabel()
pLabel.Draw(), lLabel.Draw()
c1.SaveAs('xim_compare.png')

c2 = Canvas('c2')
c2.cd()
h_rev_xip.Rebin(4)
h_rev_xip.Scale( 1/h_rev_xip.GetEntries() )
h_rev_xip.SetLineColor(ROOT.kRed)
h_rev_xip.SetFillStyle(0)
h_rev_xip.SetTitle('')
h_rev_xip.GetXaxis().SetTitle('#xi -')
h_rev_xip.GetXaxis().SetLimits(0,0.2)
h_rev_xip.Draw('HIST')
h_xi_xip.Rebin(4)
h_xi_xip.Scale( 1/h_xi_xip.GetEntries() )
h_xi_xip.SetLineColor(ROOT.kBlue)
h_xi_xip.SetFillStyle(0)
h_xi_xip.Draw('HIST same')
legend = TLegend(0.65,0.65,0.75,0.8)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.038)
legend.AddEntry(h_rev_xip, 'Reverse Elastic', 'l')
legend.AddEntry(h_xi_xip, 'Tight #xi', 'l')
legend.Draw()
pLabel, lLabel = prelimLabel(), lumiLabel()
pLabel.Draw(), lLabel.Draw()
c2.SaveAs('xip_compare.png')












