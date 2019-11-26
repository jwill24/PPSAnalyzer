#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor
from ROOT import gROOT

#gROOT.LoadMacro("tdrstyle.C")
#gROOT.ProcessLine("setTDRStyle();")
#gROOT.LoadMacro("CMS_lumi.C")
#gROOT.ProcessLine("CMS_lumi(c1);")

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
    lab = PaveText( 0.135, 0.95, 0.2, 0.96 )
    #lab.SetTextAlign( 1+10 )
    #lab.SetTextFont( 52 )
    lab.AddText( text )
    #lab.Draw( "same" )
    lab.Draw()
    return lab

def prelimLabel():
    label = TPaveText(0.07,0.74,.50,0.91)
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
    label = TPaveText(-.02,0.93,.6,1.13)
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
    label = TPaveText(1.48,0.92,1.98,1.14)
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
    

file = TFile( "histOut_matching.root" )
file.ls() 

#-----------------------------------
#c1 = Canvas("c1")
#c1.cd()

#h_diph_mass = file.Get("plots/h_diph_mass")
#h_diph_mass.Draw()
#topLabel("CMS Preliminary")
#c1.SaveAs("h_diphoton_mass.png")


#-----------------------------------
c2 = Canvas("c2")
c2.cd()

gr_matching = file.Get("plots/gr_matching")
gr_matching.GetXaxis().SetTitle("m_{pp}/m_{#gamma#gamma}")
gr_matching.GetYaxis().SetTitle("y_{pp} - y_{#gamma#gamma}")
gr_matching.Draw("AP")
gr_matching.GetXaxis().SetLimits(0.,2.)
gr_matching.GetYaxis().SetRangeUser(-1.,1.)
gr_matching.SetMarkerSize(0.5)
gr_matching.SetMarkerStyle(24)
gr_matching.Draw("AP")
#l1 = TLine(.9,-.1,.9,.1)
#l2 = TLine(1.1,-.1,1.1,.1)
#l3 = TLine(.9,-.1,1.1,-.1)
#l4 = TLine(.9,.1,1.1,.1)
#l1.SetLineColor(2)
#l2.SetLineColor(2)
#l3.SetLineColor(2)
#l4.SetLineColor(2)
#l1.Draw()
#l2.Draw()
#l3.Draw()
#l4.Draw()
#l5 = TLine(.8,-.15,.8,.15)
#l6 = TLine(1.2,-.15,1.2,.15)
#l7 = TLine(.8,-.15,1.2,-.15)
#l8 = TLine(.8,.15,1.2,.15)
#l5.SetLineColor(4)
#l6.SetLineColor(4)
#l7.SetLineColor(4)
#l8.SetLineColor(4)
#l5.Draw()
#l6.Draw()
#l7.Draw()
#l8.Draw()
b2 = TBox(.8, -.15, 1.2, .15)
b2.SetFillColor(5) #207
b2.SetLineColor(1)
b2.Draw()
b1 = TBox(.9, -.1, 1.1, .1)
b1.SetFillColor(3) #63
b1.SetLineColor(1)
b1.Draw()
legend = TLegend(0.7,0.8,0.9,0.9)
legend.AddEntry(b1,"2#sigma matching",'l')
legend.AddEntry(b2,"3#sigma matching",'l')
legend.Draw()
c2.Update() 
pLabel = prelimLabel()
pLabel.Draw()
sLabel = selectionLabel("Elastic selection")
sLabel.Draw()
lLabel = lumiLabel()
lLabel.Draw()
c2.SaveAs("matching.png")






