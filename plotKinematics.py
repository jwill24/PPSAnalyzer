# Make protonPlot compatible with multiple years

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

lab = '#xi^{#gamma#gamma} #in PPS selection'
selection = 'Xi'
method = 'multiRP'
years = ['2016','2017','2018']
#years = ['2018']
s_years = '+'.join(years)
samples = sampleColors()
samples.append(['aqgc',92,92])
samples.append(['data',kBlack,kBlack])
aqgcFile = TFile('outputHists/2017/histOut_aqgc2017_Xi_multiRP.root')
v_files = []
for year in years:
    for s in samples:
        v_files.append( (s[0]+year, TFile('outputHists/%s/histOut_%s_%s_%s.root' % (year,s[0]+year,selection,method))) )


def plotRatio(name, h1, v_hist, hs, log):
    c = Canvas('c')

    h_sum = TH1F('h_sum','sum',h1.GetNbinsX(), h1.GetXaxis().GetXmin(), h1.GetXaxis().GetXmax())
    for h in v_hist: h_sum.Add(h)
 
    pad1 = TPad('pad1', 'pad1', 0.0, 0.3, 1., 1.)
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
    ymax = h1.GetMaximum()*pow(10,1.0) if log else h1.GetMaximum()*1.5 
    stack.SetMaximum(ymax)
    if log: stack.SetMinimum(1)
    #stack.GetHistogram().GetYaxis().SetTitleFont(43)
    stack.GetHistogram().GetYaxis().SetTitleOffset(1.0)
    stack.GetHistogram().GetYaxis().SetTitleSize(0.05)
    stack.GetHistogram().GetYaxis().SetTitle('Events')
    pLabel, sLabel, lLabel = prelimLabel('left',log,h1.GetMaximum()), selectionLabel(lab,True,log,h1.GetMaximum()), lumiLabel(True,years)
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
    h_ratio.SetMarkerColor(ROOT.kBlack)
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

    if len(years) == 1: c.SaveAs('plots/'+years[0]+'/'+name+'_'+selection+'.pdf')
    else: c.SaveAs('plots/combined/'+name+'_'+selection+'_'+s_years+'.pdf') # saving as pdf

def prelimLabel(location,log,maximum):
    if location == 'left':
        label = TPaveText( 0.135, 0.76, 0.2, 0.84, 'NB NDC' )
        label.AddText( "#font[62]{CMS}" )
        label.AddText( "#scale[0.75]{#font[52]{Preliminary}}" )
    elif location == 'top':
        label = TPaveText( 0.12, 0.9, 0.2, 0.92, 'NB NDC' )
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

def selectionLabel(text,ratio,log,maximum):
    label = TPaveText( 0.1, 0.9, 0.18, 0.92, 'NB NDC' )
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

def setPlot(h, sample, rbin):
    fill, line = getColors(sample)
    h.SetTitle('')
    h.Rebin(rbin)
    #h.SetFillColorAlpha(fill,0.4)
    h.SetFillColor(fill)
    h.SetLineColor(line) 
    h.SetLineWidth(2)
    return h

def getHist(sample, year, name):
    for s in v_files:
        if sample+year == s[0]: 
            h = s[1].Get('plots/'+name)
        if sample == 'aqgc' and 'aqgc' in s[0]: # FIXME: temporary until MC samples are produced
            h = aqgcFile.Get('plots/'+name)
    return h

def makePlot(inName, outName, xTitle, rbin, log):
    v = []
        
    for i, year in enumerate(years):

        if i == 0:
            h_standard = getHist('data',year,inName)
            bins = h_standard.GetNbinsX()
            first = h_standard.GetXaxis().GetXmin()
            last = h_standard.GetXaxis().GetXmax()
            
            h_data = TH1F('h_data', '', bins, first, last)
            h_ggj = TH1F('h_ggj', '', bins, first, last)
            h_gj = TH1F('h_gj', '', bins, first, last)
            h_qcd = TH1F('h_qcd', '', bins, first, last)
            h_wg = TH1F('h_wg', '', bins, first, last)
            h_zg = TH1F('h_zg', '', bins, first, last)
            h_tt = TH1F('h_tt', '', bins, first, last)
            h_aqgc = TH1F('h_aqgc', '', bins, first, last)

        h_data.Add( getHist('data',year,inName) )
        h_ggj.Add( getHist('ggj',year,inName) )
        h_gj.Add( getHist('g+j',year,inName) )
        h_qcd.Add( getHist('qcd',year,inName) )
        h_wg.Add( getHist('wg',year,inName) )
        h_zg.Add( getHist('zg',year,inName) )
        h_tt.Add( getHist('tt',year,inName) )
        h_aqgc.Add( getHist('aqgc',year,inName) ) 

    h_data.SetTitle('')
    h_data.SetXTitle(xTitle)
    h_data.SetYTitle('Events')
    h_data.Rebin(rbin)
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(0.7)

    setPlot(h_ggj, 'ggj', rbin)
    setPlot(h_gj, 'g+j', rbin)
    setPlot(h_qcd, 'qcd', rbin)
    setPlot(h_wg, 'wg', rbin)
    setPlot(h_zg, 'zg', rbin)
    setPlot(h_tt, 'tt', rbin)
    setPlot(h_aqgc, 'aqgc', rbin)
    h_aqgc.SetFillColor(0)
    h_aqgc.Scale(100)
        
    v.append(h_tt), v.append(h_zg), v.append(h_wg), v.append(h_gj), v.append(h_ggj), v.append(h_qcd)
        
    plotRatio(outName, h_data, v, h_aqgc, log)

def getColors(sample):
    for s in samples:
        if sample == s[0]:
            return s[1], s[2]
    


#-----------------------


makePlot('h_diph_mass', 'h_mass_comp', 'm_{#gamma#gamma} GeV', 4, True)
#makePlot('h_acop', 'h_acop_comp', '1- |#Delta #phi|/#pi', 2, True)
makePlot('h_single_pt', 'h_pt_comp', 'p_{T}^{#gamma} GeV', 4, True)
#makePlot('h_lead_pt', 'h_lead_pt_comp', 'Leading p_{T}^{#gamma} GeV', 2, True)
#makePlot('h_sub_pt', 'h_sub_pt_comp', 'Subleading p_{T}^{#gamma} GeV', 2, True)
makePlot('h_single_eta', 'h_eta_comp', '#eta ^{#gamma}', 2, False)
#makePlot('h_lead_eta', 'h_lead_eta_comp', 'Leading #eta ^{#gamma}', 4, False)
#makePlot('h_sub_eta', 'h_sub_eta_comp', 'Subleading #eta ^{#gamma}', 4, False)
#makePlot('h_single_r9', 'h_r9_comp', 'R_{9} ^{#gamma}', 1, True)
#makePlot('h_lead_r9', 'h_lead_r9_comp', 'Leading R_{9} ^{#gamma}', 2, True)
#makePlot('h_sub_r9', 'h_sub_r9_comp', 'Subleading R_{9} ^{#gamma}', 2, True)
#makePlot('h_eb_hoe', 'h_eb_hoe_comp', 'EB H/E', 1, True)
#makePlot('h_eb_sieie', 'h_eb_sieie_comp', 'EB #sigma_{i#etai#eta}', 1, True)
makePlot('h_nvtx', 'h_nvtx_comp', 'Number of vertices', 1, True)
makePlot('h_vtx_z', 'h_vtx_z_comp', 'Vertex z position', 1, True)
#makePlot('h_xip', 'h_xip_comp', '#xi_{#gamma#gamma}^{+}', 4, True)
#makePlot('h_xim', 'h_xim_comp', '#xi_{#gamma#gamma}^{-}', 2, True)
makePlot('h_fgr', 'h_fgr_comp', 'fixedGridRho', 1, True)
makePlot('h_num_pho', 'h_num_pho_comp', 'Number of photons', 1, True)

