#!/Usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, THStack, TGaxis, TH1F
from ROOT import gROOT, gStyle
from common import sampleColors, Canvas, Prettify, lumiLabel, asym_error_bars

gStyle.SetOptStat(0)

#selections = [['HLT','After HLT'], ['Preselection','Preselection'], ['ID', 'Preselc. + ID'], ['ReverseElastic','Reverse'], ['Elastic','Diphoton selection'], ['Xi', 'Tight #xi']]
selections = [['ID','Preselection'], ['Elastic','Elastic selection'], ['Xi', '#xi_{#gamma#gamma}^{#pm} #in PPS']]
#selections = [['HLT','After HLT'], ['Elastic','Diphoton selection'], ['Xi', '#xi_{#gamma#gamma}^{#pm} #in PPS']]
#selections = [['Elastic','Diphoton selection'], ['Xi', '#xi_{#gamma#gamma}^{#pm} #in PPS']]
years = ['2017','2018']
#years = ['2017']
s_years = '+'.join(years)
#scale2018 = 55.72/37.2

h_data =  ROOT.TH1F('h_data', '', len(selections), 0, len(selections))
h_ggj =   ROOT.TH1F('h_ggj', '', len(selections), 0, len(selections))
h_gj =    ROOT.TH1F('h_gj', '', len(selections), 0, len(selections))
h_qcd =   ROOT.TH1F('h_qcd', '', len(selections), 0, len(selections))
h_wg =    ROOT.TH1F('h_wg', '', len(selections), 0, len(selections))
h_zg =    ROOT.TH1F('h_zg', '', len(selections), 0, len(selections))
h_tt =    ROOT.TH1F('h_tt', '', len(selections), 0, len(selections))
h_aqgc =  ROOT.TH1F('h_aqgc', '', len(selections), 0, len(selections))
h_errors = ROOT.TH1F('h_errors', '', len(selections), 0, len(selections))
h_stack = ROOT.THStack('norm_stack','')
vec = [h_tt, h_zg, h_wg, h_gj, h_ggj, h_qcd]

bgs = sampleColors()
for i, bg in enumerate(bgs): bg.insert(1,vec[i]) 
v_hist = []



def prelimLabel():
    label = TPaveText( 0.1, 0.91, 0.2, 0.93, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.SetTextAlign(11)
    label.AddText( "#font[62]{CMS} #font[52]{Preliminary}" )
    label.SetTextSize(0.048)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

def setPlot(h, fill, line): 
    h.Sumw2()
    h.SetTitle('')
    h.SetFillColor(fill)
    h.SetLineColor(line)    
    h.SetLineWidth(2)
    return h

def makeLegend(h1,v_hist,hs):
    legend = TLegend(0.52, 0.55, 0.69, 0.85)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.040)
    legend.AddEntry(h1,'Data', 'lp')
    backgrounds = ['t#bar{t} + j (NLO)', 'Incl. Z + #gamma (NLO)', 'Incl. W + #gamma (NLO)', '#gamma + j', 'Incl. #gamma#gamma + j (NLO)', 'QCD (e#gamma enriched)']
    for i in range( len(backgrounds) ):
        legend.AddEntry(v_hist[i],backgrounds[i],'f')
    legend.AddEntry(hs,'AQGC #times 100','l')
    return legend

for selection in selections:

    #print 'Selection:', selection[0]

    for i, year in enumerate(years): 
        dataFile = TFile('outputHists/'+year+'/histOut_data'+year+'_'+selection[0]+'.root') 
        aqgcFile = TFile('outputHists/'+'2017'+'/histOut_aqgc'+'2017'+'_'+selection[0]+'.root') # FIXME: waiting on 2018 samples

        thisBin = selections.index(selection)+1

        #print 'data'+year, 'Events:', dataFile.Get('plots/h_diph_mass').Integral()
        
        if i == 0:
            h_data.SetBinContent( thisBin, dataFile.Get('plots/h_diph_mass').Integral() )
            h_aqgc.SetBinContent( thisBin, aqgcFile.Get('plots/h_diph_mass').Integral() )
        else:
            h_data.SetBinContent( thisBin, h_data.GetBinContent(thisBin)+dataFile.Get('plots/h_num_pho').Integral() )
            h_aqgc.SetBinContent( thisBin, h_aqgc.GetBinContent(thisBin)+aqgcFile.Get('plots/h_num_pho').Integral() )

        for bg in bgs:

            f = TFile('outputHists/'+year+'/histOut_'+str(bg[0])+year+'_'+selection[0]+'.root') 
            hist = f.Get('plots/h_diph_mass')
            
            errors = []
            for i in range(100): errors.append( math.pow( hist.GetBinError(i), 2 ) )
            error = math.sqrt( sum(errors) )
            h_errors.SetBinContent( thisBin, h_errors.GetBinContent(thisBin)+error ) 
            print 'MC:', bg[0]+year, 'Events:', hist.Integral(), 'Error:', error


            if i == 0: bg[1].SetBinContent( thisBin, hist.Integral() )
            else: bg[1].SetBinContent( thisBin, bg[1].GetBinContent(thisBin)+hist.Integral() )


h_mc_err = 0
for bg in bgs:
    setPlot(bg[1], bg[2], bg[3])
    h_stack.Add(bg[1])
    v_hist.append(bg[1])
    if h_mc_err == 0: h_mc_err = bg[1].Clone()
    else: h_mc_err.Add(bg[1])

# print totals
for s in selections: print 'Selection:', s[0], 'Data:', h_data.GetBinContent(selections.index(s)+1), 'Total MC:', h_stack.GetStack().Last().GetBinContent(selections.index(s)+1), 'Error:', h_errors.GetBinContent(selections.index(s)+1) 

c = Canvas('c')

h_sum = TH1F('h_sum','sum',h_data.GetNbinsX(), h_data.GetXaxis().GetXmin(), h_data.GetXaxis().GetXmax())
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
pad1.SetLogy()
h_stack.Draw('HIST')

h_mc_err.Draw("e2 same")
h_mc_err.SetMarkerSize(0)
h_mc_err.SetFillColor(1)
h_mc_err.SetFillStyle(3004)

#h_stack.GetHistogram().GetYaxis().SetTitleFont(43)
#h_stack.GetHistogram().GetYaxis().SetTitleOffset(1.0)
h_stack.GetHistogram().GetYaxis().SetTitleSize(0.05) 
h_stack.GetHistogram().GetYaxis().SetTitle('Events') 
#h_stack.SetMaximum( h_data.GetMaximum()*5 )
h_stack.SetMaximum( h_stack.GetMaximum()*50 )
h_stack.SetMinimum(1)
h_asym_data = asym_error_bars(h_data) 
h_asym_data.SetMarkerStyle(20)
h_asym_data.SetMarkerSize(0.9)
h_asym_data.GetXaxis().SetTitle('Events')
h_asym_data.GetXaxis().SetTitleSize(26)
h_asym_data.Draw('p e2 same') # testing e2
h_aqgc.SetLineColor(92), h_aqgc.SetLineWidth(2), h_aqgc.SetFillColor(0), h_aqgc.Scale(100) if year == '2017' else h_aqgc.Scale(100*94.91/37.2) # FIXME
h_aqgc.Draw('HIST same')
lLabel, pLabel = lumiLabel(True,years), prelimLabel()
lLabel.Draw(), pLabel.Draw()
leg = makeLegend(h_asym_data,v_hist,h_aqgc)
leg.Draw()

pad2.cd()
h_ratio = h_data.Clone('h_ratio')
h_ratio.Sumw2()
h_ratio.Divide(h_sum) 
h_ratio.SetMinimum(-0.4)
h_ratio.SetMaximum(2.4)
#h_ratio.SetMinimum(0.1)
#h_ratio.SetMaximum(1.9)
#h_ratio.GetYaxis().SetTickLength(0.5)
h_ratio.SetMarkerStyle(20)
h_ratio.SetMarkerSize(0.9)
h_ratio.SetLineColor(ROOT.kBlack)
h_ratio.Draw('p same')
for i in range( len(selections) ): h_ratio.GetXaxis().SetBinLabel(i+1,selections[i][1])
denom_err, denom_err2 = h_mc_err.Clone(), h_mc_err.Clone()
denom_err2.Sumw2(False)
denom_err.Divide(denom_err2)
denom_err.Draw("e2 same")
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

c.SaveAs('cutflow_'+s_years+'.png')
c.SaveAs('cutflow_'+s_years+'.pdf')
