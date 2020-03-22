#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include <fstream>
#include <iostream>

#define input_file "Skims/nanoAOD_Run2017B_Skim.root"

void makeProtonTree( TString file=input_file )
{

  TFile f( file );
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

  for ( unsigned int i=0; i<tr->GetEntries(); i++ ) { // Loop over entries
    tr->GetEntry( i );
    if (i > 10) return;

    std::cout << "" << std::endl;
    std::cout << "i: " << i << " Era: " << input_file[21] << " xangle: "<< xangle << std::endl;

    for ( unsigned int j=0; j<num_proton; j++ ) { // Loop over protons
      
      if (sector45[j]) {
	  std::cout << "xip: " << proton_xi[j] << std::endl;
	}
      else {
	std::cout << "xim: " << proton_xi[j] << std::endl;
      }

    } // End loop over protons

  } // End loop over entries

}
