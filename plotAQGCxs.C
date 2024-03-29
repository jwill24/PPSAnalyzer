// Make FPMC scan

#include "TH1.h"
#include "TFile.h"
#include <fstream>
#include <iostream>

#define output_file "aqgc_scan_fpmc.pdf"

void plotAQGCxs( TString outFile=output_file )
{

  TFile* out = new TFile( outFile, "RECREATE" );

  struct sample_t
  {
    double zeta1, zeta2;
    double xsec;
  };

  TGraph g_el_vals;
  TGraph2D g_xs;

  std::vector<sample_t> samples = {
    {5.e-12, 5.e-12,  214.347},
    {5.e-12, 1.e-12,  122.200},
    {5.e-12, 5.e-13,  112.824},
    {5.e-12, 1.e-13,  105.668},
    {5.e-12, 0.,      103.926},
    {5.e-12, -1.e-13, 102.203},
    {5.e-12, -5.e-13, 95.5},
    {5.e-12, -1.e-12, 87.558},
    {5.e-12, -5.e-12, 41.137},

    {1.e-12, 5.e-12,  45.294},
    {1.e-12, 1.e-12,  8.574},
    {1.e-12, 5.e-13,  6.127},
    {1.e-12, 1.e-13,  4.513},
    {1.e-12, 0.,      4.157},
    {1.e-12, -1.e-13, 3.820},
    {1.e-12, -5.e-13, 2.663},
    {1.e-12, -1.e-12, 1.645},
    {1.e-12, -5.e-12, 10.652},

    {5.e-13, 5.e-12,  33.516},
    {5.e-13, 1.e-12,  3.724},
    {5.e-13, 5.e-13,  2.143},
    {5.e-13, 1.e-13,  1.222},
    {5.e-13, 0.,      1.039},
    {5.e-13, -1.e-13, 8.756e-1},
    {5.e-13, -5.e-13, 4.114e-1},
    {5.e-13, -1.e-12, 2.598e-1},
    {5.e-13, -5.e-12, 16.195},

    {1.e-13, 5.e-12,  25.590},
    {1.e-13, 1.e-12,  1.341},
    {1.e-13, 5.e-13,  4.529e-1},
    {1.e-13, 1.e-13,  8.574e-2},
    {1.e-13, 0.,      4.157e-2},
    {1.e-13, -1.e-13, 1.645e-2},
    {1.e-13, -5.e-13, 0.107},
    {1.e-13, -1.e-12, 0.648},
    {1.e-13, -5.e-12, 22.126},

    {0., 5.e-12,  23.816},
    {0., 1.e-12,  9.530e-1},
    {0., 5.e-13,  2.382e-1},
    {0., 1.e-13,  9.525e-3},
    {0., -1.e-13, 9.528e-3},
    {0., -5.e-13, 2.382e-1},
    {0., -1.e-12, 9.530e-1},
    {0., -5.e-12, 23.816},

    {-1.e-13, 5.e-12,  22.126},
    {-1.e-13, 1.e-12,  6.478e-1},
    {-1.e-13, 5.e-13,  1.065e-1},
    {-1.e-13, 1.e-13,  1.645e-2},
    {-1.e-13, 0.,      4.157e-2},
    {-1.e-13, -1.e-13, 8.574e-2},
    {-1.e-13, -5.e-13, 4.529e-1},
    {-1.e-13, -1.e-12, 1.341},
    {-1.e-13, -5.e-12, 28.590},

    {-5.e-13, 5.e-12,  16.159},
    {-5.e-13, 1.e-12,  2.598e-1},
    {-5.e-13, 5.e-13,  4.11e-1},
    {-5.e-13, 1.e-13,  8.756e-1},
    {-5.e-13, 0.,      1.039},
    {-5.e-13, -1.e-13, 1.222},
    {-5.e-13, -5.e-13, 2.143},
    {-5.e-13, -1.e-12, 3.724},
    {-5.e-13, -5.e-12, 33.516},

    {-1.e-12, 5.e-12,  10.652},
    {-1.e-12, 1.e-12,  1.646},
    {-1.e-12, 5.e-13,  2.663},
    {-1.e-12, 1.e-13,  3.820},
    {-1.e-12, 0.,      4.157},
    {-1.e-12, -1.e-13, 4.513},
    {-1.e-12, -5.e-13, 6.127},
    {-1.e-12, -1.e-12, 8.574},
    {-1.e-12, -5.e-12, 45.295},

    {-5.e-12, 5.e-12,  41.137},
    {-5.e-12, 1.e-12,  87.558},
    {-5.e-12, 5.e-13,  95.504},
    {-5.e-12, 1.e-13,  102.204},
    {-5.e-12, 0.,      103.926},
    {-5.e-12, -1.e-13, 105.668},
    {-5.e-12, -5.e-13, 112.825},
    {-5.e-12, -1.e-12, 122.200},
    {-5.e-12, -5.e-12, 214.348},

    {-2.e-12, 3.e-12,  4.417},
    {2.e-12,  -3.e-12, 4.417}, 
    {-2.e-12, 4.e-12,  4.157},
    {2.e-12,  -4.e-12, 4.157},
    {-1.e-12, 4.e-12,  5.543},
    {1.e-12,  -4.e-12, 5.543},
    {-3.e-12, 4.e-12,  11.085},
    {3.e-12,  -4.e-12, 11.085},

    {-1.5e-12, 4.5e-12, 5.261},
    {1.5e-12, -4.5e-12, 5.261},
    {-2.0e-12, 1.5e-12, 8.379},
    {2.0e-12, -1.5e-12, 8.379},
    {-2.5e-12, 5.0e-12, 6.495},
    {2.5e-12, -5.0e-12, 6.495},

    {0.,     -2.5e-12,  5.954},
    {0.,      2.5e-12,  5.954},
    {1.e-12, -2.5e-12,  1.451},
    {-1.e-12, 2.5e-12,  1.451},
    {-2.e-12, 0.0,      16.628},
    {2.e-12,  0.0,      16.628},
    {-3.e-12, 0.0,      37.413},
    {3.e-12,  0.0,      37.413},
    {-4.e-12, 0.0,      66.513},
    {4.e-12,  0.0,      66.513},
    {1.5e-12, -3.5e-12, 2.836},
    {-1.5e-12, 3.5e-12, 2.836},
    {-2.5e-12, 3.e-12,  8.574},
    {2.5e-12, -3.e-12,  8.574},
    {-2.5e-12, -2.e-12, 47.113},
    {2.5e-12,  2.e-12,  47.113},
    {3.5e-12, 3.e-12,   95.871},
    {-3.5e-12, -3.e-12, 95.871},
    {-4.0e-12, 2.0e-12, 42.610},
    {4.0e-12, -2.0e-12, 42.610},
    
    
  };

  unsigned short i;
  for ( auto& s : samples ) {
    g_el_vals.SetPoint( i, s.zeta1*1.e12, s.zeta2*1.e12 );
    g_xs.SetPoint( i, s.zeta1*1.e12, s.zeta2*1.e12, s.xsec );
    ++i;
  }
  

  //gStyle->SetPalette( kBeach );
  //gStyle->SetPalette( kBlackBody );
  gStyle->SetPalette( kLightTemperature );
  //gStyle->SetPalette( kThermometer );
  //gStyle->SetPalette( kViridis );
  //gStyle->SetPalette( kGistEarth );
  
  TCanvas c;
  c.cd();
  c.SetTicks(1,1);
  g_xs.SetNpx(50);
  g_xs.SetNpy(50);
  g_xs.Draw( "colz" );
  g_xs.SetTitle("");
  //g_xs.GetHistogram()->GetYaxis()->SetTitleOffset(0.2);
  //g_xs.GetYaxis()->SetTitleOffset(0.2);
  g_xs.GetHistogram()->GetXaxis()->SetTitle("#zeta_{1} (GeV^{-4}) #times 10^{-12}");
  g_xs.GetHistogram()->GetYaxis()->SetTitle("#zeta_{2} (GeV^{-4}) #times 10^{-12}");
  g_el_vals.SetMarkerStyle( 3 );
  //g_el_vals.Draw( "p same" );
  c.SetLogz();
  c.SaveAs("aqgc_scan_fpmc.png");

}



