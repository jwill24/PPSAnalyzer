#!/usr/bin/env python                                                                                                                                                               
import os, sys
import math, random
import numpy as np
#import matplotlib.pyplot as plt
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, gStyle
from ROOT import TFile, TTree, AddressOf, TGraphErrors, TCanvas, TBox, TLegend, TPaveText, TH2F, TH1F

gStyle.SetOptStat(0)

gROOT.ProcessLine(
"struct diphStruct {\
   Float_t   mass;\
   Float_t   rap;\
   Float_t   xim;\
   Float_t   xip;\
   Long64_t  xangle;\
   Char_t    era[5];\
};");

gROOT.ProcessLine(
"struct proStruct {\
   Int_t    num_m;\
   Int_t    num_p;\
   Float_t  xim[12];\
   Float_t  xip[12];\
};");

from ROOT import diphStruct, proStruct
diph_struct = diphStruct()
pro_struct  = proStruct()


# Flags
experiments = 5     # number of iterations
plotting = True     # make matching plot for each experiment
testing  = False    # only run over a few events
test_events = 10    # number of events to use for testing
method = 'singleRP' # singleRP or multiRP reconstruction


diphoton_file = TFile( 'diphotonEvents_'+method+'.root' )
proton_file = TFile( 'protonEvents_'+method+'.root' )


diphoton_tree = diphoton_file.Get( 'tree' )
diphoton_tree.SetBranchAddress('mass', AddressOf( diph_struct, 'mass'))
diphoton_tree.SetBranchAddress('rap', AddressOf( diph_struct, 'rap'))
diphoton_tree.SetBranchAddress('xim', AddressOf( diph_struct, 'xim'))
diphoton_tree.SetBranchAddress('xip', AddressOf( diph_struct, 'xip'))
diphoton_tree.SetBranchAddress('xangle', AddressOf( diph_struct, 'xangle'))
diphoton_tree.SetBranchAddress('era', AddressOf( diph_struct, 'era'))

tree_B_120 = proton_file.Get( 'tree_B_120' )
tree_B_120.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_B_120.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_B_120.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_B_120.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_B_130 = proton_file.Get( 'tree_B_130' )
tree_B_130.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_B_130.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_B_130.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_B_130.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_B_140 = proton_file.Get( 'tree_B_140' )
tree_B_140.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_B_140.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_B_140.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_B_140.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_B_150 = proton_file.Get( 'tree_B_150' )
tree_B_150.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_B_150.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_B_150.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_B_150.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))

tree_C_120 = proton_file.Get( 'tree_C_120' )
tree_C_120.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_C_120.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_C_120.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_C_120.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_C_130 = proton_file.Get( 'tree_C_130' )
tree_C_130.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_C_130.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_C_130.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_C_130.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_C_140 = proton_file.Get( 'tree_C_140' )
tree_C_140.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_C_140.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_C_140.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_C_140.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_C_150 = proton_file.Get( 'tree_C_150' )
tree_C_150.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_C_150.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_C_150.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_C_150.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))

tree_D_120 = proton_file.Get( 'tree_D_120' )
tree_D_120.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_D_120.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_D_120.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_D_120.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_D_130 = proton_file.Get( 'tree_D_130' )
tree_D_130.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_D_130.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_D_130.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_D_130.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_D_140 = proton_file.Get( 'tree_D_140' )
tree_D_140.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_D_140.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_D_140.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_D_140.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_D_150 = proton_file.Get( 'tree_D_150' )
tree_D_150.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_D_150.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_D_150.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_D_150.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))

tree_E_120 = proton_file.Get( 'tree_E_120' )
tree_E_120.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_E_120.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_E_120.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_E_120.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_E_130 = proton_file.Get( 'tree_E_130' )
tree_E_130.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_E_130.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_E_130.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_E_130.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_E_140 = proton_file.Get( 'tree_E_140' )
tree_E_140.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_E_140.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_E_140.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_E_140.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_E_150 = proton_file.Get( 'tree_E_150' )
tree_E_150.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_E_150.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_E_150.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_E_150.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))

tree_F_120 = proton_file.Get( 'tree_F_120' )
tree_F_120.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_F_120.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_F_120.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_F_120.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_F_130 = proton_file.Get( 'tree_F_130' )
tree_F_130.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_F_130.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_F_130.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_F_130.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_F_140 = proton_file.Get( 'tree_F_140' )
tree_F_140.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_F_140.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_F_140.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_F_140.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))
tree_F_150 = proton_file.Get( 'tree_F_150' )
tree_F_150.SetBranchAddress('num_m', AddressOf( pro_struct, 'num_m'))
tree_F_150.SetBranchAddress('num_p', AddressOf( pro_struct, 'num_p'))
tree_F_150.SetBranchAddress('xim', AddressOf( pro_struct, 'xim'))
tree_F_150.SetBranchAddress('xip', AddressOf( pro_struct, 'xip'))

gr_estimate = TGraphErrors('gr_estimate')
h2_estimate = TH2F( 'h2_estimate', '', 100, -20, 20, 100, -20, 20)
h2_xim = TH2F( 'h2_xim', '', 100, 0, 0.2, 100, 0, 0.2 )
h2_xip = TH2F( 'h2_xip', '', 100, 0, 0.2, 100, 0, 0.2 )

h_xip = TH1F('h_xip', '#xi ^{+}', 100, 0., 0.25)
h_xim = TH1F('h_xim', '#xi ^{-}', 100, 0., 0.25)

#----------------------------------

def find_nearest(array, value):
    if len(array) == 0: return -1
    #array = np.asarray(array)
    #idx = (np.abs(array - value)).argmin()
    #return array[idx]
    return min(array, key=lambda x:abs(x-value))

#----------------------------------

def getMass(xim,xip):
    if xim < 0 or xip < 0: return -1
    else: return 13000 * math.sqrt(xim*xip)

#----------------------------------

def getRap(xip,xim):
    if xim < 0 or xip < 0: return -999
    else: return 0.5*math.log(xim/xip)

#----------------------------------

def rapidity_err(xim,xip):
    rel_xi_err = 0.08
    xim_err, xip_err = xim * rel_xi_err, xip * rel_xi_err
    return 0.5 * math.sqrt( pow(xim_err/xim,2) + pow(xip_err/xip,2) )

#----------------------------------

def isMatching(cms_mass,cms_rap,pro_xim,pro_xip):
    pps_mass, pps_rap = getMass(pro_xim,pro_xip), getRap(pro_xim,pro_xip)
    if pps_mass == -1: return 999, 999
    pps_rap_err = rapidity_err(pro_xim,pro_xip)
    pps_mass_err = pps_mass * pps_rap_err
    rel_mass_err, rel_rap_err = 0.02, 0.074
    mass_point = (pps_mass - cms_mass) / (pps_mass_err + cms_mass*rel_mass_err)
    rap_point = (pps_rap - cms_rap) / (pps_rap_err + rel_rap_err*cms_rap)
    return mass_point, rap_point

#----------------------------------

def getAverage(v):
    return float( sum(v) ) / float( len(v) )

#----------------------------------

def plot_estimate(gr,name):
    c = TCanvas('c','',750,600)
    c.cd()
    
    gr.SetLineColor(ROOT.kBlack)
    gr.SetTitle('')
    gr.GetXaxis().SetTitle("(m_{pp}-m_{#gamma#gamma})/#sigma(m_{pp}-m_{#gamma#gamma})")
    gr.GetYaxis().SetTitle("(y_{pp} - y_{#gamma#gamma})/#sigma(y_{pp} - y_{#gamma#gamma})")
    gr.GetXaxis().SetLimits(-20,20)
    gr.GetYaxis().SetRangeUser(-20,20)
    gr.SetMarkerSize(0.5)
    gr.SetMarkerStyle(24)
    gr.Draw("AP")
    
    b2 = TBox(-3, -3, 3, 3)
    b2.SetFillStyle(3001) # transparent
    b2.SetFillColor(5)
    b2.SetLineColor(1)
    b2.Draw()
    b1 = TBox(-2, -2, 2, 2)
    b1.SetFillStyle(3001) # transparent
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
    sLabel = selectionLabel('Background Estimation ('+method+')')
    sLabel.Draw()
    lLabel = lumiLabel()
    lLabel.Draw()
    c.SaveAs(name)

#----------------------------------

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

#----------------------------------

def selectionLabel(text):
    label = TPaveText(0.08, 0.88, .6, 0.95, 'NB NDC' )
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetLineWidth(0)
    label.SetLineStyle(0)
    label.AddText( text )
    label.SetTextSize( 0.03 )
    label.SetTextAlign(11)
    label.SetTextFont( 52 )
    label.SetTextColor( 1 )
    return label

#----------------------------------

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

#----------------------------------

entries = diphoton_tree.GetEntries()
if testing: entries, experiments = test_events, 1

v_count, v_20sig, v_3sig, v_2sig = [], [], [], []

for e in range(experiments):

    count, matching_2sig, matching_3sig, matching_20sig = 0, 0, 0, 0
    gr_estimate.Set(0)

    for i in range(entries):
        diphoton_tree.GetEntry(i)

        #print 'i:', i, 'era:', diph_struct.era, 'xangle:', diph_struct.xangle
        v_xim, v_xip = [], []
    
        # Get entry by era and xangle
        if diph_struct.era == '2017B':
            if diph_struct.xangle == 120: tree_B_120.GetEntry( random.randrange(0,tree_B_120.GetEntries()) )        
            if diph_struct.xangle == 130: tree_B_130.GetEntry( random.randrange(0,tree_B_130.GetEntries()) )        
            if diph_struct.xangle == 140: tree_B_140.GetEntry( random.randrange(0,tree_B_140.GetEntries()) )        
            if diph_struct.xangle == 150: tree_B_150.GetEntry( random.randrange(0,tree_B_150.GetEntries()) )        
        elif diph_struct.era == '2017C':
            if diph_struct.xangle == 120: tree_C_120.GetEntry( random.randrange(0,tree_C_120.GetEntries()) )        
            if diph_struct.xangle == 130: tree_C_130.GetEntry( random.randrange(0,tree_C_130.GetEntries()) )        
            if diph_struct.xangle == 140: tree_C_140.GetEntry( random.randrange(0,tree_C_140.GetEntries()) )        
            if diph_struct.xangle == 150: tree_C_150.GetEntry( random.randrange(0,tree_C_150.GetEntries()) )        
        elif diph_struct.era == '2017D':
            if diph_struct.xangle == 120: tree_D_120.GetEntry( random.randrange(0,tree_D_120.GetEntries()) )        
            if diph_struct.xangle == 130: tree_D_130.GetEntry( random.randrange(0,tree_D_130.GetEntries()) )        
            if diph_struct.xangle == 140: tree_D_140.GetEntry( random.randrange(0,tree_D_140.GetEntries()) )        
            if diph_struct.xangle == 150: tree_D_150.GetEntry( random.randrange(0,tree_D_150.GetEntries()) )        
        elif diph_struct.era == '2017E':
            if diph_struct.xangle == 120: tree_E_120.GetEntry( random.randrange(0,tree_E_120.GetEntries()) )        
            if diph_struct.xangle == 130: tree_E_130.GetEntry( random.randrange(0,tree_E_130.GetEntries()) )        
            if diph_struct.xangle == 140: tree_E_140.GetEntry( random.randrange(0,tree_E_140.GetEntries()) )        
            if diph_struct.xangle == 150: tree_E_150.GetEntry( random.randrange(0,tree_E_150.GetEntries()) )        
        elif diph_struct.era == '2017F':
            if diph_struct.xangle == 120: tree_F_120.GetEntry( random.randrange(0,tree_F_120.GetEntries()) )        
            if diph_struct.xangle == 130: tree_F_130.GetEntry( random.randrange(0,tree_F_130.GetEntries()) )        
            if diph_struct.xangle == 140: tree_F_140.GetEntry( random.randrange(0,tree_F_140.GetEntries()) )        
            if diph_struct.xangle == 150: tree_F_150.GetEntry( random.randrange(0,tree_F_150.GetEntries()) )        

        if pro_struct.num_m == 0 or pro_struct.num_p == 0: continue

        for j in range(pro_struct.num_m): v_xim.append( pro_struct.xim[j] )
        for j in range(pro_struct.num_p): v_xip.append( pro_struct.xip[j] )
        pro_xim, pro_xip = find_nearest(v_xim, diph_struct.xim), find_nearest(v_xip, diph_struct.xip) 
        
        #h_xip.Fill( pro_xip ), h_xim.Fill( pro_xim )
        #h2_xim.Fill( pro_xim, diph_struct.xim )
        #h2_xip.Fill( pro_xip, diph_struct.xip )

        # Check for matching
        mass_match, rap_match = isMatching(diph_struct.mass, diph_struct.rap, pro_xim, pro_xip)

        # Plot events
        if plotting: gr_estimate.SetPoint( gr_estimate.GetN(), mass_match, rap_match )
        #h2_estimate.Fill(mass_match, rap_match)

        count += 1
        if abs(mass_match) < 20 and abs(rap_match) < 20: matching_20sig += 1
        if abs(mass_match) < 3 and abs(rap_match) < 3: matching_3sig += 1
        if abs(mass_match) < 2 and abs(rap_match) < 2: matching_2sig += 1


    print 'Experiment number:', e, 'Number of 3-sigma matching:', matching_3sig, 'Number of 2-sigma matching:', matching_2sig
    v_20sig.append(matching_20sig), v_3sig.append(matching_3sig), v_2sig.append(matching_2sig), v_count.append(count)

    if plotting: plot_estimate( gr_estimate, 'background_estimate_%d.png' % e )

print ''
print ''
print 'Average matching ----> 20 sigma:', getAverage(v_20sig), '3 sigma:', getAverage(v_3sig), '2 sigma:', getAverage(v_2sig)
print 'Average num events:', getAverage(v_count)


# Plotting for cross checks
'''    
c = TCanvas('c','',750,600)
c.cd()
h2_estimate.GetXaxis().SetTitle("(m_{pp}-m_{#gamma#gamma})/#sigma(m_{pp}-m_{#gamma#gamma})")
h2_estimate.GetYaxis().SetTitle("(y_{pp} - y_{#gamma#gamma})/#sigma(y_{pp} - y_{#gamma#gamma})")
h2_estimate.Draw('colz')
c.SaveAs('h2_estimate.png')

c1 = TCanvas('c1','',750,600)
c1.cd()
h_xim.Draw()
c1.SaveAs('h_pro_xim.png')

c2 = TCanvas('c2','',750,600)
c2.cd()
h_xip.Draw()
c2.SaveAs('h_pro_xip.png')

c3 = TCanvas('c3', '', 750, 600)
c3.cd()
h2_xim.GetXaxis().SetTitle('PPS #xi^{-}')
h2_xim.GetYaxis().SetTitle('CMS #xi^{-}')
h2_xim.Draw('colz')
c3.SaveAs('h2_xim_matching.png')

c4 = TCanvas('c4', '', 750, 600)
c4.cd()
h2_xip.GetXaxis().SetTitle('PPS #xi^{-}')
h2_xip.GetYaxis().SetTitle('CMS #xi^{-}')
h2_xip.Draw('colz')
c4.SaveAs('h2_xip_matching.png')

c5 = TCanvas('c5', '2#sigma Matching', 740, 600)
c5.cd()
distribution_2sig = TH1F( 'distribution_2sig', '', 100, 0, 15)
for x in v_2sig:
    distribution_2sig.Fill(x)
distribution_2sig.GetYaxis().SetTitle('Experiments')
distribution_2sig.GetXaxis().SetTitle('Events matching')
distribution_2sig.Draw()
std = round( distribution_2sig.GetStdDev(), 3 )
std_label = TPaveText( 0.6, 0.8, 0.64, 0.87, 'NB NDC' )
std_label.SetFillStyle(0)
std_label.SetBorderSize(0)
std_label.SetLineWidth(0)
std_label.SetLineStyle(0)
std_label.SetTextAlign(11)
std_label.AddText( "Standard Deviation = " + str(std) )
std_label.SetTextSize(0.03)
std_label.SetTextFont( 42 )
std_label.SetTextColor( 1 )
std_label.Draw()
c5.SaveAs('2sigma_distribution.png')

'''

