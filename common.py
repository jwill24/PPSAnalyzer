#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import gROOT, gStyle, TColor, TCanvas, TPaveText, TLegend

lightBlue, red, yellow, purple, darkGreen, green = ROOT.kCyan-9, 208, ROOT.kYellow-9, 38, ROOT.kTeal+3, ROOT.kGreen-9

class Color(int):
    __slots__ = ["object", "name"]

    def __new__(cls, r, g, b, name=""):
        self = int.__new__(cls, TColor.GetFreeColorIndex())
        self.object = TColor(self, r, g, b, name, 1.0)
        self.name = name
        return self


def makeColors():
    colors = [Color(0.93, 0.67, 0.93, 'pink'),
              Color(0.886, 0.475, 0.886, 'darkPink'),
              Color(0.59, 0.59, 0.91, 'purple'),
              Color(0.59, 0.91, 0.91, 'lightBlue'),
              Color(0.91, 0.59, 0.59, 'red'),
              Color(0.99, 0.91, 0.59, 'yellow'),
              Color(0.91, 0.82, 0.15, 'gold'),
              Color(0.29, 0.64, 0.98, 'darkBlue'),
              Color(0.67, 0.83, 0.99, 'blue')]
    for color in colors: setattr(ROOT, color.name, color)
    return colors

def sampleColors():
    colors = makeColors()
    # Laurent's colors
    #samples = [['tt', ROOT.blue, ROOT.darkBlue],['zg', ROOT.lightBlue, ROOT.kCyan],['wg', ROOT.purple, 214],
    #           ['g+j',ROOT.yellow, ROOT.gold],['ggj', ROOT.red, 206],['qcd', ROOT.pink, ROOT.darkPink]]
    # My colors
    samples = [['tt', ROOT.kGreen-9, ROOT.kGreen-9],['zg', ROOT.kYellow-9, ROOT.kYellow-9],['wg', 38, 38],
               ['g+j',ROOT.kTeal+3, ROOT.kTeal+3],['ggj', 208, 208],['qcd', ROOT.kCyan-9, ROOT.kCyan-9]]
    return samples

def Canvas(name):
    c = TCanvas(name,'c',750,600)
    return c

def Prettify( hist ):
    x = hist.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4)
    x.SetLabelFont(43)
    x.SetLabelSize(18)
    x.SetTickLength(0.05)
    y = hist.GetYaxis()
    y.SetTitle('Data / MC')
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

def lumiLabel(ratio,years):
    label = TPaveText( 0.70, 0.9, 0.8, 0.92, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    if len(years) == 1 and years[0] == '2017': luminosity = '37.19'
    elif years[0] == '2018': luminosity = '55.72'
    elif len(years) == 2: luminosity = '92.91'
    label.AddText( luminosity+" fb^{-1} (13 TeV)" )
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
    backgrounds = ['t#bar{t} + j (NLO)', 'Incl. Z + #gamma', 'Incl. W + #gamma', '#gamma + j', 'Incl. #gamma#gamma + j\
 (NLO)', 'QCD (e#gamma enriched)']
    for i in range( len(backgrounds) ):
        legend.AddEntry(v_hist[i],backgrounds[i],'f')
    legend.AddEntry(hs,'AQGC #times 100','l')
    return legend

def asym_error_bars(hist):
    alpha = 1 - 0.6827
    g = ROOT.TGraphAsymmErrors(hist)
    for i in range(0,g.GetN()):
        N = g.GetY()[i]
        if N == 0: continue
        L = 0. if N == 0 else ( ROOT.Math.gamma_quantile( 0.5*alpha, N, 1. ) )
        U = ( ROOT.Math.gamma_quantile_c( alpha, N+1, 1 ) ) if N == 0 else ( ROOT.Math.gamma_quantile_c( 0.5*alpha, N+1, 1 ) )
        g.SetPointEXlow( i, 0. )
        g.SetPointEXhigh( i, 0. )
        g.SetPointEYlow( i, N-L )
        g.SetPointEYhigh( i, U-N )
    return g
