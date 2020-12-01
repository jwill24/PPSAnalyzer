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

lab = 'HLT selection'
selection = 'HLT'
#years = ['2017','2018']
years = ['2018']
s_years = '+'.join(years)

protonFiles = [['2017',TFile('outputHists/2017/histOut_data2017_'+selection+'_singleRP.root'),TFile('outputHists/2017/histOut_data2017_'+selection+'_multiRP.root')],
               ['2018',TFile('outputHists/2018/histOut_data2018_'+selection+'_singleRP.root'),TFile('outputHists/2018/histOut_data2017_'+selection+'_multiRP.root')]]
#protonFiles = [['2017',TFile('outputHists/2017/histOut_data2017_'+selection+'_singleRP.root'),TFile('outputHists/2017/histOut_data2017_'+selection+'_multiRP.root')]]

proton_pot = [['45f','(45F)', 0.016], ['45n','(45N)', 0.013], ['56n','(56N)', 0.048], ['56f','(56F)', 0.037]]

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

def makeProtonPlot(name, xTitle, rbin, log):
    c = Canvas('c')
    c.cd()
    c.SetTicks(1,1)
    if log: c.SetLogy()
    h = getHist('data',year,name)
    h.SetTitle('')
    h.SetXTitle(xTitle)
    h.SetYTitle('Events')
    h.Rebin(rbin)
    h.SetFillColor(208)
    h.SetLineColor(208)
    if log: h.SetMaximum( h.GetMaximum()*30 )
    else: h.SetMaximum( h.GetMaximum()*1.2 )
    if 'detType' in name: h.GetXaxis().SetBinLabel(1,'Strip'), h.GetXaxis().SetBinLabel(2,'Pixel')
    h.Draw('HIST')
    pLabel, sLabel, lLabel = prelimLabel('left',log,h.GetMaximum()), selectionLabel(lab,False,log,h.GetMaximum()), lumiLabel(False,years)
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    c.SaveAs('plots/'+year+'/'+name+'_'+selection+'.pdf')


def makeXiComp(sector,log):
    sec = 'p' if sector == '45' else 'm'
    c = Canvas('c')
    c.cd()
    c.SetTicks(1,1)
    if log: c.SetLogy()
    #c.SetGrid(1,1)
    h_near = ROOT.TH1F('h_near', '', 100, 0.0, 0.3) 
    h_far = ROOT.TH1F('h_far', '', 100, 0.0, 0.3) 
    h_multi = ROOT.TH1F('h_multi', '', 100, 0.0, 0.3) 
    # Add hists
    for year in years:
        for pf in protonFiles:
            if year == pf[0]: pf_single, pf_multi = pf[1], pf[2]
        h_near.Add( pf_single.Get('plots/h_pro_xi_'+sector+'n') )
        h_far.Add( pf_single.Get('plots/h_pro_xi_'+sector+'f') )
        h_multi.Add( pf_multi.Get('plots/h_pro_xi'+sec) )

    h_far.SetLineColor(210)
    #h_far.Rebin(2)
    h_near.SetLineColor(62)
    #h_near.Rebin(2)
    h_multi.SetLineColor(207)
    #h_multi.Rebin(2)
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
    pLabel, lLabel = prelimLabel('top',log,h_far.GetMaximum()), lumiLabel(False,years)
    pLabel.Draw(), lLabel.Draw()
    c.SaveAs('plots/%s/h_xi_comp_%s.pdf' % (s_years,sector)) 

def makeProtonSide(log):
    c = Canvas('c')
    c.cd()
    if log: c.SetLogy()
    c.SetTicks(1,1)
    h_single = ROOT.TH1F('h_single', '', 3, 0, 3)
    h_multi = ROOT.TH1F('h_multi', '', 3, 0, 3)
    for year in years:
        for pf in protonFiles:
            if year == pf[0]: pf_single, pf_multi = pf[1], pf[2]
        h_single.Add( pf_single.Get('plots/h_proton_side') )
        h_multi.Add( pf_multi.Get('plots/h_proton_side') )
    
    h_multi.Scale(1.0/100.0)
    h_multi.GetYaxis().SetTitle('Events/0.01')
    h_multi.GetXaxis().SetBinLabel(1,'No protons'), h_multi.GetXaxis().SetBinLabel(2,'sector45 only'), h_multi.GetXaxis().SetBinLabel(3,'sector56 only'), h_multi.GetXaxis().SetBinLabel(4,'Both')
    h_multi.Draw('p')
    h_single.Scale(1.0/100.0)
    h_single.Draw('p same')
    h_single.SetMarkerColor(62), h_multi.SetMarkerColor(207)
    h_single.SetLineColor(62), h_multi.SetLineColor(207)
    h_single.SetLineWidth(2), h_multi.SetLineWidth(2)
    h_single.SetMarkerStyle(20), h_multi.SetMarkerStyle(20)
    h_multi.SetMinimum(0.0), h_multi.SetMaximum( h_multi.GetMaximum()*1.5 )
    h_single.SetMarkerSize(0.9), h_multi.SetMarkerSize(0.9)
    c.SetGrid(0,1)
    legend = TLegend(0.6,0.7,0.8,0.78)
    legend.SetTextSize(0.03)
    legend.SetLineColor( 0 )
    legend.SetFillColor( 0 )
    legend.AddEntry(h_single,"singleRP",'lp')
    legend.AddEntry(h_multi,"multiRP",'lp')
    legend.Draw()
    pLabel, lLabel = prelimLabel('top',log,h_single.GetMaximum()), lumiLabel(False,years)
    pLabel.Draw(), lLabel.Draw()
    c.SaveAs('h_proton_side_'+selection+'.png')
    
def makeDetType():
    c = Canvas('c')
    c.cd()
    c.SetTicks(1,1)
    h_type = ROOT.TH1F('h_type', '', 2, 3, 5)
    for year in years:
        for pf in protonFiles:
            if year == pf[0]: pfile = pf[1]
        h_type.Add( pfile.Get('plots/h_detType') )
    h_type.Scale(1.0/1000.0)
    h_type.GetXaxis().SetBinLabel(1,'Si Strip'), h_type.GetXaxis().SetBinLabel(2,'Pixel')
    h_type.GetYaxis().SetTitle('Events/0.001')
    h_type.Draw('p')
    h_type.SetLineColor(ROOT.kBlack)
    h_type.SetLineWidth(2)
    h_type.SetMarkerStyle(20)
    h_type.SetMinimum(0.0), h_type.SetMaximum( h_type.GetMaximum() * 1.5 )
    h_type.SetMarkerSize(0.9)
    c.SetGrid(0,1)
    pLabel, sLabel, lLabel = prelimLabel('left',False,h_type.GetMaximum()), selectionLabel('singleRP',False,False,h_type.GetMaximum()), lumiLabel(False,years)
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    c.SaveAs('h_detType_'+selection+'_'+s_years+'.png')

def makeHitMap(sector):
    c = Canvas('c')
    c.cd()
    c.SetTicks(1,1)
    h_map = ROOT.TH2F('h_map', '', 100, 0, 12, 100, -8, 8)
    for year in years:
        for pf in protonFiles:
            if year == pf[0]: pfile = pf[1]
        h_map.Add( pfile.Get('plots/h_hitmap'+sector) )
    h_map.GetXaxis().SetTitle('x (mm)')
    h_map.GetYaxis().SetTitle('y (mm)')
    h_map.Draw('colz')
    pLabel, lLabel = prelimLabel('top',False,h_map.GetMaximum()), lumiLabel(False,years)
    pLabel.Draw(), lLabel.Draw()
    c.SaveAs('hitmap_'+sector+'_'+s_years+'_'+selection+'.png')

def makeXiAcceptance(pot,log):
    c = Canvas('c')
    c.cd()
    if log: c.SetLogy()
    c.SetTicks(1,1)
    c.SetGrid(1,1)
    h = ROOT.TH1F('h', '', 100, 0, 0.3)
    for year in years:
        for pf in protonFiles:
            if year == pf[0]: pfile = pf[1]
        h.Add( pfile.Get('plots/h_pro_xi_'+pot) )
    h.Rebin(2)
    #h.Scale(1.0/100.0)
    for pp in proton_pot:
        if pot == pp[0]: v_pot = pp
    h.GetXaxis().SetTitle('#xi '+v_pot[1])
    h.GetYaxis().SetTitle('Events')
    h.SetLineColor(ROOT.kBlack)
    h.SetMarkerStyle(24)
    minx, miny, maxx, maxy = 0.0001, h.GetMinimum(), 0.2, h.GetMaximum()*10 if log else h.GetMaximum()*1.2
    c.DrawFrame(minx, miny, maxx, maxy)
    h.Draw('p e2')
    h.SetMaximum(maxy)
    pLabel, lLabel = prelimLabel('top',log,maxy), lumiLabel(log,years)
    pLabel.Draw(), lLabel.Draw()
    #l1 = ROOT.TLine(0.015,miny,0.015,maxy)
    #l2 = ROOT.TLine(v_pot[2],miny,v_pot[2],maxy)
    #l1.SetLineStyle(3), l2.SetLineStyle(3)
    #l1.SetLineColor(ROOT.kGreen), l2.SetLineColor(ROOT.kRed)
    #l1.Draw(), l2.Draw()
    #legend = TLegend(0.6,0.6,0.7,0.7)
    #legend.SetTextSize(0.03)
    #legend.SetLineColor( 0 )
    #legend.SetFillColor( 0 )
    #legend.AddEntry(l1,'Nominal accept.','l')
    #legend.AddEntry(l2,'Observed accept.','l')
    #legend.Draw()
    c.SaveAs('h_xi_'+pot+'_'+s_years+'.png')

#-----------------------


#makeProtonPlot('h_num_pro', 'Number of protons', 1, False)
#makeProtonPlot('h_detType', 'Proton Detector Type', 1, False)
#makeProtonPlot('h_pro_xip', 'Proton #xi ^{+}', 1, True)
#makeProtonPlot('h_pro_xim', 'Proton #xi ^{-}', 1, True)
#makeProtonPlot('h_pro_xi_45f', 'Proton #xi 45F', 1, False)
#makeProtonPlot('h_pro_xi_45n', 'Proton #xi 45N', 1, False)
#makeProtonPlot('h_pro_xi_56n', 'Proton #xi 56N', 1, False)
#makeProtonPlot('h_pro_xi_56f', 'Proton #xi 56F', 1, False)

makeXiComp('45',True)
makeXiComp('56',True)


#makeProtonSide(False)


#makeHitMap('45')
#makeHitMap('56')


## singleRP only
#makeDetType()
#makeXiAcceptance('45f',True)
#makeXiAcceptance('45n',True)
#makeXiAcceptance('56n',True)
#makeXiAcceptance('56f',True)
