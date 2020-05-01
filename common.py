#!/usr/bin/env python
import os, sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import gROOT, gStyle, TColor, TCanvas, TPaveText, TLegend

lightBlue, red, yellow, purple, darkGreen, green = ROOT.kCyan-9, 208, ROOT.kYellow-9, 38, ROOT.kTeal+3, ROOT.kGreen-9
sqrts = 13000.0
rel_xi_err = 0.08

class Color(int):
    __slots__ = ["object", "name"]

    def __new__(cls, r, g, b, name=""):
        self = int.__new__(cls, TColor.GetFreeColorIndex())
        self.object = TColor(self, float(r)/float(255), float(g)/float(255), float(b)/float(255), name, 1.0)
        self.name = name
        return self


def makeColors():
    colors = [Color(166, 217, 217, 'aqua'),        # palette1
              Color(149, 196, 196, 'darkAqua'),    # palette1
              Color(110, 202, 202, 'teal'),        # palette1
              Color(99, 184, 184, 'darkTeal'),     # palette1
              Color(255, 179, 179, 'rose'),        # palette1
              Color(234, 161, 161, 'darkRose'),    # palette1
              Color(255, 209, 181, 'apricot'),     # palette1
              Color(233, 188, 163, 'darkApricot'), # palette1
              Color(255, 235, 186, 'sand'),        # palette1
              Color(232, 212, 167, 'darkSand'),    # palette1
              Color(171, 238, 199, 'seafoam'),     # palette1
              Color(154, 216, 179, 'darkSeafoam'), # palette1
              Color(36, 163, 163, 'turquois'),       # palette2
              Color(32, 149, 149, 'darkTurquois'),   # palette2
              Color(163, 209, 94, 'lime'),           # palette2
              Color(147, 190, 85, 'darkLime'),       # palette2
              Color(252, 222, 97, 'mustard'),        # palette2
              Color(232, 200, 87, 'darkMustard'),    # palette2
              Color(245, 140, 148, 'blush'),         # palette2
              Color(226, 126, 133, 'darkBlush'),     # palette2
              Color(219, 212, 153, 'granola'),       # palette2
              Color(200, 191, 138, 'darkGranola'),   # palette2
              Color(84, 191, 209, 'azure'),          # palette2
              Color(76, 174, 191, 'darkAzure'),      # palette2
              Color( 242, 132, 128, 'coral'),          # palette3
              Color( 204, 89, 86, 'darkCoral'),        # palette3
              Color( 55, 174, 187, 'munsell'),         # palette3
              Color( 22, 127, 142, 'darkMunsell'),     # palette3
              Color( 61, 233, 171, 'carribean'),       # palette3
              Color( 18, 181, 118, 'darkCarribean'),   # palette3
              Color( 103, 121, 145, 'independence'),   # palette3
              Color( 156, 246, 246, 'celeste'),        # palette3
              Color( 125, 201, 200, 'darkCeleste'),    # palette3
              Color( 168, 89, 111, 'magenta'),         # palette3
              Color( 127, 44, 62, 'darkMagenta'),      # palette3
              Color( 249, 182, 181, 'spanish'),        # palette3
              Color( 207, 135, 134, 'darkSpanish'),    # palette3
              Color( 151, 223, 252, 'sky'),              # palette4
              Color( 255, 107, 108, 'bittersweet'),      # palette4
              Color( 97, 132, 216, 'glaucous'),          # palette4
              Color( 159, 211, 86, 'yellowgreen'),       # palette4
              Color( 253, 221, 98, 'naples'),            # palette4
              Color( 255, 169, 163, 'melon'),            # palette4
              Color( 205, 199, 229, 'lavender'),         # palette4
              Color( 30, 145, 214, 'tufts'),             # palette4
              Color( 135, 191, 255, 'french'),           # palette4
              Color( 254, 215, 102, 'crayola'),          # palette4
              Color( 122, 199, 79, 'mantis'),            # palette4
              Color( 255, 224, 181, 'navajo'),           # palette4
              Color( 146, 94, 120, 'mauve'),             # palette4
              Color( 247, 169, 168, 'pastel'),           # palette4
              Color( 77, 157, 224, 'carolina'),          # palette4
              Color(0.93, 0.67, 0.93, 'pink'),             # laurent
              Color(0.89, 0.48, 0.89, 'darkPink'),         # laurent
              Color(0.59, 0.59, 0.91, 'purple'),           # laurent
              Color(0.59, 0.91, 0.91, 'lightBlue'),        # laurent
              Color(0.91, 0.59, 0.59, 'red'),              # laurent
              Color(0.99, 0.91, 0.59, 'yellow'),           # laurent
              Color(0.91, 0.82, 0.15, 'gold'),             # laurent
              Color(0.29, 0.64, 0.98, 'darkBlue'),         # laurent
              Color(0.67, 0.83, 0.99, 'blue')]             # laurent
    for color in colors: setattr(ROOT, color.name, color)
    return colors

def sampleColors():
    colors = makeColors()
    # Laurent's colors
    #samples = [['tt', ROOT.blue, ROOT.darkBlue],['zg', ROOT.lightBlue, ROOT.kCyan],['wg', ROOT.purple, 214],
    #           ['g+j',ROOT.yellow, ROOT.gold],['ggj', ROOT.red, 206],['qcd', ROOT.pink, ROOT.darkPink]]
    # My colors
    #samples = [['tt', ROOT.kGreen-9, ROOT.kGreen-9],['zg', ROOT.kYellow-9, ROOT.kYellow-9],['wg', 38, 38],
    #           ['g+j',ROOT.kTeal+3, ROOT.kTeal+3],['ggj', 208, 208],['qcd', ROOT.kCyan-9, ROOT.kCyan-9]]
    # Palette 1
    #samples = [['tt', ROOT.aqua, ROOT.darkAqua],['zg', ROOT.sand, ROOT.darkSand],['wg', ROOT.apricot, ROOT.darkApricot],
    #           ['g+j',ROOT.rose, ROOT.darkRose],['ggj', ROOT.teal, ROOT.darkTeal],['qcd', ROOT.seafoam, ROOT.darkSeafoam]]
    # Palette 2
    samples = [['tt', ROOT.azure, ROOT.darkAzure],['zg', ROOT.granola, ROOT.darkGranola],['wg', ROOT.blush, ROOT.darkBlush],
               ['g+j',ROOT.mustard, ROOT.darkMustard],['ggj', ROOT.lime, ROOT.darkLime],['qcd', ROOT.turquois, ROOT.darkTurquois]]
    # Palette 3
    #samples = [['tt', ROOT.carribean, ROOT.darkCarribean],['zg', ROOT.spanish, ROOT.darkSpanish],['wg', ROOT.magenta, ROOT.darkMagenta],
    #           ['g+j',ROOT.munsell, ROOT.darkMunsell],['ggj', ROOT.coral, ROOT.darkCoral],['qcd', ROOT.celeste, ROOT.darkCeleste]]
    # Palette 4
    #samples = [['tt', ROOT.pastel, ROOT.pastel],['zg', ROOT.mauve, ROOT.mauve],['wg', ROOT.mantis, ROOT.mantis],
    #           ['g+j',ROOT.glaucous, ROOT.glaucous],['ggj', ROOT.bittersweet, ROOT.bittersweet],['qcd', ROOT.celeste, ROOT.celeste]]
    return samples

def Canvas(name):
    c = TCanvas(name,'c',600,600)
    return c

def Prettify( hist ):
    x = hist.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4)
    x.SetLabelFont(43)
    x.SetLabelOffset(0.03)
    x.SetLabelSize(20)
    x.SetTickLength(0.05)
    y = hist.GetYaxis()
    y.SetTitle('Data / Pred.')
    y.SetNdivisions(507)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.3)
    y.SetLabelFont(43)
    y.SetLabelSize(18)

def lumiLabel(ratio,years):
    label = TPaveText( 0.65, 0.91, 0.75, 0.93, 'NB NDC' )
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
    legend = TLegend(0.6, 0.55, 0.77, 0.85)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.038)
    legend.AddEntry(h1,'Data', 'lp')
    backgrounds = ['t#bar{t} + j (NLO)', 'Incl. Z + #gamma (NLO)', 'Incl. W + #gamma (NLO)', '#gamma + j', 'Incl. #gamma#gamma + j (NLO)', 'QCD (e#gamma enriched)']
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

def open_root(path):
    r_file = ROOT.TFile.Open(path)
    if not r_file.__nonzero__() or not r_file.IsOpen(): raise NameError('File ' + path + ' not open')
    return r_file

def get_root_obj(root_file, obj_name):
    r_obj = root_file.Get(obj_name)
    if not r_obj.__nonzero__(): raise NameError('Root Object ' + obj_name + ' not found')
    return r_obj

# Apply mass cut
def mass_cut(diph_mass):
    if diph_mass > 350: return True
    else: return False

# Apply hoe cut
def hoe_cut(pho1,pho2):
    if pho1.hoe <= 0.1 and pho2.hoe <= 0.1: return True
    else: return False

## Apply hoe cut
#def hoe_cut(pho1,pho2):
#    if pho1.isScEtaEB and pho1.hoe > 0.082: return False
#    if pho1.isScEtaEE and pho1.hoe > 0.075: return False
#    if pho2.isScEtaEB and pho2.hoe > 0.082: return False
#    if pho2.isScEtaEE and pho2.hoe > 0.075: return False
#    return True

# Apply acoplanarity cut
def acop_cut(acop):
    if acop < 0.005: return True
    else: return False

# Apply photon ID
def photon_id(pho1,pho2):
    if pho1.mvaID_WP90 == 1 and pho2.mvaID_WP90 == 1: return True # loose MVA ID                                                                                                                     
    else: return False

# Apply electron veto
def electron_veto(pho1,pho2):
    if pho1.electronVeto == 1 and pho2.electronVeto == 1: return True
    else: return False

# Tight xi cut
def xi_cut(xip,xim):
    if xip < 0.015 or xip > 0.2: return False
    if xim < 0.015 or xim > 0.2: return False
    return True

# Apply eta veto
def eta_cut(pho1,pho2):
    if abs(pho1.eta) > 2.5 or abs(pho2.eta) > 2.5: return False # Out of fiducial range
    #if pho1.isScEtaEE and pho2.isScEtaEE: return False         # EEEE events
    if pho1.eta > 1.4442 and pho1.eta < 1.566: return False     # transition region
    if pho1.eta < -1.442 and pho1.eta > -1.566: return False    # transition region
    if pho2.eta > 1.4442 and pho2.eta < 1.566: return False     # transition region
    if pho2.eta < -1.442 and pho2.eta > -1.566: return False    # transition region
    return True

# Check for two opposite-side protons
def two_protons(protons):
    if len(protons) >= 2:
        proton_45 = proton_56 = False
        for proton in protons:
            if proton.sector45 == 1: proton_45 = True
            elif proton.sector56 == 1: proton_56 = True
        if proton_45 and proton_56: return True
        else: return False
    else: return False

def mass(xi1,xi2):
    if xi1 < 0 or xi2 < 0:
        print '---> Weird. Negtative xi value. xi1:', xi1, 'xi2:', xi2
        return -1
    else: return sqrts*math.sqrt(xi1*xi2)

def rapidity(xi1,xi2):
    if xi1 < 0 or xi2 < 0: return -999
    else: return 0.5*math.log(xi1/xi2)

def mass_err(pro1,pro2):
    return mass(pro1.xi,pro2.xi) * rapidity_err(pro1,pro2)

def rapidity_err(pro1,pro2):
    xi1_err, xi2_err = pro1.xi*rel_xi_err, pro2.xi*rel_xi_err
    return 0.5 * math.sqrt( pow(xi1_err/pro1.xi,2) + pow(xi2_err/pro2.xi,2) )

def mass_matching(mp):
    if abs(mp) <= 3: return True
    else: return False

def rap_matching(rp):
    if abs(rp) <= 3: return True
    else: return False

def getEra(run):
    if run > 297023 and run < 299330:   return '2017B'
    elif run > 299359 and run < 302045: return '2017C'
    elif run > 302111 and run < 302679: return '2017D'
    elif run > 303708 and run < 304798: return '2017E'
    elif run > 305016 and run < 306462: return '2017F'
    elif run > 305016 and run < 306462: return '2018A'
    elif run > 305016 and run < 306462: return '2018B'
    elif run > 305016 and run < 306462: return '2018C'
    elif run > 305016 and run < 306462: return '2018D'
    else: return 'none'
