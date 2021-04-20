// Make FPMC scan and print out limit values

#include "TH1.h"
#include "TFile.h"
#include <fstream>
#include <iostream>


void plotALPxs()
{

  struct sample_t
  {
    double f, m;
    double xsec;
  };

  TGraph g_el_vals;
  TGraph2D g_xs;

  std::vector<sample_t> samples = {

    {1.e1, 500,  2.700}, // AAF0 = 100
    {1.e1, 750,  2.453},
    {1.e1, 1000, 2.076},
    {1.e1, 1250, 1.713},
    {1.e1, 1500, 1.399},
    {1.e1, 2000, 9.516e-1},

    {5.e0, 500,  1.575}, // AAF0 = 200
    {5.e0, 750,  1.423},
    {5.e0, 1000, 1.032},
    {5.e0, 1250, 0.734},
    {5.e0, 1500, 0.528},
    {5.e0, 2000, 0.288},

    {2.e0, 500,  2.340e-1}, // AAF0 = 500
    {2.e0, 750,  4.152e-1},
    {2.e0, 1000, 3.042e-1},
    {2.e0, 1250, 1.704e-1},
    {2.e0, 1500, 9.429e-2},
    {2.e0, 2000, 3.390e-2},

    {1.01, 500,  4.063e-2}, // AAF0 = 990
    {1.01, 750,  1.110e-1}, 
    {1.01, 1000, 1.005e-1}, 
    {1.01, 1250, 5.538e-2}, 
    {1.01, 1500, 2.788e-2}, 
    {1.01, 2000, 6.690e-3}, 

    {1.05, 500,  4.466e-2}, // AAF0 = 952.4
    {1.05, 750,  1.203e-1}, 
    {1.05, 1000, 1.079e-1}, 
    {1.05, 1250, 5.920e-2}, 
    {1.05, 1500, 2.980e-2}, 
    {1.05, 2000, 7.287e-3}, 

    {1.e0, 500,  3.957e-2}, // AAF0 = 1,000 
    {1.e0, 750,  1.089e-1},
    {1.e0, 1000, 9.850e-2},
    {1.e0, 1250, 5.414e-2},
    {1.e0, 1500, 2.748e-2},
    {1.e0, 2000, 6.475e-3},

    {5.e-1, 500,  8.551e-3}, // AAF0 = 2,000 
    {5.e-1, 750,  2.713e-2},
    {5.e-1, 1000, 2.651e-2},
    {5.e-1, 1250, 1.485e-2},
    {5.e-1, 1500, 7.668e-3},
    {5.e-1, 2000, 1.537e-3},

    {1.e-1, 500,  3.229e-4}, // AAF0 = 10,000
    {1.e-1, 600,  7.861e-4}, 
    {1.e-1, 700,  1.031e-3}, 
    {1.e-1, 750,  1.066e-3},
    {1.e-1, 800,  1.124e-3}, 
    {1.e-1, 900,  1.123e-3}, 
    {1.e-1, 1000, 1.085e-3},
    {1.e-1, 1250, 6.154e-4},
    {1.e-1, 1500, 3.228e-4},
    {1.e-1, 2000, 6.330e-5},

    {0.08, 500,  2.060e-4}, // AAF0 = 12,500
    {0.08, 600,  5.028e-4},
    {0.08, 700,  6.550e-4},
    {0.08, 750,  6.833e-4},
    {0.08, 800,  7.138e-4},
    {0.08, 900,  7.173e-4},
    {0.08, 1000, 6.923e-4},
    {0.08, 1250, 3.948e-4},
    {0.08, 1500, 2.069e-4},
    {0.08, 2000, 4.074e-5},

    {0.06, 500,  1.156e-4}, // AAF0 = 16,667
    {0.06, 600,  2.824e-4}, 
    {0.06, 700,  3.697e-4}, 
    {0.06, 750,  3.802e-4},
    {0.06, 800,  4.027e-4},
    {0.06, 900,  4.011e-4},
    {0.06, 1000, 3.882e-4},
    {0.06, 1250, 2.233e-4},
    {0.06, 1500, 1.167e-4},
    {0.06, 2000, 2.290e-5},

    {0.05, 500,  8.066e-5}, // AAF0 = 20,000
    {0.05, 600,  1.960e-4}, 
    {0.05, 700,  2.538e-4},
    {0.05, 750,  2.653e-4},
    {0.05, 800,  2.791e-4},
    {0.05, 900,  2.795e-4},
    {0.05, 1000, 2.696e-4},
    {0.05, 1250, 1.552e-4},
    {0.05, 1500, 8.073e-5},
    {0.05, 2000, 1.594e-5},

    {0.04, 500,  5.190e-5}, // AAF0 = 25,000
    {0.04, 600,  1.251e-4}, 
    {0.04, 700,  1.625e-4},
    {0.04, 750,  1.702e-4},
    {0.04, 800,  1.796e-4},
    {0.04, 900,  1.789e-4},
    {0.04, 1000, 1.730e-4},
    {0.04, 1250, 9.949e-5},
    {0.04, 1500, 5.148e-5},
    {0.04, 2000, 1.015e-5},

    //{0.03, 500,  e-5}, // AAF0 = 33,333.33
    {0.03, 600,  7.055e-5}, 
    {0.03, 700,  9.166e-5},
    {0.03, 750,  9.604e-5},
    {0.03, 800,  1.006e-4},
    {0.03, 900,  1.008e-4},
    {0.03, 1000, 9.750e-5},
    {0.03, 1250, 5.593e-5},
    {0.03, 1500, 2.894e-5},
    {0.03, 2000, 5.715e-6},

    {0.02, 500,  1.331e-5}, // AAF0 = 50,000
    {0.02, 750,  4.390e-5},
    {0.02, 1000, 4.363e-5},
    {0.02, 1250, 2.488e-5},
    {0.02, 1500, 1.283e-5},
    {0.02, 2000, 2.537e-6},
    
        
  };

  unsigned short i;
  for ( auto& s : samples ) {
    g_el_vals.SetPoint( i, s.m, s.f );
    g_xs.SetPoint( i, s.m, s.f, s.xsec );
    ++i;
  }

  std::vector<float> mass_points = {500.0, 750.0, 1000.0, 1250.0, 1500.0, 2000.0};
  //std::vector<float> mass_points = {500.0, 600.0, 700.0, 750.0, 800.0, 900.0, 1000.0, 1100.0,  1250.0, 1300.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0};

  // shape-based asymptotic analysis (6 points)
  //std::vector<float> observed =  {0.1895, 0.1107, 0.1358, 0.1711, 0.2793, 4.9696};
  //std::vector<float> two_minus = {0.0682, 0.0482, 0.0521, 0.0651, 0.0948, 1.4844}; 
  //std::vector<float> one_minus = {0.1125, 0.0756, 0.0826, 0.1059, 0.1608, 2.6105};
  //std::vector<float> limit =     {0.2031, 0.1299, 0.1450, 0.1895, 0.2959, 5.0000};
  //std::vector<float> one_plus =  {0.3764, 0.2334, 0.2629, 0.3511, 0.5577, 9.7434};
  //std::vector<float> two_plus =  {0.6158, 0.3937, 0.4396, 0.5743, 0.8971, 15.1616};

  // smeared shape-based asymptotic analysis (6 points)
  std::vector<float> observed =  {0.3398, 0.1164, 0.2284, 0.1753, 0.2819, 4.9730};
  std::vector<float> two_minus = {0.0804, 0.0597, 0.0636, 0.0733, 0.0997, 1.4937}; 
  std::vector<float> one_minus = {0.1285, 0.0905, 0.0980, 0.1163, 0.1666, 2.6130};
  std::vector<float> limit =     {0.2236, 0.1514, 0.1660, 0.2041, 0.3037, 5.0312};
  std::vector<float> one_plus =  {0.4037, 0.2612, 0.2917, 0.3684, 0.5676, 9.7241};
  std::vector<float> two_plus =  {0.6779, 0.4338, 0.4865, 0.6187, 0.9208, 15.2557};


  // shape-based analysis (6 points)
  //std::vector<float> two_minus = {0.216, 0.132, 0.157, 0.211, 0.335, 6.592}; 
  //std::vector<float> one_minus = {0.244, 0.136, 0.171, 0.222, 0.376, 6.922};
  //std::vector<float> limit =     {0.261, 0.150, 0.177, 0.243, 0.404, 7.323};
  //std::vector<float> one_plus =  {0.283, 0.177, 0.189, 0.263, 0.424, 7.736};
  //std::vector<float> two_plus =  {0.310, 0.181, 0.197, 0.275, 0.473, 7.981};
  //std::vector<float> two_plus =  {6.487, 3,577, 4.011, 5.241, 8.600, 7.981};

  // counting experiment (16 points)
  //std::vector<float> two_minus = {0.291, 0.186, 0.168, 0.155, 0.159, 0.156, 0.181, 0.211, 0.266, 0.285, 0.436, 0.571, 0.874, 1.552, 3.165, 10.142};
  //std::vector<float> one_minus = {0.331, 0.217, 0.185, 0.181, 0.178, 0.180, 0.210, 0.233, 0.294, 0.326, 0.498, 0.657, 0.965, 1.702, 3.635, 11.383};
  //std::vector<float> limit =     {0.452, 0.286, 0.243, 0.252, 0.235, 0.250, 0.273, 0.309, 0.403, 0.428, 0.633, 0.873, 1.308, 2.332, 4.948, 15.143};
  //std::vector<float> one_plus =  {0.613, 0.409, 0.340, 0.336, 0.330, 0.352, 0.406, 0.450, 0.563, 0.600, 0.907, 1.261, 1.878, 3.293, 7.067, 21.375};
  //std::vector<float> two_plus =  {0.895, 0.596, 0.497, 0.500, 0.477, 0.484, 0.572, 0.639, 0.790, 0.868, 1.317, 1.792, 2.662, 4.692, 10.054, 30.462};
  //std::vector<float> observed =  {0.451, 0.288, 0.242, 0.256, 0.240, 0.251, 0.290, 0.323, 0.397, 0.440, 0.667, 99.99, 1.329, 99.99, 99.999, 15.316};


  // counting experiment
  //std::vector<float> two_minus = {0.291, 0.155, 0.181, 0.266, 0.436, 10.142};
  //std::vector<float> one_minus = {0.331, 0.181, 0.210, 0.294, 0.498, 11.383};
  //std::vector<float> limit =     {0.452, 0.252, 0.273, 0.403, 0.633, 15.143};
  //std::vector<float> one_plus =  {0.613, 0.336, 0.406, 0.563, .907, 21.375};
  //std::vector<float> two_plus =  {0.895, 0.500, .572, 0.790, 1.317, 30.462};


  std::cout << "two minus points" << std::endl;
  std::cout << "------------------" << std::endl;
  for ( int i = 0; i < 6; i++ ) {
    double tmp_diff = 999.0;
    double f_limit = 999.0;
    for ( int j = 1; j < 20000; j++ ) {
      double y = 0.0001*j;      
      if ( abs( g_xs.Interpolate(mass_points[i], y) - two_minus[i]*0.001 ) < tmp_diff ) {
	tmp_diff = abs( g_xs.Interpolate(mass_points[i], y) - two_minus[i]*0.001 );
	f_limit = y;
      } else continue;
    }
    std::cout << "Mass: " << mass_points[i] << " f limit: " << f_limit << std::endl;
  }

  std::cout << "" << std::endl;
  std::cout << "one minus points" << std::endl;
  std::cout << "------------------" << std::endl;
  for ( int i = 0; i < 6; i++ ) {
    double tmp_diff = 999.0;
    double f_limit = 999.0;
    for ( int j = 1; j < 20000; j++ ) {
      double y = 0.0001*j;      
      if ( abs( g_xs.Interpolate(mass_points[i], y) - one_minus[i]*0.001 ) < tmp_diff ) {
	tmp_diff = abs( g_xs.Interpolate(mass_points[i], y) - one_minus[i]*0.001 );
	f_limit = y;
      } else continue;
    }
    std::cout << "Mass: " << mass_points[i] << " f limit: " << f_limit << std::endl;
  }

  std::cout << "" << std::endl;
  std::cout << "median points" << std::endl;
  std::cout << "------------------" << std::endl;
  for ( int i = 0; i < 6; i++ ) {
    double tmp_diff = 999.0;
    double f_limit = 999.0;
    for ( int j = 1; j < 20000; j++ ) {
      double y = 0.0001*j;      
      if ( abs( g_xs.Interpolate(mass_points[i], y) - limit[i]*0.001 ) < tmp_diff ) {
	tmp_diff = abs( g_xs.Interpolate(mass_points[i], y) - limit[i]*0.001 );
	f_limit = y;
      } else continue;
    }
    std::cout << "Mass: " << mass_points[i] << " f limit: " << f_limit << std::endl;
  }

  std::cout << "" << std::endl;
  std::cout << "one plus points" << std::endl;
  std::cout << "------------------" << std::endl;
  for ( int i = 0; i < 6; i++ ) {
    double tmp_diff = 999.0;
    double f_limit = 999.0;
    for ( int j = 1; j < 20000; j++ ) {
      double y = 0.0001*j;      
      if ( abs( g_xs.Interpolate(mass_points[i], y) - one_plus[i]*0.001 ) < tmp_diff ) {
	tmp_diff = abs( g_xs.Interpolate(mass_points[i], y) - one_plus[i]*0.001 );
	f_limit = y;
      } else continue;
    }
    std::cout << "Mass: " << mass_points[i] << " f limit: " << f_limit << std::endl;
  }

  std::cout << "" << std::endl;
  std::cout << "two plus points" << std::endl;
  std::cout << "------------------" << std::endl;
  for ( int i = 0; i < 6; i++ ) {
    double tmp_diff = 999.0;
    double f_limit = 999.0;
    for ( int j = 1; j < 20000; j++ ) {
      double y = 0.0001*j;      
      if ( abs( g_xs.Interpolate(mass_points[i], y) - two_plus[i]*0.001 ) < tmp_diff ) {
	tmp_diff = abs( g_xs.Interpolate(mass_points[i], y) - two_plus[i]*0.001 );
	f_limit = y;
      } else continue;
    }
    std::cout << "Mass: " << mass_points[i] << " f limit: " << f_limit << std::endl;
  }


  std::cout << "" << std::endl;
  std::cout << "Observed points" << std::endl;
  std::cout << "------------------" << std::endl;
  for ( int i = 0; i < 6; i++ ) {
    double tmp_diff = 999.0;
    double f_limit = 999.0;
    for ( int j = 1; j < 20000; j++ ) {
      double y = 0.0001*j;      
      if ( abs( g_xs.Interpolate(mass_points[i], y) - observed[i]*0.001 ) < tmp_diff ) {
	tmp_diff = abs( g_xs.Interpolate(mass_points[i], y) - observed[i]*0.001 );
	f_limit = y;
      } else continue;
    }
    std::cout << "Mass: " << mass_points[i] << " f limit: " << f_limit << std::endl;
  }



  

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
  //g_el_vals.Draw( "p same" );
  c.SetLogz();
  c.SaveAs("alp_scan_fpmc.png");



}



