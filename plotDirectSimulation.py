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

histFile = TFile("output_hists_2017postTS2.root")
