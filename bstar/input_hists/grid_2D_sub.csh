#! /bin/sh
# python Flist.py
# Have to copy over the necessary files first to make sure they're up-to-date
cp /uscms_data/d3/lcorcodi/BStar13TeV/CMSSW_7_4_1/src/BStar13TeV/bstar_theta_PtSF*.txt ./
cp /uscms_data/d3/lcorcodi/BStar13TeV/CMSSW_7_4_1/src/BStar13TeV/rootlogon.C ./
cp /uscms_data/d3/lcorcodi/BStar13TeV/CMSSW_7_4_1/src/BStar13TeV/Bstar_Functions.py ./
cp /uscms_data/d3/lcorcodi/BStar13TeV/CMSSW_7_4_1/src/BStar13TeV/Triggerweight_2jethack_data.root ./
cp /uscms_data/d3/lcorcodi/BStar13TeV/CMSSW_7_4_1/src/BStar13TeV/PileUp_Ratio_ttbar.root ./
cp /uscms_data/d3/lcorcodi/BStar13TeV/CMSSW_7_4_1/src/BStar13TeV/HistoWeight.py ./


tar czvf tarball.tgz bstar_theta_PtSF*.txt rootlogon.C TWanalyzer_2Dalphabet.py Bstar_Functions.py Triggerweight_2jethack_data.root PileUp_Ratio_ttbar.root
# mv Files*.txt txt_temp
./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \twoD.listOfJobs commands.cmd
./runManySections.py --submitCondor commands.cmd
condor_q lcorcodi
