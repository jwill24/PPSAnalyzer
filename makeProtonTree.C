#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include <fstream>
#include <iostream>

#define output_file "protonEvents.root"

void makeProtonTree( TString outFile=output_file )
{

  TFile* out = new TFile( outFile, "RECREATE" );

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

  unsigned short maxProSide = 12;
  unsigned int num_m, num_p;
  float xim[maxProSide], xip[maxProSide];

  tree_B_120->Branch("num_m", &num_m, "num_m/I");
  tree_B_120->Branch("num_p", &num_p, "num_p/I");
  tree_B_120->Branch("xim", xim, "xim[num_m]/F");
  tree_B_120->Branch("xip", xip, "xim[num_p]/F");
  tree_B_130->Branch("num_m", &num_m, "num_m/I");
  tree_B_130->Branch("num_p", &num_p, "num_p/I");
  tree_B_130->Branch("xim", xim, "xim[num_m]/F");
  tree_B_130->Branch("xip", xip, "xim[num_p]/F");
  tree_B_140->Branch("num_m", &num_m, "num_m/I");
  tree_B_140->Branch("num_p", &num_p, "num_p/I");
  tree_B_140->Branch("xim", xim, "xim[num_m]/F");
  tree_B_140->Branch("xip", xip, "xim[num_p]/F");
  tree_B_150->Branch("num_m", &num_m, "num_m/I");
  tree_B_150->Branch("num_p", &num_p, "num_p/I");
  tree_B_150->Branch("xim", xim, "xim[num_m]/F");
  tree_B_150->Branch("xip", xip, "xim[num_p]/F");

  tree_C_120->Branch("num_m", &num_m, "num_m/I");
  tree_C_120->Branch("num_p", &num_p, "num_p/I");
  tree_C_120->Branch("xim", xim, "xim[num_m]/F");
  tree_C_120->Branch("xip", xip, "xim[num_p]/F");
  tree_C_130->Branch("num_m", &num_m, "num_m/I");
  tree_C_130->Branch("num_p", &num_p, "num_p/I");
  tree_C_130->Branch("xim", xim, "xim[num_m]/F");
  tree_C_130->Branch("xip", xip, "xim[num_p]/F");
  tree_C_140->Branch("num_m", &num_m, "num_m/I");
  tree_C_140->Branch("num_p", &num_p, "num_p/I");
  tree_C_140->Branch("xim", xim, "xim[num_m]/F");
  tree_C_140->Branch("xip", xip, "xim[num_p]/F");
  tree_C_150->Branch("num_m", &num_m, "num_m/I");
  tree_C_150->Branch("num_p", &num_p, "num_p/I");
  tree_C_150->Branch("xim", xim, "xim[num_m]/F");
  tree_C_150->Branch("xip", xip, "xim[num_p]/F");

  tree_D_120->Branch("num_m", &num_m, "num_m/I");
  tree_D_120->Branch("num_p", &num_p, "num_p/I");
  tree_D_120->Branch("xim", xim, "xim[num_m]/F");
  tree_D_120->Branch("xip", xip, "xim[num_p]/F");
  tree_D_130->Branch("num_m", &num_m, "num_m/I");
  tree_D_130->Branch("num_p", &num_p, "num_p/I");
  tree_D_130->Branch("xim", xim, "xim[num_m]/F");
  tree_D_130->Branch("xip", xip, "xim[num_p]/F");
  tree_D_140->Branch("num_m", &num_m, "num_m/I");
  tree_D_140->Branch("num_p", &num_p, "num_p/I");
  tree_D_140->Branch("xim", xim, "xim[num_m]/F");
  tree_D_140->Branch("xip", xip, "xim[num_p]/F");
  tree_D_150->Branch("num_m", &num_m, "num_m/I");
  tree_D_150->Branch("num_p", &num_p, "num_p/I");
  tree_D_150->Branch("xim", xim, "xim[num_m]/F");
  tree_D_150->Branch("xip", xip, "xim[num_p]/F");

  tree_E_120->Branch("num_m", &num_m, "num_m/I");
  tree_E_120->Branch("num_p", &num_p, "num_p/I");
  tree_E_120->Branch("xim", xim, "xim[num_m]/F");
  tree_E_120->Branch("xip", xip, "xim[num_p]/F");
  tree_E_130->Branch("num_m", &num_m, "num_m/I");
  tree_E_130->Branch("num_p", &num_p, "num_p/I");
  tree_E_130->Branch("xim", xim, "xim[num_m]/F");
  tree_E_130->Branch("xip", xip, "xim[num_p]/F");
  tree_E_140->Branch("num_m", &num_m, "num_m/I");
  tree_E_140->Branch("num_p", &num_p, "num_p/I");
  tree_E_140->Branch("xim", xim, "xim[num_m]/F");
  tree_E_140->Branch("xip", xip, "xim[num_p]/F");
  tree_E_150->Branch("num_m", &num_m, "num_m/I");
  tree_E_150->Branch("num_p", &num_p, "num_p/I");
  tree_E_150->Branch("xim", xim, "xim[num_m]/F");
  tree_E_150->Branch("xip", xip, "xim[num_p]/F");

  tree_F_120->Branch("num_m", &num_m, "num_m/I");
  tree_F_120->Branch("num_p", &num_p, "num_p/I");
  tree_F_120->Branch("xim", xim, "xim[num_m]/F");
  tree_F_120->Branch("xip", xip, "xim[num_p]/F");
  tree_F_130->Branch("num_m", &num_m, "num_m/I");
  tree_F_130->Branch("num_p", &num_p, "num_p/I");
  tree_F_130->Branch("xim", xim, "xim[num_m]/F");
  tree_F_130->Branch("xip", xip, "xim[num_p]/F");
  tree_F_140->Branch("num_m", &num_m, "num_m/I");
  tree_F_140->Branch("num_p", &num_p, "num_p/I");
  tree_F_140->Branch("xim", xim, "xim[num_m]/F");
  tree_F_140->Branch("xip", xip, "xim[num_p]/F");
  tree_F_150->Branch("num_m", &num_m, "num_m/I");
  tree_F_150->Branch("num_p", &num_p, "num_p/I");
  tree_F_150->Branch("xim", xim, "xim[num_m]/F");
  tree_F_150->Branch("xip", xip, "xim[num_p]/F");

  TChain chain("Events");
  chain.Add( "Skims/2017/nanoAOD_Run2017B_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017C_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017D_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017E_Skim.root" );
  chain.Add( "Skims/2017/nanoAOD_Run2017F_Skim.root" );

  unsigned int run, event, num_proton;
  float crossingAngle;
  const unsigned short maxPro = 21;
  float proton_xi[maxPro];
  bool sector45[maxPro];

  chain.SetBranchAddress( "run", &run );
  chain.SetBranchAddress( "LHCInfo_crossingAngle", &crossingAngle );
  //chain.SetBranchAddress( "nProton_singleRP", &num_proton );
  //chain.SetBranchAddress( "Proton_singleRP_xi", proton_xi );
  //chain.SetBranchAddress( "Proton_singleRP_sector45", sector45 );
  chain.SetBranchAddress( "nProton_multiRP", &num_proton );
  chain.SetBranchAddress( "Proton_multiRP_xi", proton_xi );
  chain.SetBranchAddress( "Proton_multiRP_sector45", sector45 );


  unsigned int entries = chain.GetEntries();
  float progress = 0.00;
  int barWidth = 70;

  for ( unsigned int i=0; i<entries; i++ ) { // Loop over entries

    chain.GetEntry( i );

    //if ( i%1000000 == 0 ) std::cout << "i: " << i << " " << 100*i/entries << "% done" << std::endl;

    if ( i%100000 == 0 ) {
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


    if ( num_proton > 20 ) {
      //std::cout << "Skipping event i:" << i << " num proton: " << num_proton << std::endl;
      continue;
    }

    num_p = num_m = 0;

    for ( unsigned int j=0; j<num_proton; j++ ) { // Loop over protons

	  if (sector45[j]) {
	    xip[num_p] = proton_xi[j];
	    num_p += 1;
	  }
	  else {
	    xim[num_m] = proton_xi[j];
	    num_m += 1;
	  }


    } // End loop over protons

    // Fill tree based on era and crossingAngle
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
    

  } // End loop over entries

  std::cout << std::endl;


  std::cout << "Writing file" << std::endl;
  out->Write();
  out->Close();

}
