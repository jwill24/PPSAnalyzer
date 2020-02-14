#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)

lab = 'HLT selection'
selection = 'HLTpuUp'
fillColor = 212
lumi = 37200.0 # pb

lightBlue, red, yellow, purple, darkGreen, green = ROOT.kCyan-9, 208, ROOT.kYellow-9, 38, ROOT.kTeal+3, ROOT.kGreen-9

ggj =  ['outputHists/histOut_ggj_'+selection+'_2017.root',138.5,4000000,red]
gj =   ['outputHists/histOut_g+j_'+selection+'_2017.root',873.7,80000000, darkGreen]
qcd =  ['outputHists/histOut_qcd_'+selection+'_2017.root',117500,4000000, lightBlue]
wg =   ['outputHists/histOut_wg_'+selection+'_2017.root',465,6300000, purple] 
zg =   ['outputHists/histOut_zg_'+selection+'_2017.root',55.47,30000000, yellow]
tt =   ['outputHists/histOut_tt_'+selection+'_2017.root',494.9,8026103, green]
aqgc = ['outputHists/histOut_aqgc_'+selection+'_2017.root',3.86e-5,300000, 92] 


# Histogram files
dataFile = TFile('outputHists/histOut_data_'+selection+'_2017.root')
ggjFile  = TFile(ggj[0])
gjFile   = TFile(gj[0])
qcdFile  = TFile(qcd[0])
wgFile   = TFile(wg[0])
zgFile   = TFile(zg[0])
ttFile   = TFile(tt[0])
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
    h_data = asym_error_bars(h1)
    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetFillColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.Draw('p e2 same')
    hs.Draw('HIST same')
    if any(['Elastic' in lab, 'Xi' in lab]):
        ymax=stack.GetMaximum()*2 if log else stack.GetMaximum()*1.2
        ymax2=h_data.GetMaximum()*2 if log else h_data.GetMaximum()*1.2
    else:
        ymax=stack.GetMaximum()*10 if log else stack.GetMaximum()*1.6
        ymax2=h_data.GetMaximum()*10 if log else h_data.GetMaximum()*1.6
    stack.SetMaximum(max(ymax,ymax2))
    if log: stack.SetMinimum(1)
    #stack.GetHistogram().GetYaxis().SetTitleSize(20)
    #stack.GetHistogram().GetYaxis().SetTitleFont(43)
    #stack.GetHistogram().GetYaxis().SetTitleOffset(4)
    stack.GetHistogram().GetYaxis().SetTitle('Events')
    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel(lab,True,log), lumiLabel(True)
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    legend = makeLegend(h1,v_hist,hs)
    legend.Draw()

    pad2.cd()
    h_ratio = h1.Clone('h_ratio')

    h_ratio.Sumw2()
    h_ratio.Divide(h_sum)
    h_ratio.SetMinimum(-0.499)
    h_ratio.SetMaximum(2.499)
    h_ratio.SetLineColor(ROOT.kBlack)
    h_ratio.SetMarkerStyle(20)
    h_ratio.SetMarkerColorAlpha(ROOT.kBlack,1)
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

def asym_error_bars(hist):
    alpha = 1 - 0.6827
    g = ROOT.TGraphAsymmErrors(hist)
    for i in range(0,g.GetN()):
        N = g.GetY()[i]
        if N == 0: continue #FIXME skip the empty bins??
        L = 0. if N == 0 else ( ROOT.Math.gamma_quantile( 0.5*alpha, N, 1. ) )
        U = ( ROOT.Math.gamma_quantile_c( alpha, N+1, 1 ) ) if N == 0 else ( ROOT.Math.gamma_quantile_c( 0.5*alpha, N+1, 1 ) )
        g.SetPointEXlow( i, 0. ) #FIXME
        g.SetPointEXhigh( i, 0. ) #FIXME
        g.SetPointEYlow( i, N-L )
        g.SetPointEYhigh( i, U-N )
    return g

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

def selectionLabel(text,ratio,log):
    if log: label = TPaveText( 0.1, 0.9, 0.18, 0.92, 'NB NDC' ) 
    else: label = TPaveText( 0.15, 0.9, 0.2, 0.92, 'NB NDC' ) 
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( text )
    if ratio: label.SetTextSize( 0.048 )
    else: label.SetTextSize( 0.034 )
    label.SetTextAlign(11)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def lumiLabel(ratio):
    label = TPaveText( 0.70, 0.9, 0.8, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "37.19 fb^{-1} (13 TeV)" )
    if ratio: label.SetTextSize( 0.048 )
    else: label.SetTextSize( 0.034 )
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
    backgrounds = ['t#bar{t} + j (NLO)', 'Incl. Z + #gamma', 'Incl. W + #gamma', '#gamma + j', 'Incl. #gamma#gamma + j (NLO)', 'QCD (e#gamma enriched)']
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

def makePlot(inName, outName, xTitle, rbin, log):
    v = []
    h_data = dataFile.Get('plots/' + inName)
    h_data.SetTitle('')
    h_data.SetXTitle(xTitle)
    h_data.SetYTitle('Events')
    h_data.Rebin(rbin)
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(0.7)

    h_ggj = ggjFile.Get('plots/' + inName)
    setPlot(h_ggj, ggj[3], rbin, ggj[1], ggj[2])
    
    h_gj = gjFile.Get('plots/' + inName)
    setPlot(h_gj, gj[3], rbin, gj[1], gj[2])

    h_qcd = qcdFile.Get('plots/' + inName)
    setPlot(h_qcd, qcd[3], rbin, qcd[1], qcd[2])

    h_wg = wgFile.Get('plots/' + inName)
    setPlot(h_wg, wg[3], rbin, wg[1], wg[2])

    h_zg = zgFile.Get('plots/' + inName)
    setPlot(h_zg, zg[3], rbin, zg[1], zg[2])

    h_tt = ttFile.Get('plots/' + inName)
    setPlot(h_tt, tt[3], rbin, tt[1], tt[2])

    h_aqgc = aqgcFile.Get('plots/' + inName)
    setPlot(h_aqgc, aqgc[3], rbin, aqgc[1], aqgc[2])
    h_aqgc.SetFillColor(0), h_aqgc.Scale(100)

    v.append(h_tt), 
    v.append(h_zg), v.append(h_wg), v.append(h_gj), v.append(h_ggj), v.append(h_qcd)
    
    plotRatio(outName, h_data, v, h_aqgc, log)
    
def makeProtonPlot(name, xTitle, rbin, log):
    c = Canvas('c')
    c.cd()
    h = dataFile.Get('plots/' + name)
    h.SetTitle('')
    h.SetXTitle(xTitle)
    h.SetYTitle('Events')
    h.Rebin(rbin)
    h.SetFillColor(ROOT.kTeal-4)
    h.SetMaximum( h.GetMaximum()*1.2 )
    if 'detType' in name: h.GetXaxis().SetBinLabel(1,'Pixel'), h.GetXaxis().SetBinLabel(2,'Strip')
    h.Draw('HIST')
    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel(lab,False,log), lumiLabel(False)
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    c.SaveAs('plots/'+name+'_'+selection+'.png')



#-----------------------

makePlot('h_diph_mass', 'h_mass_comp', 'm_{#gamma#gamma} GeV', 4, True)
makePlot('h_acop', 'h_acop_comp', '1- |#Delta #phi|/#pi', 2, True)
makePlot('h_single_pt', 'h_pt_comp', 'p_{T}^{#gamma} GeV', 2, True)
makePlot('h_lead_pt', 'h_lead_pt_comp', 'Leading p_{T}^{#gamma} GeV', 2, True)
makePlot('h_sub_pt', 'h_sub_pt_comp', 'Subleading p_{T}^{#gamma} GeV', 2, True)
makePlot('h_single_eta', 'h_eta_comp', '#eta ^{#gamma}', 4, False)
makePlot('h_lead_eta', 'h_lead_eta_comp', 'Leading #eta ^{#gamma}', 4, False)
makePlot('h_sub_eta', 'h_sub_eta_comp', 'Subleading #eta ^{#gamma}', 4, False)
makePlot('h_single_r9', 'h_r9_comp', 'R_{9} ^{#gamma}', 2, True)
makePlot('h_lead_r9', 'h_lead_r9_comp', 'Leading R_{9} ^{#gamma}', 2, True)
makePlot('h_sub_r9', 'h_sub_r9_comp', 'Subleading R_{9} ^{#gamma}', 2, True)
makePlot('h_nvtx', 'h_nvtx_comp', 'Number of vertices', 1, True)
makePlot('h_vtx_z', 'h_vtx_z_comp', 'Vertex z position', 1, True)
makePlot('h_xip', 'h_xip_comp', '#xi_{#gamma#gamma}^{+}', 4, True)
makePlot('h_xim', 'h_xim_comp', '#xi_{#gamma#gamma}^{-}', 4, True)
makePlot('h_fgr', 'h_fgr_comp', 'fixedGridRho', 1, True)
makePlot('h_num_pho', 'h_num_pho_comp', 'Number of photons', 1, False)



makeProtonPlot('h_num_pro', 'Number of protons', 1, False)
makeProtonPlot('h_detType', 'Proton Detector Type', 1, False)
makeProtonPlot('h_pro_xip', 'Proton #xi ^{+}', 1, False)
makeProtonPlot('h_pro_xim', 'Proton #xi ^{-}', 1, False)

