# PPSAnalyzer
Tools for RunII CMS PPS Diphoton analysis

## General instructions

### Create skims of nanoAOD files
The script to run the post-processing step is `postProcessor.py`.

Use the `keep_drop.txt` file to select relevant branches for your purposes.

### Create basic histograms
Create histograms using the `diphotonAnalyzer.py`.

For special purposes, create signal histograms using `signalStudy.py`

### Build nicer histograms
Finally, use the various plotting macros for the relevant plots:

`cutflow.py` builds a stacked histogram of various selection regions.

`plotDirectSimulation.py` makes acceptance and efficiency plots from the proton direct simulation.

`plotEfficiency.py` plots the signal efficiency of signal samples through CMS selection criteria.

`plotID.py` is for comparison of multiple EGamma photon IDs.

`plotKinematics.py` builds Data/MC stacked histograms and ratio plots for various photon kinematics.

`plotMatching.py` creates forward-central matching plots.

`plotProtonValidation.py` creates validation plots directly from the output of the PPS reconstruction plotter macro.

`plotProtons.py` makes proton plots from data such as xi, proton side, deector types, and more.

`plotResol.py` makes plots from simulation histograms of either photon or proton variables.

`plotSignal.py` makes plots of simulated diphoton kinematics.

`plotXi.py` compares the xi distributions of various selection regions.
