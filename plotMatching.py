#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, TGraphErrors
from ROOT import gROOT, gStyle

gStyle.SetOptStat(0)
extension = 'pdf'

#years = ['2016','2017','2018']
years = ['2018']
s_years = '+'.join(years)
files = [['2016',TFile('outputHists/2016/histOut_data2016_ReverseElastic_multiRP.root')],
         ['2017',TFile('outputHists/2017/histOut_data2017_ReverseElastic_multiRP.root')],
         ['2018',TFile('outputHists/2018/histOut_data2018_ReverseElastic_multiRP.root')]]
#files = [['2016',TFile('outputHists/2016/histOut_data2016_Xi_multiRP.root')],
#         ['2017',TFile('outputHists/2017/histOut_data2017_Xi_singleRP.root')],
#         ['2018',TFile('outputHists/2018/histOut_data2018_Xi_singleRP.root')]]

#files = [['2018',TFile('outputHists/2018/histOut_data2018_ReverseElastic_multiRP.root')]]


def Canvas(name):
    canvas = TCanvas(name,'',750,600)
    return canvas

def PaveText(x1,y1,x2,y2):
    txt = TPaveText(x1,y1,x2,y2)
    txt.SetFillStyle(0)
    txt.SetLineWidth(0)
    txt.SetLineStyle(0)
    txt.SetTextFont(52)
    txt.SetTextSize(0.033)
    return txt

def topLabel(text):
    lab = PaveText( 0.1, 0.9, 0.18, 0.92, 'NB NDC' )
    lab.AddText( text )
    lab.Draw()
    return lab

def prelimLabel():
    label = TPaveText( 0.14, 0.8, 0.2, 0.87, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.SetTextAlign(11)
    label.AddText( "#font[62]{CMS}" )
    label.AddText( "#scale[0.75]{#font[52]{Preliminary}}" )
    label.SetTextSize(0.043)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def selectionLabel(text):
    label = TPaveText(0.08, 0.89, .6, 0.95, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( text )
    label.SetTextSize( 0.033 )
    label.SetTextAlign(11)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label
    
def lumiLabel():
    label = TPaveText( 0.7, 0.89, 0.8, 0.93, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    if len(years) == 1 and years[0] == '2016': luminosity = '9.78'
    elif len(years) == 1 and years[0] == '2017': luminosity = '37.19'
    elif len(years) == 1 and years[0] == '2018': luminosity = '55.72'
    elif len(years) == 2: luminosity = '92.91'
    elif len(years) == 3: luminosity = '102.7'
    label.AddText( luminosity+" fb^{-1} (13 TeV)" )
    label.SetTextSize( 0.033 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label
    
def getGraph(year,kind='none'):
    for f in files:
        if year == f[0]: 
            if kind == 'none': g = f[1].Get('plots/gr_matching')
            elif kind == 'xim': g = f[1].Get('plots/gr_xim_matching')
            elif kind == 'xip': g = f[1].Get('plots/gr_xip_matching')
    return g

def massrap_matching(blinded):
    c = Canvas("c")
    c.cd()
    c.SetTicks(1,1)
    
    gr = ROOT.TGraphErrors('gr')
    gr.SetName('gr')
    count_20, count_5, count_3, count_2, x, y = 0, 0, 0, 0, ROOT.Double(0), ROOT.Double(0)
    for i, year in enumerate(years): 
        g = getGraph(year)
        n_gr = gr.GetN() if i > 0 else 0
        for j in range(g.GetN()):
            g.GetPoint(j,x,y)
            ex = g.GetErrorX(j)
            ey = g.GetErrorY(j)
            gr.SetPoint(n_gr+j,x,y)
            gr.SetPointError(n_gr+j,ex,ey)
            if abs(x) < 20 and abs(y) < 20: count_20 += 1
            if abs(x) < 5 and abs(y) < 5: count_5 += 1
            if abs(x) < 3 and abs(y) < 3: count_3 += 1
            if abs(x) < 2 and abs(y) < 2: count_2 += 1

    print 'Total events:', gr.GetN(), '20sig:', count_20, '5sig:', count_5, '3sig:', count_3, '2sig:', count_2

    gr.SetLineColor(ROOT.kBlack)
    gr.SetTitle('')
    gr.GetXaxis().SetTitle("(m_{pp}-m_{#gamma#gamma})/#sigma(m_{pp}-m_{#gamma#gamma})")
    gr.GetYaxis().SetTitle("(y_{pp} - y_{#gamma#gamma})/#sigma(y_{pp} - y_{#gamma#gamma})")
    gr.GetXaxis().SetLimits(-20,20)
    gr.GetYaxis().SetRangeUser(-20,20)
    gr.SetMarkerSize(0.5)
    gr.SetMarkerStyle(24)
    gr.Draw("AP")

    b3 = TBox(-5, -5, 5, 5)
    b3.SetLineColor(ROOT.kRed)
    b3.SetFillStyle(0)
    #b3.Draw()
    b2 = TBox(-3, -3, 3, 3)
    if not blinded: b2.SetFillStyle(3001) # transparent
    b2.SetFillColor(5)
    b2.SetLineColor(1)
    b2.Draw()
    b1 = TBox(-2, -2, 2, 2)
    if not blinded: b1.SetFillStyle(3001) # transparent
    b1.SetFillColor(3) 
    b1.SetLineColor(1)
    b1.Draw()
    legend = TLegend(0.7,0.8,0.9,0.9)
    legend.AddEntry(b1,"2#sigma matching",'f')
    legend.AddEntry(b2,"3#sigma matching",'f')
    #legend.AddEntry(b3,"5#sigma matching",'l')
    legend.Draw()
    c.Update() 
    pLabel = prelimLabel()
    pLabel.Draw()
    sLabel = selectionLabel("#xi^{#pm}_{#gamma#gamma} #in PPS")
    #sLabel = selectionLabel("Reverse acop. selection")
    sLabel.Draw()
    lLabel = lumiLabel()
    lLabel.Draw()
    s_blind = '_blinded' if blinded else ''
    c.SaveAs("plots/matching/massrap_matching_"+s_years+"_multiRP%s.%s" % (s_blind,extension))

def xi_matching(sector):
    c = Canvas("c")
    c.cd()
    c.SetTicks(1,1)

    gr = ROOT.TGraphErrors('gr')
    gr_m = ROOT.TGraphErrors('gr_m')
    gr.SetName('gr')
    gr_m.SetName('gr_m')
    x, y = ROOT.Double(0), ROOT.Double(0)
    for i, year in enumerate(years):

        g = getGraph(year,'xi'+sector)
        n_grm = gr_m.GetN() if i > 0 else 0
        n_gr = gr.GetN() if i > 0 else 0
        for j in range(g.GetN()):
            g.GetPoint(j,x,y)
            ex = g.GetErrorX(j) # FIXME?
            ey = g.GetErrorY(j)
            diff = abs(y-x)
            if diff < 0.003:
            #if diff < 0.02 * x: # only using relative PPS xi error
                gr_m.SetPoint(n_grm+j,x,y) 
                gr_m.SetPointError(n_grm+j,ex,ey)
            else:
                gr.SetPoint(n_gr+j,x,y) 
                gr.SetPointError(n_gr+j,ex,ey)
 

    gr.SetMarkerSize(0.6)
    gr.SetMarkerStyle(24)
    gr_m.SetMarkerSize(0.6)
    gr_m.SetMarkerStyle(24) 
    gr_m.SetMarkerColor(ROOT.kRed)
    gr_multi = ROOT.TMultiGraph('gr_multi','')
    gr_multi.Add(gr,'AP')
    gr_multi.Add(gr_m,'AP')
    c.SetGrid()
    min, max = 0.0001, 0.25
    c.DrawFrame(min,min,max,max)
    gr_multi.Draw()
    gr_multi.GetXaxis().SetTitleOffset(1.3)
    gr_multi.GetYaxis().SetTitleOffset(1.3)
    if sector == 'm':
        gr_multi.GetXaxis().SetTitle("#xi(p)"+"^{-}")
        gr_multi.GetYaxis().SetTitle("#xi(#gamma#gamma)"+"^{-}")
    elif sector == 'p':
        gr_multi.GetXaxis().SetTitle("#xi(p)"+"^{+}")
        gr_multi.GetYaxis().SetTitle("#xi(#gamma#gamma)"+"^{+}")
    
    # Draw y = x line
    l = TLine(min, min, max, max)
    l.SetLineStyle(2)
    l.SetLineWidth(2)
    l.Draw()

    # Draw shaded region for no acceptance
    b = TBox(min, min, 0.015, max)
    b.SetFillStyle(3001)
    b.SetFillColor(ROOT.kGray)
    b.SetLineColor(1)
    b.Draw()

    # Make legend
    legend = TLegend(0.65,0.45,0.8,0.6)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.038)
    legend.AddEntry(b,"No acceptance",'f')
    legend.AddEntry(gr,"Not matching",'p')
    legend.AddEntry(gr_m,"Matching at 2#sigma",'p')
    legend.Draw()

    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel("Tight #xi selection"), lumiLabel()
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    #c.SaveAs("plots/matching/xi"+sector+"_matching_"+s_years+".pdf")
    c.SaveAs("plots/matching/xi%s_matching_%s.%s" % (sector,s_years,extension))

def oneDim_matching(blinded):
    c1 = Canvas("c1")
    c2 = Canvas("c2")

    h_mass = ROOT.TH1F('h_mass', '', 40, -20, 20)
    h_rap = ROOT.TH1F('h_rap', '', 40, -20, 20)
    x, y = ROOT.Double(0), ROOT.Double(0)
    for i, year in enumerate(years):
        g = getGraph(year)
        for j in range(g.GetN()):
            g.GetPoint(j,x,y)
            ex = g.GetErrorX(j)
            ey = g.GetErrorY(j)
            h_mass.Fill(x)
            h_rap.Fill(y)

    c1.cd()
    c1.SetTicks(1,1)
    h_mass.GetXaxis().SetTitle('(m_{pp}-m_{#gamma#gamma})/#sigma(m_{pp}-m_{#gamma#gamma}}')
    h_mass.GetYaxis().SetTitle('Events')
    h_mass.SetMarkerStyle(24)
    h_mass.SetLineColor( ROOT.kBlack )
    h_mass.Sumw2()
    min, max = h_mass.GetMinimum(), h_mass.GetMaximum()+3
    h_mass.SetMaximum(max)
    h_mass.Draw('p')
    '''
    l1 = TLine(-2,h_mass.GetMinimum(),-2,max)
    l1.SetLineColor( ROOT.kRed+1 )
    l1.SetLineStyle(2)
    l1.SetLineWidth(2)
    l2 = TLine(2,h_mass.GetMinimum(),2,max)
    l2.SetLineColor( ROOT.kRed+1 )
    l2.SetLineStyle(2)
    l2.SetLineWidth(2)
    l3 = TLine(-3,h_mass.GetMinimum(),-3,max)
    l3.SetLineColor( ROOT.kRed+1 )
    l3.SetLineStyle(1)
    l3.SetLineWidth(2)
    l4 = TLine(3,h_mass.GetMinimum(),3,max)
    l4.SetLineColor( ROOT.kRed+1 )
    l4.SetLineStyle(1)
    l4.SetLineWidth(2)
    '''
    b2 = TBox(-3, min, 3, max-0.05)
    if not blinded: b2.SetFillStyle(3001) # transparent
    b2.SetFillColor(5)
    b2.SetLineColor(1)
    b2.Draw()
    b1 = TBox(-2, min, 2, max-0.05)
    if not blinded: b1.SetFillStyle(3001) # transparent
    b1.SetFillColor(3)
    b1.SetLineColor(1)
    b1.Draw()
    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel("#xi^{#pm}_{#gamma#gamma} #in PPS"), lumiLabel()
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    legend = TLegend(0.7,0.8,0.9,0.9)
    legend.AddEntry(b1,"2#sigma matching",'f')
    legend.AddEntry(b2,"3#sigma matching",'f')
    legend.Draw()
    c1.SaveAs('plots/matching/h_mass_1d.%s' % extension)
    c2.cd()
    c2.SetTicks(1,1)
    h_rap.GetXaxis().SetTitle('(y_{pp}-y_{#gamma#gamma})/#sigma(y_{pp}-y_{#gamma#gamma}}')
    h_rap.GetYaxis().SetTitle('Events')
    h_rap.SetMarkerStyle(24)
    h_rap.SetLineColor( ROOT.kBlack )
    h_rap.Sumw2()
    h_rap.SetMaximum(max)
    h_rap.Draw('p')
    b2.Draw()
    b1.Draw()
    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel("#xi^{#pm}_{#gamma#gamma} #in PPS"), lumiLabel()
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    legend = TLegend(0.7,0.8,0.9,0.9)
    legend.AddEntry(b1,"2#sigma matching",'f')
    legend.AddEntry(b2,"3#sigma matching",'f')
    legend.Draw()
    c2.SaveAs('plots/matching/h_rap_1d.%s' % extension)

    

#------------------------------------------------

massrap_matching(False)

#oneDim_matching(True)

#xi_matching('m')
#xi_matching('p')


'''
# Make hit map of matching
h2_matching = ROOT.TH2F( 'h2_matching', '', 100, -20, 20, 100, -20, 20 )
gr = file.Get('plots/gr_matching')
x,y = ROOT.Double(0), ROOT.Double(0)
for i in range( gr.GetN() ):
    gr.GetPoint(i,x,y)
    h2_matching.Fill(x,y)
h2_matching.GetXaxis().SetTitle("(m_{pp}-m_{#gamma#gamma})/#sigma(m_{pp}-m_{#gamma#gamma})")
h2_matching.GetYaxis().SetTitle("(y_{pp} - y_{#gamma#gamma})/#sigma(y_{pp} - y_{#gamma#gamma})")
c = Canvas('c')
c.cd()
h2_matching.Draw('colz')
c.SaveAs('reverse_matching_2d.png')

# Make xi matching 2d hists
h2_xim = ROOT.TH2F( 'h2_xim', '', 100, 0, 0.2, 100, 0, 0.2 )
h2_xip = ROOT.TH2F( 'h2_xip', '', 100, 0, 0.2, 100, 0, 0.2 )

gr_xim = file.Get('plots/gr_xim_matching')
gr_xip = file.Get('plots/gr_xim_matching')

for i in range( gr_xim.GetN() ):
    gr_xim.GetPoint(i,x,y)
    h2_xim.Fill(x,y)

for i in range( gr_xip.GetN() ):
    gr_xip.GetPoint(i,x,y)
    h2_xip.Fill(x,y)

h2_xim.GetXaxis().SetTitle('PPS #xi^{-}')
h2_xim.GetYaxis().SetTitle('CMS #xi^{-}')
h2_xip.GetXaxis().SetTitle('PPS #xi^{+}')
h2_xip.GetYaxis().SetTitle('CMS #xi^{+}')

c1 = Canvas('c1')
c1.cd()
h2_xim.Draw('colz')
c1.SaveAs('reverse_xim_matching_2d.png')

c2 = Canvas('c2')
c2.cd()
h2_xip.Draw('colz')
c2.SaveAs('reverse_xip_matching_2d.png')
'''
