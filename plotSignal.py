#!/usr/bin/env python  
import os, sys, glob
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)

#color = ROOT.kBlue-7 # SM
color = 212 # AQGC
colors = [ROOT.kGreen+1, ROOT.kCyan-7, ROOT.kAzure-3, ROOT.kViolet+8, ROOT.kMagenta-7, ROOT.kRed-4]
weight = 3.86e-5*37200/300000

signalFile = TFile('outputHists/2017/histOut_aqgc2017_5e-13_0_Preselection_multiRP.root')
#signalFile = TFile('outputHists/2017/histOut_LbL2017_SM_Preselection_multiRP.root')

#alpFiles = glob.glob('outputHists/2017/histOut_alp2017_fe-1_m*_Preselection_multiRP.root')
alpFiles = ['outputHists/2017/histOut_alp2017_fe-1_m500_Preselection_multiRP.root',
            'outputHists/2017/histOut_alp2017_fe-1_m750_Preselection_multiRP.root',
            'outputHists/2017/histOut_alp2017_fe-1_m1000_Preselection_multiRP.root',
            'outputHists/2017/histOut_alp2017_fe-1_m1250_Preselection_multiRP.root',
            'outputHists/2017/histOut_alp2017_fe-1_m1500_Preselection_multiRP.root',
            'outputHists/2017/histOut_alp2017_fe-1_m2000_Preselection_multiRP.root']


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
    label.AddText( "FPMC, SM pred." )
    return label

def makeSignalPlot(name, xTitle, rbin, log):
    c = Canvas('c')
    c.cd()
    if log: c.SetLogy()
    h = signalFile.Get('plots/' + name)
    entries = h.Integral()
    h.SetTitle('')
    h.GetYaxis().SetTitleOffset(1.5)
    h.SetYTitle('Events fraction')
    h.SetXTitle(xTitle)
    h.Rebin(rbin)
    h.Scale(1./entries)
    h.SetFillColor(color)
    h.SetLineColor(color)
    h.SetMaximum( h.GetMaximum()*1.2 )
    h.Draw('HIST')
    sLabel, cLabel, selLabel = simLabel(), condLabel(), selectionLabel('FPMC, BSM #gamma#gamma#rightarrow#gamma#gamma pred.')
    sLabel.Draw(), cLabel.Draw(), selLabel.Draw()
    c.SaveAs('plots/signal/'+name+'_signal.pdf')


def makeALPplot(name, xTitle, log):
    c = Canvas('c')
    c.cd()
    if log: c.SetLogy()

    legend = TLegend(0.7, 0.45, 0.8, 0.75)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.028)

    tf = []
    for i, file in enumerate(alpFiles):
        mass = file[39:][:(len(file[39:])-26)]
        tf.append(TFile(file))
        h_tmp = tf[i].Get('plots/%s' % name)
        h_tmp.SetTitle('')
        h_tmp.GetYaxis().SetTitleOffset(1.5)
        h_tmp.SetYTitle('Events fraction')
        h_tmp.SetXTitle(xTitle)
        h_tmp.SetMaximum(1.0)
        h_tmp.Scale(1./h_tmp.Integral())
        h_tmp.SetFillColorAlpha(colors[i], 0.4)
        h_tmp.SetLineColor(colors[i])
        if i == 0: h_tmp.Draw('HIST')
        else: h_tmp.Draw('HIST same')
        legend.AddEntry(h_tmp, 'm=%s (GeV)' % mass, 'f')
        
    legend.Draw()
    sLabel, cLabel, selLabel = simLabel(), condLabel(), selectionLabel('FPMC, #gamma#gamma#rightarrow a#rightarrow#gamma#gamma')
    sLabel.Draw(), cLabel.Draw(), selLabel.Draw()
    c.SaveAs('plots/signal/'+name+'_ALP.pdf')


#------------------------------------------------


#makeSignalPlot('h_diph_mass', 'm_{#gamma#gamma} (GeV)', 1, False)
#makeSignalPlot('h_single_eta', '#eta^{#gamma}', 1, False)
#makeSignalPlot('h_single_pt', 'p_{T}^{#gamma} (GeV)', 1, True)
#makeSignalPlot('h_acop', '1- |#Delta #phi|/#pi', 1, True)

#makeSignalPlot('h_single_r9', 'R_{9}', 1, True)
#makeSignalPlot('h_eb_hoe', 'EB H/E', 1, True)
#makeSignalPlot('h_ee_hoe', 'EE H/E', 1, True)
#makeSignalPlot('h_eb_sieie', 'EB #sigma_{i#etai#eta}', 1, True)
#makeSignalPlot('h_ee_sieie', 'EE #sigma_{i#etai#eta}', 1, True)

makeALPplot('h_diph_mass', 'm_{#gamma#gamma} (GeV)', False)
makeALPplot('h_single_eta', '#eta^{#gamma}', False)
makeALPplot('h_single_pt', 'p_{T}^{#gamma} (GeV)', True)
makeALPplot('h_acop', '1- |#Delta #phi|/#pi', True)
