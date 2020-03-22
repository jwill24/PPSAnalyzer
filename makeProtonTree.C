#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include <fstream>
#include <iostream>

#define input_file "Skims/nanoAOD_Run2017B_Skim.root"
#define output_file "protonEvents.root"

void makeProtonTree( TString inFile=input_file, TString outFile=output_file )
{

  TFile* out = new TFile( outFile, "RECREATE" );
  TTree* tree_B_140 = new TTree( "tree_B_140", "tree for protons");

  unsigned short maxProSide = 6;
  unsigned int num_m, num_p;
  float xim[maxProSide], xip[maxProSide];
  tree_B_140->Branch("num_m", &num_m, "num_m/I");
  tree_B_140->Branch("num_p", &num_p, "num_p/I");
  tree_B_140->Branch("xim", xim, "xim[num_m]/F");
  tree_B_140->Branch("xip", xip, "xim[num_p]/F");


  TFile f( inFile );
  if ( !f.IsOpen() ) return;
  TTree* tr = dynamic_cast<TTree*>( f.Get( "Events" ) );

  unsigned int run, num_proton;
  float xangle;
  const unsigned short maxPro = 12;
  float proton_xi[maxPro];
  bool sector45[maxPro];
  tr->SetBranchAddress( "run", &run );
  tr->SetBranchAddress( "LHCInfo_xangle", &xangle );
  tr->SetBranchAddress( "nProton_singleRP", &num_proton );
  tr->SetBranchAddress( "Proton_singleRP_xi", proton_xi );
  tr->SetBranchAddress( "Proton_singleRP_sector45", sector45 );


  for ( unsigned int i=0; i<10; i++ ) { // Loop over entries tr->GetEntries()
    tr->GetEntry( i );
    
    std::cout << "" << std::endl;
    std::cout << "i: " << i << " Era: " << input_file[21] << " xangle: "<< xangle << std::endl;

    num_p = num_m = 0;

    for ( unsigned int j=0; j<num_proton; j++ ) { // Loop over protons

      if (TString(input_file[21]) == "B") {
	if (xangle == 140) {


	  if (sector45[j]) {
	    xip[num_p] = proton_xi[j];
	    num_p += 1;
	  }
	  else {
	    xim[num_m] = proton_xi[j];
	    num_m += 1;
	  }


	}
      }
      
    } // End loop over protons

    std::cout << "Filling the tree" << std::endl;
    if ( xangle == 140 && TString(input_file[21]) == "B" ) tree_B_140->Fill();
    
  } // End loop over entries

  std::cout << "Writing file" << std::endl;
  out->Write();
  out->Close();

}
