#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

#selection = 'Preselection'
selection = 'Elastic selection'

fillColor = 212

#dataFile = 'outputHists/histOut_data_preselection_2017.root'
dataFile = 'outputHists/histOut_data_elastic_2017.root'

# calculated from script
xs_ggj = 138.5
xs_gj = 873.7
xs_qcd = 117500.
#xs_wg = 465.0
xs_wg = 191.1
xs_zg = 55.47

n_ggj = 4000000 
n_gj = 80000000
n_qcd = 4000000
n_wg = 6300000
n_zg = 30000000

#n_ggj = 3883535 
#n_gj = 79243357 
#n_qcd = 3883535
#n_wg = 6283083
#n_zg = 30490034

lumi = 37200.0 # pb

gStyle.SetOptStat(0)

# Histogram files
dFile = TFile( dataFile )
ggjFile = TFile( "outputHists/histOut_ggj_elastic_2017.root" )
gjFile = TFile( "outputHists/histOut_gj_elastic_2017.root" )
qcdFile = TFile( "outputHists/histOut_qcd_elastic_2017.root" )
wgFile = TFile( "outputHists/histOut_wg_elastic_2017.root" )
zgFile = TFile( "outputHists/histOut_zg_elastic_2017.root" )
aqgcFile = TFile( "outputHists/histOut_aqgc_elastic_2017.root" )

def Canvas(name):
    c = TCanvas(name,'c',750,600)
    return c

def Prettify( hist ):
    x = hist.GetXaxis()
    y = hist.GetYaxis()
    x.SetLabelFont( 43 );
    x.SetTitleFont( 43 );
    y.SetLabelFont( 43 );
    y.SetTitleFont( 43 );

def plotRatio(name, h1, v_hist, log):
    c = Canvas('c')

    h_sum = TH1F('h_sum','sum',h1.GetNbinsX(), h1.GetXaxis().GetXmin(), h1.GetXaxis().GetXmax())
    for h in v_hist: h_sum.Add(h)
 
    pad1 = TPad('pad1', 'pad1', 0., 0.3, 1., 1.)
    pad1.SetBottomMargin(0.005)
    pad1.Draw()

    c.cd()
    pad2 = TPad('pad2', 'pad2', 0., 0.05, 1., 0.28)
    pad2.SetTopMargin(0.005)
    pad2.SetBottomMargin(0.3)
    pad2.Draw()

    pad1.cd()
    if log: pad1.SetLogy()
    stack = THStack('norm_stack','')
    for h in v_hist: stack.Add(h)
    #Prettify( stack.GetHistogram() )
    stack.Draw('HIST')
    h1.Draw('p same')
    stack.GetHistogram().GetYaxis().SetTitle('Events')
    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel(selection), lumiLabel()
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    legend = makeLegend(h1,v_hist)
    legend.Draw()

    pad2.cd()
    h_ratio = h1.Clone('h_ratio')
    h_ratio.SetMarkerStyle(20)
    h_ratio.Sumw2()
    h_ratio.Divide(h_sum)
    h_ratio.SetMinimum(0.)
    h_ratio.SetMaximum(2)
    h_ratio.Draw('p same')

    l = TLine(h_ratio.GetXaxis().GetXmin(), 1, h_ratio.GetXaxis().GetXmax(), 1)
    l.Draw()

    x = h_ratio.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4)
    x.SetLabelFont(43)
    x.SetLabelSize(20)
    y = h_ratio.GetYaxis()
    y.SetTitle('Data / MC')
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    c.SaveAs(name+'.png')

def prelimLabel():
    #label = TPaveText( 0.135, 0.8, 0.2, 0.86, 'NB NDC' )
    label = TPaveText( 0.8, 0.79, 0.87, 0.86, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    #label.SetTextAlign(11)
    label.SetTextAlign(31)
    label.AddText( "#font[62]{CMS}" )
    label.AddText( "#scale[0.75]{#font[52]{Preliminary}}" )
    label.SetTextSize(0.05)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def selectionLabel(text):
    label = TPaveText( 0.1, 0.9, 0.18, 0.92, 'NB NDC' ) 
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( text )
    label.SetTextSize( 0.042 )
    label.SetTextAlign(11)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def lumiLabel():
    label = TPaveText( 0.72, 0.9, 0.8, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "37.19 fb^{-1} (13 TeV)" )
    label.SetTextSize( 0.042 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label

def makeLegend(h1,v_hist):
    legend = TLegend(0.7, 0.5, 0.87, 0.75) 
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(h1,'Data', 'p')
    backgrounds = ['Incl. Z + #gamma', 'Incl. W + #gamma', '#gamma + j', 'Incl. #gamma#gamma + j (NLO)', 'QCD (e#gamma enriched)']
    for i in range( len(backgrounds) ):
        legend.AddEntry(v_hist[i],backgrounds[i],'f')
    return legend
    
def setPlot(h, color, xs, nevts):
    h.SetTitle('')
    h.Rebin(4)
    h.SetFillColor(color)
    h.SetLineColor(color)
    h.Scale(xs*lumi/nevts)
    return h

#-----------------------

v_mass = []

h_diph_mass = dFile.Get("plots/h_diph_mass")
h_diph_mass.SetTitle('')
h_diph_mass.SetXTitle('m_{#gamma#gamma} GeV')
h_diph_mass.SetYTitle('Events')
h_diph_mass.Rebin(4)
h_diph_mass.SetMarkerStyle(20)
h_diph_mass.SetMarkerSize(0.7)

h_ggj_diph_mass = ggjFile.Get("plots/h_diph_mass")
#setPlot(h_ggj_diph_mass, 208, xs_ggj, n_ggj)
setPlot(h_ggj_diph_mass,208, 37200., 1)

h_gj_diph_mass = gjFile.Get("plots/h_diph_mass")
setPlot(h_gj_diph_mass, 38, xs_gj, n_gj)

h_wg_diph_mass = wgFile.Get("plots/h_diph_mass")
setPlot(h_wg_diph_mass, 29, xs_wg, n_wg)

h_zg_diph_mass = zgFile.Get("plots/h_diph_mass")
setPlot(h_zg_diph_mass, 210, xs_zg, n_zg)

h_qcd_diph_mass = qcdFile.Get("plots/h_diph_mass")
setPlot(h_qcd_diph_mass, 228, xs_qcd, n_qcd)

v_mass.append(h_zg_diph_mass)
v_mass.append(h_wg_diph_mass)
v_mass.append(h_gj_diph_mass)
v_mass.append(h_ggj_diph_mass)
v_mass.append(h_qcd_diph_mass)

plotRatio('h_mass_comp', h_diph_mass, v_mass, True)

#-----------------------

v_pt = []

h_single_pt = dFile.Get("plots/h_single_pt")
h_single_pt.SetTitle('')
h_single_pt.SetXTitle('p_{T}^{#gamma} GeV')
h_single_pt.SetYTitle('Events')
h_single_pt.Rebin(4)
h_single_pt.SetMarkerStyle(20)
h_single_pt.SetMarkerSize(0.7)

h_ggj_single_pt = ggjFile.Get("plots/h_single_pt")
setPlot(h_ggj_single_pt, 208, xs_ggj, n_ggj)

h_gj_single_pt = gjFile.Get("plots/h_single_pt")
setPlot(h_gj_single_pt, 38, xs_gj, n_gj)

h_wg_single_pt = wgFile.Get("plots/h_single_pt")
setPlot(h_wg_single_pt, 29, xs_wg, n_wg)

h_zg_single_pt = zgFile.Get("plots/h_single_pt")
setPlot(h_zg_single_pt, 210, xs_zg, n_zg)

h_qcd_single_pt = qcdFile.Get("plots/h_single_pt")
setPlot(h_qcd_single_pt, 228, xs_qcd, n_qcd)

v_pt.append(h_zg_single_pt)
v_pt.append(h_wg_single_pt)
v_pt.append(h_gj_single_pt)
v_pt.append(h_ggj_single_pt)
v_pt.append(h_qcd_single_pt)

plotRatio('h_pt_comp', h_single_pt, v_pt, True)

#-----------------------
'''
c1 = Canvas("c1")
c1.cd()
c1.SetLogy()
h_diph_mass = dFile.Get("plots/h_diph_mass")
h_diph_mass.Rebin(2)
#h_diph_mass.GetXaxis().SetRange(15,100)
h_diph_mass.SetTitle("")
h_diph_mass.SetXTitle('m_{#gamma#gamma} GeV')
h_diph_mass.SetYTitle('Events')
h_diph_mass.SetFillColor(fillColor)
h_diph_mass.SetLineColor(fillColor)
h_diph_mass.Draw()
pLabel, sLabel, lLabel = prelimLabel(), selectionLabel(selection), lumiLabel()
pLabel.Draw()
sLabel.Draw()
lLabel.Draw()
c1.SaveAs("h_diph_mass.png")

#-----------------------

c2 = Canvas("c2")
c2.cd()
c2.SetLogy()
h_single_pt = dFile.Get("plots/h_single_pt")
h_single_pt.Rebin(2)
#h_single_pt.GetXaxis().SetRange(15,100)
h_single_pt.GetXaxis().SetRange(7,100)
h_single_pt.SetTitle("")
h_single_pt.SetXTitle('Single photon p_{T}')
h_single_pt.SetYTitle('Events')
h_single_pt.SetFillColor(fillColor)
h_single_pt.SetLineColor(fillColor)
h_single_pt.Draw()
pLabel.Draw()
sLabel.Draw()
lLabel.Draw()
c2.SaveAs("h_single_pt.png")

#-----------------------

c3 = Canvas("c3")
c3.cd()
c3.SetLogy()
h_acop = dFile.Get("plots/h_acop")
h_acop.SetTitle("")
h_acop.SetXTitle('1 - #void8 #Delta #phi_{#gamma#gamma}/#pi #void8')
h_acop.SetYTitle('Events')
h_acop.SetFillColor(fillColor)
h_acop.SetLineColor(fillColor)
h_acop.Draw()
pLabel.Draw()
sLabel.Draw()
lLabel.Draw()
c3.SaveAs("h_acop.png")

#-----------------------

c4 = Canvas("c4")
c4.cd()
h_single_eta = dFile.Get("plots/h_single_eta")
h_single_eta.Rebin(2)
#h_single_eta.GetXaxis().SetRange(8,92)
h_single_eta.Draw()
h_single_eta.SetTitle("")
h_single_eta.SetXTitle('Single photon #eta')
h_single_eta.SetYTitle('Events')
h_single_eta.SetFillColor(fillColor)
h_single_eta.SetLineColor(fillColor)
pLabel.Draw()
sLabel.Draw()
lLabel.Draw()
c4.SaveAs("h_single_eta.png")


#-----------------------

c5 = Canvas("c5")
c5.cd()
c5.SetLogy()
h_xip = dFile.Get("plots/h_xip")
h_xip.GetXaxis().SetRange(0,60)
h_xip.Draw()
h_xip.SetTitle("")
h_xip.SetXTitle('#xi _{#gamma#gamma}^{+}')
h_xip.SetYTitle('Events')
h_xip.SetFillColor(fillColor)
h_xip.SetLineColor(fillColor)
pLabel.Draw()
sLabel.Draw()
lLabel.Draw()
c5.SaveAs("h_xip.png")

#-----------------------

c6 = Canvas("c6")
c6.cd()
c6.SetLogy()
h_xim = dFile.Get("plots/h_xim")
h_xim.GetXaxis().SetRange(0,60)
h_xim.Draw()
h_xim.SetTitle("")
h_xim.SetXTitle('#xi _{#gamma#gamma}^{-}')
h_xim.SetYTitle('Events')
h_xim.SetFillColor(fillColor)
h_xim.SetLineColor(fillColor)
pLabel.Draw()
sLabel.Draw()
lLabel.Draw()
c6.SaveAs("h_xim.png")
'''
#-----------------------


