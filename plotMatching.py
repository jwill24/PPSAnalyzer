#!/usr/bin/env python
import os, sys
from itertools import combinations
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TAttText, TLine, TLegend, TBox, TColor, TGraphErrors
from ROOT import gROOT


file = TFile( "outputHists/2017/histOut_data_Xi_2017.root" )
#file = TFile( "outputHists/2017/histOut_data_XipuUp_2017.root" )
file.ls() 


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
    

def massrap_matching(blinded):
    c = Canvas("c")
    c.cd()

    gr_matching = file.Get("plots/gr_matching")
    gr_matching.SetLineColor(ROOT.kBlack)
    gr_matching.SetTitle('')
    gr_matching.GetXaxis().SetTitle("(m_{pp}-m_{#gamma#gamma})/#sigma(m_{pp}-m_{#gamma#gamma})")
    gr_matching.GetYaxis().SetTitle("(y_{pp} - y_{#gamma#gamma})/#sigma(y_{pp} - y_{#gamma#gamma})")
    gr_matching.GetXaxis().SetLimits(-20,20)
    gr_matching.GetYaxis().SetRangeUser(-20,20)
    gr_matching.SetMarkerSize(0.5)
    gr_matching.SetMarkerStyle(24)
    gr_matching.Draw("AP")

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
    legend.Draw()
    c.Update() 
    pLabel = prelimLabel()
    pLabel.Draw()
    sLabel = selectionLabel("Tight #xi selection")
    sLabel.Draw()
    lLabel = lumiLabel()
    lLabel.Draw()
    c.SaveAs("plots/matching/massrap_matching.png")


def xi_matching(sector):
    c = Canvas("c")
    c.cd()

    gr_xi_matching = file.Get("plots/gr_xi"+sector+"_matching")
    ymax = gr_xi_matching.GetYaxis().GetXmax()
    gr_xi_matching.GetXaxis().SetLimits(0,0.25)
    gr_xi_matching.GetYaxis().SetRangeUser(0,ymax)
    gr_xi_matching.SetLineColor(ROOT.kBlack)
    gr_xi_matching.SetTitle('')
    if sector == 'm':
        gr_xi_matching.GetXaxis().SetTitle("#xi(p)"+"^{-}")
        gr_xi_matching.GetYaxis().SetTitle("#xi(#gamma#gamma)"+"^{-}")
    elif sector == 'p':
        gr_xi_matching.GetXaxis().SetTitle("#xi(p)"+"^{+}")
        gr_xi_matching.GetYaxis().SetTitle("#xi(#gamma#gamma)"+"^{+}")
    gr_xi_matching.GetXaxis().SetTitleOffset(1.5)
    gr_xi_matching.GetYaxis().SetTitleOffset(1.5)
    gr_xi_matching.SetMarkerSize(0.6)
    gr_xi_matching.SetMarkerStyle(24)
    gr_xi_matching.Draw("AP")


    # Draw y = x line
    l = TLine(0, 0, 0.25, ymax)
    l.SetLineStyle(2)
    l.SetLineWidth(2)
    l.Draw()

    # Draw shaded region for no acceptance
    b = TBox(0, 0, 0.015, ymax)
    b.SetFillStyle(3001)
    b.SetFillColor(ROOT.kGray)
    b.SetLineColor(1)
    b.Draw()

    pLabel, sLabel, lLabel = prelimLabel(), selectionLabel("Tight #xi selection"), lumiLabel()
    pLabel.Draw(), sLabel.Draw(), lLabel.Draw()
    c.SaveAs("plots/matching/xi"+sector+"_matching.png")

#------------------------------------------------

massrap_matching(False)

xi_matching('m')
xi_matching('p')

