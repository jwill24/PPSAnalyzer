# plot legacy data protons vs new reconstruction conditions

#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLegend, TH1F
from ROOT import gROOT, gStyle
from common import Canvas, lumiLabel

gStyle.SetOptStat(0)
extension = 'pdf'

def prelimLabel(location,log):
    if location == 'left':
        label = TPaveText( 0.135, 0.76, 0.2, 0.84, 'NB NDC' )
        label.AddText( "#font[62]{CMS}" )
        label.AddText( "#scale[0.75]{#font[52]{Preliminary}}" )
    elif location == 'top':
        label = TPaveText( 0.15, 0.9, 0.25, 0.92, 'NB NDC' )
        label.AddText( "#font[62]{CMS} #font[52]{Preliminary}" )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.SetTextAlign(11) # Align bottom left
    if location == 'top': label.SetTextSize(0.04)
    else: label.SetTextSize(0.05)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

#-----------------------------------------
def makeComp(hist,label,log):
    var = hist.split('_')[-1]

    new_file = TFile("tmp/histOut_data2017D_new_HLT_multiRP.root")
    old_file = TFile("tmp/histOut_data2017D_old_HLT_multiRP.root")

    h_new = new_file.Get('plots/%s' % hist)
    h_old = old_file.Get('plots/%s' % hist)

    c1 = Canvas('c1')
    c1.SetLeftMargin(0.15)
    c1.cd()
    c1.SetTicks(1,1)
    if log: c1.SetLogy()
    h_new.SetTitle('')
    h_new.GetYaxis().SetTitleOffset(2.1)
    h_new.GetYaxis().SetTitle('Events')
    h_new.GetXaxis().SetTitleOffset(1.2)
    h_new.GetXaxis().SetTitle(label)
    h_new.SetMarkerStyle(20)
    h_new.SetMarkerColor(r.kRed)
    h_new.GetXaxis().SetNdivisions(507)
    h_old.SetLineColor(r.kBlue)
    h_new.Rebin(4), h_old.Rebin(4)
    h_new.Draw('p')
    h_old.Draw('HIST same')
    legend = TLegend(0.69,0.75,0.82,0.85)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.023)
    legend.AddEntry(h_old, 'Legacy data', 'l')
    legend.AddEntry(h_new, 'Reminiaod data', 'p')
    legend.Draw()
    pLabel = prelimLabel('top',False)
    pLabel.Draw()
    c1.SaveAs('plots/reMiniAOD_validation_%s.%s' % (var,extension))

#-----------------------------------------

def makeProComp(var,label,log):
    new_file = TFile("tmp/histOut_data2017D_new_HLT_multiRP.root")
    old_file = TFile("tmp/histOut_data2017D_old_HLT_multiRP.root")
    
    str_45 = 'xip' if var == 'xi' else 'thetaY_45'
    str_56 = 'xim' if var == 'xi' else 'thetaY_56'
    
    h_new_45 = new_file.Get('plots/h_pro_%s' % str_45)
    h_new_56 = new_file.Get('plots/h_pro_%s' % str_56)
    h_old_45 = old_file.Get('plots/h_pro_%s' % str_45)
    h_old_56 = old_file.Get('plots/h_pro_%s' % str_56)

    c1 = Canvas('c1')
    c1.SetLeftMargin(0.15)
    c1.cd()
    c1.SetTicks(1,1)
    if log: c1.SetLogy()
    h_new_45.SetTitle('')
    h_new_45.GetYaxis().SetTitleOffset(2.1)
    h_new_45.GetYaxis().SetTitle('Events')
    h_new_45.GetXaxis().SetTitleOffset(1.2)
    h_new_45.GetXaxis().SetTitle(label)
    h_new_45.SetLineColor(r.kRed)
    h_new_45.GetXaxis().SetNdivisions(507)
    h_old_45.SetLineColor(r.kBlue)
    h_new_45.Draw('HIST')
    h_old_45.Draw('HIST same')
    text45 = TPaveText(0.72,0.81,0.9,0.9,'NB NDC')
    text45.AddText('sector 45')
    text45.SetTextSize(0.032)
    text45.SetTextFont(42)
    text45.SetFillStyle(0)
    text45.Draw()
    legend = TLegend(0.6,0.6,0.75,0.7)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.028)
    legend.AddEntry(h_old_45, 'Legacy data', 'l')
    legend.AddEntry(h_new_45, 'Reminiaod data', 'l')
    legend.Draw()
    pLabel = prelimLabel('top',False)
    pLabel.Draw()
    c1.SaveAs('plots/reMiniAOD_validation_%s_45.%s' % (var,extension))

    c2 = Canvas('c2')
    c2.SetLeftMargin(0.15)
    c2.cd()
    c2.SetTicks(1,1)
    if log: c2.SetLogy()
    h_new_56.SetTitle('')
    h_new_56.GetYaxis().SetTitleOffset(2.1)
    h_new_56.GetYaxis().SetTitle('Events')
    h_new_56.GetXaxis().SetTitleOffset(1.2)
    h_new_56.GetXaxis().SetTitle(label)
    h_new_56.SetLineColor(r.kRed)
    h_new_56.GetXaxis().SetNdivisions(507)
    h_old_56.SetLineColor(r.kBlue)
    h_new_56.Draw('HIST')
    h_old_56.Draw('HIST same')
    text56 = TPaveText(0.72,0.81,0.9,0.9,'NB NDC')
    text56.AddText('sector 56')
    text56.SetTextSize(0.032)
    text56.SetTextFont(42)
    text56.SetFillStyle(0)
    text56.Draw()
    pLabel.Draw()
    legend.Draw()
    c2.SaveAs('plots/reMiniAOD_validation_%s_56.%s' % (var,extension))

#-----------------------------------------

# CMS comparison plots
makeComp('h_single_pt','p_{T}^{#gamma} (GeV)',True)
makeComp('h_single_eta','#eta^{#gamma}',False)
makeComp('h_single_r9', 'R_{9}^{#gamma}', True)
makeComp('h_diph_mass', 'm^{#gamma#gamma} (GeV)', True)

# PPS comparison plots
#makeProComp('thetaY','#theta_{y} (rad)', False)
#makeProComp('xi', '#xi', False)
