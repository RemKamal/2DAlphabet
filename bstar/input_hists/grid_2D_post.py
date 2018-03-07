#! /usr/bin/env python
#BUILT FOR MULTIPLE LUMIS
import re
import os
import subprocess
from os import listdir
from os.path import isfile, join
import glob
import math
import ROOT
from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')
parser.add_option('-q', '--justqcd', metavar='F', type='string', action='store',
				  default	=	'off',
				  dest		=	'justqcd',
				  help		=	'on, off')

 
(options, args) = parser.parse_args()

cuts = options.cuts

import Bstar_Functions	
from Bstar_Functions import *

#Load up cut values based on what selection we want to run 
Cons = LoadConstants()
cLumi = Cons['lumi']

# Grab xsec values
xsec_bsl = Cons['xsec_bsl']
xsec_bsr = Cons['xsec_bsr']
xsec_ttbar = Cons['xsec_ttbar']
xsec_qcd = Cons['xsec_qcd']
xsec_st = Cons['xsec_st']
xsec_bpl = Cons['xsec_bpl']


files = sorted(glob.glob("*job*of*.root"))

# Setup some names that we'll loop over
filestr = ['none','JES_up','JES_down','JER_up','JER_down','JMS_up','JMS_down','JMR_up','JMR_down']
pdfstr = ['pdf_up','pdf_down']
pilestr = ['pileup_up','pileup_down']

j = []
for f in files:
	j.append(f.replace('_jo'+re.search('_jo(.+?)_PSET', f).group(1),""))

# Sum up the jobs
files_to_sum = list(set(j))
print files_to_sum
commands = []
commands.append('rm *.log') 
commands.append('rm temprootfiles/*.root')
commands.append('rm -rf notneeded')
for f in files_to_sum:
	commands.append('rm '+f) 
	commands.append('hadd ' + f + " " + f.replace('_PSET','_job*_PSET') )
	commands.append('mv ' +  f.replace('_PSET','_job*_PSET') + ' temprootfiles/')
	#commands.append('mv ' +  f + ' rootfiles/')

# Sum up the QCD files
commands.append('rm rootfiles/TW2DalphabetQCD_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root')
commands.append('python HistoWeight.py -i TW2DalphabetQCDHT500_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -o rootfiles/TW2DalphabetweightedQCDHT500_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_qcd['HT500']))
commands.append('python HistoWeight.py -i TW2DalphabetQCDHT700_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -o rootfiles/TW2DalphabetweightedQCDHT700_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_qcd['HT700']))
commands.append('python HistoWeight.py -i TW2DalphabetQCDHT1000_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -o rootfiles/TW2DalphabetweightedQCDHT1000_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_qcd['HT1000']))
commands.append('python HistoWeight.py -i TW2DalphabetQCDHT1500_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -o rootfiles/TW2DalphabetweightedQCDHT1500_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_qcd['HT1500']))
commands.append('python HistoWeight.py -i TW2DalphabetQCDHT2000_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -o rootfiles/TW2DalphabetweightedQCDHT2000_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_qcd['HT2000']))
commands.append('hadd TW2DalphabetQCD_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root rootfiles/TW2DalphabetweightedQCDHT*_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root')
commands.append('mv TW2DalphabetQCD_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root rootfiles/')
commands.append('mv TW2DalphabetQCDHT*_Trigger_nominal_*_PSET_'+cuts+'.root temprootfiles/')

# Exit out if you're just doing qcd
if options.justqcd == 'on':
	for s in commands :
		print 'executing ' + s
		subprocess.call( [s], shell=True )
	quit()


# Do all of the ttbars
for scale in ['scaleup','scaledown']:
	commands.append('rm rootfiles/TW2Dalphabetweightedttbar'+scale+'_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root')
	commands.append('python HistoWeight.py -i TW2Dalphabetttbar'+scale+'_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -o rootfiles/TW2Dalphabetweightedttbar'+scale+'_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_ttbar['PH'+scale]))
	commands.append('mv TW2Dalphabetttbar'+scale+'_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root temprootfiles/')
for f in filestr:
	commands.append('rm rootfiles/TW2Dalphabetweightedttbar_Trigger_nominal_'+f+'_PSET_'+cuts+'.root') #removes old file with same name in /rootfiles/
	commands.append('python HistoWeight.py -i TW2Dalphabetttbar_Trigger_nominal_'+f+'_PSET_'+cuts+'.root -o rootfiles/TW2Dalphabetweightedttbar_Trigger_nominal_'+f+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_ttbar['PH']))
	commands.append('mv TW2Dalphabetttbar_Trigger_nominal_'+f+'_PSET_'+cuts+'.root temprootfiles/')
for p in pdfstr:
	commands.append('rm rootfiles/TW2Dalphabetweightedttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root') #removes old file with same name in /rootfiles/
	commands.append('python HistoWeight.py -i TW2Dalphabetttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root -o rootfiles/TW2Dalphabetweightedttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_ttbar['PH']))
	commands.append('mv TW2Dalphabetttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root temprootfiles/')
for p in pilestr:
	commands.append('rm rootfiles/TW2Dalphabetweightedttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root') #removes old file with same name in /rootfiles/
	commands.append('python HistoWeight.py -i TW2Dalphabetttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root -o rootfiles/TW2Dalphabetweightedttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root -n auto -w ' + str(cLumi*xsec_ttbar['PH']))
	commands.append('mv TW2Dalphabetttbar_Trigger_nominal_none_'+p+'_PSET_'+cuts+'.root temprootfiles/')


# Move the data
# commands.append('rm rootfiles/TW2Dalphabetdata_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root')
# commands.append('mv TW2Dalphabetdata_Trigger_nominal_'+filestr[0]+'_PSET_'+cuts+'.root rootfiles/')	


# Do all of the signals
for coup in ['LH','RH']:
	sigfiles = sorted(glob.glob('TW2Dalphabetsignal'+coup+'*_PSET_'+cuts+'.root'))
	for f in sigfiles:
		mass = f[20:24]#.lstrip('TW2Dalphabetsignal'+coup).rstrip('_Trigger_nominal_'+g+'_PSET_'+cuts+'.root')
		if coup == 'RH':
			xsec_sig = xsec_bsr[mass]
		elif coup == 'LH':
			xsec_sig = xsec_bsl[mass]
		commands.append('rm ' + f.replace('TW2Dalphabetsignal'+coup,'TW2Dalphabetweightedsignal'+coup))
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('TW2Dalphabetsignal'+coup,'TW2Dalphabetweightedsignal'+coup)+' -n auto -w ' + str(cLumi*xsec_sig))
		commands.append('mv '+f.replace('TW2Dalphabetsignal'+coup,'TW2Dalphabetweightedsignal'+coup)+' rootfiles/')
		commands.append('mv '+f+' temprootfiles/')



# Singletop
# ---------
# Start off weighting everything correctly
for st in ['tW', 'tWB', 't', 'tB']:
	stfiles = sorted(glob.glob('TW2Dalphabetsingletop_'+st+'_*_PSET_'+cuts+'.root'))
	for f in stfiles:
		xsec_ST = xsec_st[st.upper()]
		commands.append('rm ' + f.replace('TW2Dalphabetsingletop_'+st,'TW2Dalphabetweightedsingletop_'+st))
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('TW2Dalphabetsingletop_'+st,'TW2Dalphabetweightedsingletop_'+st)+' -n auto -w ' + str(cLumi*xsec_ST))
		commands.append('mv '+f.replace('TW2Dalphabetsingletop_'+st,'TW2Dalphabetweightedsingletop_'+st)+' rootfiles/')
		commands.append('mv '+f+' temprootfiles/')


# Now add the right stuff together (no pdf stuff here)
for f in filestr:	
	commands.append('rm rootfiles/TW2Dalphabetweightedsingletop_Trigger_nominal_'+f+'_PSET_'+cuts+'.root')
	commands.append('hadd rootfiles/TW2Dalphabetweightedsingletop_Trigger_nominal_'+f+'_PSET_'+cuts+'.root rootfiles/TW2Dalphabetweightedsingletop*_Trigger_nominal_'+f+'_PSET_'+cuts+'.root')



for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )







