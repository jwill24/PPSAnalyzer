// FIXME FIXME FIXME 
// TURNED OFF APERTURE CUTS FOR SINGLERP RUN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// USING SINGLERP VARIABLES!!!!!!!!!!!!!

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include <fstream>
#include <iostream>
#include "/home/t3-ku/juwillia/CMSSW_10_6_13/src/PPSAnalyzer/data/aperture_param_v2.h"

#define output_file "protonEvents_singleRP_2018.root"

void fillFiducialCutsVectors(
			     TString era, std::map<std::pair<int, int>, double> &fiducialXLow_,
			     std::map<std::pair<int, int>, double> &fiducialXHigh_,
			     std::map<std::pair<int, int>, double> &fiducialYLow_,
			     std::map<std::pair<int, int>, double> &fiducialYHigh_) {
  if (era == "2017B") {
    fiducialXLow_[std::pair<int, int>(0, 2)] = 1.995;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.479;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -11.098;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 4.298;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.422;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.698;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 4.698;
  } else if (era == "2017C1") {
    fiducialXLow_[std::pair<int, int>(0, 2)] = 1.860;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.334;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -11.098;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 4.298;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.422;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.698;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 4.698;
  } else if (era == "2017E") {
    fiducialXLow_[std::pair<int, int>(0, 2)] = 1.995;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.479;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -10.098;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 4.998;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.422;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -9.698;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 5.398;
  } else if (era == "2017F1") {
    fiducialXLow_[std::pair<int, int>(0, 2)] = 1.995;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.479;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -10.098;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 4.998;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.422;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -9.698;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 5.398;
  } else if (era == "2018A") {
    fiducialXLow_[std::pair<int, int>(0, 0)] = 2.710;
    fiducialXHigh_[std::pair<int, int>(0, 0)] = 17.927;
    fiducialYLow_[std::pair<int, int>(0, 0)] = -11.598;
    fiducialYHigh_[std::pair<int, int>(0, 0)] = 3.698;
    fiducialXLow_[std::pair<int, int>(0, 2)] = 2.278;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -10.898;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 4.398;
    fiducialXLow_[std::pair<int, int>(1, 0)] = 3.000;
    fiducialXHigh_[std::pair<int, int>(1, 0)] = 18.498;
    fiducialYLow_[std::pair<int, int>(1, 0)] = -11.298;
    fiducialYHigh_[std::pair<int, int>(1, 0)] = 4.098;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.420;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 20.045;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.398;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 5.098;
  } else if (era == "2018B1") {
    fiducialXLow_[std::pair<int, int>(0, 0)] = 2.850;
    fiducialXHigh_[std::pair<int, int>(0, 0)] = 17.927;
    fiducialYLow_[std::pair<int, int>(0, 0)] = -11.598;
    fiducialYHigh_[std::pair<int, int>(0, 0)] = 3.698;
    fiducialXLow_[std::pair<int, int>(0, 2)] = 2.420;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -10.798;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 4.298;
    fiducialXLow_[std::pair<int, int>(1, 0)] = 3.000;
    fiducialXHigh_[std::pair<int, int>(1, 0)] = 18.070;
    fiducialYLow_[std::pair<int, int>(1, 0)] = -11.198;
    fiducialYHigh_[std::pair<int, int>(1, 0)] = 4.098;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.420;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 25.045;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.398;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 5.098;
  } else if (era == "2018B2") {
    fiducialXLow_[std::pair<int, int>(0, 0)] = 2.562;
    fiducialXHigh_[std::pair<int, int>(0, 0)] = 17.640;
    fiducialYLow_[std::pair<int, int>(0, 0)] = -11.098;
    fiducialYHigh_[std::pair<int, int>(0, 0)] = 4.198;
    fiducialXLow_[std::pair<int, int>(0, 2)] = 2.135;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -11.398;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 3.798;
    fiducialXLow_[std::pair<int, int>(1, 0)] = 3.000;
    fiducialXHigh_[std::pair<int, int>(1, 0)] = 17.931;
    fiducialYLow_[std::pair<int, int>(1, 0)] = -10.498;
    fiducialYHigh_[std::pair<int, int>(1, 0)] = 4.698;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.279;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.760;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.598;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 4.498;
  } else if (era == "2018C") {
    fiducialXLow_[std::pair<int, int>(0, 0)] = 2.564;
    fiducialXHigh_[std::pair<int, int>(0, 0)] = 17.930;
    fiducialYLow_[std::pair<int, int>(0, 0)] = -11.098;
    fiducialYHigh_[std::pair<int, int>(0, 0)] = 4.198;
    fiducialXLow_[std::pair<int, int>(0, 2)] = 2.278;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -11.398;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 3.698;
    fiducialXLow_[std::pair<int, int>(1, 0)] = 3.000;
    fiducialXHigh_[std::pair<int, int>(1, 0)] = 17.931;
    fiducialYLow_[std::pair<int, int>(1, 0)] = -10.498;
    fiducialYHigh_[std::pair<int, int>(1, 0)] = 4.698;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.279;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.760;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.598;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 4.398;
  } else if (era == "2018D1") {
    fiducialXLow_[std::pair<int, int>(0, 0)] = 2.847;
    fiducialXHigh_[std::pair<int, int>(0, 0)] = 17.930;
    fiducialYLow_[std::pair<int, int>(0, 0)] = -11.098;
    fiducialYHigh_[std::pair<int, int>(0, 0)] = 4.098;
    fiducialXLow_[std::pair<int, int>(0, 2)] = 2.278;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -11.398;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 3.698;
    fiducialXLow_[std::pair<int, int>(1, 0)] = 3.000;
    fiducialXHigh_[std::pair<int, int>(1, 0)] = 17.931;
    fiducialYLow_[std::pair<int, int>(1, 0)] = -10.498;
    fiducialYHigh_[std::pair<int, int>(1, 0)] = 4.698;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.279;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.760;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.598;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 4.398;
  } else if (era == "2018D2") {
    fiducialXLow_[std::pair<int, int>(0, 0)] = 2.847;
    fiducialXHigh_[std::pair<int, int>(0, 0)] = 17.931;
    fiducialYLow_[std::pair<int, int>(0, 0)] = -10.598;
    fiducialYHigh_[std::pair<int, int>(0, 0)] = 4.498;
    fiducialXLow_[std::pair<int, int>(0, 2)] = 2.278;
    fiducialXHigh_[std::pair<int, int>(0, 2)] = 24.620;
    fiducialYLow_[std::pair<int, int>(0, 2)] = -11.598;
    fiducialYHigh_[std::pair<int, int>(0, 2)] = 3.398;
    fiducialXLow_[std::pair<int, int>(1, 0)] = 3.000;
    fiducialXHigh_[std::pair<int, int>(1, 0)] = 17.931;
    fiducialYLow_[std::pair<int, int>(1, 0)] = -10.498;
    fiducialYHigh_[std::pair<int, int>(1, 0)] = 4.698;
    fiducialXLow_[std::pair<int, int>(1, 2)] = 2.279;
    fiducialXHigh_[std::pair<int, int>(1, 2)] = 24.760;
    fiducialYLow_[std::pair<int, int>(1, 2)] = -10.598;
    fiducialYHigh_[std::pair<int, int>(1, 2)] = 3.898;
  } else
    std::cout << "WARNING: Era not recognized!" << std::endl;
  return;
}

bool OutsideAperture(const std::string &period, const std::string &arm, double xangle, double xi, double th_x_star)
{

  TF2 aperture("a", GetApertureParametrisation_version2(period, arm).c_str());
    
  aperture.SetParameter("xangle", xangle);
  aperture.SetParameter("xi", xi);
  const double th_x_star_upper_limit = -aperture.EvalPar(nullptr);

  return (th_x_star > th_x_star_upper_limit);
}

bool EfficiencyCut(double run ,int decRPId, double arm, double xi, double x, double y)
{

  if ( run < 297018 ) {
    if (arm == 0 && xi < 0.016) return true; // 2016 runs have no pixels, lower cut on strips
    else if (arm == 1 && xi < 0.019) return true;
    else return false;
  }

  uint32_t station;
  if (decRPId == 3 || decRPId == 103) station = 0;
  else station = 2;

  if ( ( run > 297019  && run < 306463 ) &&  station == 0 ) return false;  // strip tracks in 2017

  TString era;

  if (run > 297019 && run < 299330 ) era = "2017B";
  else if (run > 299336 && run < 302679 ) era = "2017C1";
  else if (run > 303708 && run < 304798 ) era = "2017E";
  else if (run > 305016 && run < 306463 ) era = "2017F1";
  else if (run > 315256 && run < 316996 ) era = "2018A";
  else if (run > 317079 && run < 317697 ) era = "2018B1";
  else if (run > 318621 && run < 319313 ) era = "2018B2";
  else if (run > 319336 && run < 320394 ) era = "2018C";
  else if (run > 320393 && run < 322634 ) era = "2018D1";
  else if (run > 323362 && run < 325274 ) era = "2018D2";
  
  std::map<std::pair<int, int>, double> fiducialXLow_ = {};
  std::map<std::pair<int, int>, double> fiducialXHigh_ = {};
  std::map<std::pair<int, int>, double> fiducialYLow_ = {};
  std::map<std::pair<int, int>, double> fiducialYHigh_ = {};


  fillFiducialCutsVectors(era, fiducialXLow_, fiducialXHigh_, fiducialYLow_, fiducialYHigh_);

  float pixelX0_rotated = 0;
  float pixelY0_rotated = 0;
  if (station == 0) {
    pixelX0_rotated = x * TMath::Cos((-8. / 180.) * TMath::Pi()) -
      y * TMath::Sin((-8. / 180.) * TMath::Pi());
    pixelY0_rotated = x * TMath::Sin((-8. / 180.) * TMath::Pi()) +
      y * TMath::Cos((-8. / 180.) * TMath::Pi());
    x = pixelX0_rotated;
    y = pixelY0_rotated;
  }

  if (
      y > fiducialYHigh_[std::pair<int, int>(arm, station)] ||
      y < fiducialYLow_[std::pair<int, int>(arm, station)] ||
      x < fiducialXLow_[std::pair<int, int>(arm, station)] ||
      x > fiducialXHigh_[std::pair<int, int>(arm, station)])
    return true;
  else
    return false;
}

std::string getPeriod(double run)
{
  if (run > 273724 && run < 280386) return "2016_preTS2";
  else if (run > 297023 && run < 302664) return "2017_preTS2";
  else if (run > 302664 && run < 306462) return "2017_postTS2";
  else if ( run > 315256 && run < 325173) return "2018";
  else {
    std::cout << "NOT IN PPS RUN RANGE: " << run << std::endl;
    return "Not in PPS run range";
  }
}

void makeProtonTree( TString outFile=output_file )
{

  TFile* out = new TFile( outFile, "RECREATE" );

  // 2018
  TTree* tree_A_120 = new TTree( "tree_A_120", "tree for 120 protons");
  TTree* tree_A_121 = new TTree( "tree_A_121", "tree for 121 protons");
  TTree* tree_A_122 = new TTree( "tree_A_122", "tree for 122 protons");
  TTree* tree_A_123 = new TTree( "tree_A_123", "tree for 123 protons");
  TTree* tree_A_124 = new TTree( "tree_A_124", "tree for 124 protons");
  TTree* tree_A_125 = new TTree( "tree_A_125", "tree for 125 protons");
  TTree* tree_A_126 = new TTree( "tree_A_126", "tree for 126 protons");
  TTree* tree_A_127 = new TTree( "tree_A_127", "tree for 127 protons");
  TTree* tree_A_128 = new TTree( "tree_A_128", "tree for 128 protons");
  TTree* tree_A_129 = new TTree( "tree_A_129", "tree for 129 protons");
  TTree* tree_A_130 = new TTree( "tree_A_130", "tree for 130 protons");
  TTree* tree_A_131 = new TTree( "tree_A_131", "tree for 131 protons");
  TTree* tree_A_132 = new TTree( "tree_A_132", "tree for 132 protons");
  TTree* tree_A_133 = new TTree( "tree_A_133", "tree for 133 protons");
  TTree* tree_A_134 = new TTree( "tree_A_134", "tree for 134 protons");
  TTree* tree_A_135 = new TTree( "tree_A_135", "tree for 135 protons");
  TTree* tree_A_136 = new TTree( "tree_A_136", "tree for 136 protons");
  TTree* tree_A_137 = new TTree( "tree_A_137", "tree for 137 protons");
  TTree* tree_A_138 = new TTree( "tree_A_138", "tree for 138 protons");
  TTree* tree_A_139 = new TTree( "tree_A_139", "tree for 139 protons");
  TTree* tree_A_140 = new TTree( "tree_A_140", "tree for 140 protons");
  TTree* tree_A_141 = new TTree( "tree_A_141", "tree for 141 protons");
  TTree* tree_A_142 = new TTree( "tree_A_142", "tree for 142 protons");
  TTree* tree_A_143 = new TTree( "tree_A_143", "tree for 143 protons");
  TTree* tree_A_144 = new TTree( "tree_A_144", "tree for 144 protons");
  TTree* tree_A_145 = new TTree( "tree_A_145", "tree for 145 protons");
  TTree* tree_A_146 = new TTree( "tree_A_146", "tree for 146 protons");
  TTree* tree_A_147 = new TTree( "tree_A_147", "tree for 147 protons");
  TTree* tree_A_148 = new TTree( "tree_A_148", "tree for 148 protons");
  TTree* tree_A_149 = new TTree( "tree_A_149", "tree for 149 protons");
  TTree* tree_A_150 = new TTree( "tree_A_150", "tree for 150 protons");
  TTree* tree_A_151 = new TTree( "tree_A_151", "tree for 151 protons");
  TTree* tree_A_152 = new TTree( "tree_A_152", "tree for 152 protons");
  TTree* tree_A_153 = new TTree( "tree_A_153", "tree for 153 protons");
  TTree* tree_A_154 = new TTree( "tree_A_154", "tree for 154 protons");
  TTree* tree_A_155 = new TTree( "tree_A_155", "tree for 155 protons");
  TTree* tree_A_156 = new TTree( "tree_A_156", "tree for 156 protons");
  TTree* tree_A_157 = new TTree( "tree_A_157", "tree for 157 protons");
  TTree* tree_A_158 = new TTree( "tree_A_158", "tree for 158 protons");
  TTree* tree_A_159 = new TTree( "tree_A_159", "tree for 159 protons");
  TTree* tree_A_160 = new TTree( "tree_A_160", "tree for 160 protons");

  TTree* tree_B_120 = new TTree( "tree_B_120", "tree for 120 protons");
  TTree* tree_B_121 = new TTree( "tree_B_121", "tree for 121 protons");
  TTree* tree_B_122 = new TTree( "tree_B_122", "tree for 122 protons");
  TTree* tree_B_123 = new TTree( "tree_B_123", "tree for 123 protons");
  TTree* tree_B_124 = new TTree( "tree_B_124", "tree for 124 protons");
  TTree* tree_B_125 = new TTree( "tree_B_125", "tree for 125 protons");
  TTree* tree_B_126 = new TTree( "tree_B_126", "tree for 126 protons");
  TTree* tree_B_127 = new TTree( "tree_B_127", "tree for 127 protons");
  TTree* tree_B_128 = new TTree( "tree_B_128", "tree for 128 protons");
  TTree* tree_B_129 = new TTree( "tree_B_129", "tree for 129 protons");
  TTree* tree_B_130 = new TTree( "tree_B_130", "tree for 130 protons");
  TTree* tree_B_131 = new TTree( "tree_B_131", "tree for 131 protons");
  TTree* tree_B_132 = new TTree( "tree_B_132", "tree for 132 protons");
  TTree* tree_B_133 = new TTree( "tree_B_133", "tree for 133 protons");
  TTree* tree_B_134 = new TTree( "tree_B_134", "tree for 134 protons");
  TTree* tree_B_135 = new TTree( "tree_B_135", "tree for 135 protons");
  TTree* tree_B_136 = new TTree( "tree_B_136", "tree for 136 protons");
  TTree* tree_B_137 = new TTree( "tree_B_137", "tree for 137 protons");
  TTree* tree_B_138 = new TTree( "tree_B_138", "tree for 138 protons");
  TTree* tree_B_139 = new TTree( "tree_B_139", "tree for 139 protons");
  TTree* tree_B_140 = new TTree( "tree_B_140", "tree for 140 protons");
  TTree* tree_B_141 = new TTree( "tree_B_141", "tree for 141 protons");
  TTree* tree_B_142 = new TTree( "tree_B_142", "tree for 142 protons");
  TTree* tree_B_143 = new TTree( "tree_B_143", "tree for 143 protons");
  TTree* tree_B_144 = new TTree( "tree_B_144", "tree for 144 protons");
  TTree* tree_B_145 = new TTree( "tree_B_145", "tree for 145 protons");
  TTree* tree_B_146 = new TTree( "tree_B_146", "tree for 146 protons");
  TTree* tree_B_147 = new TTree( "tree_B_147", "tree for 147 protons");
  TTree* tree_B_148 = new TTree( "tree_B_148", "tree for 148 protons");
  TTree* tree_B_149 = new TTree( "tree_B_149", "tree for 149 protons");
  TTree* tree_B_150 = new TTree( "tree_B_150", "tree for 150 protons");
  TTree* tree_B_151 = new TTree( "tree_B_151", "tree for 151 protons");
  TTree* tree_B_152 = new TTree( "tree_B_152", "tree for 152 protons");
  TTree* tree_B_153 = new TTree( "tree_B_153", "tree for 153 protons");
  TTree* tree_B_154 = new TTree( "tree_B_154", "tree for 154 protons");
  TTree* tree_B_155 = new TTree( "tree_B_155", "tree for 155 protons");
  TTree* tree_B_156 = new TTree( "tree_B_156", "tree for 156 protons");
  TTree* tree_B_157 = new TTree( "tree_B_157", "tree for 157 protons");
  TTree* tree_B_158 = new TTree( "tree_B_158", "tree for 158 protons");
  TTree* tree_B_159 = new TTree( "tree_B_159", "tree for 159 protons");
  TTree* tree_B_160 = new TTree( "tree_B_160", "tree for 160 protons");

  TTree* tree_C_120 = new TTree( "tree_C_120", "tree for 120 protons");
  TTree* tree_C_121 = new TTree( "tree_C_121", "tree for 121 protons");
  TTree* tree_C_122 = new TTree( "tree_C_122", "tree for 122 protons");
  TTree* tree_C_123 = new TTree( "tree_C_123", "tree for 123 protons");
  TTree* tree_C_124 = new TTree( "tree_C_124", "tree for 124 protons");
  TTree* tree_C_125 = new TTree( "tree_C_125", "tree for 125 protons");
  TTree* tree_C_126 = new TTree( "tree_C_126", "tree for 126 protons");
  TTree* tree_C_127 = new TTree( "tree_C_127", "tree for 127 protons");
  TTree* tree_C_128 = new TTree( "tree_C_128", "tree for 128 protons");
  TTree* tree_C_129 = new TTree( "tree_C_129", "tree for 129 protons");
  TTree* tree_C_130 = new TTree( "tree_C_130", "tree for 130 protons");
  TTree* tree_C_131 = new TTree( "tree_C_131", "tree for 131 protons");
  TTree* tree_C_132 = new TTree( "tree_C_132", "tree for 132 protons");
  TTree* tree_C_133 = new TTree( "tree_C_133", "tree for 133 protons");
  TTree* tree_C_134 = new TTree( "tree_C_134", "tree for 134 protons");
  TTree* tree_C_135 = new TTree( "tree_C_135", "tree for 135 protons");
  TTree* tree_C_136 = new TTree( "tree_C_136", "tree for 136 protons");
  TTree* tree_C_137 = new TTree( "tree_C_137", "tree for 137 protons");
  TTree* tree_C_138 = new TTree( "tree_C_138", "tree for 138 protons");
  TTree* tree_C_139 = new TTree( "tree_C_139", "tree for 139 protons");
  TTree* tree_C_140 = new TTree( "tree_C_140", "tree for 140 protons");
  TTree* tree_C_141 = new TTree( "tree_C_141", "tree for 141 protons");
  TTree* tree_C_142 = new TTree( "tree_C_142", "tree for 142 protons");
  TTree* tree_C_143 = new TTree( "tree_C_143", "tree for 143 protons");
  TTree* tree_C_144 = new TTree( "tree_C_144", "tree for 144 protons");
  TTree* tree_C_145 = new TTree( "tree_C_145", "tree for 145 protons");
  TTree* tree_C_146 = new TTree( "tree_C_146", "tree for 146 protons");
  TTree* tree_C_147 = new TTree( "tree_C_147", "tree for 147 protons");
  TTree* tree_C_148 = new TTree( "tree_C_148", "tree for 148 protons");
  TTree* tree_C_149 = new TTree( "tree_C_149", "tree for 149 protons");
  TTree* tree_C_150 = new TTree( "tree_C_150", "tree for 150 protons");
  TTree* tree_C_151 = new TTree( "tree_C_151", "tree for 151 protons");
  TTree* tree_C_152 = new TTree( "tree_C_152", "tree for 152 protons");
  TTree* tree_C_153 = new TTree( "tree_C_153", "tree for 153 protons");
  TTree* tree_C_154 = new TTree( "tree_C_154", "tree for 154 protons");
  TTree* tree_C_155 = new TTree( "tree_C_155", "tree for 155 protons");
  TTree* tree_C_156 = new TTree( "tree_C_156", "tree for 156 protons");
  TTree* tree_C_157 = new TTree( "tree_C_157", "tree for 157 protons");
  TTree* tree_C_158 = new TTree( "tree_C_158", "tree for 158 protons");
  TTree* tree_C_159 = new TTree( "tree_C_159", "tree for 159 protons");
  TTree* tree_C_160 = new TTree( "tree_C_160", "tree for 160 protons");

  TTree* tree_D_120 = new TTree( "tree_D_120", "tree for 120 protons");
  TTree* tree_D_121 = new TTree( "tree_D_121", "tree for 121 protons");
  TTree* tree_D_122 = new TTree( "tree_D_122", "tree for 122 protons");
  TTree* tree_D_123 = new TTree( "tree_D_123", "tree for 123 protons");
  TTree* tree_D_124 = new TTree( "tree_D_124", "tree for 124 protons");
  TTree* tree_D_125 = new TTree( "tree_D_125", "tree for 125 protons");
  TTree* tree_D_126 = new TTree( "tree_D_126", "tree for 126 protons");
  TTree* tree_D_127 = new TTree( "tree_D_127", "tree for 127 protons");
  TTree* tree_D_128 = new TTree( "tree_D_128", "tree for 128 protons");
  TTree* tree_D_129 = new TTree( "tree_D_129", "tree for 129 protons");
  TTree* tree_D_130 = new TTree( "tree_D_130", "tree for 130 protons");
  TTree* tree_D_131 = new TTree( "tree_D_131", "tree for 131 protons");
  TTree* tree_D_132 = new TTree( "tree_D_132", "tree for 132 protons");
  TTree* tree_D_133 = new TTree( "tree_D_133", "tree for 133 protons");
  TTree* tree_D_134 = new TTree( "tree_D_134", "tree for 134 protons");
  TTree* tree_D_135 = new TTree( "tree_D_135", "tree for 135 protons");
  TTree* tree_D_136 = new TTree( "tree_D_136", "tree for 136 protons");
  TTree* tree_D_137 = new TTree( "tree_D_137", "tree for 137 protons");
  TTree* tree_D_138 = new TTree( "tree_D_138", "tree for 138 protons");
  TTree* tree_D_139 = new TTree( "tree_D_139", "tree for 139 protons");
  TTree* tree_D_140 = new TTree( "tree_D_140", "tree for 140 protons");
  TTree* tree_D_141 = new TTree( "tree_D_141", "tree for 141 protons");
  TTree* tree_D_142 = new TTree( "tree_D_142", "tree for 142 protons");
  TTree* tree_D_143 = new TTree( "tree_D_143", "tree for 143 protons");
  TTree* tree_D_144 = new TTree( "tree_D_144", "tree for 144 protons");
  TTree* tree_D_145 = new TTree( "tree_D_145", "tree for 145 protons");
  TTree* tree_D_146 = new TTree( "tree_D_146", "tree for 146 protons");
  TTree* tree_D_147 = new TTree( "tree_D_147", "tree for 147 protons");
  TTree* tree_D_148 = new TTree( "tree_D_148", "tree for 148 protons");
  TTree* tree_D_149 = new TTree( "tree_D_149", "tree for 149 protons");
  TTree* tree_D_150 = new TTree( "tree_D_150", "tree for 150 protons");
  TTree* tree_D_151 = new TTree( "tree_D_151", "tree for 151 protons");
  TTree* tree_D_152 = new TTree( "tree_D_152", "tree for 152 protons");
  TTree* tree_D_153 = new TTree( "tree_D_153", "tree for 153 protons");
  TTree* tree_D_154 = new TTree( "tree_D_154", "tree for 154 protons");
  TTree* tree_D_155 = new TTree( "tree_D_155", "tree for 155 protons");
  TTree* tree_D_156 = new TTree( "tree_D_156", "tree for 156 protons");
  TTree* tree_D_157 = new TTree( "tree_D_157", "tree for 157 protons");
  TTree* tree_D_158 = new TTree( "tree_D_158", "tree for 158 protons");
  TTree* tree_D_159 = new TTree( "tree_D_159", "tree for 159 protons");
  TTree* tree_D_160 = new TTree( "tree_D_160", "tree for 160 protons");
  //
  
  /* 2017
  TTree* tree_B_120 = new TTree( "tree_B_120", "tree for 120 protons");
  TTree* tree_B_130 = new TTree( "tree_B_130", "tree for 130 protons");
  TTree* tree_B_140 = new TTree( "tree_B_140", "tree for 140 protons");
  TTree* tree_B_150 = new TTree( "tree_B_150", "tree for 150 protons");

  TTree* tree_C_120 = new TTree( "tree_C_120", "tree for 120 protons");
  TTree* tree_C_130 = new TTree( "tree_C_130", "tree for 130 protons");
  TTree* tree_C_140 = new TTree( "tree_C_140", "tree for 140 protons");
  TTree* tree_C_150 = new TTree( "tree_C_150", "tree for 150 protons");

  TTree* tree_D_120 = new TTree( "tree_D_120", "tree for 120 protons");
  TTree* tree_D_130 = new TTree( "tree_D_130", "tree for 130 protons");
  TTree* tree_D_140 = new TTree( "tree_D_140", "tree for 140 protons");
  TTree* tree_D_150 = new TTree( "tree_D_150", "tree for 150 protons");

  TTree* tree_E_120 = new TTree( "tree_E_120", "tree for 120 protons");
  TTree* tree_E_130 = new TTree( "tree_E_130", "tree for 130 protons");
  TTree* tree_E_140 = new TTree( "tree_E_140", "tree for 140 protons");
  TTree* tree_E_150 = new TTree( "tree_E_150", "tree for 150 protons");

  TTree* tree_F_120 = new TTree( "tree_F_120", "tree for 120 protons");
  TTree* tree_F_130 = new TTree( "tree_F_130", "tree for 130 protons");
  TTree* tree_F_140 = new TTree( "tree_F_140", "tree for 140 protons");
  TTree* tree_F_150 = new TTree( "tree_F_150", "tree for 150 protons");
  */

  /* 2016
  TTree* tree_B = new TTree( "tree_B", "tree for RunB protons");
  TTree* tree_C = new TTree( "tree_C", "tree for RunC protons");
  TTree* tree_G = new TTree( "tree_G", "tree for RunG protons");
  */

  unsigned short maxProSide = 12;
  unsigned int num_m, num_p;
  float xim[maxProSide], xip[maxProSide];
  unsigned int idm[maxProSide], idp[maxProSide];

  // 2018
  tree_A_120->Branch("num_m", &num_m, "num_m/I");
  tree_A_120->Branch("num_p", &num_p, "num_p/I");
  tree_A_120->Branch("xim", xim, "xim[num_m]/F");
  tree_A_120->Branch("xip", xip, "xim[num_p]/F");
  tree_A_120->Branch("idm", idm, "idm[num_m]/I");
  tree_A_120->Branch("idp", idp, "idp[num_p]/I");
  tree_A_121->Branch("num_m", &num_m, "num_m/I");
  tree_A_121->Branch("num_p", &num_p, "num_p/I");
  tree_A_121->Branch("xim", xim, "xim[num_m]/F");
  tree_A_121->Branch("xip", xip, "xim[num_p]/F");
  tree_A_121->Branch("idm", idm, "idm[num_m]/I");
  tree_A_121->Branch("idp", idp, "idp[num_p]/I");
  tree_A_122->Branch("num_m", &num_m, "num_m/I");
  tree_A_122->Branch("num_p", &num_p, "num_p/I");
  tree_A_122->Branch("xim", xim, "xim[num_m]/F");
  tree_A_122->Branch("xip", xip, "xim[num_p]/F");
  tree_A_122->Branch("idm", idm, "idm[num_m]/I");
  tree_A_122->Branch("idp", idp, "idp[num_p]/I");
  tree_A_123->Branch("num_m", &num_m, "num_m/I");
  tree_A_123->Branch("num_p", &num_p, "num_p/I");
  tree_A_123->Branch("idm", idm, "idm[num_m]/I");
  tree_A_123->Branch("idp", idp, "idp[num_p]/I");
  tree_A_123->Branch("xim", xim, "xim[num_m]/F");
  tree_A_123->Branch("xip", xip, "xim[num_p]/F");
  tree_A_124->Branch("num_m", &num_m, "num_m/I");
  tree_A_124->Branch("num_p", &num_p, "num_p/I");
  tree_A_124->Branch("xim", xim, "xim[num_m]/F");
  tree_A_124->Branch("xip", xip, "xim[num_p]/F");
  tree_A_124->Branch("idm", idm, "idm[num_m]/I");
  tree_A_124->Branch("idp", idp, "idp[num_p]/I");
  tree_A_125->Branch("num_m", &num_m, "num_m/I");
  tree_A_125->Branch("num_p", &num_p, "num_p/I");
  tree_A_125->Branch("xim", xim, "xim[num_m]/F");
  tree_A_125->Branch("xip", xip, "xim[num_p]/F");
  tree_A_125->Branch("idm", idm, "idm[num_m]/I");
  tree_A_125->Branch("idp", idp, "idp[num_p]/I");
  tree_A_126->Branch("num_m", &num_m, "num_m/I");
  tree_A_126->Branch("num_p", &num_p, "num_p/I");
  tree_A_126->Branch("xim", xim, "xim[num_m]/F");
  tree_A_126->Branch("xip", xip, "xim[num_p]/F");
  tree_A_126->Branch("idm", idm, "idm[num_m]/I");
  tree_A_126->Branch("idp", idp, "idp[num_p]/I");
  tree_A_127->Branch("num_m", &num_m, "num_m/I");
  tree_A_127->Branch("num_p", &num_p, "num_p/I");
  tree_A_127->Branch("xim", xim, "xim[num_m]/F");
  tree_A_127->Branch("xip", xip, "xim[num_p]/F");
  tree_A_127->Branch("idm", idm, "idm[num_m]/I");
  tree_A_127->Branch("idp", idp, "idp[num_p]/I");
  tree_A_128->Branch("num_m", &num_m, "num_m/I");
  tree_A_128->Branch("num_p", &num_p, "num_p/I");
  tree_A_128->Branch("xim", xim, "xim[num_m]/F");
  tree_A_128->Branch("xip", xip, "xim[num_p]/F");
  tree_A_128->Branch("idm", idm, "idm[num_m]/I");
  tree_A_128->Branch("idp", idp, "idp[num_p]/I");
  tree_A_129->Branch("num_m", &num_m, "num_m/I");
  tree_A_129->Branch("num_p", &num_p, "num_p/I");
  tree_A_129->Branch("xim", xim, "xim[num_m]/F");
  tree_A_129->Branch("xip", xip, "xim[num_p]/F");
  tree_A_129->Branch("idm", idm, "idm[num_m]/I");
  tree_A_129->Branch("idp", idp, "idp[num_p]/I");
  tree_A_130->Branch("num_m", &num_m, "num_m/I");
  tree_A_130->Branch("num_p", &num_p, "num_p/I");
  tree_A_130->Branch("xim", xim, "xim[num_m]/F");
  tree_A_130->Branch("xip", xip, "xim[num_p]/F");
  tree_A_130->Branch("idm", idm, "idm[num_m]/I");
  tree_A_130->Branch("idp", idp, "idp[num_p]/I");
  tree_A_131->Branch("num_m", &num_m, "num_m/I");
  tree_A_131->Branch("num_p", &num_p, "num_p/I");
  tree_A_131->Branch("xim", xim, "xim[num_m]/F");
  tree_A_131->Branch("xip", xip, "xim[num_p]/F");
  tree_A_131->Branch("idm", idm, "idm[num_m]/I");
  tree_A_131->Branch("idp", idp, "idp[num_p]/I");
  tree_A_132->Branch("num_m", &num_m, "num_m/I");
  tree_A_132->Branch("num_p", &num_p, "num_p/I");
  tree_A_132->Branch("xim", xim, "xim[num_m]/F");
  tree_A_132->Branch("xip", xip, "xim[num_p]/F");
  tree_A_132->Branch("idm", idm, "idm[num_m]/I");
  tree_A_132->Branch("idp", idp, "idp[num_p]/I");
  tree_A_133->Branch("num_m", &num_m, "num_m/I");
  tree_A_133->Branch("num_p", &num_p, "num_p/I");
  tree_A_133->Branch("xim", xim, "xim[num_m]/F");
  tree_A_133->Branch("xip", xip, "xim[num_p]/F");
  tree_A_133->Branch("idm", idm, "idm[num_m]/I");
  tree_A_133->Branch("idp", idp, "idp[num_p]/I");
  tree_A_134->Branch("num_m", &num_m, "num_m/I");
  tree_A_134->Branch("num_p", &num_p, "num_p/I");
  tree_A_134->Branch("xim", xim, "xim[num_m]/F");
  tree_A_134->Branch("xip", xip, "xim[num_p]/F");
  tree_A_134->Branch("idm", idm, "idm[num_m]/I");
  tree_A_134->Branch("idp", idp, "idp[num_p]/I");
  tree_A_135->Branch("num_m", &num_m, "num_m/I");
  tree_A_135->Branch("num_p", &num_p, "num_p/I");
  tree_A_135->Branch("xim", xim, "xim[num_m]/F");
  tree_A_135->Branch("xip", xip, "xim[num_p]/F");
  tree_A_135->Branch("idm", idm, "idm[num_m]/I");
  tree_A_135->Branch("idp", idp, "idp[num_p]/I");
  tree_A_136->Branch("num_m", &num_m, "num_m/I");
  tree_A_136->Branch("num_p", &num_p, "num_p/I");
  tree_A_136->Branch("xim", xim, "xim[num_m]/F");
  tree_A_136->Branch("xip", xip, "xim[num_p]/F");
  tree_A_136->Branch("idm", idm, "idm[num_m]/I");
  tree_A_136->Branch("idp", idp, "idp[num_p]/I");
  tree_A_137->Branch("num_m", &num_m, "num_m/I");
  tree_A_137->Branch("num_p", &num_p, "num_p/I");
  tree_A_137->Branch("xim", xim, "xim[num_m]/F");
  tree_A_137->Branch("xip", xip, "xim[num_p]/F");
  tree_A_137->Branch("idm", idm, "idm[num_m]/I");
  tree_A_137->Branch("idp", idp, "idp[num_p]/I");
  tree_A_138->Branch("num_m", &num_m, "num_m/I");
  tree_A_138->Branch("num_p", &num_p, "num_p/I");
  tree_A_138->Branch("xim", xim, "xim[num_m]/F");
  tree_A_138->Branch("xip", xip, "xim[num_p]/F");
  tree_A_138->Branch("idm", idm, "idm[num_m]/I");
  tree_A_138->Branch("idp", idp, "idp[num_p]/I");
  tree_A_139->Branch("num_m", &num_m, "num_m/I");
  tree_A_139->Branch("num_p", &num_p, "num_p/I");
  tree_A_139->Branch("xim", xim, "xim[num_m]/F");
  tree_A_139->Branch("xip", xip, "xim[num_p]/F");
  tree_A_139->Branch("idm", idm, "idm[num_m]/I");
  tree_A_139->Branch("idp", idp, "idp[num_p]/I");
  tree_A_140->Branch("num_m", &num_m, "num_m/I");
  tree_A_140->Branch("num_p", &num_p, "num_p/I");
  tree_A_140->Branch("xim", xim, "xim[num_m]/F");
  tree_A_140->Branch("xip", xip, "xim[num_p]/F");
  tree_A_140->Branch("idm", idm, "idm[num_m]/I");
  tree_A_140->Branch("idp", idp, "idp[num_p]/I");
  tree_A_141->Branch("num_m", &num_m, "num_m/I");
  tree_A_141->Branch("num_p", &num_p, "num_p/I");
  tree_A_141->Branch("xim", xim, "xim[num_m]/F");
  tree_A_141->Branch("xip", xip, "xim[num_p]/F");
  tree_A_141->Branch("idm", idm, "idm[num_m]/I");
  tree_A_141->Branch("idp", idp, "idp[num_p]/I");
  tree_A_142->Branch("num_m", &num_m, "num_m/I");
  tree_A_142->Branch("num_p", &num_p, "num_p/I");
  tree_A_142->Branch("xim", xim, "xim[num_m]/F");
  tree_A_142->Branch("xip", xip, "xim[num_p]/F");
  tree_A_142->Branch("idm", idm, "idm[num_m]/I");
  tree_A_142->Branch("idp", idp, "idp[num_p]/I");
  tree_A_143->Branch("num_m", &num_m, "num_m/I");
  tree_A_143->Branch("num_p", &num_p, "num_p/I");
  tree_A_143->Branch("xim", xim, "xim[num_m]/F");
  tree_A_143->Branch("xip", xip, "xim[num_p]/F");
  tree_A_143->Branch("idm", idm, "idm[num_m]/I");
  tree_A_143->Branch("idp", idp, "idp[num_p]/I");
  tree_A_144->Branch("num_m", &num_m, "num_m/I");
  tree_A_144->Branch("num_p", &num_p, "num_p/I");
  tree_A_144->Branch("xim", xim, "xim[num_m]/F");
  tree_A_144->Branch("xip", xip, "xim[num_p]/F");
  tree_A_144->Branch("idm", idm, "idm[num_m]/I");
  tree_A_144->Branch("idp", idp, "idp[num_p]/I");
  tree_A_145->Branch("num_m", &num_m, "num_m/I");
  tree_A_145->Branch("num_p", &num_p, "num_p/I");
  tree_A_145->Branch("xim", xim, "xim[num_m]/F");
  tree_A_145->Branch("xip", xip, "xim[num_p]/F");
  tree_A_145->Branch("idm", idm, "idm[num_m]/I");
  tree_A_145->Branch("idp", idp, "idp[num_p]/I");
  tree_A_146->Branch("num_m", &num_m, "num_m/I");
  tree_A_146->Branch("num_p", &num_p, "num_p/I");
  tree_A_146->Branch("xim", xim, "xim[num_m]/F");
  tree_A_146->Branch("xip", xip, "xim[num_p]/F");
  tree_A_146->Branch("idm", idm, "idm[num_m]/I");
  tree_A_146->Branch("idp", idp, "idp[num_p]/I");
  tree_A_147->Branch("num_m", &num_m, "num_m/I");
  tree_A_147->Branch("num_p", &num_p, "num_p/I");
  tree_A_147->Branch("xim", xim, "xim[num_m]/F");
  tree_A_147->Branch("xip", xip, "xim[num_p]/F");
  tree_A_147->Branch("idm", idm, "idm[num_m]/I");
  tree_A_147->Branch("idp", idp, "idp[num_p]/I");
  tree_A_148->Branch("num_m", &num_m, "num_m/I");
  tree_A_148->Branch("num_p", &num_p, "num_p/I");
  tree_A_148->Branch("xim", xim, "xim[num_m]/F");
  tree_A_148->Branch("xip", xip, "xim[num_p]/F");
  tree_A_148->Branch("idm", idm, "idm[num_m]/I");
  tree_A_148->Branch("idp", idp, "idp[num_p]/I");
  tree_A_149->Branch("num_m", &num_m, "num_m/I");
  tree_A_149->Branch("num_p", &num_p, "num_p/I");
  tree_A_149->Branch("xim", xim, "xim[num_m]/F");
  tree_A_149->Branch("xip", xip, "xim[num_p]/F");
  tree_A_149->Branch("idm", idm, "idm[num_m]/I");
  tree_A_149->Branch("idp", idp, "idp[num_p]/I");
  tree_A_150->Branch("num_m", &num_m, "num_m/I");
  tree_A_150->Branch("num_p", &num_p, "num_p/I");
  tree_A_150->Branch("xim", xim, "xim[num_m]/F");
  tree_A_150->Branch("xip", xip, "xim[num_p]/F");
  tree_A_150->Branch("idm", idm, "idm[num_m]/I");
  tree_A_150->Branch("idp", idp, "idp[num_p]/I");
  tree_A_151->Branch("num_m", &num_m, "num_m/I");
  tree_A_151->Branch("num_p", &num_p, "num_p/I");
  tree_A_151->Branch("xim", xim, "xim[num_m]/F");
  tree_A_151->Branch("xip", xip, "xim[num_p]/F");
  tree_A_151->Branch("idm", idm, "idm[num_m]/I");
  tree_A_151->Branch("idp", idp, "idp[num_p]/I");
  tree_A_152->Branch("num_m", &num_m, "num_m/I");
  tree_A_152->Branch("num_p", &num_p, "num_p/I");
  tree_A_152->Branch("xim", xim, "xim[num_m]/F");
  tree_A_152->Branch("xip", xip, "xim[num_p]/F");
  tree_A_152->Branch("idm", idm, "idm[num_m]/I");
  tree_A_152->Branch("idp", idp, "idp[num_p]/I");
  tree_A_153->Branch("num_m", &num_m, "num_m/I");
  tree_A_153->Branch("num_p", &num_p, "num_p/I");
  tree_A_153->Branch("xim", xim, "xim[num_m]/F");
  tree_A_153->Branch("xip", xip, "xim[num_p]/F");
  tree_A_153->Branch("idm", idm, "idm[num_m]/I");
  tree_A_153->Branch("idp", idp, "idp[num_p]/I");
  tree_A_154->Branch("num_m", &num_m, "num_m/I");
  tree_A_154->Branch("num_p", &num_p, "num_p/I");
  tree_A_154->Branch("xim", xim, "xim[num_m]/F");
  tree_A_154->Branch("xip", xip, "xim[num_p]/F");
  tree_A_154->Branch("idm", idm, "idm[num_m]/I");
  tree_A_154->Branch("idp", idp, "idp[num_p]/I");
  tree_A_155->Branch("num_m", &num_m, "num_m/I");
  tree_A_155->Branch("num_p", &num_p, "num_p/I");
  tree_A_155->Branch("xim", xim, "xim[num_m]/F");
  tree_A_155->Branch("xip", xip, "xim[num_p]/F");
  tree_A_155->Branch("idm", idm, "idm[num_m]/I");
  tree_A_155->Branch("idp", idp, "idp[num_p]/I");
  tree_A_156->Branch("num_m", &num_m, "num_m/I");
  tree_A_156->Branch("num_p", &num_p, "num_p/I");
  tree_A_156->Branch("xim", xim, "xim[num_m]/F");
  tree_A_156->Branch("xip", xip, "xim[num_p]/F");
  tree_A_156->Branch("idm", idm, "idm[num_m]/I");
  tree_A_156->Branch("idp", idp, "idp[num_p]/I");
  tree_A_157->Branch("num_m", &num_m, "num_m/I");
  tree_A_157->Branch("num_p", &num_p, "num_p/I");
  tree_A_157->Branch("xim", xim, "xim[num_m]/F");
  tree_A_157->Branch("xip", xip, "xim[num_p]/F");
  tree_A_157->Branch("idm", idm, "idm[num_m]/I");
  tree_A_157->Branch("idp", idp, "idp[num_p]/I");
  tree_A_158->Branch("num_m", &num_m, "num_m/I");
  tree_A_158->Branch("num_p", &num_p, "num_p/I");
  tree_A_158->Branch("xim", xim, "xim[num_m]/F");
  tree_A_158->Branch("xip", xip, "xim[num_p]/F");
  tree_A_158->Branch("idm", idm, "idm[num_m]/I");
  tree_A_158->Branch("idp", idp, "idp[num_p]/I");
  tree_A_159->Branch("num_m", &num_m, "num_m/I");
  tree_A_159->Branch("num_p", &num_p, "num_p/I");
  tree_A_159->Branch("xim", xim, "xim[num_m]/F");
  tree_A_159->Branch("xip", xip, "xim[num_p]/F");
  tree_A_159->Branch("idm", idm, "idm[num_m]/I");
  tree_A_159->Branch("idp", idp, "idp[num_p]/I");
  tree_A_160->Branch("num_m", &num_m, "num_m/I");
  tree_A_160->Branch("num_p", &num_p, "num_p/I");
  tree_A_160->Branch("xim", xim, "xim[num_m]/F");
  tree_A_160->Branch("xip", xip, "xim[num_p]/F");
  tree_A_160->Branch("idm", idm, "idm[num_m]/I");
  tree_A_160->Branch("idp", idp, "idp[num_p]/I");

  tree_B_120->Branch("num_m", &num_m, "num_m/I");
  tree_B_120->Branch("num_p", &num_p, "num_p/I");
  tree_B_120->Branch("xim", xim, "xim[num_m]/F");
  tree_B_120->Branch("xip", xip, "xim[num_p]/F");
  tree_B_120->Branch("idm", idm, "idm[num_m]/I");
  tree_B_120->Branch("idp", idp, "idp[num_p]/I");
  tree_B_121->Branch("num_m", &num_m, "num_m/I");
  tree_B_121->Branch("num_p", &num_p, "num_p/I");
  tree_B_121->Branch("xim", xim, "xim[num_m]/F");
  tree_B_121->Branch("xip", xip, "xim[num_p]/F");
  tree_B_121->Branch("idm", idm, "idm[num_m]/I");
  tree_B_121->Branch("idp", idp, "idp[num_p]/I");
  tree_B_122->Branch("num_m", &num_m, "num_m/I");
  tree_B_122->Branch("num_p", &num_p, "num_p/I");
  tree_B_122->Branch("xim", xim, "xim[num_m]/F");
  tree_B_122->Branch("xip", xip, "xim[num_p]/F");
  tree_B_122->Branch("idm", idm, "idm[num_m]/I");
  tree_B_122->Branch("idp", idp, "idp[num_p]/I");
  tree_B_123->Branch("num_m", &num_m, "num_m/I");
  tree_B_123->Branch("num_p", &num_p, "num_p/I");
  tree_B_123->Branch("idm", idm, "idm[num_m]/I");
  tree_B_123->Branch("idp", idp, "idp[num_p]/I");
  tree_B_123->Branch("xim", xim, "xim[num_m]/F");
  tree_B_123->Branch("xip", xip, "xim[num_p]/F");
  tree_B_124->Branch("num_m", &num_m, "num_m/I");
  tree_B_124->Branch("num_p", &num_p, "num_p/I");
  tree_B_124->Branch("xim", xim, "xim[num_m]/F");
  tree_B_124->Branch("xip", xip, "xim[num_p]/F");
  tree_B_124->Branch("idm", idm, "idm[num_m]/I");
  tree_B_124->Branch("idp", idp, "idp[num_p]/I");
  tree_B_125->Branch("num_m", &num_m, "num_m/I");
  tree_B_125->Branch("num_p", &num_p, "num_p/I");
  tree_B_125->Branch("xim", xim, "xim[num_m]/F");
  tree_B_125->Branch("xip", xip, "xim[num_p]/F");
  tree_B_125->Branch("idm", idm, "idm[num_m]/I");
  tree_B_125->Branch("idp", idp, "idp[num_p]/I");
  tree_B_126->Branch("num_m", &num_m, "num_m/I");
  tree_B_126->Branch("num_p", &num_p, "num_p/I");
  tree_B_126->Branch("xim", xim, "xim[num_m]/F");
  tree_B_126->Branch("xip", xip, "xim[num_p]/F");
  tree_B_126->Branch("idm", idm, "idm[num_m]/I");
  tree_B_126->Branch("idp", idp, "idp[num_p]/I");
  tree_B_127->Branch("num_m", &num_m, "num_m/I");
  tree_B_127->Branch("num_p", &num_p, "num_p/I");
  tree_B_127->Branch("xim", xim, "xim[num_m]/F");
  tree_B_127->Branch("xip", xip, "xim[num_p]/F");
  tree_B_127->Branch("idm", idm, "idm[num_m]/I");
  tree_B_127->Branch("idp", idp, "idp[num_p]/I");
  tree_B_128->Branch("num_m", &num_m, "num_m/I");
  tree_B_128->Branch("num_p", &num_p, "num_p/I");
  tree_B_128->Branch("xim", xim, "xim[num_m]/F");
  tree_B_128->Branch("xip", xip, "xim[num_p]/F");
  tree_B_128->Branch("idm", idm, "idm[num_m]/I");
  tree_B_128->Branch("idp", idp, "idp[num_p]/I");
  tree_B_129->Branch("num_m", &num_m, "num_m/I");
  tree_B_129->Branch("num_p", &num_p, "num_p/I");
  tree_B_129->Branch("xim", xim, "xim[num_m]/F");
  tree_B_129->Branch("xip", xip, "xim[num_p]/F");
  tree_B_129->Branch("idm", idm, "idm[num_m]/I");
  tree_B_129->Branch("idp", idp, "idp[num_p]/I");
  tree_B_130->Branch("num_m", &num_m, "num_m/I");
  tree_B_130->Branch("num_p", &num_p, "num_p/I");
  tree_B_130->Branch("xim", xim, "xim[num_m]/F");
  tree_B_130->Branch("xip", xip, "xim[num_p]/F");
  tree_B_130->Branch("idm", idm, "idm[num_m]/I");
  tree_B_130->Branch("idp", idp, "idp[num_p]/I");
  tree_B_131->Branch("num_m", &num_m, "num_m/I");
  tree_B_131->Branch("num_p", &num_p, "num_p/I");
  tree_B_131->Branch("xim", xim, "xim[num_m]/F");
  tree_B_131->Branch("xip", xip, "xim[num_p]/F");
  tree_B_131->Branch("idm", idm, "idm[num_m]/I");
  tree_B_131->Branch("idp", idp, "idp[num_p]/I");
  tree_B_132->Branch("num_m", &num_m, "num_m/I");
  tree_B_132->Branch("num_p", &num_p, "num_p/I");
  tree_B_132->Branch("xim", xim, "xim[num_m]/F");
  tree_B_132->Branch("xip", xip, "xim[num_p]/F");
  tree_B_132->Branch("idm", idm, "idm[num_m]/I");
  tree_B_132->Branch("idp", idp, "idp[num_p]/I");
  tree_B_133->Branch("num_m", &num_m, "num_m/I");
  tree_B_133->Branch("num_p", &num_p, "num_p/I");
  tree_B_133->Branch("xim", xim, "xim[num_m]/F");
  tree_B_133->Branch("xip", xip, "xim[num_p]/F");
  tree_B_133->Branch("idm", idm, "idm[num_m]/I");
  tree_B_133->Branch("idp", idp, "idp[num_p]/I");
  tree_B_134->Branch("num_m", &num_m, "num_m/I");
  tree_B_134->Branch("num_p", &num_p, "num_p/I");
  tree_B_134->Branch("xim", xim, "xim[num_m]/F");
  tree_B_134->Branch("xip", xip, "xim[num_p]/F");
  tree_B_134->Branch("idm", idm, "idm[num_m]/I");
  tree_B_134->Branch("idp", idp, "idp[num_p]/I");
  tree_B_135->Branch("num_m", &num_m, "num_m/I");
  tree_B_135->Branch("num_p", &num_p, "num_p/I");
  tree_B_135->Branch("xim", xim, "xim[num_m]/F");
  tree_B_135->Branch("xip", xip, "xim[num_p]/F");
  tree_B_135->Branch("idm", idm, "idm[num_m]/I");
  tree_B_135->Branch("idp", idp, "idp[num_p]/I");
  tree_B_136->Branch("num_m", &num_m, "num_m/I");
  tree_B_136->Branch("num_p", &num_p, "num_p/I");
  tree_B_136->Branch("xim", xim, "xim[num_m]/F");
  tree_B_136->Branch("xip", xip, "xim[num_p]/F");
  tree_B_136->Branch("idm", idm, "idm[num_m]/I");
  tree_B_136->Branch("idp", idp, "idp[num_p]/I");
  tree_B_137->Branch("num_m", &num_m, "num_m/I");
  tree_B_137->Branch("num_p", &num_p, "num_p/I");
  tree_B_137->Branch("xim", xim, "xim[num_m]/F");
  tree_B_137->Branch("xip", xip, "xim[num_p]/F");
  tree_B_137->Branch("idm", idm, "idm[num_m]/I");
  tree_B_137->Branch("idp", idp, "idp[num_p]/I");
  tree_B_138->Branch("num_m", &num_m, "num_m/I");
  tree_B_138->Branch("num_p", &num_p, "num_p/I");
  tree_B_138->Branch("xim", xim, "xim[num_m]/F");
  tree_B_138->Branch("xip", xip, "xim[num_p]/F");
  tree_B_138->Branch("idm", idm, "idm[num_m]/I");
  tree_B_138->Branch("idp", idp, "idp[num_p]/I");
  tree_B_139->Branch("num_m", &num_m, "num_m/I");
  tree_B_139->Branch("num_p", &num_p, "num_p/I");
  tree_B_139->Branch("xim", xim, "xim[num_m]/F");
  tree_B_139->Branch("xip", xip, "xim[num_p]/F");
  tree_B_139->Branch("idm", idm, "idm[num_m]/I");
  tree_B_139->Branch("idp", idp, "idp[num_p]/I");
  tree_B_140->Branch("num_m", &num_m, "num_m/I");
  tree_B_140->Branch("num_p", &num_p, "num_p/I");
  tree_B_140->Branch("xim", xim, "xim[num_m]/F");
  tree_B_140->Branch("xip", xip, "xim[num_p]/F");
  tree_B_140->Branch("idm", idm, "idm[num_m]/I");
  tree_B_140->Branch("idp", idp, "idp[num_p]/I");
  tree_B_141->Branch("num_m", &num_m, "num_m/I");
  tree_B_141->Branch("num_p", &num_p, "num_p/I");
  tree_B_141->Branch("xim", xim, "xim[num_m]/F");
  tree_B_141->Branch("xip", xip, "xim[num_p]/F");
  tree_B_141->Branch("idm", idm, "idm[num_m]/I");
  tree_B_141->Branch("idp", idp, "idp[num_p]/I");
  tree_B_142->Branch("num_m", &num_m, "num_m/I");
  tree_B_142->Branch("num_p", &num_p, "num_p/I");
  tree_B_142->Branch("xim", xim, "xim[num_m]/F");
  tree_B_142->Branch("xip", xip, "xim[num_p]/F");
  tree_B_142->Branch("idm", idm, "idm[num_m]/I");
  tree_B_142->Branch("idp", idp, "idp[num_p]/I");
  tree_B_143->Branch("num_m", &num_m, "num_m/I");
  tree_B_143->Branch("num_p", &num_p, "num_p/I");
  tree_B_143->Branch("xim", xim, "xim[num_m]/F");
  tree_B_143->Branch("xip", xip, "xim[num_p]/F");
  tree_B_143->Branch("idm", idm, "idm[num_m]/I");
  tree_B_143->Branch("idp", idp, "idp[num_p]/I");
  tree_B_144->Branch("num_m", &num_m, "num_m/I");
  tree_B_144->Branch("num_p", &num_p, "num_p/I");
  tree_B_144->Branch("xim", xim, "xim[num_m]/F");
  tree_B_144->Branch("xip", xip, "xim[num_p]/F");
  tree_B_144->Branch("idm", idm, "idm[num_m]/I");
  tree_B_144->Branch("idp", idp, "idp[num_p]/I");
  tree_B_145->Branch("num_m", &num_m, "num_m/I");
  tree_B_145->Branch("num_p", &num_p, "num_p/I");
  tree_B_145->Branch("xim", xim, "xim[num_m]/F");
  tree_B_145->Branch("xip", xip, "xim[num_p]/F");
  tree_B_145->Branch("idm", idm, "idm[num_m]/I");
  tree_B_145->Branch("idp", idp, "idp[num_p]/I");
  tree_B_146->Branch("num_m", &num_m, "num_m/I");
  tree_B_146->Branch("num_p", &num_p, "num_p/I");
  tree_B_146->Branch("xim", xim, "xim[num_m]/F");
  tree_B_146->Branch("xip", xip, "xim[num_p]/F");
  tree_B_146->Branch("idm", idm, "idm[num_m]/I");
  tree_B_146->Branch("idp", idp, "idp[num_p]/I");
  tree_B_147->Branch("num_m", &num_m, "num_m/I");
  tree_B_147->Branch("num_p", &num_p, "num_p/I");
  tree_B_147->Branch("xim", xim, "xim[num_m]/F");
  tree_B_147->Branch("xip", xip, "xim[num_p]/F");
  tree_B_147->Branch("idm", idm, "idm[num_m]/I");
  tree_B_147->Branch("idp", idp, "idp[num_p]/I");
  tree_B_148->Branch("num_m", &num_m, "num_m/I");
  tree_B_148->Branch("num_p", &num_p, "num_p/I");
  tree_B_148->Branch("xim", xim, "xim[num_m]/F");
  tree_B_148->Branch("xip", xip, "xim[num_p]/F");
  tree_B_148->Branch("idm", idm, "idm[num_m]/I");
  tree_B_148->Branch("idp", idp, "idp[num_p]/I");
  tree_B_149->Branch("num_m", &num_m, "num_m/I");
  tree_B_149->Branch("num_p", &num_p, "num_p/I");
  tree_B_149->Branch("xim", xim, "xim[num_m]/F");
  tree_B_149->Branch("xip", xip, "xim[num_p]/F");
  tree_B_149->Branch("idm", idm, "idm[num_m]/I");
  tree_B_149->Branch("idp", idp, "idp[num_p]/I");
  tree_B_150->Branch("num_m", &num_m, "num_m/I");
  tree_B_150->Branch("num_p", &num_p, "num_p/I");
  tree_B_150->Branch("xim", xim, "xim[num_m]/F");
  tree_B_150->Branch("xip", xip, "xim[num_p]/F");
  tree_B_150->Branch("idm", idm, "idm[num_m]/I");
  tree_B_150->Branch("idp", idp, "idp[num_p]/I");
  tree_B_151->Branch("num_m", &num_m, "num_m/I");
  tree_B_151->Branch("num_p", &num_p, "num_p/I");
  tree_B_151->Branch("xim", xim, "xim[num_m]/F");
  tree_B_151->Branch("xip", xip, "xim[num_p]/F");
  tree_B_151->Branch("idm", idm, "idm[num_m]/I");
  tree_B_151->Branch("idp", idp, "idp[num_p]/I");
  tree_B_152->Branch("num_m", &num_m, "num_m/I");
  tree_B_152->Branch("num_p", &num_p, "num_p/I");
  tree_B_152->Branch("xim", xim, "xim[num_m]/F");
  tree_B_152->Branch("xip", xip, "xim[num_p]/F");
  tree_B_152->Branch("idm", idm, "idm[num_m]/I");
  tree_B_152->Branch("idp", idp, "idp[num_p]/I");
  tree_B_153->Branch("num_m", &num_m, "num_m/I");
  tree_B_153->Branch("num_p", &num_p, "num_p/I");
  tree_B_153->Branch("xim", xim, "xim[num_m]/F");
  tree_B_153->Branch("xip", xip, "xim[num_p]/F");
  tree_B_153->Branch("idm", idm, "idm[num_m]/I");
  tree_B_153->Branch("idp", idp, "idp[num_p]/I");
  tree_B_154->Branch("num_m", &num_m, "num_m/I");
  tree_B_154->Branch("num_p", &num_p, "num_p/I");
  tree_B_154->Branch("xim", xim, "xim[num_m]/F");
  tree_B_154->Branch("xip", xip, "xim[num_p]/F");
  tree_B_154->Branch("idm", idm, "idm[num_m]/I");
  tree_B_154->Branch("idp", idp, "idp[num_p]/I");
  tree_B_155->Branch("num_m", &num_m, "num_m/I");
  tree_B_155->Branch("num_p", &num_p, "num_p/I");
  tree_B_155->Branch("xim", xim, "xim[num_m]/F");
  tree_B_155->Branch("xip", xip, "xim[num_p]/F");
  tree_B_155->Branch("idm", idm, "idm[num_m]/I");
  tree_B_155->Branch("idp", idp, "idp[num_p]/I");
  tree_B_156->Branch("num_m", &num_m, "num_m/I");
  tree_B_156->Branch("num_p", &num_p, "num_p/I");
  tree_B_156->Branch("xim", xim, "xim[num_m]/F");
  tree_B_156->Branch("xip", xip, "xim[num_p]/F");
  tree_B_156->Branch("idm", idm, "idm[num_m]/I");
  tree_B_156->Branch("idp", idp, "idp[num_p]/I");
  tree_B_157->Branch("num_m", &num_m, "num_m/I");
  tree_B_157->Branch("num_p", &num_p, "num_p/I");
  tree_B_157->Branch("xim", xim, "xim[num_m]/F");
  tree_B_157->Branch("xip", xip, "xim[num_p]/F");
  tree_B_157->Branch("idm", idm, "idm[num_m]/I");
  tree_B_157->Branch("idp", idp, "idp[num_p]/I");
  tree_B_158->Branch("num_m", &num_m, "num_m/I");
  tree_B_158->Branch("num_p", &num_p, "num_p/I");
  tree_B_158->Branch("xim", xim, "xim[num_m]/F");
  tree_B_158->Branch("xip", xip, "xim[num_p]/F");
  tree_B_158->Branch("idm", idm, "idm[num_m]/I");
  tree_B_158->Branch("idp", idp, "idp[num_p]/I");
  tree_B_159->Branch("num_m", &num_m, "num_m/I");
  tree_B_159->Branch("num_p", &num_p, "num_p/I");
  tree_B_159->Branch("xim", xim, "xim[num_m]/F");
  tree_B_159->Branch("xip", xip, "xim[num_p]/F");
  tree_B_159->Branch("idm", idm, "idm[num_m]/I");
  tree_B_159->Branch("idp", idp, "idp[num_p]/I");
  tree_B_160->Branch("num_m", &num_m, "num_m/I");
  tree_B_160->Branch("num_p", &num_p, "num_p/I");
  tree_B_160->Branch("xim", xim, "xim[num_m]/F");
  tree_B_160->Branch("xip", xip, "xim[num_p]/F");
  tree_B_160->Branch("idm", idm, "idm[num_m]/I");
  tree_B_160->Branch("idp", idp, "idp[num_p]/I");

  tree_C_120->Branch("num_m", &num_m, "num_m/I");
  tree_C_120->Branch("num_p", &num_p, "num_p/I");
  tree_C_120->Branch("xim", xim, "xim[num_m]/F");
  tree_C_120->Branch("xip", xip, "xim[num_p]/F");
  tree_C_120->Branch("idm", idm, "idm[num_m]/I");
  tree_C_120->Branch("idp", idp, "idp[num_p]/I");
  tree_C_121->Branch("num_m", &num_m, "num_m/I");
  tree_C_121->Branch("num_p", &num_p, "num_p/I");
  tree_C_121->Branch("xim", xim, "xim[num_m]/F");
  tree_C_121->Branch("xip", xip, "xim[num_p]/F");
  tree_C_121->Branch("idm", idm, "idm[num_m]/I");
  tree_C_121->Branch("idp", idp, "idp[num_p]/I");
  tree_C_122->Branch("num_m", &num_m, "num_m/I");
  tree_C_122->Branch("num_p", &num_p, "num_p/I");
  tree_C_122->Branch("xim", xim, "xim[num_m]/F");
  tree_C_122->Branch("xip", xip, "xim[num_p]/F");
  tree_C_122->Branch("idm", idm, "idm[num_m]/I");
  tree_C_122->Branch("idp", idp, "idp[num_p]/I");
  tree_C_123->Branch("num_m", &num_m, "num_m/I");
  tree_C_123->Branch("num_p", &num_p, "num_p/I");
  tree_C_123->Branch("idm", idm, "idm[num_m]/I");
  tree_C_123->Branch("idp", idp, "idp[num_p]/I");
  tree_C_123->Branch("xim", xim, "xim[num_m]/F");
  tree_C_123->Branch("xip", xip, "xim[num_p]/F");
  tree_C_124->Branch("num_m", &num_m, "num_m/I");
  tree_C_124->Branch("num_p", &num_p, "num_p/I");
  tree_C_124->Branch("xim", xim, "xim[num_m]/F");
  tree_C_124->Branch("xip", xip, "xim[num_p]/F");
  tree_C_124->Branch("idm", idm, "idm[num_m]/I");
  tree_C_124->Branch("idp", idp, "idp[num_p]/I");
  tree_C_125->Branch("num_m", &num_m, "num_m/I");
  tree_C_125->Branch("num_p", &num_p, "num_p/I");
  tree_C_125->Branch("xim", xim, "xim[num_m]/F");
  tree_C_125->Branch("xip", xip, "xim[num_p]/F");
  tree_C_125->Branch("idm", idm, "idm[num_m]/I");
  tree_C_125->Branch("idp", idp, "idp[num_p]/I");
  tree_C_126->Branch("num_m", &num_m, "num_m/I");
  tree_C_126->Branch("num_p", &num_p, "num_p/I");
  tree_C_126->Branch("xim", xim, "xim[num_m]/F");
  tree_C_126->Branch("xip", xip, "xim[num_p]/F");
  tree_C_126->Branch("idm", idm, "idm[num_m]/I");
  tree_C_126->Branch("idp", idp, "idp[num_p]/I");
  tree_C_127->Branch("num_m", &num_m, "num_m/I");
  tree_C_127->Branch("num_p", &num_p, "num_p/I");
  tree_C_127->Branch("xim", xim, "xim[num_m]/F");
  tree_C_127->Branch("xip", xip, "xim[num_p]/F");
  tree_C_127->Branch("idm", idm, "idm[num_m]/I");
  tree_C_127->Branch("idp", idp, "idp[num_p]/I");
  tree_C_128->Branch("num_m", &num_m, "num_m/I");
  tree_C_128->Branch("num_p", &num_p, "num_p/I");
  tree_C_128->Branch("xim", xim, "xim[num_m]/F");
  tree_C_128->Branch("xip", xip, "xim[num_p]/F");
  tree_C_128->Branch("idm", idm, "idm[num_m]/I");
  tree_C_128->Branch("idp", idp, "idp[num_p]/I");
  tree_C_129->Branch("num_m", &num_m, "num_m/I");
  tree_C_129->Branch("num_p", &num_p, "num_p/I");
  tree_C_129->Branch("xim", xim, "xim[num_m]/F");
  tree_C_129->Branch("xip", xip, "xim[num_p]/F");
  tree_C_129->Branch("idm", idm, "idm[num_m]/I");
  tree_C_129->Branch("idp", idp, "idp[num_p]/I");
  tree_C_130->Branch("num_m", &num_m, "num_m/I");
  tree_C_130->Branch("num_p", &num_p, "num_p/I");
  tree_C_130->Branch("xim", xim, "xim[num_m]/F");
  tree_C_130->Branch("xip", xip, "xim[num_p]/F");
  tree_C_130->Branch("idm", idm, "idm[num_m]/I");
  tree_C_130->Branch("idp", idp, "idp[num_p]/I");
  tree_C_131->Branch("num_m", &num_m, "num_m/I");
  tree_C_131->Branch("num_p", &num_p, "num_p/I");
  tree_C_131->Branch("xim", xim, "xim[num_m]/F");
  tree_C_131->Branch("xip", xip, "xim[num_p]/F");
  tree_C_131->Branch("idm", idm, "idm[num_m]/I");
  tree_C_131->Branch("idp", idp, "idp[num_p]/I");
  tree_C_132->Branch("num_m", &num_m, "num_m/I");
  tree_C_132->Branch("num_p", &num_p, "num_p/I");
  tree_C_132->Branch("xim", xim, "xim[num_m]/F");
  tree_C_132->Branch("xip", xip, "xim[num_p]/F");
  tree_C_132->Branch("idm", idm, "idm[num_m]/I");
  tree_C_132->Branch("idp", idp, "idp[num_p]/I");
  tree_C_133->Branch("num_m", &num_m, "num_m/I");
  tree_C_133->Branch("num_p", &num_p, "num_p/I");
  tree_C_133->Branch("xim", xim, "xim[num_m]/F");
  tree_C_133->Branch("xip", xip, "xim[num_p]/F");
  tree_C_133->Branch("idm", idm, "idm[num_m]/I");
  tree_C_133->Branch("idp", idp, "idp[num_p]/I");
  tree_C_134->Branch("num_m", &num_m, "num_m/I");
  tree_C_134->Branch("num_p", &num_p, "num_p/I");
  tree_C_134->Branch("xim", xim, "xim[num_m]/F");
  tree_C_134->Branch("xip", xip, "xim[num_p]/F");
  tree_C_134->Branch("idm", idm, "idm[num_m]/I");
  tree_C_134->Branch("idp", idp, "idp[num_p]/I");
  tree_C_135->Branch("num_m", &num_m, "num_m/I");
  tree_C_135->Branch("num_p", &num_p, "num_p/I");
  tree_C_135->Branch("xim", xim, "xim[num_m]/F");
  tree_C_135->Branch("xip", xip, "xim[num_p]/F");
  tree_C_135->Branch("idm", idm, "idm[num_m]/I");
  tree_C_135->Branch("idp", idp, "idp[num_p]/I");
  tree_C_136->Branch("num_m", &num_m, "num_m/I");
  tree_C_136->Branch("num_p", &num_p, "num_p/I");
  tree_C_136->Branch("xim", xim, "xim[num_m]/F");
  tree_C_136->Branch("xip", xip, "xim[num_p]/F");
  tree_C_136->Branch("idm", idm, "idm[num_m]/I");
  tree_C_136->Branch("idp", idp, "idp[num_p]/I");
  tree_C_137->Branch("num_m", &num_m, "num_m/I");
  tree_C_137->Branch("num_p", &num_p, "num_p/I");
  tree_C_137->Branch("xim", xim, "xim[num_m]/F");
  tree_C_137->Branch("xip", xip, "xim[num_p]/F");
  tree_C_137->Branch("idm", idm, "idm[num_m]/I");
  tree_C_137->Branch("idp", idp, "idp[num_p]/I");
  tree_C_138->Branch("num_m", &num_m, "num_m/I");
  tree_C_138->Branch("num_p", &num_p, "num_p/I");
  tree_C_138->Branch("xim", xim, "xim[num_m]/F");
  tree_C_138->Branch("xip", xip, "xim[num_p]/F");
  tree_C_138->Branch("idm", idm, "idm[num_m]/I");
  tree_C_138->Branch("idp", idp, "idp[num_p]/I");
  tree_C_139->Branch("num_m", &num_m, "num_m/I");
  tree_C_139->Branch("num_p", &num_p, "num_p/I");
  tree_C_139->Branch("xim", xim, "xim[num_m]/F");
  tree_C_139->Branch("xip", xip, "xim[num_p]/F");
  tree_C_139->Branch("idm", idm, "idm[num_m]/I");
  tree_C_139->Branch("idp", idp, "idp[num_p]/I");
  tree_C_140->Branch("num_m", &num_m, "num_m/I");
  tree_C_140->Branch("num_p", &num_p, "num_p/I");
  tree_C_140->Branch("xim", xim, "xim[num_m]/F");
  tree_C_140->Branch("xip", xip, "xim[num_p]/F");
  tree_C_140->Branch("idm", idm, "idm[num_m]/I");
  tree_C_140->Branch("idp", idp, "idp[num_p]/I");
  tree_C_141->Branch("num_m", &num_m, "num_m/I");
  tree_C_141->Branch("num_p", &num_p, "num_p/I");
  tree_C_141->Branch("xim", xim, "xim[num_m]/F");
  tree_C_141->Branch("xip", xip, "xim[num_p]/F");
  tree_C_141->Branch("idm", idm, "idm[num_m]/I");
  tree_C_141->Branch("idp", idp, "idp[num_p]/I");
  tree_C_142->Branch("num_m", &num_m, "num_m/I");
  tree_C_142->Branch("num_p", &num_p, "num_p/I");
  tree_C_142->Branch("xim", xim, "xim[num_m]/F");
  tree_C_142->Branch("xip", xip, "xim[num_p]/F");
  tree_C_142->Branch("idm", idm, "idm[num_m]/I");
  tree_C_142->Branch("idp", idp, "idp[num_p]/I");
  tree_C_143->Branch("num_m", &num_m, "num_m/I");
  tree_C_143->Branch("num_p", &num_p, "num_p/I");
  tree_C_143->Branch("xim", xim, "xim[num_m]/F");
  tree_C_143->Branch("xip", xip, "xim[num_p]/F");
  tree_C_143->Branch("idm", idm, "idm[num_m]/I");
  tree_C_143->Branch("idp", idp, "idp[num_p]/I");
  tree_C_144->Branch("num_m", &num_m, "num_m/I");
  tree_C_144->Branch("num_p", &num_p, "num_p/I");
  tree_C_144->Branch("xim", xim, "xim[num_m]/F");
  tree_C_144->Branch("xip", xip, "xim[num_p]/F");
  tree_C_144->Branch("idm", idm, "idm[num_m]/I");
  tree_C_144->Branch("idp", idp, "idp[num_p]/I");
  tree_C_145->Branch("num_m", &num_m, "num_m/I");
  tree_C_145->Branch("num_p", &num_p, "num_p/I");
  tree_C_145->Branch("xim", xim, "xim[num_m]/F");
  tree_C_145->Branch("xip", xip, "xim[num_p]/F");
  tree_C_145->Branch("idm", idm, "idm[num_m]/I");
  tree_C_145->Branch("idp", idp, "idp[num_p]/I");
  tree_C_146->Branch("num_m", &num_m, "num_m/I");
  tree_C_146->Branch("num_p", &num_p, "num_p/I");
  tree_C_146->Branch("xim", xim, "xim[num_m]/F");
  tree_C_146->Branch("xip", xip, "xim[num_p]/F");
  tree_C_146->Branch("idm", idm, "idm[num_m]/I");
  tree_C_146->Branch("idp", idp, "idp[num_p]/I");
  tree_C_147->Branch("num_m", &num_m, "num_m/I");
  tree_C_147->Branch("num_p", &num_p, "num_p/I");
  tree_C_147->Branch("xim", xim, "xim[num_m]/F");
  tree_C_147->Branch("xip", xip, "xim[num_p]/F");
  tree_C_147->Branch("idm", idm, "idm[num_m]/I");
  tree_C_147->Branch("idp", idp, "idp[num_p]/I");
  tree_C_148->Branch("num_m", &num_m, "num_m/I");
  tree_C_148->Branch("num_p", &num_p, "num_p/I");
  tree_C_148->Branch("xim", xim, "xim[num_m]/F");
  tree_C_148->Branch("xip", xip, "xim[num_p]/F");
  tree_C_148->Branch("idm", idm, "idm[num_m]/I");
  tree_C_148->Branch("idp", idp, "idp[num_p]/I");
  tree_C_149->Branch("num_m", &num_m, "num_m/I");
  tree_C_149->Branch("num_p", &num_p, "num_p/I");
  tree_C_149->Branch("xim", xim, "xim[num_m]/F");
  tree_C_149->Branch("xip", xip, "xim[num_p]/F");
  tree_C_149->Branch("idm", idm, "idm[num_m]/I");
  tree_C_149->Branch("idp", idp, "idp[num_p]/I");
  tree_C_150->Branch("num_m", &num_m, "num_m/I");
  tree_C_150->Branch("num_p", &num_p, "num_p/I");
  tree_C_150->Branch("xim", xim, "xim[num_m]/F");
  tree_C_150->Branch("xip", xip, "xim[num_p]/F");
  tree_C_150->Branch("idm", idm, "idm[num_m]/I");
  tree_C_150->Branch("idp", idp, "idp[num_p]/I");
  tree_C_151->Branch("num_m", &num_m, "num_m/I");
  tree_C_151->Branch("num_p", &num_p, "num_p/I");
  tree_C_151->Branch("xim", xim, "xim[num_m]/F");
  tree_C_151->Branch("xip", xip, "xim[num_p]/F");
  tree_C_151->Branch("idm", idm, "idm[num_m]/I");
  tree_C_151->Branch("idp", idp, "idp[num_p]/I");
  tree_C_152->Branch("num_m", &num_m, "num_m/I");
  tree_C_152->Branch("num_p", &num_p, "num_p/I");
  tree_C_152->Branch("xim", xim, "xim[num_m]/F");
  tree_C_152->Branch("xip", xip, "xim[num_p]/F");
  tree_C_152->Branch("idm", idm, "idm[num_m]/I");
  tree_C_152->Branch("idp", idp, "idp[num_p]/I");
  tree_C_153->Branch("num_m", &num_m, "num_m/I");
  tree_C_153->Branch("num_p", &num_p, "num_p/I");
  tree_C_153->Branch("xim", xim, "xim[num_m]/F");
  tree_C_153->Branch("xip", xip, "xim[num_p]/F");
  tree_C_153->Branch("idm", idm, "idm[num_m]/I");
  tree_C_153->Branch("idp", idp, "idp[num_p]/I");
  tree_C_154->Branch("num_m", &num_m, "num_m/I");
  tree_C_154->Branch("num_p", &num_p, "num_p/I");
  tree_C_154->Branch("xim", xim, "xim[num_m]/F");
  tree_C_154->Branch("xip", xip, "xim[num_p]/F");
  tree_C_154->Branch("idm", idm, "idm[num_m]/I");
  tree_C_154->Branch("idp", idp, "idp[num_p]/I");
  tree_C_155->Branch("num_m", &num_m, "num_m/I");
  tree_C_155->Branch("num_p", &num_p, "num_p/I");
  tree_C_155->Branch("xim", xim, "xim[num_m]/F");
  tree_C_155->Branch("xip", xip, "xim[num_p]/F");
  tree_C_155->Branch("idm", idm, "idm[num_m]/I");
  tree_C_155->Branch("idp", idp, "idp[num_p]/I");
  tree_C_156->Branch("num_m", &num_m, "num_m/I");
  tree_C_156->Branch("num_p", &num_p, "num_p/I");
  tree_C_156->Branch("xim", xim, "xim[num_m]/F");
  tree_C_156->Branch("xip", xip, "xim[num_p]/F");
  tree_C_156->Branch("idm", idm, "idm[num_m]/I");
  tree_C_156->Branch("idp", idp, "idp[num_p]/I");
  tree_C_157->Branch("num_m", &num_m, "num_m/I");
  tree_C_157->Branch("num_p", &num_p, "num_p/I");
  tree_C_157->Branch("xim", xim, "xim[num_m]/F");
  tree_C_157->Branch("xip", xip, "xim[num_p]/F");
  tree_C_157->Branch("idm", idm, "idm[num_m]/I");
  tree_C_157->Branch("idp", idp, "idp[num_p]/I");
  tree_C_158->Branch("num_m", &num_m, "num_m/I");
  tree_C_158->Branch("num_p", &num_p, "num_p/I");
  tree_C_158->Branch("xim", xim, "xim[num_m]/F");
  tree_C_158->Branch("xip", xip, "xim[num_p]/F");
  tree_C_158->Branch("idm", idm, "idm[num_m]/I");
  tree_C_158->Branch("idp", idp, "idp[num_p]/I");
  tree_C_159->Branch("num_m", &num_m, "num_m/I");
  tree_C_159->Branch("num_p", &num_p, "num_p/I");
  tree_C_159->Branch("xim", xim, "xim[num_m]/F");
  tree_C_159->Branch("xip", xip, "xim[num_p]/F");
  tree_C_159->Branch("idm", idm, "idm[num_m]/I");
  tree_C_159->Branch("idp", idp, "idp[num_p]/I");
  tree_C_160->Branch("num_m", &num_m, "num_m/I");
  tree_C_160->Branch("num_p", &num_p, "num_p/I");
  tree_C_160->Branch("xim", xim, "xim[num_m]/F");
  tree_C_160->Branch("xip", xip, "xim[num_p]/F");
  tree_C_160->Branch("idm", idm, "idm[num_m]/I");
  tree_C_160->Branch("idp", idp, "idp[num_p]/I");

  tree_D_120->Branch("num_m", &num_m, "num_m/I");
  tree_D_120->Branch("num_p", &num_p, "num_p/I");
  tree_D_120->Branch("xim", xim, "xim[num_m]/F");
  tree_D_120->Branch("xip", xip, "xim[num_p]/F");
  tree_D_120->Branch("idm", idm, "idm[num_m]/I");
  tree_D_120->Branch("idp", idp, "idp[num_p]/I");
  tree_D_121->Branch("num_m", &num_m, "num_m/I");
  tree_D_121->Branch("num_p", &num_p, "num_p/I");
  tree_D_121->Branch("xim", xim, "xim[num_m]/F");
  tree_D_121->Branch("xip", xip, "xim[num_p]/F");
  tree_D_121->Branch("idm", idm, "idm[num_m]/I");
  tree_D_121->Branch("idp", idp, "idp[num_p]/I");
  tree_D_122->Branch("num_m", &num_m, "num_m/I");
  tree_D_122->Branch("num_p", &num_p, "num_p/I");
  tree_D_122->Branch("xim", xim, "xim[num_m]/F");
  tree_D_122->Branch("xip", xip, "xim[num_p]/F");
  tree_D_122->Branch("idm", idm, "idm[num_m]/I");
  tree_D_122->Branch("idp", idp, "idp[num_p]/I");
  tree_D_123->Branch("num_m", &num_m, "num_m/I");
  tree_D_123->Branch("num_p", &num_p, "num_p/I");
  tree_D_123->Branch("idm", idm, "idm[num_m]/I");
  tree_D_123->Branch("idp", idp, "idp[num_p]/I");
  tree_D_123->Branch("xim", xim, "xim[num_m]/F");
  tree_D_123->Branch("xip", xip, "xim[num_p]/F");
  tree_D_124->Branch("num_m", &num_m, "num_m/I");
  tree_D_124->Branch("num_p", &num_p, "num_p/I");
  tree_D_124->Branch("xim", xim, "xim[num_m]/F");
  tree_D_124->Branch("xip", xip, "xim[num_p]/F");
  tree_D_124->Branch("idm", idm, "idm[num_m]/I");
  tree_D_124->Branch("idp", idp, "idp[num_p]/I");
  tree_D_125->Branch("num_m", &num_m, "num_m/I");
  tree_D_125->Branch("num_p", &num_p, "num_p/I");
  tree_D_125->Branch("xim", xim, "xim[num_m]/F");
  tree_D_125->Branch("xip", xip, "xim[num_p]/F");
  tree_D_125->Branch("idm", idm, "idm[num_m]/I");
  tree_D_125->Branch("idp", idp, "idp[num_p]/I");
  tree_D_126->Branch("num_m", &num_m, "num_m/I");
  tree_D_126->Branch("num_p", &num_p, "num_p/I");
  tree_D_126->Branch("xim", xim, "xim[num_m]/F");
  tree_D_126->Branch("xip", xip, "xim[num_p]/F");
  tree_D_126->Branch("idm", idm, "idm[num_m]/I");
  tree_D_126->Branch("idp", idp, "idp[num_p]/I");
  tree_D_127->Branch("num_m", &num_m, "num_m/I");
  tree_D_127->Branch("num_p", &num_p, "num_p/I");
  tree_D_127->Branch("xim", xim, "xim[num_m]/F");
  tree_D_127->Branch("xip", xip, "xim[num_p]/F");
  tree_D_127->Branch("idm", idm, "idm[num_m]/I");
  tree_D_127->Branch("idp", idp, "idp[num_p]/I");
  tree_D_128->Branch("num_m", &num_m, "num_m/I");
  tree_D_128->Branch("num_p", &num_p, "num_p/I");
  tree_D_128->Branch("xim", xim, "xim[num_m]/F");
  tree_D_128->Branch("xip", xip, "xim[num_p]/F");
  tree_D_128->Branch("idm", idm, "idm[num_m]/I");
  tree_D_128->Branch("idp", idp, "idp[num_p]/I");
  tree_D_129->Branch("num_m", &num_m, "num_m/I");
  tree_D_129->Branch("num_p", &num_p, "num_p/I");
  tree_D_129->Branch("xim", xim, "xim[num_m]/F");
  tree_D_129->Branch("xip", xip, "xim[num_p]/F");
  tree_D_129->Branch("idm", idm, "idm[num_m]/I");
  tree_D_129->Branch("idp", idp, "idp[num_p]/I");
  tree_D_130->Branch("num_m", &num_m, "num_m/I");
  tree_D_130->Branch("num_p", &num_p, "num_p/I");
  tree_D_130->Branch("xim", xim, "xim[num_m]/F");
  tree_D_130->Branch("xip", xip, "xim[num_p]/F");
  tree_D_130->Branch("idm", idm, "idm[num_m]/I");
  tree_D_130->Branch("idp", idp, "idp[num_p]/I");
  tree_D_131->Branch("num_m", &num_m, "num_m/I");
  tree_D_131->Branch("num_p", &num_p, "num_p/I");
  tree_D_131->Branch("xim", xim, "xim[num_m]/F");
  tree_D_131->Branch("xip", xip, "xim[num_p]/F");
  tree_D_131->Branch("idm", idm, "idm[num_m]/I");
  tree_D_131->Branch("idp", idp, "idp[num_p]/I");
  tree_D_132->Branch("num_m", &num_m, "num_m/I");
  tree_D_132->Branch("num_p", &num_p, "num_p/I");
  tree_D_132->Branch("xim", xim, "xim[num_m]/F");
  tree_D_132->Branch("xip", xip, "xim[num_p]/F");
  tree_D_132->Branch("idm", idm, "idm[num_m]/I");
  tree_D_132->Branch("idp", idp, "idp[num_p]/I");
  tree_D_133->Branch("num_m", &num_m, "num_m/I");
  tree_D_133->Branch("num_p", &num_p, "num_p/I");
  tree_D_133->Branch("xim", xim, "xim[num_m]/F");
  tree_D_133->Branch("xip", xip, "xim[num_p]/F");
  tree_D_133->Branch("idm", idm, "idm[num_m]/I");
  tree_D_133->Branch("idp", idp, "idp[num_p]/I");
  tree_D_134->Branch("num_m", &num_m, "num_m/I");
  tree_D_134->Branch("num_p", &num_p, "num_p/I");
  tree_D_134->Branch("xim", xim, "xim[num_m]/F");
  tree_D_134->Branch("xip", xip, "xim[num_p]/F");
  tree_D_134->Branch("idm", idm, "idm[num_m]/I");
  tree_D_134->Branch("idp", idp, "idp[num_p]/I");
  tree_D_135->Branch("num_m", &num_m, "num_m/I");
  tree_D_135->Branch("num_p", &num_p, "num_p/I");
  tree_D_135->Branch("xim", xim, "xim[num_m]/F");
  tree_D_135->Branch("xip", xip, "xim[num_p]/F");
  tree_D_135->Branch("idm", idm, "idm[num_m]/I");
  tree_D_135->Branch("idp", idp, "idp[num_p]/I");
  tree_D_136->Branch("num_m", &num_m, "num_m/I");
  tree_D_136->Branch("num_p", &num_p, "num_p/I");
  tree_D_136->Branch("xim", xim, "xim[num_m]/F");
  tree_D_136->Branch("xip", xip, "xim[num_p]/F");
  tree_D_136->Branch("idm", idm, "idm[num_m]/I");
  tree_D_136->Branch("idp", idp, "idp[num_p]/I");
  tree_D_137->Branch("num_m", &num_m, "num_m/I");
  tree_D_137->Branch("num_p", &num_p, "num_p/I");
  tree_D_137->Branch("xim", xim, "xim[num_m]/F");
  tree_D_137->Branch("xip", xip, "xim[num_p]/F");
  tree_D_137->Branch("idm", idm, "idm[num_m]/I");
  tree_D_137->Branch("idp", idp, "idp[num_p]/I");
  tree_D_138->Branch("num_m", &num_m, "num_m/I");
  tree_D_138->Branch("num_p", &num_p, "num_p/I");
  tree_D_138->Branch("xim", xim, "xim[num_m]/F");
  tree_D_138->Branch("xip", xip, "xim[num_p]/F");
  tree_D_138->Branch("idm", idm, "idm[num_m]/I");
  tree_D_138->Branch("idp", idp, "idp[num_p]/I");
  tree_D_139->Branch("num_m", &num_m, "num_m/I");
  tree_D_139->Branch("num_p", &num_p, "num_p/I");
  tree_D_139->Branch("xim", xim, "xim[num_m]/F");
  tree_D_139->Branch("xip", xip, "xim[num_p]/F");
  tree_D_139->Branch("idm", idm, "idm[num_m]/I");
  tree_D_139->Branch("idp", idp, "idp[num_p]/I");
  tree_D_140->Branch("num_m", &num_m, "num_m/I");
  tree_D_140->Branch("num_p", &num_p, "num_p/I");
  tree_D_140->Branch("xim", xim, "xim[num_m]/F");
  tree_D_140->Branch("xip", xip, "xim[num_p]/F");
  tree_D_140->Branch("idm", idm, "idm[num_m]/I");
  tree_D_140->Branch("idp", idp, "idp[num_p]/I");
  tree_D_141->Branch("num_m", &num_m, "num_m/I");
  tree_D_141->Branch("num_p", &num_p, "num_p/I");
  tree_D_141->Branch("xim", xim, "xim[num_m]/F");
  tree_D_141->Branch("xip", xip, "xim[num_p]/F");
  tree_D_141->Branch("idm", idm, "idm[num_m]/I");
  tree_D_141->Branch("idp", idp, "idp[num_p]/I");
  tree_D_142->Branch("num_m", &num_m, "num_m/I");
  tree_D_142->Branch("num_p", &num_p, "num_p/I");
  tree_D_142->Branch("xim", xim, "xim[num_m]/F");
  tree_D_142->Branch("xip", xip, "xim[num_p]/F");
  tree_D_142->Branch("idm", idm, "idm[num_m]/I");
  tree_D_142->Branch("idp", idp, "idp[num_p]/I");
  tree_D_143->Branch("num_m", &num_m, "num_m/I");
  tree_D_143->Branch("num_p", &num_p, "num_p/I");
  tree_D_143->Branch("xim", xim, "xim[num_m]/F");
  tree_D_143->Branch("xip", xip, "xim[num_p]/F");
  tree_D_143->Branch("idm", idm, "idm[num_m]/I");
  tree_D_143->Branch("idp", idp, "idp[num_p]/I");
  tree_D_144->Branch("num_m", &num_m, "num_m/I");
  tree_D_144->Branch("num_p", &num_p, "num_p/I");
  tree_D_144->Branch("xim", xim, "xim[num_m]/F");
  tree_D_144->Branch("xip", xip, "xim[num_p]/F");
  tree_D_144->Branch("idm", idm, "idm[num_m]/I");
  tree_D_144->Branch("idp", idp, "idp[num_p]/I");
  tree_D_145->Branch("num_m", &num_m, "num_m/I");
  tree_D_145->Branch("num_p", &num_p, "num_p/I");
  tree_D_145->Branch("xim", xim, "xim[num_m]/F");
  tree_D_145->Branch("xip", xip, "xim[num_p]/F");
  tree_D_145->Branch("idm", idm, "idm[num_m]/I");
  tree_D_145->Branch("idp", idp, "idp[num_p]/I");
  tree_D_146->Branch("num_m", &num_m, "num_m/I");
  tree_D_146->Branch("num_p", &num_p, "num_p/I");
  tree_D_146->Branch("xim", xim, "xim[num_m]/F");
  tree_D_146->Branch("xip", xip, "xim[num_p]/F");
  tree_D_146->Branch("idm", idm, "idm[num_m]/I");
  tree_D_146->Branch("idp", idp, "idp[num_p]/I");
  tree_D_147->Branch("num_m", &num_m, "num_m/I");
  tree_D_147->Branch("num_p", &num_p, "num_p/I");
  tree_D_147->Branch("xim", xim, "xim[num_m]/F");
  tree_D_147->Branch("xip", xip, "xim[num_p]/F");
  tree_D_147->Branch("idm", idm, "idm[num_m]/I");
  tree_D_147->Branch("idp", idp, "idp[num_p]/I");
  tree_D_148->Branch("num_m", &num_m, "num_m/I");
  tree_D_148->Branch("num_p", &num_p, "num_p/I");
  tree_D_148->Branch("xim", xim, "xim[num_m]/F");
  tree_D_148->Branch("xip", xip, "xim[num_p]/F");
  tree_D_148->Branch("idm", idm, "idm[num_m]/I");
  tree_D_148->Branch("idp", idp, "idp[num_p]/I");
  tree_D_149->Branch("num_m", &num_m, "num_m/I");
  tree_D_149->Branch("num_p", &num_p, "num_p/I");
  tree_D_149->Branch("xim", xim, "xim[num_m]/F");
  tree_D_149->Branch("xip", xip, "xim[num_p]/F");
  tree_D_149->Branch("idm", idm, "idm[num_m]/I");
  tree_D_149->Branch("idp", idp, "idp[num_p]/I");
  tree_D_150->Branch("num_m", &num_m, "num_m/I");
  tree_D_150->Branch("num_p", &num_p, "num_p/I");
  tree_D_150->Branch("xim", xim, "xim[num_m]/F");
  tree_D_150->Branch("xip", xip, "xim[num_p]/F");
  tree_D_150->Branch("idm", idm, "idm[num_m]/I");
  tree_D_150->Branch("idp", idp, "idp[num_p]/I");
  tree_D_151->Branch("num_m", &num_m, "num_m/I");
  tree_D_151->Branch("num_p", &num_p, "num_p/I");
  tree_D_151->Branch("xim", xim, "xim[num_m]/F");
  tree_D_151->Branch("xip", xip, "xim[num_p]/F");
  tree_D_151->Branch("idm", idm, "idm[num_m]/I");
  tree_D_151->Branch("idp", idp, "idp[num_p]/I");
  tree_D_152->Branch("num_m", &num_m, "num_m/I");
  tree_D_152->Branch("num_p", &num_p, "num_p/I");
  tree_D_152->Branch("xim", xim, "xim[num_m]/F");
  tree_D_152->Branch("xip", xip, "xim[num_p]/F");
  tree_D_152->Branch("idm", idm, "idm[num_m]/I");
  tree_D_152->Branch("idp", idp, "idp[num_p]/I");
  tree_D_153->Branch("num_m", &num_m, "num_m/I");
  tree_D_153->Branch("num_p", &num_p, "num_p/I");
  tree_D_153->Branch("xim", xim, "xim[num_m]/F");
  tree_D_153->Branch("xip", xip, "xim[num_p]/F");
  tree_D_153->Branch("idm", idm, "idm[num_m]/I");
  tree_D_153->Branch("idp", idp, "idp[num_p]/I");
  tree_D_154->Branch("num_m", &num_m, "num_m/I");
  tree_D_154->Branch("num_p", &num_p, "num_p/I");
  tree_D_154->Branch("xim", xim, "xim[num_m]/F");
  tree_D_154->Branch("xip", xip, "xim[num_p]/F");
  tree_D_154->Branch("idm", idm, "idm[num_m]/I");
  tree_D_154->Branch("idp", idp, "idp[num_p]/I");
  tree_D_155->Branch("num_m", &num_m, "num_m/I");
  tree_D_155->Branch("num_p", &num_p, "num_p/I");
  tree_D_155->Branch("xim", xim, "xim[num_m]/F");
  tree_D_155->Branch("xip", xip, "xim[num_p]/F");
  tree_D_155->Branch("idm", idm, "idm[num_m]/I");
  tree_D_155->Branch("idp", idp, "idp[num_p]/I");
  tree_D_156->Branch("num_m", &num_m, "num_m/I");
  tree_D_156->Branch("num_p", &num_p, "num_p/I");
  tree_D_156->Branch("xim", xim, "xim[num_m]/F");
  tree_D_156->Branch("xip", xip, "xim[num_p]/F");
  tree_D_156->Branch("idm", idm, "idm[num_m]/I");
  tree_D_156->Branch("idp", idp, "idp[num_p]/I");
  tree_D_157->Branch("num_m", &num_m, "num_m/I");
  tree_D_157->Branch("num_p", &num_p, "num_p/I");
  tree_D_157->Branch("xim", xim, "xim[num_m]/F");
  tree_D_157->Branch("xip", xip, "xim[num_p]/F");
  tree_D_157->Branch("idm", idm, "idm[num_m]/I");
  tree_D_157->Branch("idp", idp, "idp[num_p]/I");
  tree_D_158->Branch("num_m", &num_m, "num_m/I");
  tree_D_158->Branch("num_p", &num_p, "num_p/I");
  tree_D_158->Branch("xim", xim, "xim[num_m]/F");
  tree_D_158->Branch("xip", xip, "xim[num_p]/F");
  tree_D_158->Branch("idm", idm, "idm[num_m]/I");
  tree_D_158->Branch("idp", idp, "idp[num_p]/I");
  tree_D_159->Branch("num_m", &num_m, "num_m/I");
  tree_D_159->Branch("num_p", &num_p, "num_p/I");
  tree_D_159->Branch("xim", xim, "xim[num_m]/F");
  tree_D_159->Branch("xip", xip, "xim[num_p]/F");
  tree_D_159->Branch("idm", idm, "idm[num_m]/I");
  tree_D_159->Branch("idp", idp, "idp[num_p]/I");
  tree_D_160->Branch("num_m", &num_m, "num_m/I");
  tree_D_160->Branch("num_p", &num_p, "num_p/I");
  tree_D_160->Branch("xim", xim, "xim[num_m]/F");
  tree_D_160->Branch("xip", xip, "xim[num_p]/F");
  tree_D_160->Branch("idm", idm, "idm[num_m]/I");
  tree_D_160->Branch("idp", idp, "idp[num_p]/I");
  //

  /* 2017
  tree_B_120->Branch("num_m", &num_m, "num_m/I");
  tree_B_120->Branch("num_p", &num_p, "num_p/I");
  tree_B_120->Branch("xim", xim, "xim[num_m]/F");
  tree_B_120->Branch("xip", xip, "xim[num_p]/F");
  tree_B_120->Branch("idm", idm, "idm[num_m]/I");
  tree_B_120->Branch("idp", idp, "idp[num_p]/I");
  tree_B_130->Branch("num_m", &num_m, "num_m/I");
  tree_B_130->Branch("num_p", &num_p, "num_p/I");
  tree_B_130->Branch("xim", xim, "xim[num_m]/F");
  tree_B_130->Branch("xip", xip, "xim[num_p]/F");
  tree_B_130->Branch("idm", idm, "idm[num_m]/I");
  tree_B_130->Branch("idp", idp, "idp[num_p]/I");
  tree_B_140->Branch("num_m", &num_m, "num_m/I");
  tree_B_140->Branch("num_p", &num_p, "num_p/I");
  tree_B_140->Branch("xim", xim, "xim[num_m]/F");
  tree_B_140->Branch("xip", xip, "xim[num_p]/F");
  tree_B_140->Branch("idm", idm, "idm[num_m]/I");
  tree_B_140->Branch("idp", idp, "idp[num_p]/I");
  tree_B_150->Branch("num_m", &num_m, "num_m/I");
  tree_B_150->Branch("num_p", &num_p, "num_p/I");
  tree_B_150->Branch("xim", xim, "xim[num_m]/F");
  tree_B_150->Branch("xip", xip, "xim[num_p]/F");
  tree_B_150->Branch("idm", idm, "idm[num_m]/I");
  tree_B_150->Branch("idp", idp, "idp[num_p]/I");

  tree_C_120->Branch("num_m", &num_m, "num_m/I");
  tree_C_120->Branch("num_p", &num_p, "num_p/I");
  tree_C_120->Branch("xim", xim, "xim[num_m]/F");
  tree_C_120->Branch("xip", xip, "xim[num_p]/F");
  tree_C_120->Branch("idm", idm, "idm[num_m]/I");
  tree_C_120->Branch("idp", idp, "idp[num_p]/I");
  tree_C_130->Branch("num_m", &num_m, "num_m/I");
  tree_C_130->Branch("num_p", &num_p, "num_p/I");
  tree_C_130->Branch("xim", xim, "xim[num_m]/F");
  tree_C_130->Branch("xip", xip, "xim[num_p]/F");
  tree_C_130->Branch("idm", idm, "idm[num_m]/I");
  tree_C_130->Branch("idp", idp, "idp[num_p]/I");
  tree_C_140->Branch("num_m", &num_m, "num_m/I");
  tree_C_140->Branch("num_p", &num_p, "num_p/I");
  tree_C_140->Branch("xim", xim, "xim[num_m]/F");
  tree_C_140->Branch("xip", xip, "xim[num_p]/F");
  tree_C_140->Branch("idm", idm, "idm[num_m]/I");
  tree_C_140->Branch("idp", idp, "idp[num_p]/I");
  tree_C_150->Branch("num_m", &num_m, "num_m/I");
  tree_C_150->Branch("num_p", &num_p, "num_p/I");
  tree_C_150->Branch("xim", xim, "xim[num_m]/F");
  tree_C_150->Branch("xip", xip, "xim[num_p]/F");
  tree_C_150->Branch("idm", idm, "idm[num_m]/I");
  tree_C_150->Branch("idp", idp, "idp[num_p]/I");

  tree_D_120->Branch("num_m", &num_m, "num_m/I");
  tree_D_120->Branch("num_p", &num_p, "num_p/I");
  tree_D_120->Branch("xim", xim, "xim[num_m]/F");
  tree_D_120->Branch("xip", xip, "xim[num_p]/F");
  tree_D_120->Branch("idm", idm, "idm[num_m]/I");
  tree_D_120->Branch("idp", idp, "idp[num_p]/I");
  tree_D_130->Branch("num_m", &num_m, "num_m/I");
  tree_D_130->Branch("num_p", &num_p, "num_p/I");
  tree_D_130->Branch("xim", xim, "xim[num_m]/F");
  tree_D_130->Branch("xip", xip, "xim[num_p]/F");
  tree_D_130->Branch("idm", idm, "idm[num_m]/I");
  tree_D_130->Branch("idp", idp, "idp[num_p]/I");
  tree_D_140->Branch("num_m", &num_m, "num_m/I");
  tree_D_140->Branch("num_p", &num_p, "num_p/I");
  tree_D_140->Branch("xim", xim, "xim[num_m]/F");
  tree_D_140->Branch("xip", xip, "xim[num_p]/F");
  tree_D_140->Branch("idm", idm, "idm[num_m]/I");
  tree_D_140->Branch("idp", idp, "idp[num_p]/I");
  tree_D_150->Branch("num_m", &num_m, "num_m/I");
  tree_D_150->Branch("num_p", &num_p, "num_p/I");
  tree_D_150->Branch("xim", xim, "xim[num_m]/F");
  tree_D_150->Branch("xip", xip, "xim[num_p]/F");
  tree_D_150->Branch("idm", idm, "idm[num_m]/I");
  tree_D_150->Branch("idp", idp, "idp[num_p]/I");

  tree_E_120->Branch("num_m", &num_m, "num_m/I");
  tree_E_120->Branch("num_p", &num_p, "num_p/I");
  tree_E_120->Branch("xim", xim, "xim[num_m]/F");
  tree_E_120->Branch("xip", xip, "xim[num_p]/F");
  tree_E_120->Branch("idm", idm, "idm[num_m]/I");
  tree_E_120->Branch("idp", idp, "idp[num_p]/I");
  tree_E_130->Branch("num_m", &num_m, "num_m/I");
  tree_E_130->Branch("num_p", &num_p, "num_p/I");
  tree_E_130->Branch("xim", xim, "xim[num_m]/F");
  tree_E_130->Branch("xip", xip, "xim[num_p]/F");
  tree_E_130->Branch("idm", idm, "idm[num_m]/I");
  tree_E_130->Branch("idp", idp, "idp[num_p]/I");
  tree_E_140->Branch("num_m", &num_m, "num_m/I");
  tree_E_140->Branch("num_p", &num_p, "num_p/I");
  tree_E_140->Branch("xim", xim, "xim[num_m]/F");
  tree_E_140->Branch("xip", xip, "xim[num_p]/F");
  tree_E_140->Branch("idm", idm, "idm[num_m]/I");
  tree_E_140->Branch("idp", idp, "idp[num_p]/I");
  tree_E_150->Branch("num_m", &num_m, "num_m/I");
  tree_E_150->Branch("num_p", &num_p, "num_p/I");
  tree_E_150->Branch("xim", xim, "xim[num_m]/F");
  tree_E_150->Branch("xip", xip, "xim[num_p]/F");
  tree_E_150->Branch("idm", idm, "idm[num_m]/I");
  tree_E_150->Branch("idp", idp, "idp[num_p]/I");

  tree_F_120->Branch("num_m", &num_m, "num_m/I");
  tree_F_120->Branch("num_p", &num_p, "num_p/I");
  tree_F_120->Branch("xim", xim, "xim[num_m]/F");
  tree_F_120->Branch("xip", xip, "xim[num_p]/F");
  tree_F_120->Branch("idm", idm, "idm[num_m]/I");
  tree_F_120->Branch("idp", idp, "idp[num_p]/I");
  tree_F_130->Branch("num_m", &num_m, "num_m/I");
  tree_F_130->Branch("num_p", &num_p, "num_p/I");
  tree_F_130->Branch("xim", xim, "xim[num_m]/F");
  tree_F_130->Branch("xip", xip, "xim[num_p]/F");
  tree_F_130->Branch("idm", idm, "idm[num_m]/I");
  tree_F_130->Branch("idp", idp, "idp[num_p]/I");
  tree_F_140->Branch("num_m", &num_m, "num_m/I");
  tree_F_140->Branch("num_p", &num_p, "num_p/I");
  tree_F_140->Branch("xim", xim, "xim[num_m]/F");
  tree_F_140->Branch("xip", xip, "xim[num_p]/F");
  tree_F_140->Branch("idm", idm, "idm[num_m]/I");
  tree_F_140->Branch("idp", idp, "idp[num_p]/I");
  tree_F_150->Branch("num_m", &num_m, "num_m/I");
  tree_F_150->Branch("num_p", &num_p, "num_p/I");
  tree_F_150->Branch("xim", xim, "xim[num_m]/F");
  tree_F_150->Branch("xip", xip, "xim[num_p]/F");
  tree_F_150->Branch("idm", idm, "idm[num_m]/I");
  tree_F_150->Branch("idp", idp, "idp[num_p]/I");
  */

  /* 2016
  tree_B->Branch("num_m", &num_m, "num_m/I");
  tree_B->Branch("num_p", &num_p, "num_p/I");
  tree_B->Branch("xim", xim, "xim[num_m]/F");
  tree_B->Branch("xip", xip, "xim[num_p]/F");

  tree_C->Branch("num_m", &num_m, "num_m/I");
  tree_C->Branch("num_p", &num_p, "num_p/I");
  tree_C->Branch("xim", xim, "xim[num_m]/F");
  tree_C->Branch("xip", xip, "xim[num_p]/F");

  tree_G->Branch("num_m", &num_m, "num_m/I");
  tree_G->Branch("num_p", &num_p, "num_p/I");
  tree_G->Branch("xim", xim, "xim[num_m]/F");
  tree_G->Branch("xip", xip, "xim[num_p]/F");
  */

  TChain chain("Events");

  /*
  chain.Add( "Skims/2016/nanoAOD_Run2016B_Skim.root" );
  chain.Add( "Skims/2016/nanoAOD_Run2016C_Skim.root" );
  chain.Add( "Skims/2016/nanoAOD_Run2016G_Skim.root" );
  */

  /*
  chain.Add( "Skims/2017/nanoAOD_Run2017B_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017C_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017D_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017E_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017F_Skim.root" );
  */

  //
  chain.Add( "Skims/2018/nanoAOD_Run2018A_Skim.root" );
  chain.Add( "Skims/2018/nanoAOD_Run2018B_Skim.root" );
  chain.Add( "Skims/2018/nanoAOD_Run2018C_Skim.root" );
  chain.Add( "Skims/2018/nanoAOD_Run2018D_Skim.root" );
  //

  unsigned int run, event, num_proton, num_trk;
  float crossingAngle;
  const unsigned short maxPro = 31;
  const unsigned short maxTrk = 31;
  float proton_xi[maxPro], thetaX[maxPro];
  bool sector45[maxPro];
  float trackX[maxTrk], trackY[maxTrk];
  int decRPId[maxTrk], trkIdx[maxTrk];

  chain.SetBranchAddress( "run", &run );
  chain.SetBranchAddress( "LHCInfo_crossingAngle", &crossingAngle );

  chain.SetBranchAddress( "nProton_singleRP", &num_proton );
  chain.SetBranchAddress( "Proton_singleRP_xi", proton_xi );
  chain.SetBranchAddress( "Proton_singleRP_sector45", sector45 );
  chain.SetBranchAddress( "PPSLocalTrack_singleRPProtonIdx", trkIdx );

  //chain.SetBranchAddress( "nProton_multiRP", &num_proton );
  //chain.SetBranchAddress( "Proton_multiRP_xi", proton_xi );
  //chain.SetBranchAddress( "Proton_multiRP_sector45", sector45 );
  //chain.SetBranchAddress( "Proton_multiRP_thetaX", thetaX );
  //chain.SetBranchAddress( "PPSLocalTrack_multiRPProtonIdx", trkIdx );

  chain.SetBranchAddress( "nPPSLocalTrack", &num_trk );
  chain.SetBranchAddress( "PPSLocalTrack_x", trackX );
  chain.SetBranchAddress( "PPSLocalTrack_y", trackY );
  chain.SetBranchAddress( "PPSLocalTrack_decRPId", decRPId );


  unsigned int entries = chain.GetEntries();
  std::cout << "Entries: " << entries << std::endl;
  unsigned int denom = round(entries/100);
  float progress = 0.00;
  int barWidth = 70;

  for ( unsigned int i=0; i<entries; i++ ) { // Loop over entries

    chain.GetEntry( i );
    
    if ( i%denom == 0 ) {
	std::cout << "[";
	int pos = barWidth * progress;
	for (int i = 0; i < barWidth; ++i) {
	  if (i < pos) std::cout << "=";
	  else if (i == pos) std::cout << ">";
	  else std::cout << " ";
	}
	std::cout << "] " << int(progress * 100.0) << " %\r";
	std::cout.flush();
	progress += 0.01; // increase by 1%
      }
    
    if ( num_proton > 20 ) continue;

    num_p = num_m = 0;
    std::string period = getPeriod(run);
    
    for ( unsigned int j=0; j<num_proton; j++ ) { // Loop over protons
      
      if (sector45[j]) {
	
	// Aperture cut - TURNING OFF FOR SINGLERP
	//if ( OutsideAperture(period, "arm0", crossingAngle, proton_xi[j], thetaX[j]) ) continue;
	
	bool cut_p = false;
	int decRPId_p;

	for ( unsigned int k=0; k<num_trk; k++ ) {
	  if ( trkIdx[k] == j ) {
	    if ( EfficiencyCut(run, decRPId[k], 0, proton_xi[j], trackX[k], trackY[k]) ) cut_p = true;
	    else decRPId_p = decRPId[k];
	  }
	}
	
	// Efficiency cut
	if (cut_p) continue;
	
	xip[num_p] = proton_xi[j];
	idp[num_p] = decRPId_p;
	num_p += 1;
      }
      else {
	
	// Aperture cut - TURNING OFF FOR SINGLERP
	//if ( OutsideAperture(period, "arm1", crossingAngle, proton_xi[j], thetaX[j]) ) continue;
	
	bool cut_m = false;
	int decRPId_m;
	
	for ( unsigned int k=0; k<num_trk; k++ ) {
	  if ( trkIdx[k] == j ) {
	    if ( EfficiencyCut(run, decRPId[k], 1, proton_xi[j], trackX[k], trackY[k]) ) cut_m = true;
	    else decRPId_m = decRPId[k];
	  }
	}
	
	// Efficiency cut
	if (cut_m) continue;
	
	xim[num_m] = proton_xi[j];
	idm[num_m] = decRPId_m;
	num_m += 1;
      }
      
      
    } // End loop over protons
    
    // Fill tree based on era and crossingAngle

    /* 2016
    if ( run > 272006 && run < 275387 ) tree_B->Fill();
    else if ( run > 275656 && run < 276284 ) tree_C->Fill();
    else if ( run > 278819 && run < 280386 ) tree_G->Fill();
    */

    /* 2017
    if ( run > 297023 && run < 299330 ) { // Run2017B
      if ( crossingAngle == 120 ) tree_B_120->Fill();
      else if ( crossingAngle == 130 ) tree_B_130->Fill();
      else if ( crossingAngle == 140 ) tree_B_140->Fill();
      else if ( crossingAngle == 150 ) tree_B_150->Fill();
    } else if ( run > 299359 && run < 302045 ) { // Run2017C
      if ( crossingAngle == 120 ) tree_C_120->Fill();
      else if ( crossingAngle == 130 ) tree_C_130->Fill();
      else if ( crossingAngle == 140 ) tree_C_140->Fill();
      else if ( crossingAngle == 150 ) tree_C_150->Fill();
    } else if ( run > 302111 && run < 302679 ) { // Run2017D
      if ( crossingAngle == 120 ) tree_D_120->Fill();
      else if ( crossingAngle == 130 ) tree_D_130->Fill();
      else if ( crossingAngle == 140 ) tree_D_140->Fill();
      else if ( crossingAngle == 150 ) tree_D_150->Fill();
    } else if ( run > 303708 && run < 304798 ) { // Run2017E
      if ( crossingAngle == 120 ) tree_E_120->Fill();
      else if ( crossingAngle == 130 ) tree_E_130->Fill();
      else if ( crossingAngle == 140 ) tree_E_140->Fill();
      else if ( crossingAngle == 150 ) tree_E_150->Fill();
    } else if ( run > 305016 && run < 306463 ) { // Run2017F
      if ( crossingAngle == 120 ) tree_F_120->Fill();
      else if ( crossingAngle == 130 ) tree_F_130->Fill();
      else if ( crossingAngle == 140 ) tree_F_140->Fill();
      else if ( crossingAngle == 150 ) tree_F_150->Fill();
      }
    */

    // 2018
    if ( run > 315256 && run < 316996 ) { //Run2018A
      if ( crossingAngle == 120 ) tree_A_120->Fill();
      else if ( crossingAngle == 121 ) tree_A_121->Fill();
      else if ( crossingAngle == 122 ) tree_A_122->Fill();
      else if ( crossingAngle == 123 ) tree_A_123->Fill();
      else if ( crossingAngle == 124 ) tree_A_124->Fill();
      else if ( crossingAngle == 125 ) tree_A_125->Fill();
      else if ( crossingAngle == 126 ) tree_A_126->Fill();
      else if ( crossingAngle == 127 ) tree_A_127->Fill();
      else if ( crossingAngle == 128 ) tree_A_128->Fill();
      else if ( crossingAngle == 129 ) tree_A_129->Fill();
      else if ( crossingAngle == 130 ) tree_A_130->Fill();
      else if ( crossingAngle == 131 ) tree_A_131->Fill();
      else if ( crossingAngle == 132 ) tree_A_132->Fill();
      else if ( crossingAngle == 133 ) tree_A_133->Fill();
      else if ( crossingAngle == 134 ) tree_A_134->Fill();
      else if ( crossingAngle == 135 ) tree_A_135->Fill();
      else if ( crossingAngle == 136 ) tree_A_136->Fill();
      else if ( crossingAngle == 137 ) tree_A_137->Fill();
      else if ( crossingAngle == 138 ) tree_A_138->Fill();
      else if ( crossingAngle == 139 ) tree_A_139->Fill();
      else if ( crossingAngle == 140 ) tree_A_140->Fill();
      else if ( crossingAngle == 141 ) tree_A_141->Fill();
      else if ( crossingAngle == 142 ) tree_A_142->Fill();
      else if ( crossingAngle == 143 ) tree_A_143->Fill();
      else if ( crossingAngle == 144 ) tree_A_144->Fill();
      else if ( crossingAngle == 145 ) tree_A_145->Fill();
      else if ( crossingAngle == 146 ) tree_A_146->Fill();
      else if ( crossingAngle == 147 ) tree_A_147->Fill();
      else if ( crossingAngle == 148 ) tree_A_148->Fill();
      else if ( crossingAngle == 149 ) tree_A_149->Fill();
      else if ( crossingAngle == 150 ) tree_A_150->Fill();
      else if ( crossingAngle == 151 ) tree_A_151->Fill();
      else if ( crossingAngle == 152 ) tree_A_152->Fill();
      else if ( crossingAngle == 153 ) tree_A_153->Fill();
      else if ( crossingAngle == 154 ) tree_A_154->Fill();
      else if ( crossingAngle == 155 ) tree_A_155->Fill();
      else if ( crossingAngle == 156 ) tree_A_156->Fill();
      else if ( crossingAngle == 157 ) tree_A_157->Fill();
      else if ( crossingAngle == 158 ) tree_A_158->Fill();
      else if ( crossingAngle == 159 ) tree_A_159->Fill();
      else if ( crossingAngle == 160 ) tree_A_160->Fill();
    } else if ( run > 317079 && run < 319078 ) { //Run2018B
      if ( crossingAngle == 120 ) tree_B_120->Fill();
      else if ( crossingAngle == 121 ) tree_B_121->Fill();
      else if ( crossingAngle == 122 ) tree_B_122->Fill();
      else if ( crossingAngle == 123 ) tree_B_123->Fill();
      else if ( crossingAngle == 124 ) tree_B_124->Fill();
      else if ( crossingAngle == 125 ) tree_B_125->Fill();
      else if ( crossingAngle == 126 ) tree_B_126->Fill();
      else if ( crossingAngle == 127 ) tree_B_127->Fill();
      else if ( crossingAngle == 128 ) tree_B_128->Fill();
      else if ( crossingAngle == 129 ) tree_B_129->Fill();
      else if ( crossingAngle == 130 ) tree_B_130->Fill();
      else if ( crossingAngle == 131 ) tree_B_131->Fill();
      else if ( crossingAngle == 132 ) tree_B_132->Fill();
      else if ( crossingAngle == 133 ) tree_B_133->Fill();
      else if ( crossingAngle == 134 ) tree_B_134->Fill();
      else if ( crossingAngle == 135 ) tree_B_135->Fill();
      else if ( crossingAngle == 136 ) tree_B_136->Fill();
      else if ( crossingAngle == 137 ) tree_B_137->Fill();
      else if ( crossingAngle == 138 ) tree_B_138->Fill();
      else if ( crossingAngle == 139 ) tree_B_139->Fill();
      else if ( crossingAngle == 140 ) tree_B_140->Fill();
      else if ( crossingAngle == 141 ) tree_B_141->Fill();
      else if ( crossingAngle == 142 ) tree_B_142->Fill();
      else if ( crossingAngle == 143 ) tree_B_143->Fill();
      else if ( crossingAngle == 144 ) tree_B_144->Fill();
      else if ( crossingAngle == 145 ) tree_B_145->Fill();
      else if ( crossingAngle == 146 ) tree_B_146->Fill();
      else if ( crossingAngle == 147 ) tree_B_147->Fill();
      else if ( crossingAngle == 148 ) tree_B_148->Fill();
      else if ( crossingAngle == 149 ) tree_B_149->Fill();
      else if ( crossingAngle == 150 ) tree_B_150->Fill();
      else if ( crossingAngle == 151 ) tree_B_151->Fill();
      else if ( crossingAngle == 152 ) tree_B_152->Fill();
      else if ( crossingAngle == 153 ) tree_B_153->Fill();
      else if ( crossingAngle == 154 ) tree_B_154->Fill();
      else if ( crossingAngle == 155 ) tree_B_155->Fill();
      else if ( crossingAngle == 156 ) tree_B_156->Fill();
      else if ( crossingAngle == 157 ) tree_B_157->Fill();
      else if ( crossingAngle == 158 ) tree_B_158->Fill();
      else if ( crossingAngle == 159 ) tree_B_159->Fill();
      else if ( crossingAngle == 160 ) tree_B_160->Fill();
    } else if ( run > 319336 && run < 320066 ) { //Run2018C
      if ( crossingAngle == 120 ) tree_C_120->Fill();
      else if ( crossingAngle == 121 ) tree_C_121->Fill();
      else if ( crossingAngle == 122 ) tree_C_122->Fill();
      else if ( crossingAngle == 123 ) tree_C_123->Fill();
      else if ( crossingAngle == 124 ) tree_C_124->Fill();
      else if ( crossingAngle == 125 ) tree_C_125->Fill();
      else if ( crossingAngle == 126 ) tree_C_126->Fill();
      else if ( crossingAngle == 127 ) tree_C_127->Fill();
      else if ( crossingAngle == 128 ) tree_C_128->Fill();
      else if ( crossingAngle == 129 ) tree_C_129->Fill();
      else if ( crossingAngle == 130 ) tree_C_130->Fill();
      else if ( crossingAngle == 131 ) tree_C_131->Fill();
      else if ( crossingAngle == 132 ) tree_C_132->Fill();
      else if ( crossingAngle == 133 ) tree_C_133->Fill();
      else if ( crossingAngle == 134 ) tree_C_134->Fill();
      else if ( crossingAngle == 135 ) tree_C_135->Fill();
      else if ( crossingAngle == 136 ) tree_C_136->Fill();
      else if ( crossingAngle == 137 ) tree_C_137->Fill();
      else if ( crossingAngle == 138 ) tree_C_138->Fill();
      else if ( crossingAngle == 139 ) tree_C_139->Fill();
      else if ( crossingAngle == 140 ) tree_C_140->Fill();
      else if ( crossingAngle == 141 ) tree_C_141->Fill();
      else if ( crossingAngle == 142 ) tree_C_142->Fill();
      else if ( crossingAngle == 143 ) tree_C_143->Fill();
      else if ( crossingAngle == 144 ) tree_C_144->Fill();
      else if ( crossingAngle == 145 ) tree_C_145->Fill();
      else if ( crossingAngle == 146 ) tree_C_146->Fill();
      else if ( crossingAngle == 147 ) tree_C_147->Fill();
      else if ( crossingAngle == 148 ) tree_C_148->Fill();
      else if ( crossingAngle == 149 ) tree_C_149->Fill();
      else if ( crossingAngle == 150 ) tree_C_150->Fill();
      else if ( crossingAngle == 151 ) tree_C_151->Fill();
      else if ( crossingAngle == 152 ) tree_C_152->Fill();
      else if ( crossingAngle == 153 ) tree_C_153->Fill();
      else if ( crossingAngle == 154 ) tree_C_154->Fill();
      else if ( crossingAngle == 155 ) tree_C_155->Fill();
      else if ( crossingAngle == 156 ) tree_C_156->Fill();
      else if ( crossingAngle == 157 ) tree_C_157->Fill();
      else if ( crossingAngle == 158 ) tree_C_158->Fill();
      else if ( crossingAngle == 159 ) tree_C_159->Fill();
      else if ( crossingAngle == 160 ) tree_C_160->Fill();
    } else if ( run > 320672 && run < 325173 ) { //Run2018D
      if ( crossingAngle == 120 ) tree_D_120->Fill();
      else if ( crossingAngle == 121 ) tree_D_121->Fill();
      else if ( crossingAngle == 122 ) tree_D_122->Fill();
      else if ( crossingAngle == 123 ) tree_D_123->Fill();
      else if ( crossingAngle == 124 ) tree_D_124->Fill();
      else if ( crossingAngle == 125 ) tree_D_125->Fill();
      else if ( crossingAngle == 126 ) tree_D_126->Fill();
      else if ( crossingAngle == 127 ) tree_D_127->Fill();
      else if ( crossingAngle == 128 ) tree_D_128->Fill();
      else if ( crossingAngle == 129 ) tree_D_129->Fill();
      else if ( crossingAngle == 130 ) tree_D_130->Fill();
      else if ( crossingAngle == 131 ) tree_D_131->Fill();
      else if ( crossingAngle == 132 ) tree_D_132->Fill();
      else if ( crossingAngle == 133 ) tree_D_133->Fill();
      else if ( crossingAngle == 134 ) tree_D_134->Fill();
      else if ( crossingAngle == 135 ) tree_D_135->Fill();
      else if ( crossingAngle == 136 ) tree_D_136->Fill();
      else if ( crossingAngle == 137 ) tree_D_137->Fill();
      else if ( crossingAngle == 138 ) tree_D_138->Fill();
      else if ( crossingAngle == 139 ) tree_D_139->Fill();
      else if ( crossingAngle == 140 ) tree_D_140->Fill();
      else if ( crossingAngle == 141 ) tree_D_141->Fill();
      else if ( crossingAngle == 142 ) tree_D_142->Fill();
      else if ( crossingAngle == 143 ) tree_D_143->Fill();
      else if ( crossingAngle == 144 ) tree_D_144->Fill();
      else if ( crossingAngle == 145 ) tree_D_145->Fill();
      else if ( crossingAngle == 146 ) tree_D_146->Fill();
      else if ( crossingAngle == 147 ) tree_D_147->Fill();
      else if ( crossingAngle == 148 ) tree_D_148->Fill();
      else if ( crossingAngle == 149 ) tree_D_149->Fill();
      else if ( crossingAngle == 150 ) tree_D_150->Fill();
      else if ( crossingAngle == 151 ) tree_D_151->Fill();
      else if ( crossingAngle == 152 ) tree_D_152->Fill();
      else if ( crossingAngle == 153 ) tree_D_153->Fill();
      else if ( crossingAngle == 154 ) tree_D_154->Fill();
      else if ( crossingAngle == 155 ) tree_D_155->Fill();
      else if ( crossingAngle == 156 ) tree_D_156->Fill();
      else if ( crossingAngle == 157 ) tree_D_157->Fill();
      else if ( crossingAngle == 158 ) tree_D_158->Fill();
      else if ( crossingAngle == 159 ) tree_D_159->Fill();
      else if ( crossingAngle == 160 ) tree_D_160->Fill();
    }
    //

  } // End loop over entries

  std::cout << std::endl;


  std::cout << "Writing file" << std::endl;
  out->Write();
  out->Close();

}
