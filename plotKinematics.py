#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)

lab = 'After HLT'
selection = 'HLTnoPUR'
fillColor = 212
lumi = 37200.0 # pb

ggj =  ['outputHists/histOut_ggj_'+selection+'_2017.root',138.5,4000000,208]
gj =   ['outputHists/histOut_g+j_'+selection+'_2017.root',873.7,80000000,38]
qcd =  ['outputHists/histOut_qcd_'+selection+'_2017.root',117500,4000000,69]
wg =   ['outputHists/histOut_wg_'+selection+'_2017.root',465,6300000,29] 
zg =   ['outputHists/histOut_zg_'+selection+'_2017.root',55.47,30000000,212]
aqgc = ['outputHists/histOut_aqgc_'+selection+'_2017.root',3.86e-5,300000,92] 

# Histogram files
dataFile = TFile('outputHists/histOut_data_'+selection+'_2017.root')
ggjFile  = TFile(ggj[0])
gjFile   = TFile(gj[0])
qcdFile  = TFile(qcd[0])
wgFile   = TFile(wg[0])
zgFile   = TFile(zg[0])
aqgcFile = TFile(aqgc[0])

def Canvas(name):
    c = TCanvas(name,'c',750,600)
    return c

def Prettify( hist ):
    x = hist.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4)
    x.SetLabelFont(43)
    x.SetLabelSize(20)
    x.SetTickLength(0.05)
    y = hist.GetYaxis()
    y.SetTitle('Data / MC')
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

def plotRatio(name, h1, v_hist, hs, log):
    c = Canvas('c')

    h_sum = TH1F('h_sum','sum',h1.GetNbinsX(), h1.GetXaxis().GetXmin(), h1.GetXaxis().GetXmax())
    for h in v_hist: h_sum.Add(h)
 
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
    if log: pad1.SetLogy()
    stack = THStack('norm_stack','')
    h_mc_err = 0
    for h in v_hist: 
        stack.Add(h)
        if h_mc_err == 0: h_mc_err = h.Clone()
        else: h_mc_err.Add(h)
    stack.Draw('HIST')
    h_mc_err.Draw("e2 same")
    h_mc_err.SetMarkerSize(0)
    h_mc_err.SetFillColor(1)
    h_mc_err.SetFillStyle(3004)
    h1.Draw('p same')
    hs.Draw('HIST same')
    ymax=stack.GetMaximum()*200 if log else stack.GetMaximum()*1.5
    ymax2=h1.GetMaximum()*10 if log else h1.GetMaximum()*2
    stack.SetMaximum(max(ymax,ymax2))
    stack.SetMinimum(1)
    #stack.GetHistogram().GetYaxis().SetTitleSize(20)
    #stack.GetHistogram().GetYaxis().SetTitleFont(43)
    #stack.GetHistogram().GetYaxis().SetTitleOffset(4)
    stack.GetHistogram().GetYaxis().SetTitle('Events')
    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel(lab), lumiLabel()
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    legend = makeLegend(h1,v_hist,hs)
    legend.Draw()

    pad2.cd()
    h_ratio = h1.Clone('h_ratio')

    h_ratio.Sumw2()
    h_ratio.Divide(h_sum)
    h_ratio.SetMinimum(-0.499)
    h_ratio.SetMaximum(2.499)
    #h_ratio.SetMinimum(0.1)
    #h_ratio.SetMaximum(1.9)
    #h_ratio.GetYaxis().SetTickLength(0.5)
    h_ratio.SetMarkerStyle(20)
    h_ratio.SetMarkerSize(0.7)
    h_ratio.Draw('p same')
    denom_err, denom_err2 = h_mc_err.Clone(), h_mc_err.Clone()
    denom_err2.Sumw2(False)
    denom_err.Divide(denom_err2)
    denom_err.Draw("e2same")
    denom_err.SetFillColor(1)
    denom_err.SetFillStyle(3004)

    l1 = TLine(h_ratio.GetXaxis().GetXmin(), 1, h_ratio.GetXaxis().GetXmax(), 1)
    l2 = TLine(h_ratio.GetXaxis().GetXmin(), 1.5, h_ratio.GetXaxis().GetXmax(), 1.5)
    l3 = TLine(h_ratio.GetXaxis().GetXmin(), 0.5, h_ratio.GetXaxis().GetXmax(), 0.5)
    l4 = TLine(h_ratio.GetXaxis().GetXmin(), 0., h_ratio.GetXaxis().GetXmax(), 0.)
    l5 = TLine(h_ratio.GetXaxis().GetXmin(), 2, h_ratio.GetXaxis().GetXmax(), 2.)
    l2.SetLineStyle(3), l3.SetLineStyle(3), l4.SetLineStyle(3), l5.SetLineStyle(3)
    l1.Draw(), l2.Draw(), l3.Draw(), l4.Draw(), l5.Draw()

    Prettify( h_ratio )

    c.SaveAs('plots/'+name+'_'+selection+'.png')

def prelimLabel():
    label = TPaveText( 0.135, 0.76, 0.2, 0.84, 'NB NDC' ) # Left label
    #label = TPaveText( 0.8, 0.79, 0.87, 0.86, 'NB NDC' ) # Right label
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.SetTextAlign(11) # Align bottom left
    #label.SetTextAlign(31) # Align bottom right
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
    label.SetTextSize( 0.048 )
    label.SetTextAlign(11)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def lumiLabel():
    label = TPaveText( 0.70, 0.9, 0.8, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "37.19 fb^{-1} (13 TeV)" )
    label.SetTextSize( 0.048 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label

def makeLegend(h1,v_hist,hs):
    legend = TLegend(0.65, 0.55, 0.82, 0.85) 
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.038)
    legend.AddEntry(h1,'Data', 'lep')
    backgrounds = ['Incl. Z + #gamma', 'Incl. W + #gamma', '#gamma + j', 'Incl. #gamma#gamma + j (NLO)', 'QCD (e#gamma enriched)']
    for i in range( len(backgrounds) ):
        legend.AddEntry(v_hist[i],backgrounds[i],'f')
    legend.AddEntry(hs,'AQGC #times 100','l')
    return legend
    
def setPlot(h, color, rbin, xs, nevts):
    h.SetTitle('')
    h.Rebin(rbin)
    h.SetFillColorAlpha(color,0.4)
    h.SetLineColor(color)    
    #h.Scale(xs*lumi/nevts)
    return h

#-----------------------

v_mass = []
mass_rbin = 4

h_diph_mass = dataFile.Get("plots/h_diph_mass")
h_diph_mass.SetTitle('')
h_diph_mass.SetXTitle('m_{#gamma#gamma} GeV')
h_diph_mass.SetYTitle('Events')
h_diph_mass.Rebin(mass_rbin)
h_diph_mass.SetMarkerStyle(20)
h_diph_mass.SetMarkerSize(0.7)

h_ggj_diph_mass = ggjFile.Get("plots/h_diph_mass")
setPlot(h_ggj_diph_mass, ggj[3], mass_rbin, ggj[1], ggj[2])

h_gj_diph_mass = gjFile.Get("plots/h_diph_mass")
setPlot(h_gj_diph_mass, gj[3], mass_rbin, gj[1], gj[2])

h_wg_diph_mass = wgFile.Get("plots/h_diph_mass")
setPlot(h_wg_diph_mass, wg[3], mass_rbin, wg[1], wg[2])

h_zg_diph_mass = zgFile.Get("plots/h_diph_mass")
setPlot(h_zg_diph_mass, zg[3], mass_rbin, zg[1], zg[2])

h_qcd_diph_mass = qcdFile.Get("plots/h_diph_mass")
setPlot(h_qcd_diph_mass, qcd[3], mass_rbin, qcd[1], qcd[2])

h_aqgc_diph_mass = aqgcFile.Get("plots/h_diph_mass")
setPlot(h_aqgc_diph_mass, aqgc[3], mass_rbin, aqgc[1], aqgc[2])
h_aqgc_diph_mass.SetFillColor(0), h_aqgc_diph_mass.Scale(100)

v_mass.append(h_zg_diph_mass)
v_mass.append(h_wg_diph_mass)
v_mass.append(h_gj_diph_mass)
v_mass.append(h_ggj_diph_mass)
v_mass.append(h_qcd_diph_mass)

plotRatio('h_mass_comp', h_diph_mass, v_mass, h_aqgc_diph_mass, True)

#-----------------------

v_pt = []
pt_rbin = 2

h_single_pt = dataFile.Get("plots/h_single_pt")
h_single_pt.SetTitle('')
h_single_pt.SetXTitle('p_{T}^{#gamma} GeV')
h_single_pt.SetYTitle('Events')
h_single_pt.Rebin(pt_rbin)
h_single_pt.SetMarkerStyle(20)
h_single_pt.SetMarkerSize(0.7)

h_ggj_single_pt = ggjFile.Get("plots/h_single_pt")
setPlot(h_ggj_single_pt, ggj[3], pt_rbin, ggj[1], ggj[2])

h_gj_single_pt = gjFile.Get("plots/h_single_pt")
setPlot(h_gj_single_pt, gj[3], pt_rbin, gj[1], gj[2])

h_wg_single_pt = wgFile.Get("plots/h_single_pt")
setPlot(h_wg_single_pt, wg[3], pt_rbin, wg[1], wg[2])

h_zg_single_pt = zgFile.Get("plots/h_single_pt")
setPlot(h_zg_single_pt, zg[3], pt_rbin, zg[1], zg[2])

h_qcd_single_pt = qcdFile.Get("plots/h_single_pt")
setPlot(h_qcd_single_pt, qcd[3], pt_rbin, qcd[1], qcd[2])

h_aqgc_single_pt = aqgcFile.Get("plots/h_single_pt")
setPlot(h_aqgc_single_pt, aqgc[3], pt_rbin, aqgc[1], aqgc[2])
h_aqgc_single_pt.SetFillColor(0), h_aqgc_single_pt.Scale(100)

v_pt.append(h_zg_single_pt)
v_pt.append(h_wg_single_pt)
v_pt.append(h_gj_single_pt)
v_pt.append(h_ggj_single_pt)
v_pt.append(h_qcd_single_pt)

plotRatio('h_pt_comp', h_single_pt, v_pt, h_aqgc_single_pt, True)

#-----------------------

v_eta = []
eta_rbin = 4

h_single_eta = dataFile.Get("plots/h_single_eta")
h_single_eta.SetTitle('')
h_single_eta.SetXTitle('#eta ^{#gamma}')
h_single_eta.SetYTitle('Events')
h_single_eta.Rebin(eta_rbin)
h_single_eta.SetMarkerStyle(20)
h_single_eta.SetMarkerSize(0.7)

h_ggj_single_eta = ggjFile.Get("plots/h_single_eta")
setPlot(h_ggj_single_eta, ggj[3], eta_rbin, ggj[1], ggj[2])

h_gj_single_eta = gjFile.Get("plots/h_single_eta")
setPlot(h_gj_single_eta, gj[3], eta_rbin, gj[1], gj[2])

h_wg_single_eta = wgFile.Get("plots/h_single_eta")
setPlot(h_wg_single_eta, wg[3], eta_rbin, wg[1], wg[2])

h_zg_single_eta = zgFile.Get("plots/h_single_eta")
setPlot(h_zg_single_eta, zg[3], eta_rbin, zg[1], zg[2])

h_qcd_single_eta = qcdFile.Get("plots/h_single_eta")
setPlot(h_qcd_single_eta, qcd[3], eta_rbin, qcd[1], qcd[2])

h_aqgc_single_eta = aqgcFile.Get("plots/h_single_eta")
setPlot(h_aqgc_single_eta, aqgc[3], eta_rbin, aqgc[1], aqgc[2])
h_aqgc_single_eta.SetFillColor(0), h_aqgc_single_eta.Scale(100)

v_eta.append(h_zg_single_eta)
v_eta.append(h_wg_single_eta)
v_eta.append(h_gj_single_eta)
v_eta.append(h_ggj_single_eta)
v_eta.append(h_qcd_single_eta)

plotRatio('h_eta_comp', h_single_eta, v_eta, h_aqgc_single_eta, False)

#-----------------------
'''
v_acop = []
acop_rbin = 2

h_acop = dataFile.Get("plots/h_acop")
h_acop.SetTitle('')
h_acop.SetXTitle('1- |#Delta #phi|/#pi')
h_acop.SetYTitle('Events')
h_acop.Rebin(acop_rbin)
h_acop.SetMarkerStyle(20)
h_acop.SetMarkerSize(0.7)

h_ggj_acop = ggjFile.Get("plots/h_acop")
setPlot(h_ggj_acop, ggj[3], acop_rbin, ggj[1], ggj[2])

h_gj_acop = gjFile.Get("plots/h_acop")
setPlot(h_gj_acop, gj[3], acop_rbin, gj[1], gj[2])

h_wg_acop = wgFile.Get("plots/h_acop")
setPlot(h_wg_acop, wg[3], acop_rbin, wg[1], wg[2])

h_zg_acop = zgFile.Get("plots/h_acop")
setPlot(h_zg_acop, zg[3], acop_rbin, zg[1], zg[2])

h_qcd_acop = qcdFile.Get("plots/h_acop")
setPlot(h_qcd_acop, qcd[3], acop_rbin, qcd[1], qcd[2])

v_acop.append(h_zg_acop)
v_acop.append(h_wg_acop)
v_acop.append(h_gj_acop)
v_acop.append(h_ggj_acop)
v_acop.append(h_qcd_acop)

plotRatio('h_acop_comp', h_acop, v_acop, True)
'''
#-----------------------

v_nvtx = []
nvtx_rbin = 1

h_nvtx = dataFile.Get("plots/h_nvtx")
h_nvtx.SetTitle('')
h_nvtx.SetXTitle('Number of primary vertices')
h_nvtx.SetYTitle('Events')
h_nvtx.Rebin(nvtx_rbin)
h_nvtx.SetMarkerStyle(20)
h_nvtx.SetMarkerSize(0.7)

h_ggj_nvtx = ggjFile.Get("plots/h_nvtx")
setPlot(h_ggj_nvtx, ggj[3], nvtx_rbin, ggj[1], ggj[2])

h_gj_nvtx = gjFile.Get("plots/h_nvtx")
setPlot(h_gj_nvtx, gj[3], nvtx_rbin, gj[1], gj[2])

h_wg_nvtx = wgFile.Get("plots/h_nvtx")
setPlot(h_wg_nvtx, wg[3], nvtx_rbin, wg[1], wg[2])

h_zg_nvtx = zgFile.Get("plots/h_nvtx")
setPlot(h_zg_nvtx, zg[3], nvtx_rbin, zg[1], zg[2])

h_qcd_nvtx = qcdFile.Get("plots/h_nvtx")
setPlot(h_qcd_nvtx, qcd[3], nvtx_rbin, qcd[1], qcd[2])

h_aqgc_nvtx = aqgcFile.Get("plots/h_nvtx")
setPlot(h_aqgc_nvtx, aqgc[3], nvtx_rbin, aqgc[1], aqgc[2])
h_aqgc_nvtx.SetFillColor(0), h_aqgc_nvtx.Scale(100)

v_nvtx.append(h_zg_nvtx)
v_nvtx.append(h_wg_nvtx)
v_nvtx.append(h_gj_nvtx)
v_nvtx.append(h_ggj_nvtx)
v_nvtx.append(h_qcd_nvtx)

plotRatio('h_nvtx_comp', h_nvtx, v_nvtx, h_aqgc_nvtx, True)

#-----------------------

v_vtx_z = []
vtx_z_rbin = 1

h_vtx_z = dataFile.Get("plots/h_vtx_z")
h_vtx_z.SetTitle('')
h_vtx_z.SetXTitle('Vertex z position')
h_vtx_z.SetYTitle('Events')
h_vtx_z.Rebin(vtx_z_rbin)
h_vtx_z.SetMarkerStyle(20)
h_vtx_z.SetMarkerSize(0.7)

h_ggj_vtx_z = ggjFile.Get("plots/h_vtx_z")
setPlot(h_ggj_vtx_z, ggj[3], vtx_z_rbin, ggj[1], ggj[2])

h_gj_vtx_z = gjFile.Get("plots/h_vtx_z")
setPlot(h_gj_vtx_z, gj[3], vtx_z_rbin, gj[1], gj[2])

h_wg_vtx_z = wgFile.Get("plots/h_vtx_z")
setPlot(h_wg_vtx_z, wg[3], vtx_z_rbin, wg[1], wg[2])

h_zg_vtx_z = zgFile.Get("plots/h_vtx_z")
setPlot(h_zg_vtx_z, zg[3], vtx_z_rbin, zg[1], zg[2])

h_qcd_vtx_z = qcdFile.Get("plots/h_vtx_z")
setPlot(h_qcd_vtx_z, qcd[3], vtx_z_rbin, qcd[1], qcd[2])

h_aqgc_vtx_z = aqgcFile.Get("plots/h_vtx_z")
setPlot(h_aqgc_vtx_z, aqgc[3], vtx_z_rbin, aqgc[1], aqgc[2])
h_aqgc_vtx_z.SetFillColor(0), h_aqgc_vtx_z.Scale(100)

v_vtx_z.append(h_zg_vtx_z)
v_vtx_z.append(h_wg_vtx_z)
v_vtx_z.append(h_gj_vtx_z)
v_vtx_z.append(h_ggj_vtx_z)
v_vtx_z.append(h_qcd_vtx_z)

plotRatio('h_vtx_z_comp', h_vtx_z, v_vtx_z, h_aqgc_vtx_z, True)

#-----------------------

v_xip = []
xip_rbin = 4

h_xip = dataFile.Get("plots/h_xip")
h_xip.SetTitle('')
h_xip.SetXTitle('#xi_{#gamma#gamma}^{+}')
h_xip.SetYTitle('Events')
h_xip.Rebin(xip_rbin)
h_xip.SetMarkerStyle(20)
h_xip.SetMarkerSize(0.7)

h_ggj_xip = ggjFile.Get("plots/h_xip")
setPlot(h_ggj_xip, ggj[3], xip_rbin, ggj[1], ggj[2])

h_gj_xip = gjFile.Get("plots/h_xip")
setPlot(h_gj_xip, gj[3], xip_rbin, gj[1], gj[2])

h_wg_xip = wgFile.Get("plots/h_xip")
setPlot(h_wg_xip, wg[3], xip_rbin, wg[1], wg[2])

h_zg_xip = zgFile.Get("plots/h_xip")
setPlot(h_zg_xip, zg[3], xip_rbin, zg[1], zg[2])

h_qcd_xip = qcdFile.Get("plots/h_xip")
setPlot(h_qcd_xip, qcd[3], xip_rbin, qcd[1], qcd[2])

h_aqgc_xip = aqgcFile.Get("plots/h_xip")
setPlot(h_aqgc_xip, aqgc[3], xip_rbin, aqgc[1], aqgc[2])
h_aqgc_xip.SetFillColor(0), h_aqgc_xip.Scale(100)

v_xip.append(h_zg_xip)
v_xip.append(h_wg_xip)
v_xip.append(h_gj_xip)
v_xip.append(h_ggj_xip)
v_xip.append(h_qcd_xip)

plotRatio('h_xip_comp', h_xip, v_xip, h_aqgc_xip, True)

#-----------------------

v_xim = []
xim_rbin = 4

h_xim = dataFile.Get("plots/h_xim")
h_xim.SetTitle('')
h_xim.SetXTitle('#xi_{#gamma#gamma}^{-}')
h_xim.SetYTitle('Events')
h_xim.Rebin(xim_rbin)
h_xim.SetMarkerStyle(20)
h_xim.SetMarkerSize(0.7)

h_ggj_xim = ggjFile.Get("plots/h_xim")
setPlot(h_ggj_xim, ggj[3], xim_rbin, ggj[1], ggj[2])

h_gj_xim = gjFile.Get("plots/h_xim")
setPlot(h_gj_xim, gj[3], xim_rbin, gj[1], gj[2])

h_wg_xim = wgFile.Get("plots/h_xim")
setPlot(h_wg_xim, wg[3], xim_rbin, wg[1], wg[2])

h_zg_xim = zgFile.Get("plots/h_xim")
setPlot(h_zg_xim, zg[3], xim_rbin, zg[1], zg[2])

h_qcd_xim = qcdFile.Get("plots/h_xim")
setPlot(h_qcd_xim, qcd[3], xim_rbin, qcd[1], qcd[2])

h_aqgc_xim = aqgcFile.Get("plots/h_xim")
setPlot(h_aqgc_xim, aqgc[3], xim_rbin, aqgc[1], aqgc[2])
h_aqgc_xim.SetFillColor(0), h_aqgc_xim.Scale(100)

v_xim.append(h_zg_xim)
v_xim.append(h_wg_xim)
v_xim.append(h_gj_xim)
v_xim.append(h_ggj_xim)
v_xim.append(h_qcd_xim)

plotRatio('h_xim_comp', h_xim, v_xim, h_aqgc_xim, True)

#-----------------------
'''
c1 = Canvas("c1")
c1.cd()
c1.SetLogy()
h_diph_mass = dataFile.Get("plots/h_diph_mass")
h_diph_mass.Rebin(2)
#h_diph_mass.GetXaxis().SetRange(15,100)
h_diph_mass.SetTitle("")
h_diph_mass.SetXTitle('m_{#gamma#gamma} GeV')
h_diph_mass.SetYTitle('Events')
h_diph_mass.SetFillColor(fillColor)
h_diph_mass.SetLineColor(fillColor)
h_diph_mass.Draw()
pLabel, sLabel, lLabel = prelimLabel(), selectionLabel(lab), lumiLabel()
pLabel.Draw()
sLabel.Draw()
lLabel.Draw()
c1.SaveAs("h_diph_mass.png")
'''
#-----------------------



