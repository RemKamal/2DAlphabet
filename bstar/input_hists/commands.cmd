# -*- sh -*- # for font lock mode
# variable definitions
- env = export SCRAM_ARCH=slc6_amd64_gcc491; eval `scramv1 project CMSSW CMSSW_7_4_7_patch2` ; cd CMSSW_7_4_7_patch2/src ; eval `scramv1 runtime -sh`; cd -
- tag = 
- output = outputFile=
- tagmode = none
- tarfile = /uscms_data/d3/lcorcodi/BStar13TeV/CMSSW_7_4_7_patch2/src/2DCombineFitCode/bstar/input_hists/tarball.tgz
- untardir = tardir
- copycommand = cp

# Sections listed
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT500 -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT700 -g on -c default -n 1 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1000 -g on -c default -n 1 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1500 -g on -c default -n 1 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT2000 -g on -c default -n 1 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT700 -g on -c default -n 2 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1000 -g on -c default -n 2 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1500 -g on -c default -n 2 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT2000 -g on -c default -n 2 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT700 -g on -c default -n 3 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1000 -g on -c default -n 3 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1500 -g on -c default -n 3 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT2000 -g on -c default -n 3 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT700 -g on -c default -n 4 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1000 -g on -c default -n 4 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1500 -g on -c default -n 4 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT2000 -g on -c default -n 4 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT700 -g on -c default -n 5 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1000 -g on -c default -n 5 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT1500 -g on -c default -n 5 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s QCDHT2000 -g on -c default -n 5 -j 5
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbarscaleup -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbarscaledown -g on -c default
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -J up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -J down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -R up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -R down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -a up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -a down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -b up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -b down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -x up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_t -g on  -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tB -g on  -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tW -g on  -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s singletop_tWB -g on  -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -x down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -p up
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s ttbar -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1200 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1400 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1600 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH1800 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2000 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2200 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2400 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2600 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH2800 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalLH3000 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1200 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1400 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1600 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH1800 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2000 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2200 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2400 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2600 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH2800 -g on -c default -p down
output_$(JID)        python ./tardir/TWanalyzer_2Dalphabet.py -s signalRH3000 -g on -c default -p down

