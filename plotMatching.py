#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, TGraphErrors
from ROOT import gROOT


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
    #txt.SetTextAlign(1+10)
    return txt

def topLabel(text):
    lab = PaveText( 0.1, 0.9, 0.18, 0.92, 'NB NDC' )
    #lab.SetTextAlign( 1+10 )
    #lab.SetTextFont( 52 )
    lab.AddText( text )
    #lab.Draw( "same" )
    lab.Draw()
    return lab

def prelimLabel():
    #label = TPaveText(0.07,0.74,.50,0.91)
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
    label = TPaveText(0.08, 0.88, .6, 0.95, 'NB NDC' )
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
    #label = TPaveText(1.48,0.92,1.98,1.14)
    label = TPaveText( 0.7, 0.88, 0.8, 0.93, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( "37.19 fb^{-1} (13 TeV)" )
    label.SetTextSize( 0.033 )
    label.SetTextAlign(11)
    label.SetTextFont( 42 )
    label.SetTextColor( 1 )
    return label
    

#file = TFile( "histOut_matching.root" )
file = TFile( "outputHists/histOut_data_XipuUp_2017.root" )
file.ls() 


c2 = Canvas("c2")
c2.cd()

gr_matching = file.Get("plots/gr_matching")

#print 'Entries:', gr_matching.GetN()
#for point in range(0,gr_matching.GetN()):
    #print 'Error:', gr_matching.GetErrorX( point )


gr_matching.SetLineColor(ROOT.kBlack)
gr_matching.SetTitle('')
#gr_matching.GetXaxis().SetTitle("m_{pp}/m_{#gamma#gamma}")
gr_matching.GetXaxis().SetTitle("(m_{pp}-m_{#gamma#gamma})/#sigma(m_{pp}-m_{#gamma#gamma})")
#gr_matching.GetYaxis().SetTitle("y_{pp} - y_{#gamma#gamma}")
gr_matching.GetYaxis().SetTitle("(y_{pp} - y_{#gamma#gamma})/#sigma(y_{pp} - y_{#gamma#gamma})")
#gr_matching.GetXaxis().SetLimits(0.,2.)
gr_matching.GetXaxis().SetLimits(-20,20)
#gr_matching.GetYaxis().SetRangeUser(-1.,1.)
gr_matching.GetYaxis().SetRangeUser(-20,20)
gr_matching.SetMarkerSize(0.5)
gr_matching.SetMarkerStyle(24)
gr_matching.Draw("AP")

#b2 = TBox(.8, -.15, 1.2, .15)
b2 = TBox(-3, -3, 3, 3)
#b2.SetFillStyle(3001) # transparent
b2.SetFillColor(5)
b2.SetLineColor(1)
b2.Draw()
#b1 = TBox(.9, -.1, 1.1, .1)
b1 = TBox(-2, -2, 2, 2)
#b1.SetFillStyle(3001) # transparent
b1.SetFillColor(3) 
b1.SetLineColor(1)
b1.Draw()
legend = TLegend(0.7,0.8,0.9,0.9)
legend.AddEntry(b1,"2#sigma matching",'f')
legend.AddEntry(b2,"3#sigma matching",'f')
legend.Draw()
c2.Update() 
pLabel = prelimLabel()
pLabel.Draw()
sLabel = selectionLabel("Tight #xi selection")
sLabel.Draw()
lLabel = lumiLabel()
lLabel.Draw()
c2.SaveAs("matching.png")






