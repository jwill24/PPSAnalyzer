#!/usr/bin/env python                                                                                                                                                                                            
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle, kBlack
from common import sampleColors, Canvas, Prettify, lumiLabel, makeLegend, asym_error_bars

gStyle.SetOptStat(0)
gStyle.SetPalette(ROOT.kRainBow)



def prelimLabel(location,log,maximum):
    if location == 'left':
        label = TPaveText( 0.135, 0.76, 0.2, 0.84, 'NB NDC' )
        label.AddText( "#font[62]{CMS}" )
        label.AddText( "#scale[0.75]{#font[52]{Preliminary}}" )
    elif location == 'top':
        label = TPaveText( 0.1, 0.9, 0.2, 0.92, 'NB NDC' )
        label.AddText( "#font[62]{CMS} #font[52]{Preliminary}" )
    #label = TPaveText( 0.135, 0.76, 0.2, 0.84, 'NB NDC' ) # Left label
    #label = TPaveText( 0.8, 0.79, 0.87, 0.86, 'NB NDC' ) # Right label
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.SetTextAlign(11) # Align bottom left
    #label.SetTextAlign(31) # Align bottom right
    if location == 'top': label.SetTextSize(0.04)
    else: label.SetTextSize(0.05)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

#-----------------------------------------

def makeXiComp(era,sector,log):
    pf = TFile("output_reconstructionPlotter_2017"+era+".root")

    c = Canvas('c')
    c.cd()
    c.SetTicks(1,1)
    if log: c.SetLogy()
    #c.SetGrid(1,1)

    h_near = ROOT.TH1F('h_near', '', 100, 0.0, 0.3)
    h_far = ROOT.TH1F('h_far', '', 100, 0.0, 0.3)
    h_multi = ROOT.TH1F('h_multi', '', 100, 0.0, 0.3)

    # Add hists
    if sector == '45':
        h_near.Add( pf.Get('singleRPPlots/rp3/h_xi') )
        h_far.Add( pf.Get('singleRPPlots/rp23/h_xi') )
        h_multi.Add( pf.Get('multiRPPlots/arm0/h_xi') )
    elif sector == '56':
        h_near.Add( pf.Get('singleRPPlots/rp103/h_xi') )
        h_far.Add( pf.Get('singleRPPlots/rp123/h_xi') )
        h_multi.Add( pf.Get('multiRPPlots/arm1/h_xi') )
    
    h_far.SetLineColor(210)
    h_near.SetLineColor(62)
    h_multi.SetLineColor(207)
    h_far.GetYaxis().SetTitle('Events')
    h_far.GetYaxis().SetTitleOffset(1.5)
    h_far.GetXaxis().SetTitle('#xi - sector'+sector)
    if log: h_far.SetMaximum( h_far.GetMaximum()*10 )
    else: h_far.SetMaximum( h_far.GetMaximum()*1.2 )
    h_far.Draw('HIST')
    h_near.Draw('HIST same')

    h_multi.Draw('HIST same')
    legend = TLegend(0.6,0.7,0.8,0.8)
    legend.SetTextSize(0.03)
    legend.SetLineColor( 0 )
    legend.SetFillColor( 0 )
    legend.AddEntry(h_near,"singleRP near",'l')
    legend.AddEntry(h_far,"singleRP far",'l')
    legend.AddEntry(h_multi,"multiRP",'l')
    legend.Draw()
    
    pLabel, lLabel = prelimLabel('top',log,h_far.GetMaximum()), lumiLabel(False,['2017'])
    pLabel.Draw(), lLabel.Draw()
    
    c.SaveAs('h_xi_comp_'+sector+'_Run2017'+era+'.pdf')

#-----------------------------------------

makeXiComp('B','45',True)
makeXiComp('B','56',True)

makeXiComp('C','45',True)
makeXiComp('C','56',True)

makeXiComp('D','45',True)
makeXiComp('D','56',True)

makeXiComp('E','45',True)
makeXiComp('E','56',True)

makeXiComp('F','45',True)
makeXiComp('F','56',True)
