
###################################################################
##								 ##
## Name: Bstar_Functions.py	   			         ##
## Author: Kevin Nash 						 ##
## Date: 5/13/2015						 ##
## Purpose: This contains all functions used by the              ##
##	    analysis.  A method is generally placed here if 	 ##
##	    it is called more than once in reproducing all	 ##
##	    analysis results.  The functions contained here 	 ##
##	    Are capable of tuning the analysis - such as changing##
##	    cross sections, updating lumi, changing file	 ##
##	    locations, etc. with all changes propegating 	 ##
##	    to all relevant files automatically.  		 ##
##								 ##
###################################################################

import os
import array
import glob
import math
from math import sqrt, exp, log
import ROOT
import sys
import time
import subprocess
import cppyy
from array import *
from ROOT import *
#This is the most impostant Function.  Correct information here is essential to obtaining valid results.
#In order we have Luminosity, top tagging scale factor, cross sections for wprime right,left,mixed,ttbar,qcd, and singletop and their corresponding event numbers
#If I wanted to access the left handed W' cross section at 1900 GeV I could do Xsecl1900 = LoadConstants()['xsec_wpl']['1900']
def LoadConstants():
	 return  {
		'lumi':35851.0,
		'wtagsf_HP':1.0,# HP = High purity
		'wtagsfsig_HP':0.06,
		'wtagsf_LP':0.96,# LP = Low purity
		'wtagsfsig_LP':0.11,
		'ttagsf':1.07,
		'ttagsf_errUp':0.15,
		'ttagsf_errDown':0.06,
		'xsec_bsl':{'1200': 1.944,'1400': 0.7848,'1600': 0.3431,'1800': 0.1588,'2000': 0.07711,'2200': 0.03881,'2400': 0.02015,'2600': 0.01073,'2800': 0.005829,'3000': 0.003234},
		'xsec_bsr':{'1200': 1.936,'1400': 0.7816,'1600': 0.3416,'1800': 0.1583,'2000': 0.07675,'2200': 0.03864,'2400': 0.02008,'2600': 0.01068,'2800': 0.005814,'3000': 0.003224},
		'xsec_bpl':{'B1200': 0.0016852,'B1400': 0.0007134,'B1600': 0.0003220,'B1800': 0.0001523,'T1200': 0.0016852,'T1400': 0.0007134,'T1600': 0.0003220,'T1800': 0.0001523},
		'xsec_ttbar':{'MG':831.76,'PH':831.76,'PHscaleup':831.76,'PHscaledown':831.76},
		'xsec_qcd':{'PT300':7823,'PT470':648.2,'PT600':186.9,'PT800':32.293,'PT1000':9.4183,'PT1400':0.84265,'PT1800':0.114943,'PT2400':0.00683,'PT3200':0.000165,'800_BROKEN':32.293,'FLAT7000':2022100000,'HT500':31630,'HT700':6802,'HT1000':1206,'HT1500':120.4,'HT2000':25.25},
		'xsec_st':{'S':11.36,'T':136.02,'TB':80.95,'TW':35.85,'TWB':35.85},
		#'nev_bsl':{'1200':99600,'1400':100000,'1600':100000,'1800':100000,'2000':100000,'2200':97000,'2400':100000,'2600':100000,'2800':98000,'3000':100000},
		#'nev_bsr':{'1200':100000,'1400':98200,'1600':100000,'1800':97600,'2000':99200,'2200':100000,'2400':97800,'2600':99200,'2800':99200,'3000':100000},
		#'nev_bpl':{'B1200': 100000,'B1400': 99200,'B1600': 99200,'B1800': 97600, 'T1200': 299200, 'T1400': 300000,'T1600': 293400,'T1800': 299600},
		#'nev_ttbar':{'MG':11339232, 'PH':180037820,'PHscaleup':9933327,'PHscaledown':9942427},
		#'nev_qcd':{'HT500':44058594,'HT700':15020802,'HT1000':4980387,'HT1500':1648549,'HT2000':1680210},
		#'nev_st':{'S':984400,'T':49858384,'TW':998400 ,'TWB':985000}
		}

#This is also a very impostant Function.  The analysis runs on "PSETS", which correspond to the TYPE variable here.
#These each load a cut profile.  For instance 'default' is the standard selection used to set limits
def LoadCuts(TYPE):
	if TYPE=='default':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.0,0.4],
			'sjbtag':[0.5426,1.0],
			'wmass':[65.0,105.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	if TYPE=='rate_default':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.4,1.0],
			'sjbtag':[0.5426,1.0],
			'wmass':[65.0,105.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	# Used for ttbar validation
	if TYPE=='sideband1':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.0,0.4],
			'sjbtag':[0.5426,1.0],
			'wmass':[130.0,float("inf")],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	if TYPE=='rate_sideband1':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.4,1.0],
			'sjbtag':[0.5426,1.0],
			'wmass':[65.0,105.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	# Sideband closure test
	if TYPE=='sideband':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.0,0.4],
			'sjbtag':[0.5426,1.0],
			'wmass':[30.0,65.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	if TYPE=='rate_sideband':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.4,1.0],
			'sjbtag':[0.5426,1.0],
			'wmass':[30.0,65.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	if TYPE=='highWmass':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.0,0.4],
			'sjbtag':[0.5426,1.0],
			'wmass':[105.0,130.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	if TYPE=='rate_highWmass':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.4,1.0],
			'sjbtag':[0.5426,1.0],
			'wmass':[105.0,130.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4],
			'eta':[0.0,2.4]
			}
	if TYPE=='alphabet':
		return  {
			'wpt':[400.0,float("inf")],
			'tpt':[400.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[155.0,195.0],
			'tau32':[0.0,0.65],
			'tau21':[0.4,1.0],
			'sjbtag':[0.5426,1.0],
			'wmass':[65.0,105.0],
			'eta':[0.0,2.4]
			}			

#This function loads up Ntuples based on what type of set you want to analyze.  
#This needs to be updated whenever new Ntuples are produced (unless the file locations are the same).
def Load_Ntuples(string,di=''):
	print 'running on ' + string 

	if di!='':
		files=open(di+'Files_'+string+'.txt').readlines()
		for i in range(0,len(files)):
			files[i] = files[i].replace('/eos/uscms','root://cmsxrootd.fnal.gov//').replace('\n','')

		try:
			print 'A total of ' + str(len(files)) + ' files'
		except:
			print 'Bad files option'
		return files


	if string == 'ttbar':
		files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Slim_V11/*/0000/*.root")
	if string == 'ttbarscaleup':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8/crab_TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8_B2GAnaFW_V2p5_80x_Slim_V11/170612_170816/0000/*.root")
	if string == 'ttbarscaledown':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8/crab_TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8_B2GAnaFW_V2p5_80x_Slim_V11/170612_171233/0000/*.root")

	#80X 2.4
	if string == 'QCDHT500':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/170611_054714/*/*.root")
	if string == 'QCDHT700':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/170611_055847/*/*.root")
	if string == 'QCDHT1000':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/170611_061036/*/*.root")
	if string == 'QCDHT1500':
		files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V11/*/*/*.root")
	if string == 'QCDHT2000':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/170611_062212/*/*.root")

	#80X 1.1
	if string == 'QCDPT300':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")	
	if string == 'QCDPT470':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")
	if string == 'QCDPT600':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")
	if string == 'QCDPT800':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")
	if string == 'QCDPT1000':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")
	if string == 'QCDPT1400':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")
	if string == 'QCDPT1800':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")
	if string == 'QCDPT2400':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")
	if string == 'QCDPT3200':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_B2GAnaFW_V1p1_80x_Slim_V3/*/0000/*.root")

	#80X V2.4 36420 pb-1
	if string == 'data':
		files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016B-03Feb2017-v3_B2GAnaFW_80X_V2p3_Slim_V12/170726_202146/0000/*.root")
		files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016C-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/170726_202209/0000/*.root")
		files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016D-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/170726_202107/0000/*.root")
		files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016E-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/170727_200439/0000/*.root")
		files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016F-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/170726_194657/0000/*.root")
		files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016G-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/170726_200042/0000/*.root")
		files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016H-03Feb2017_ver2-v1_B2GAnaFW_80X_V2p3_Slim_V12/170726_200119/0000/*.root")
		files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016H-03Feb2017_ver3-v1_B2GAnaFW_80X_V2p3_Slim_V12/170726_201018/0000/*.root")

	#80X V2.4
	if string == 'signalRH1200':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1200_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1200_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH1400':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1400_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1400_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH1600':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1600_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1600_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH1800':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1800_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1800_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH2000':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH2200':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2200_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2200_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH2400':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2400_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2400_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH2600':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2600_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2600_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH2800':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2800_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2800_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalRH3000':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-3000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-3000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")

	#80X V2.4
	if string == 'signalLH1200':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p5_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH1200_3p2':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V3p2_80x_Slim_V12/*/0000/*.root")
	if string == 'signalLH1400':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1400_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1400_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH1600':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1600_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1600_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH1800':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-1800_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-1800_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH2000':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2000_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2000_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH2200':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2200_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH2400':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2400_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2400_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH2600':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2600_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2600_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH2800':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-2800_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-2800_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p5_80x_Slim_V11/*/0000/*.root")
	if string == 'signalLH3000':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/BstarToTW_M-3000_LH_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_BstarToTW_M-3000_LH_TuneCUETP8M1_13TeV-madgraph-pythia8_B2GAnaFW_V2p4_80x_Slim_V11/*/0000/*.root")



	#80X 2.4 (CURRENTLY tW and tWB need to be rerun on slim level)
	# if string == 'singletop_s':
	# 	files = glob.glob("/eos/uscms/store/user/lcorcodi/crab_ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_B2GAnaFW_V2p4_80x_Slim_V7/170215_084815/0000/*.root")	
	if string == 'singletop_t':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/crab_ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin_B2GAnaFW_V2p4_80x_Slim_V11/170611_062429/0000/*.root")
	if string == 'singletop_tB':
		files = glob.glob("/eos/uscms/store/user/lcorcodi/ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/crab_ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_-powhegV2-madspin_B2GAnaFW_V2p4_80x_Slim_V11/170611_064940/0000/*.root")
	if string == 'singletop_tWB':
		files = glob.glob('/eos/uscms/store/user/lcorcodi/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/crab_ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_B2GAnaFW_V2p4_80x_Slim_V11/170621_025901/0000/*.root')
	if string == 'singletop_tW':
		files = glob.glob('/eos/uscms/store/user/lcorcodi/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/crab_ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_B2GAnaFW_V2p4_80x_Slim_V11/170612_200620/0000/*.root')




	#for i in range(0,len(files)):
	#	files[i] = files[i].replace('/eos/uscms/','root://cmsxrootd.fnal.gov//')
	
	
	
	try:
		print 'A total of ' + str(len(files)) + ' files'
	except:
		print 'Bad files option'
		files = []
	return files

#This function initializes the average b tagging rates used for QCD determination
#It tages the type of functional form as an argument.  The default fit is Bifpoly

def BTR_Init(ST,CUT,di,setval):

	if setval.find("QCD")==-1:
		setval = "data"


	if ST == 'Bifpoly':
		TRBPE1 = open("./"+di+"fitdata/bpinput"+setval+"eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open("./"+di+"fitdata/bpinput"+setval+"eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",BifPoly,0,4000,5)
		eta2fit = TF1("eta2fit",BifPoly,0,4000,5)
		Params = 5
	if ST == 'Bifpoly_err':
		TRBPE1 = open("./"+di+"fitdata/bperrorinput"+setval+"eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open("./"+di+"fitdata/bperrorinput"+setval+"eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit=TF1("eta1fit",BifPolyErr,0,4000,10)
		eta2fit=TF1("eta2fit",BifPolyErr,0,4000,10)
		Params = 10

	if ST == 'pol0':
		TRBPE1 = open("./"+di+"fitdata/pol0input"+setval+"eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open("./"+di+"fitdata/pol0input"+setval+"eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol0',0,2000)
		eta2fit = TF1("eta2fit",'pol0',0,2000)
		Params = 1

	if ST == 'pol2':
		TRBPE1 = open("./"+di+"fitdata/pol2input"+setval+"eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open("./"+di+"fitdata/pol2input"+setval+"eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol2',0,2000)
		eta2fit = TF1("eta2fit",'pol2',0,2000)
		Params = 3

	if ST == 'pol3':
		TRBPE1 = open("./"+di+"fitdata/pol3input"+setval+"eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open("./"+di+"fitdata/pol3input"+setval+"eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol3',0,2000)
		eta2fit = TF1("eta2fit",'pol3',0,2000)
		Params = 4
	if ST == 'FIT':
		TRBPE1 = open("./"+di+"fitdata/newfitinput"+setval+"eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open("./"+di+"fitdata/newfitinput"+setval+"eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,2000)
		eta2fit = TF1("eta2fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,2000)
		Params = 4
	if ST == 'expofit':
		TRBPE1 = open("./"+di+"fitdata/expoconinput"+setval+"eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open("./"+di+"fitdata/expoconinput"+setval+"eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'expo(0) + pol0(2)',0,2000)
		eta2fit = TF1("eta2fit",'expo(0) + pol0(2)',0,2000)
		Params = 3

	TBP1 = TRBPE1.read()
	TBP2 = TRBPE2.read()
	print "ST = " + ST
	for i in range(0,Params):
		eta1fit.SetParameter(i,float(TBP1.split('\n')[i]) )
		eta2fit.SetParameter(i,float(TBP2.split('\n')[i]) )

	return [eta1fit.Clone(),eta2fit.Clone()] 


#This function initializes the average b tagging rates used for QCD determination
#It tages the type of functional form as an argument.  The default fit is Bifpoly

#This is a poorly written function, but I cant think of a better way to do this 
#It works, but you should be able to just have one input
def TTR_Init(ST,CUT,SET,RATE,di,ptString):
	rateFolder = ''
	if RATE != 'tpt':
		rateFolder = RATE + '/'
	if ST == 'Bifpoly':
		TRBPE1 = open(di+"fitdata/"+rateFolder+"bpinput"+SET+"eta1_PSET_"+CUT+ptString+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/"+rateFolder+"bpinput"+SET+"eta2_PSET_"+CUT+ptString+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",BifPoly,0,4000,5)
		eta2fit = TF1("eta2fit",BifPoly,0,4000,5)
		Params = 5
	if ST == 'Bifpoly_err':
		TRBPE1 = open(di+"fitdata/"+rateFolder+"bperrorinput"+SET+"eta1_PSET_"+CUT+ptString+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/"+rateFolder+"bperrorinput"+SET+"eta2_PSET_"+CUT+ptString+".txt")
		TRBPE2.seek(0)
		eta1fit=TF1("eta1fit",BifPolyErr,0,4000,10)
		eta2fit=TF1("eta2fit",BifPolyErr,0,4000,10)
		Params = 10

	if ST == 'pol0':
		TRBPE1 = open(di+"fitdata/"+rateFolder+"pol0input"+SET+"eta1_PSET_"+CUT+ptString+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/"+rateFolder+"pol0input"+SET+"eta2_PSET_"+CUT+ptString+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol0',0,4000)
		eta2fit = TF1("eta2fit",'pol0',0,4000)
		Params = 1

	if ST == 'pol2':
		TRBPE1 = open(di+"fitdata/"+rateFolder+"pol2input"+SET+"eta1_PSET_"+CUT+ptString+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/"+rateFolder+"pol2input"+SET+"eta2_PSET_"+CUT+ptString+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol2',0,4000)
		eta2fit = TF1("eta2fit",'pol2',0,4000)
		Params = 3

	if ST == 'pol3':
		TRBPE1 = open(di+"fitdata/"+rateFolder+"pol3input"+SET+"eta1_PSET_"+CUT+ptString+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/"+rateFolder+"pol3input"+SET+"eta2_PSET_"+CUT+ptString+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol3',0,4000)
		eta2fit = TF1("eta2fit",'pol3',0,4000)
		Params = 4
	if ST == 'FIT':
		TRBPE1 = open(di+"fitdata/"+rateFolder+"newfitinput"+SET+"eta1_PSET_"+CUT+ptString+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/"+rateFolder+"newfitinput"+SET+"eta2_PSET_"+CUT+ptString+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,4000)
		eta2fit = TF1("eta2fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,4000)
		Params = 4
	if ST == 'expofit':
		TRBPE1 = open(di+"fitdata/"+rateFolder+"expoconinput"+SET+"eta1_PSET_"+CUT+ptString+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/"+rateFolder+"expoconinput"+SET+"eta2_PSET_"+CUT+ptString+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'expo(0) + pol0(2)',0,4000)
		eta2fit = TF1("eta2fit",'expo(0) + pol0(2)',0,4000)
		Params = 3
	if ST == 'QUAD':
		TRBP = open(di+"Alphabet/fn_bstar_QUAD_"+SET+"_pt"+CUT+ptString+".txt")
		TRBP.seek(0)
		fit = TF1("fit",'pol2',0,300)
		Params = 3
	if ST == 'QUAD_errUp':
		TRBP = open(di+"Alphabet/fn_bstar_QUAD_"+SET+"_pt"+CUT+ptString+".txt")
		TRBP.seek(0)
		fit = TF1("fit",'[0]+ [1]*x + [2]*x*x + sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		Params = 9
	if ST == 'QUAD_errDown':
		TRBP = open(di+"Alphabet/fn_bstar_QUAD_"+SET+"_pt"+CUT+ptString+".txt")
		TRBP.seek(0)
		fit = TF1("fit",'[0]+ [1]*x + [2]*x*x - sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		Params = 9
	try:
		TBP1 = TRBPE1.read()
		TBP2 = TRBPE2.read()
	except:
		TBP = TRBP.read()
	
	for i in range(0,Params):
		try:
			eta1fit.SetParameter(i,float(TBP1.split('\n')[i]) )
			eta2fit.SetParameter(i,float(TBP2.split('\n')[i]) )
		except:
			fit.SetParameter(i,float(TBP.split('\n')[i]) )

	try:
		return [eta1fit.Clone(),eta2fit.Clone()] 
	except:
		return [fit.Clone()]

def Alpha_Init(ETA,CUT,SET,di):
# ETA = split, split_errup/down, full, full_errup/down
# CUT = default,sideband
# SET = data, QCD
# di = grid on or off
	folder = di+'fitdata/alphabet/'
	if ETA == 'split':
		TRBPE1 = open(folder+"Mt_pol2_"+SET+"_eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(folder+"Mt_pol2_"+SET+"_eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol2',0,300)
		eta2fit = TF1("eta2fit",'pol2',0,300)
		Params = 3
	if ETA == 'split_errup':
		TRBPE1 = open(folder+"Mt_pol2_"+SET+"_eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(folder+"Mt_pol2_"+SET+"_eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'[0]+ [1]*x + [2]*x*x + sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		eta2fit = TF1("eta2fit",'[0]+ [1]*x + [2]*x*x + sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		Params = 9
	if ETA == 'split_errdown':
		TRBPE1 = open(folder+"Mt_pol2_"+SET+"_eta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(folder+"Mt_pol2_"+SET+"_eta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'[0]+ [1]*x + [2]*x*x - sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		eta2fit = TF1("eta2fit",'[0]+ [1]*x + [2]*x*x - sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		Params = 9
	
	if ETA == 'full':
		TRBP = open(folder+"Mt_pol2_"+SET+"_full_PSET_"+CUT+".txt")
		TRBP.seek(0)
		eta1fit = TF1("fit",'pol2',0,300)
		Params = 3
	if ETA == 'full_errup':
		TRBP = open(folder+"Mt_pol2_"+SET+"_eta1_PSET_"+CUT+".txt")
		TRBP.seek(0)
		fit = TF1("eta1fit",'[0]+ [1]*x + [2]*x*x + sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		Params = 9
	if ETA == 'full_errdown':
		TRBP = open(folder+"Mt_pol2_"+SET+"_eta1_PSET_"+CUT+".txt")
		TRBP.seek(0)
		fit = TF1("eta1fit",'[0]+ [1]*x + [2]*x*x - sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))',0,300)
		Params = 9

	# Try to read the imported file
	try:
		TBP1 = TRBPE1.read()
		TBP2 = TRBPE2.read()
	except:
		TBP = TRBP.read()
	
	# For each parameter, try to set it in the fit (reconstructing the fit)
	for i in range(0,Params):
		try:
			eta1fit.SetParameter(i,float(TBP1.split('\n')[i]) )
			eta2fit.SetParameter(i,float(TBP2.split('\n')[i]) )
		except:
			fit.SetParameter(i,float(TBP.split('\n')[i]) )

	# return the fit
	try:
		return [eta1fit.Clone(),eta2fit.Clone()] 
	except:
		return [fit.Clone()]

#This takes the average t tagging rates that are initialized in the above function and produces 
#A QCD background estimate based on them 
def bkg_weight_pt(vector, funcs, etabins):
	for ibin in range(0,len(etabins)):
		if (etabins[ibin][0] <= abs(vector.Eta()) < etabins[ibin][1]) :
			tagratept = funcs[ibin].Eval(vector.Perp())		
	return tagratept

def bkg_weight_mass(vector, funcs, etabins):
	if (etabins[0] <= abs(vector.Eta()) < etabins[1]) :
		tagratetmass = funcs[0].Eval(vector.M())		
	return tagratetmass

def bkg_weight_twmass(vector, MtopW, funcs, etabins):
	for ibin in range(0,len(etabins)):
		if (etabins[ibin][0] <= abs(vector.Eta()) < etabins[ibin][1]) :
			tagratetwmass = funcs[ibin].Eval(MtopW)		
	return tagratetwmass

#This is the bifurcated polynomial function and its associated uncertainty 
def BifPoly( x, p ):
	xx=x[0]
	if xx<p[4]:
		return p[0]+p[1]*xx+p[2]*(xx-p[4])**2
	else:
		return p[0]+p[1]*xx+p[3]*(xx-p[4])**2
def BifPolyErr( x, p ):
	xx=x[0]
	if xx<p[9]:
		return p[0]+p[1]*xx**2+p[2]*(xx-p[9])**4+p[3]*xx+p[4]*(xx-p[9])**2+p[5]*xx*(xx-p[9])**2
	else:
		return p[0]+p[1]*xx**2+p[6]*(xx-p[9])**4+p[3]*xx+p[7]*(xx-p[9])**2+p[8]*xx*(xx-p[9])**2

#This looks up the PDF uncertainty
# def PDF_Lookup( pdfs , pdfOP ):
# 	iweight = 0.0
# 	#print "LEN"
# 	#print len(pdfs)
# 	ave =  pdfs
# 	ave =  reduce(lambda x, y: x + y, pdfs) / len(pdfs)
# 	#print ave
# 	for pdf in pdfs :
# 		iweight = iweight + (pdf-ave)*(pdf-ave)

# 	if pdfOP == "up" :
# 		return 1+sqrt((iweight) / (len(pdfs)))
# 	else :
# 		return 1-sqrt((iweight) / (len(pdfs)))

def PDF_Lookup(pdfs , pdfOP ):
	ilimweight = 0.0

	limitedpdf = []
	for curpdf in pdfs:
		if abs(curpdf)<1000.0:
			limitedpdf.append(curpdf)


	limave =  limitedpdf
	limave =  reduce(lambda x, y: x + y, limitedpdf) / len(limitedpdf)
	#print ave
	for limpdf in limitedpdf :
		ilimweight = ilimweight + (limpdf-limave)*(limpdf-limave)

	if pdfOP == "up" :
		return min(13.0,1.0+sqrt((ilimweight) / (len(limitedpdf))))
	else :
		return max(-12.0,1.0-sqrt((ilimweight) / (len(limitedpdf))))
#This looks up the b tagging scale factor or uncertainty
def Trigger_Lookup( H , TRP ):
	Weight = 1.0
	Weightup = 1.0
	Weightdown = 1.0
	if H < 1200.0:
		bin0 = TRP.FindBin(H) 
		jetTriggerWeight = TRP.GetBinContent(bin0)
		Weight = jetTriggerWeight
		deltaTriggerEff  = 0.5*(1.0-jetTriggerWeight)
		Weightup  =   min(1.0,jetTriggerWeight + deltaTriggerEff)
		Weightdown  =   max(0.0,jetTriggerWeight - deltaTriggerEff)
		
	return [Weight,Weightup,Weightdown]

#This looks up the PDF uncertainty
def SFT_Lookup( pttop ):
	ttagsf = [[0.82,0.09],[0.93,0.20]]
	ttagsfregions = [[0,550],[550,float("inf")]]

	for ipttop in range(0,len(ttagsfregions)):
		if ttagsfregions[ipttop][0]<pttop<=ttagsfregions[ipttop][1]:
			return [ttagsf[ipttop][0],ttagsf[ipttop][0]-ttagsf[ipttop][1],ttagsf[ipttop][0]+ttagsf[ipttop][1]]


#
def Trigger_Pass(tnamestr,trigs,bits):
	###TAKE OUT!
	#tnamestr = ['HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p45_v2','HLT_PFHT800_v1']

	for t in range(0,len(trigs)):
		for tname in tnamestr:	
			if trigs[t]==tname and bits[t] :
				return True
	return False

#This looks up the ttbar pt reweighting scale factor when making ttrees
def PTW_Lookup( GP ):
		genTpt = -100.
		genTBpt = -100	
		for ig in GP :
			isT = ig.pdgId() == 6 and ig.status() == 22
			isTB = ig.pdgId() == -6 and ig.status() == 22
			if isT:
				genTpt = ig.pt()
			if isTB:
				genTBpt = ig.pt()	
		if (genTpt<0) or (genTBpt<0):
			print "ERROR"

		# wTPt = exp(0.156-0.00137*genTpt)
		# wTbarPt = exp(0.156-0.00137*genTBpt)

		wTPt = exp(0.0615-0.0005*genTpt)
		wTbarPt = exp(0.0615-0.0005*genTBpt)
		return sqrt(wTPt*wTbarPt)


# This does the W jet matching requirement by looking up the deltaR separation
# of the daughter particle from the W axis. If passes, return 1.
def WJetMatching(GP):
	passed = 0
	failedDaughters = 0
	for ig in GP:
		isWp = ig.pdgId() == 24 and ig.status() == 22
		isWm = ig.pdgId() == -24 and ig.status() == 22
		if isWp or isWm:
			Wvect = TVector3()
			Wvect.SetPtEtaPhi(ig.pt(),ig.eta(),ig.phi())

			genDaughters = []
			daughterVects = []
			for d in range(ig.numberOfDaughters()):
				genDaughters.append(ig.daughter(d))
				thisDaughter = genDaughters[d]
				daughterVects.append(TVector3())
				daughterVects[d].SetPtEtaPhi(thisDaughter.pt(),thisDaughter.eta(),thisDaughter.phi())

			for daughter in daughterVects:
				if Wvect.DeltaR(daughter) > 0.8:
					failedDaughters += 1

	if failedDaughters == 0:
		passed = 1

	return passed

			 
def PU_Lookup(PU , PUP):
	PUWeight = 1.0
	PUWeightup = 1.0
	PUWeightdown = 1.0

	bin1 = PUP[0].FindBin(float(PU))

	PUWeight = PUP[0].GetBinContent(bin1)
	PUWeightup = PUP[1].GetBinContent(bin1)
	PUWeightdown = PUP[2].GetBinContent(bin1)

	return [PUWeight,PUWeightup,PUWeightdown]

def Hemispherize(LV1,LV2):
	tjets = [[],[]]
	wjets = [[],[]]
	for iLV1 in range(0,len(LV1)):
		if abs(Math.VectorUtil.DeltaPhi(LV1[0],LV1[iLV1]))> TMath.Pi()/2.0:
			tjets[1].append(iLV1)
		else:
			tjets[0].append(iLV1)
	for iLV2 in range(0,len(LV2)):
		if abs(Math.VectorUtil.DeltaPhi(LV1[0],LV2[iLV2]))> TMath.Pi()/2.0:
			wjets[1].append(iLV2)
		else:
			wjets[0].append(iLV2)
	return tjets,wjets

#This is just a quick function to automatically make a tree
#This is used right now to automatically output branches used to validate the cuts used in a run
def Make_Trees(Floats, treeName='Tree'):
	t = TTree(treeName, treeName);
	print "Booking trees"
	for F in Floats.keys():
		t.Branch(F, Floats[F], F+"/D")
	return t

# Quick way to get extrapolation uncertainty
def ExtrapUncert_Lookup(pt,purity):
	if purity == 'HP':
		x = 0.085
	elif purity == 'LP':
		x = 0.039
	extrap_uncert = x*log(pt/200)
	return extrap_uncert

#This takes all of the alternative fit forms for the average b tagging rate and 
#Compares them to the chosen nominal fit (bifpoly).  It outputs the mean squared error uncertainty from this comparison 
def Fit_Uncertainty(List):
	sigmah	    = List[0]
	fits=len(List)-1
	for ihist in range(0,len(List)):
		if List[ihist].GetName() == 'QCDbkgBifpoly':
			nominalhist = List[ihist]
	for ibin in range(0,nominalhist.GetXaxis().GetNbins()+1):

		mse=0.0
		sigma=0.0
		sumsqdiff = 0.0
		for ihist in range(0,len(List)):
			if List[ihist].GetName() != 'QCDbkgBifpoly':
				sumsqdiff+=(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))*(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))
		mse = sumsqdiff/fits
		sigma = sqrt(mse)
		sigmah.SetBinContent(ibin,sigma)
	
	return sigmah

#Same as Fit_Uncertainty but optimized to work with kinematic variables
def kinFit_Uncertainty(List,kinVar):
	sigmah	    = List[0]
	fits=len(List)-1
	for ihist in range(0,len(List)):
		if List[ihist].GetName() == 'QCDbkg'+kinVar+'Bifpoly':
			nominalhist = List[ihist]
	for ibin in range(0,nominalhist.GetXaxis().GetNbins()+1):

		mse=0.0
		sigma=0.0
		sumsqdiff = 0.0
		for ihist in range(0,len(List)):
			if List[ihist].GetName() != 'QCDbkg'+kinVar+'Bifpoly':
				sumsqdiff+=(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))*(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))
		mse = sumsqdiff/fits
		sigma = sqrt(mse)
		sigmah.SetBinContent(ibin,sigma)
	
	return sigmah


#Creates 15 bins of variable size (used in TWrate_Maker.py)
#Returns a list that are the leading edges of the bins
# NOT WORKING 12/4/16
def variableBins (TF1plot, newNumberOfBins):
	xMax = int(TF1plot.GetXaxis().GetXmax())	#maximum x value with an actual entry
	oldLeastBin = TF1plot.FindFirstBinAbove(0)	#first bin with an actual entry
	oldMaxBin = TF1plot.FindLastBinAbove(0)		#last bin with an actual entry
	oldNumberOfBins = TF1plot.GetNbinsX()		#Previous number of bins
	oldBinSize = xMax/oldNumberOfBins		#And their size

	print "xMax: " + str(xMax)
	print "oldLeastBin: " + str(oldLeastBin)
	print "oldMaxBin: " + str(oldMaxBin)
	print "oldNumberOfBins: " + str(oldNumberOfBins)
	print "oldBinSize: " + str(oldBinSize)

	#newEventsPerBin is a list designed such that low pt bins have more events per bin than high pt bins (linearized)
	#Will use point slope form with two points being (plotMax, 0) and (binOfAvg,avgEventsPerBin)

	#First point coordinates
	avgEventsPerBin = TF1plot.Integral()/oldNumberOfBins
	oldBinOfAvg = TF1plot.FindLastBinAbove(avgEventsPerBin)
	print "avgEventsPerBin: " + str(avgEventsPerBin)
	print "oldBinOfAvg: " + str(oldBinOfAvg)
	#Secon point coordinate (y is just 0)
	plotMax = TF1plot.GetBinLowEdge(oldMaxBin+1)
	#A slope from these
	slope = (-avgEventsPerBin)/(xMax-oldBinOfAvg)

	#This isn't the greatest but we divide the bins up evenly to estimate how many events in each
	#If the real distribution was linear, rebinning like this would do nothing
	newBinSize = int(xMax/newNumberOfBins)
	#Initialize array
	newEventsPerBin = [] #should only be size of newNumberOfBins
	for i in range(newNumberOfBins):
		xPosition = int(TF1plot.GetXaxis().GetBinCenter(oldMaxBin))-i*newBinSize
		if xPosition < 0:
			print "Out of range"
			continue
		#y = m(x-x1)+y1 where (x1,y1) is x intercept
		newEventsInBin = slope*(xPosition-xMax)
		newEventsPerBin.append(newEventsInBin)

	#Reverse it since you start at high pt	
	newEventsPerBin.reverse()
	print newEventsPerBin
	#Now use list of events per bin to actuall make the bins
	finalBins = [plotMax]
	totalNewBinVal = 0
	newBinIndex = len(newEventsPerBin)-1
	
	for ibin in range(oldMaxBin,oldLeastBin-1,-1):
		val = TF1plot.GetBinContent(ibin)
		if len(finalBins) == newNumberOfBins-1:
			print "on final bin"
			finalBins.append(TF1plot.GetBinLowEdge(oldLeastBin))
			print "Bin we're in: " + str(newBinIndex)
			newBinIndex-=1
			continue
		if totalNewBinVal + val < newEventsPerBin[newBinIndex]:
			totalNewBinVal += val
		elif (totalNewBinVal + val) < (newEventsPerBin[newBinIndex] + val/2):
			print "adding bin: " + 	str(TF1plot.GetBinLowEdge(ibin))
			print "totalNewBinVal = " + str(totalNewBinVal+val)	
			finalBins.append(TF1plot.GetBinLowEdge(ibin))
			print "Bin we're in: " + str(newBinIndex)
			newBinIndex-=1
			totalNewBinVal = 0
		elif (totalNewBinVal + val) > (newEventsPerBin[newBinIndex] + val/2):
			print "going back one and adding: " + 	str(TF1plot.GetBinLowEdge(ibin+1))
			print "totalNewBinVal = " + str(totalNewBinVal) + "instead of " + str(totalNewBinVal+val)	
			finalBins.append(TF1plot.GetBinLowEdge(ibin+1))
			print "Bin we're in: " + str(newBinIndex)	
			newBinIndex-=1
			totalNewBinVal = 0

	finalBins.reverse()
	return finalBins

#Makes the blue pull plots
def Make_Pull_plot( DATA,BKG,BKGUP,BKGDOWN ):
	pull = DATA.Clone("pull")
	pull.Add(BKG,-1)
	sigma = 0.0
	FScont = 0.0
	BKGcont = 0.0
	for ibin in range(1,pull.GetNbinsX()+1):
		FScont = DATA.GetBinContent(ibin)
		BKGcont = BKG.GetBinContent(ibin)
		if FScont>=BKGcont:
			FSerr = DATA.GetBinErrorLow(ibin)
			BKGerr = abs(BKGUP.GetBinContent(ibin)-BKG.GetBinContent(ibin))
		if FScont<BKGcont:
			FSerr = DATA.GetBinErrorUp(ibin)
			BKGerr = abs(BKGDOWN.GetBinContent(ibin)-BKG.GetBinContent(ibin))
		sigma = sqrt(FSerr*FSerr + BKGerr*BKGerr)
		if FScont == 0.0:
			pull.SetBinContent(ibin, 0.0 )	
		else:
			if sigma != 0 :
				pullcont = (pull.GetBinContent(ibin))/sigma
				pull.SetBinContent(ibin, pullcont)
			else :
				pull.SetBinContent(ibin, 0.0 )
	return pull
#Some lazy string formatting functions 
def strf( x ):
	return '%.2f' % x

def strf1( x ):
	return '%.0f' % x

# Built to wait for condor jobs to finish and then check that they didn't fail
# The script that calls this function will quit if there are any job failures
# listOfJobs input should be whatever comes before '.listOfJobs' for the set of jobs you submitted
def WaitForJobs( listOfJobs ):
	# Runs grep to count the number of jobs - output will have non-digit characters b/c of wc
	preNumberOfJobs = subprocess.check_output('grep "python" '+listOfJobs+'.listOfJobs | wc -l', shell=True)
	commentedNumberOfJobs = subprocess.check_output('grep "# python" '+listOfJobs+'.listOfJobs | wc -l', shell=True)

	# Get rid of non-digits and convert to an int
	preNumberOfJobs = int(filter(lambda x: x.isdigit(), preNumberOfJobs))
	commentedNumberOfJobs = int(filter(lambda x: x.isdigit(), commentedNumberOfJobs))
	numberOfJobs = preNumberOfJobs - commentedNumberOfJobs

	finishedJobs = 0
	# Rudementary progress bar
	while finishedJobs < numberOfJobs:
		# Count how many output files there are to see how many jobs finished
		# the `2> null.txt` writes the stderr to null.txt instead of printing it which means
		# you don't have to look at `ls: output_*.log: No such file or directory`
		finishedJobs = subprocess.check_output('ls output_*.log 2> null.txt | wc -l', shell=True)
		finishedJobs = int(filter(lambda x: x.isdigit(), finishedJobs))
		sys.stdout.write('\rProcessing ' + str(listOfJobs) + ' - ')
		# Print the count out as a 'progress bar' that refreshes (via \r)
		sys.stdout.write("%i / %i of jobs finished..." % (finishedJobs,numberOfJobs))
		# Clear the buffer
		sys.stdout.flush()
		# Sleep for one second
		time.sleep(1)


	print 'Jobs completed. Checking for errors...'
	numberOfTracebacks = subprocess.check_output('grep -i "Traceback" output*.log | wc -l', shell=True)
	numberOfSyntax = subprocess.check_output('grep -i "Syntax" output*.log | wc -l', shell=True)

	numberOfTracebacks = int(filter(lambda x: x.isdigit(), numberOfTracebacks))
	numberOfSyntax = int(filter(lambda x: x.isdigit(), numberOfSyntax))

	# Check there are no syntax or traceback errors
	# Future idea - check output file sizes
	if numberOfTracebacks > 0:
		print str(numberOfTracebacks) + ' job(s) failed with traceback error'
		quit()
	elif numberOfSyntax > 0:
		print str(numberOfSyntax) + ' job(s) failed with syntax error'
		quit()
	else:
		print 'No errors!'

# Scales the up and down pdf uncertainty distributions to the nominal value to isolate the shape uncertainty
def PDFShapeUncert(nominal, up, down):
	upShape = up.Clone("Mtw")
	downShape = down.Clone("Mtw")
	upShape.Scale(nominal.Integral()/up.Integral())
	downShape.Scale(nominal.Integral()/down.Integral())

	return upShape, downShape

# Creates ratios between the events in up/down PDF distributions to nominal distribution and
# used the ratio to derive up/down xsec values for the given mass point
def PDFNormUncert(nominal, up, down, xsec_nominal):
	ratio_up = up.Integral()/nominal.Integral()
	ratio_down = down.Integral()/nominal.Integral()

	xsec_up = ratio_up*xsec_nominal
	xsec_down = ratio_down*xsec_nominal

	return xsec_up, xsec_down
