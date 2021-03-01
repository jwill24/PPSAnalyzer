// Make FPMC scan

#include "TH1.h"
#include "TFile.h"
#include <fstream>
#include <iostream>

#define output_file "alp_scan_fpmc.pdf"

void plotALPxs( TString outFile=output_file )
{

  TFile* out = new TFile( outFile, "RECREATE" );

  struct sample_t
  {
    double f, m;
    double xsec;
  };

  TGraph g_el_vals;
  TGraph2D g_xs;

  std::vector<sample_t> samples = {

    {1.e1, 500,  9.168}, // AAF0 = 100
    {1.e1, 600,  7.808},
    {1.e1, 700,  6.583},
    {1.e1, 750,  6.008},
    {1.e1, 800,  5.583},
    {1.e1, 900,  4.745},
    {1.e1, 1000, 4.063},
    {1.e1, 1250, 2.867},
    {1.e1, 1500, 2.075},
    {1.e1, 2000, 1.169},

    {1.e0, 500,  2.214e-1}, // AAF0 = 1,000
    {1.e0, 600,  2.252e-1},
    {1.e0, 700,  2.080e-1},
    {1.e0, 750,  1.851e-1},
    {1.e0, 800,  1.588e-1},
    {1.e0, 900,  1.182e-1},
    {1.e0, 1000, 8.815e-2},
    {1.e0, 1250, 3.9778e-2},
    {1.e0, 1500, 1.710e-2},
    {1.e0, 2000, 2.410e-3},

    {5.e-1, 500,  5.417e-2}, // AAF0 = 2,000
    {5.e-1, 700,  2.318e-2},
    {5.e-1, 750,  4.746e-2},
    {5.e-1, 1000, 2.318e-2},
    {5.e-1, 1250, 1.091e-2},
    {5.e-1, 1500, 4.655e-3},
    {5.e-1, 2000, 2.150e-4},

    {1.e-1, 500,  2.148e-3}, // AAF0 = 10,000
    {1.e-1, 600,  2.251e-3},
    {1.e-1, 700,  2.168e-3},
    {1.e-1, 750,  1.923e-3},
    {1.e-1, 800,  1.655e-3},
    {1.e-1, 900,  1.260e-3},
    {1.e-1, 1000, 9.446e-4},
    {1.e-1, 1250, 4.569e-4},
    {1.e-1, 1500, 1.973e-4},
    {1.e-1, 2000, 3.722e-7},

    {0.08, 500,  1.370e-3}, // AAF0 = 12,500
    {0.08, 600,  1.442e-3},
    {0.08, 700,  1.386e-3},
    {0.08, 750,  1.231e-3},
    {0.08, 800,  1.059e-3},
    {0.08, 900,  8.018e-4},
    {0.08, 1000, 6.086e-4},
    {0.08, 1250, 2.900e-4},
    {0.08, 1500, 1.249e-4},
    {0.08, 2000, 1.515e-7},

    {0.06, 500,  7.707e-4}, // AAF0 = 16,667
    {0.06, 600,  8.099e-4},
    {0.06, 700,  7.774e-4},
    {0.06, 750,  6.951e-4},
    {0.06, 800,  5.956e-4},
    {0.06, 900,  4.499e-4},
    {0.06, 1000, 3.415e-4},
    {0.06, 1250, 1.639e-4},
    {0.06, 1500, 7.006e-5},
    {0.06, 2000, 4.706e-8},

    {0.04, 500,  3.443e-4}, // AAF0 = 25,000
    {0.04, 600,  3.587e-4},
    {0.04, 700,  3.426e-4},
    {0.04, 750,  3.102e-4},
    {0.04, 800,  2.656e-4},
    {0.04, 900,  2.008e-4},
    {0.04, 1000, 1.508e-4},
    {0.04, 1250, 7.285e-5},
    {0.04, 1500, 3.121e-5},
    {0.04, 2000, 8.784e-9},

    /*    
    {0.0316228, 500,  2.154e-4},
    {0.0316228, 750,  1.932e-4},
    {0.0316228, 1000, 9.444e-5},
    {0.0316228, 1250, 4.547e-5},
    {0.0316228, 1500, 1.944e-5},
    {0.0316228, 2000, 3.282e-9},

    {0.02, 500, }, // AAF0 = 50,000
    {0.02, 750, },
    {0.02, 1000, },
    {0.02, 1250, },
    {0.02, 1500, },
    {0.02, 2000, },
    */

    {1.e-2, 500,  2.222e-5},
    {1.e-2, 750,  1.000e-5},
    {1.e-2, 1000, 9.000e-6},
    {1.e-2, 1250, 4.500e-6},
    {1.e-2, 1500, 2.000e-6},
    {1.e-2, 2000, 5.825e-11},

    
  };

  unsigned short i;
  for ( auto& s : samples ) {
    g_el_vals.SetPoint( i, s.m, s.f );
    g_xs.SetPoint( i, s.m, s.f, s.xsec );
    ++i;
  }

  std::vector<float> mass_points = {500.0, 750.0, 1000.0, 1250.0, 1500.0, 2000.0};
  std::vector<float> limit = {0.000430241, 0.000187196, 0.000146321, 0.000155121, 0.000202985, 0.00037239};
  std::vector<float> f_points = {1e-1, 1e0, 1e1};


  for ( int i = 0; i < 6; i++ ) {
    double tmp_diff = 999.0;
    double f_limit = 999.0;
    for ( int j = 1; j < 1011; j++ ) {

      double y = 0.001*j;

      
      if ( abs( g_xs.Interpolate(mass_points[i], y) - limit[i] ) < tmp_diff ) {
	tmp_diff = abs( g_xs.Interpolate(mass_points[i], y) - limit[i] );
	f_limit = y;
      } else continue;

      //std::cout << mass_points[i] << " " << y << " " << g_xs.Interpolate(mass_points[i], y) << std::endl;

    }
    std::cout << "Mass: " << mass_points[i] << " f limit: " << f_limit << std::endl;
    
  }



  /*      
  
  

  //gStyle->SetPalette( kBeach );
  gStyle->SetPalette( kBlackBody );
  //gStyle->SetPalette( kLightTemperature );
  //gStyle->SetPalette( kThermometer );
  //gStyle->SetPalette( kViridis );
  //gStyle->SetPalette( kGistEarth );
  
  TCanvas c;
  c.cd();
  c.SetLogy();
  c.SetTicks(1,1);
  gStyle->SetTitleFont(42,"t");
  g_xs.SetNpx(100);
  g_xs.SetNpy(500);
  g_xs.Draw( "colz" );
  g_xs.SetTitle("ALP #sigma (pb), #sqrt{s}=13 TeV, p_{T}^{#gamma} > 100 GeV");
  //g_xs.GetHistogram()->GetYaxis()->SetTitleOffset(0.2);
  //g_xs.GetYaxis()->SetTitleOffset(0.2);
  g_xs.GetHistogram()->GetXaxis()->SetTitle("ALP mass (GeV)");
  g_xs.GetHistogram()->GetYaxis()->SetTitle("f^{-1} (TeV^{-1})");
  g_el_vals.SetMarkerStyle( 3 );
  g_el_vals.Draw( "p same" );
  c.SetLogz();
  c.SaveAs("alp_scan_fpmc.png");

  */

}



