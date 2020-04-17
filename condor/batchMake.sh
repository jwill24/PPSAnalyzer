#!/bin/bash

SRCDIR=/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PPSAnalyzer

#selections='HLT Preselection ID ReverseElastic Elastic Xi'
#selections='ID ReverseElastic Elastic Xi'
selections='HLT'

#samples='ggj2018 g+j2018 qcd2018 wg2018 zg2018 tt2018 data2018'
#samples='ggj2018 g+j2018 qcd2018 wg2018 zg2018 tt2018'
samples='ggj2018'
#samples='ggj2017 g+j2017 qcd2017 wg2017 zg2017 tt2017 aqgc2017 data2017'

for selection in $selections
do
    for sample in $samples
    do

	SEL=$selection
	SAM=$sample

	SHF=${SRCDIR}/condor/sub_${SAM}_${SEL}.sh
	PYF=${SRCDIR}/diphotonAnalysis.py

	if [ -f ${SHF} ];
	then
	    rm ${SHF}
	else
	    touch ${SHF}
	fi


	echo "#!/bin/bash" >> ${SHF}
	
	echo  "export XRD_NETWORKSTACK=IPv4" >> ${SHF}
	
	echo  "export LSB_JOB_REPORT_MAIL=N" >> ${SHF}
	
	echo  "export X509_USER_PROXY=/tmp/x509up_u5745" >> ${SHF}
	
	echo "export PATH=/cvmfs/cms.cern.ch/crab3/slc6_amd64_gcc493/cms/crabclient/3.3.2001/bin:/cvmfs/cms.cern.ch/crab3/slc6_amd64_gcc493/cms/crabclient/3.3.2001/bin:/cvmfs/cms.cern.ch/crab3/slc6_amd64_gcc493/cms/crabclient/3.3.2001/bin:/cvmfs/cms.cern.ch/share/overrides/bin:/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/bin/slc7_amd64_gcc700:/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/external/slc7_amd64_gcc700/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_11_0_0_pre6/bin/slc7_amd64_gcc700:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_11_0_0_pre6/external/slc7_amd64_gcc700/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/llvm/7.1.0-nmpfii/bin:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0-pafccj/bin:/cvmfs/cms.cern.ch/common:/usr/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin"  >> ${SHF}


	echo  "export LD_LIBRARY_PATH=/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/biglib/slc7_amd64_gcc700:/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/lib/slc7_amd64_gcc700:/home/t3-ku/juwillia/CMSSW_11_0_0_pre6/external/slc7_amd64_gcc700/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_11_0_0_pre6/biglib/slc7_amd64_gcc700:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_11_0_0_pre6/lib/slc7_amd64_gcc700:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_11_0_0_pre6/external/slc7_amd64_gcc700/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/llvm/7.1.0-nmpfii/lib64:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0-pafccj/lib64:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0-pafccj/lib:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/cuda/10.1.105-pafccj2/drivers"  >> ${SHF}

	echo " " >> ${SHF}
	
	echo  "cd /home/t3-ku/juwillia/CMSSW_11_0_0_pre6/src/PPSAnalyzer/" >> ${SHF}
	
	echo " " >> ${SHF}
	
	echo  "eval \`scramv1 runtime -sh\`"  >> ${SHF}
	
	echo " " >> ${SHF}

	echo  "python $PYF $SAM $SEL" >> ${SHF}

	chmod 744 ${SHF}

	echo "File:${SHF} was created"
	
    done
done


