#! /usr/bin/env python

###################################################################
##                                                               ##
## Name: TWanalyzer_2DinputMaker.py                              ##
## Author: Lucas Corcodilos (based on code by Kevin Nash)        ##
## Date: 1/15/2018                                               ##
## Purpose: This creates the 2D Pass/fail histograms             ##
##          that are used by 2D alphabet.                        ##
##                                                               ##
###################################################################

import os
import glob
import math
from math import sqrt
#import quickroot
#from quickroot import *
import ROOT 
from ROOT import *
import sys
#from DataFormats.FWLite import Events, Handle
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default   =   'data',
                  dest      =   'set',
                  help      =   'data or ttbar')
parser.add_option('-x', '--pileup', metavar='F', type='string', action='store',
                  default   =   'on',
                  dest      =   'pileup',
                  help      =   'If not data do pileup reweighting?')
parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                  default   =   'all',
                  dest      =   'num',
                  help      =   'job number')

parser.add_option('-j', '--jobs', metavar='F', type='string', action='store',
                  default   =   '1',
                  dest      =   'jobs',
                  help      =   'number of jobs')
parser.add_option('-t', '--tname', metavar='F', type='string', action='store',
                   default  =   'HLT_PFHT900,HLT_PFHT800,HLT_JET450',
                   dest     =   'tname',
                   help     =   'trigger name')
parser.add_option('-J', '--JES', metavar='F', type='string', action='store',
                  default   =   'nominal',
                  dest      =   'JES',
                  help      =   'nominal, up, or down')
parser.add_option('-R', '--JER', metavar='F', type='string', action='store',
                  default   =   'nominal',
                  dest      =   'JER',
                  help      =   'nominal, up, or down')
parser.add_option('-a', '--JMS', metavar='F', type='string', action='store',
                  default   =   'nominal',
                  dest      =   'JMS',
                  help      =   'nominal, up, or down')
parser.add_option('-b', '--JMR', metavar='F', type='string', action='store',
                  default   =   'nominal',
                  dest      =   'JMR',
                  help      =   'nominal, up, or down')
parser.add_option('-m', '--modulesuffix', metavar='F', type='string', action='store',
                  default   =   'none',
                  dest      =   'modulesuffix',
                  help      =   'ex. PtSmearUp')
parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                  default   =   'off',
                  dest      =   'grid',
                  help      =   'running on grid off or on')
parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default   =   'on',
                  dest      =   'ptreweight',
                  help      =   'on or off')
parser.add_option('-p', '--pdfweights', metavar='F', type='string', action='store',
                  default   =   'nominal',
                  dest      =   'pdfweights',
                  help      =   'nominal, up, or down')
parser.add_option('-z', '--pdfset', metavar='F', type='string', action='store',
                  default   =   'cteq66',
                  dest      =   'pdfset',
                  help      =   'pdf set')
parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default   =   'default',
                  dest      =   'cuts',
                  help      =   'Cuts type (ie default, rate, etc)')
parser.add_option('-S', '--split', metavar='F', type='string', action='store',
                  default   =   'event',
                  dest      =   'split',
                  help      =   'split by event of file') # file splitting doesn't work with ttrees
parser.add_option('-C', '--cheat', metavar='F', type='string', action='store',
                  default   =   'off',
                  dest      =   'cheat',
                  help      =   'on or off')


(options, args) = parser.parse_args()

if (options.set.find('QCD') != -1):
    setstr = 'QCD'
else:
    setstr = 'data'

print "Options summary"
print "=================="
for  opt,value in options.__dict__.items():
    #print str(option)+ ": " + str(options[option]) 
    print str(opt) +': '+ str(value)
print "=================="
print ""
di = ""
if options.grid == 'on':
    di = "tardir/"
    sys.path.insert(0, 'tardir/')

gROOT.Macro(di+"rootlogon.C")

sys.path.insert(0,'../')
from Bstar_Functions import *

tname = options.tname.split(',')
tnamestr = ''
for iname in range(0,len(tname)):
    tnamestr+=tname[iname]
    if iname!=len(tname)-1:
        tnamestr+='OR'

        
if tnamestr=='HLT_PFHT900ORHLT_PFHT800ORHLT_JET450':
    tnameformat='nominal'
elif tnamestr=='':
    tnameformat='none'
else:
    tnameformat=tnamestr
        
pie = math.pi 

#Load up cut values based on what selection we want to run 
if options.cuts == 'lowWmass' or options.cuts == 'highWmass':
    Cuts = LoadCuts('default')
elif options.cuts == 'lowWmass1' or options.cuts == 'highWmass1':
    Cuts = LoadCuts('sideband')
else:
    Cuts = LoadCuts(options.cuts)
wpt = Cuts['wpt']
tpt = Cuts['tpt']
dy = Cuts['dy']
tmass = Cuts['tmass']
tau32 = Cuts['tau32']
tau21 = Cuts['tau21']
sjbtag = Cuts['sjbtag']
wmass = Cuts['wmass']
eta1 = Cuts['eta1']
eta2 = Cuts['eta2']
eta = Cuts['eta']

Cons = LoadConstants()
lumi = Cons['lumi']
Lumi = str(lumi/1000)+'fb'
Lumi2 = str(int(lumi)) + 'pb'
ttagsf = Cons['ttagsf']

if options.cuts.find('rate') != -1:
    Wpurity = 'LP'
    wtagsf = Cons['wtagsf_LP']
    wtagsfsig = Cons['wtagsfsig_LP']
else:
    Wpurity = 'HP'
    wtagsf = Cons['wtagsf_HP']
    wtagsfsig = Cons['wtagsfsig_HP']



#For large datasets we need to parallelize the processing
jobs=int(options.jobs)
if jobs != 1:
    num=int(options.num)
    jobs=int(options.jobs)
    print "Running over " +str(jobs)+ " jobs"
    print "This will process job " +str(num)
else:
    print "Running over all events"

#This section defines some strings that are used in naming the output files

#-- Postuncorr is used for softdrop mass, post is used for LV
mod = ''
post = ''
post2 = ''
if options.JES!='nominal':
    mod = mod + 'JES' + '_' + options.JES
    post='jes'+options.JES
if options.JER!='nominal':
    mod = mod + 'JER' + '_' + options.JER
    post='jer'+options.JER
if options.JMS!='nominal':
    mod = mod + 'JMS' + '_' + options.JMS
    post2='jes'+options.JMS
if options.JMR!='nominal':
    mod = mod + 'JMR' + '_' + options.JMR
    post2='jer'+options.JMR


pstr = ""
if options.pdfweights!="nominal":
    print "using pdf uncertainty"
    pstr = "_pdf_"+options.pdfweights

pustr = ""
if options.pileup=='off':
    pustr = "_pileup_unweighted"
if options.pileup=='up':
    pustr = "_pileup_up"
if options.pileup=='down':
    pustr = "_pileup_down"

if mod == '':
    mod = options.modulesuffix

print "mod = " + mod


#------------------------------------------------------------------------

#Based on what set we want to analyze, we find all Ntuple root files 
if options.grid == "on":
    mainDir = "root://cmsxrootd.fnal.gov//store/user/lcorcodi/TTrees/"
else:
    mainDir='TTrees/'

file = TFile.Open(mainDir + "TWtreefile_"+options.set+"_Trigger_"+tnameformat+"_"+mod+".root")
tree = file.Get("Tree")

settype = 'ttbar'

#------------------------------------------------------------------------
if options.cheat == 'off':
    rateCuts = 'rate_'+options.cuts
elif options.cheat == 'on':
    rateCuts = options.cuts


if options.set != 'data':
    #Load up scale factors (to be used for MC only)

    TrigFile = TFile(di+"Triggerweight_2jethack_data.root")
    TrigPlot = TrigFile.Get("TriggerWeight_"+tnamestr+"_pre_HLT_PFHT475")


    if settype == 'ttbar':
        PileFile = TFile(di+"PileUp_Ratio_"+settype+".root")
        if options.pileup=='up':
            PilePlot = PileFile.Get("Pileup_Ratio_up")
        elif options.pileup=='down':
            PilePlot = PileFile.Get("Pileup_Ratio_down")
        else:   
            PilePlot = PileFile.Get("Pileup_Ratio")


nevHisto = file.Get("nev")
B2Gnev = nevHisto.Integral()/jobs
# For some reason, the above line makes python forget what `tpt` is so redifining
tpt = Cuts['tpt']

#---------------------------------------------------------------------------------------------------------------------#
if jobs != 1:
    f = TFile( "TW2Dalphabet"+options.set+"_Trigger_"+tnameformat+"_"+mod+pustr+pstr+"_job"+options.num+"of"+options.jobs+"_PSET_"+options.cuts+".root", "recreate" )
else:
    f = TFile( "TW2Dalphabet"+options.set+"_Trigger_"+tnameformat+"_"+mod+pustr+pstr+"_PSET_"+options.cuts+".root", "recreate" )

print "Creating histograms"


f.cd()
#---------------------------------------------------------------------------------------------------------------------#
mtwbins = [700,1100,1200,1400,1600,1900,4000]

MtwvMtPass     = TH2F("MtwvMtPass",     "mass of tw vs mass of top - Pass", 60, 50, 350, 33, 700, 4000 )

MtwvMtFail     = TH2F("MtwvMtFail",     "mass of tw vs mass of top - Fail", 60, 50, 350, 33, 700, 4000 )


nev = TH1F("nev",   "nev",      1, 0, 1 )

hmatchingFailed = TH1F("matchingFailed", "fraction of events that failed w jet matching requirement", 1, 0, 1)

MtwvMtPassTrigup   = TH2F("MtwvMtPassTrigup", "mass of tw vs mass of top trig up - Pass", 60, 50, 350, 33, 700, 4000 )
MtwvMtPassTrigdown = TH2F("MtwvMtPassTrigdown",   "mass of tw vs mass of top trig up - Pass", 60, 50, 350, 33, 700, 4000 )

MtwvMtPassWup      = TH2F("MtwvMtPassWup",    "mass of tw vs mass of top w tag SF up - Pass", 60, 50, 350, 33, 700, 4000 )
MtwvMtPassWdown    = TH2F("MtwvMtPassWdown",  "mass of tw vs mass of top w tag SF down - Pass",   60, 50, 350, 33, 700, 4000 )

MtwvMtPassTptup    = TH2F("MtwvMtPassTptup",  "mass of tw vs mass of top top pt reweight up - Pass",  60, 50, 350, 33, 700, 4000 )
MtwvMtPassTptdown  = TH2F("MtwvMtPassTptdown",    "mass of tw vs mass of top top pt reweight down - Pass",60, 50, 350, 33, 700, 4000 )

MtwvMtPassExtrapUp = TH2F("MtwvMtPassExtrapUp", "mass of tw vs mass of top extrapolation uncertainty up - Pass", 60, 50, 350, 33, 700, 4000)
MtwvMtPassExtrapDown = TH2F("MtwvMtPassExtrapDown", "mass of tw vs mass of top extrapolation uncertainty down - Pass", 60, 50, 350, 33, 700, 4000)


MtwvMtFailTrigup   = TH2F("MtwvMtFailTrigup", "mass of tw vs mass of top trig up - Fail", 60, 50, 350, 33, 700, 4000 )
MtwvMtFailTrigdown = TH2F("MtwvMtFailTrigdown",   "mass of tw vs mass of top trig up - Fail", 60, 50, 350, 33, 700, 4000 )

MtwvMtFailWup      = TH2F("MtwvMtFailWup",    "mass of tw vs mass of top w tag SF up - Fail", 60, 50, 350, 33, 700, 4000 )
MtwvMtFailWdown    = TH2F("MtwvMtFailWdown",  "mass of tw vs mass of top w tag SF down - Fail",   60, 50, 350, 33, 700, 4000 )

MtwvMtFailTptup    = TH2F("MtwvMtFailTptup",  "mass of tw vs mass of top top pt reweight up - Fail",  60, 50, 350, 33, 700, 4000 )
MtwvMtFailTptdown  = TH2F("MtwvMtFailTptdown",    "mass of tw vs mass of top top pt reweight down - Fail",60, 50, 350, 33, 700, 4000 )

MtwvMtFailExtrapUp = TH2F("MtwvMtFailExtrapUp", "mass of tw vs mass of top extrapolation uncertainty up - Fail", 60, 50, 350, 33, 700, 4000)
MtwvMtFailExtrapDown = TH2F("MtwvMtFailExtrapDown", "mass of tw vs mass of top extrapolation uncertainty down - Fail", 60, 50, 350, 33, 700, 4000)


MtwvMtPass.Sumw2()
MtwvMtFail.Sumw2()

nev.Sumw2()

hmatchingFailed.Sumw2()

MtwvMtPassTrigup.Sumw2()
MtwvMtPassTrigdown.Sumw2()

MtwvMtPassWup.Sumw2()
MtwvMtPassWdown.Sumw2()

MtwvMtPassTptup.Sumw2()
MtwvMtPassTptdown.Sumw2()

MtwvMtPassExtrapUp.Sumw2()
MtwvMtPassExtrapDown.Sumw2()


MtwvMtFailTrigup.Sumw2()
MtwvMtFailTrigdown.Sumw2()

MtwvMtFailWup.Sumw2()
MtwvMtFailWdown.Sumw2()

MtwvMtFailTptup.Sumw2()
MtwvMtFailTptdown.Sumw2()

MtwvMtFailExtrapUp.Sumw2()
MtwvMtFailExtrapDown.Sumw2()


EtaTop      = TH1F("EtaTop",        "Top Candidate eta",                  12, -2.4, 2.4 )
EtaW   = TH1F("EtaW",     "W Candidate eta",              12, -2.4, 2.4 )

PtTop       = TH1F("PtTop",         "Top Candidate pt (GeV)",             50, 450, 1500 )
PtW         = TH1F("PtW",           "W Candidate pt (GeV)",               50, 370, 1430 )
PtTopW      = TH1F("PtTopW",        "pt of tw system",                35,   0, 700 )

PhiTop    = TH1F("PhiTop",      "Top Candidate Phi (rad)",                       12, -pie, pie )
PhiW      = TH1F("PhiW",    "Top Candidate Phi (rad)",                       12, -pie, pie )
dPhi      = TH1F("dPhi",        "delta theat between Top and W Candidates",          12, 2.2, pie )

Mt      = TH1F("Mt",    "Top mass",             25,105,210)
Nsubjetiness32  = TH1F("Nsubjetiness32",    "Nsubjetiness",             8,0,1.6)
Nsubjetiness21  = TH1F("Nsubjetiness21",    "Nsubjetiness",             8,0,1.6)
deltaY      = TH1F("deltaY",    "delta y between Top and b candidates", 10,0,5)
CSV     = TH1F("CSV",       "CSV",                  10,0,1)
CSVMax      = TH1F("CSVMax",    "CSV maximum",              10,0,1)


EtaTop.Sumw2()
EtaW.Sumw2()

PtTop.Sumw2()
PtW.Sumw2()
PtTopW.Sumw2()

PhiTop.Sumw2()
PhiW.Sumw2()
dPhi.Sumw2()


Mt.Sumw2()
Nsubjetiness32.Sumw2()
Nsubjetiness21.Sumw2()
deltaY.Sumw2()
CSV.Sumw2()
CSVMax.Sumw2()


#---------------------------------------------------------------------------------------------------------------------#

# loop over events
#---------------------------------------------------------------------------------------------------------------------#
eta1Count = 0
eta2Count = 0

matchingFailed = 0

count = 0
jobiter = 0
print "Start looping"
#initialize the ttree variables
tree_vars = {   "wpt":array('d',[0.]),
                "wmass":array('d',[0.]),
                "tpt":array('d',[0.]),
                "tmass":array('d',[0.]),
                "tau32":array('d',[0.]),
                "tau21":array('d',[0.]),
                "sjbtag":array('d',[0.]),
                "flavor":array('d',[0.]),
                "mtw":array('d',[0.]),
                "weight":array('d',[0.])}

NewTree = Make_Trees(tree_vars)
treeEntries = tree.GetEntries()

goodEvents = []

# Design the splitting if necessary
if jobs != 1:
    evInJob = int(treeEntries/jobs)
    
    lowBinEdge = evInJob*(num-1)
    highBinEdge = evInJob*num

    if num == jobs:
        highBinEdge = treeEntries

else:
    lowBinEdge = 0
    highBinEdge = treeEntries

nev.SetBinContent(1,B2Gnev)
print "Range of events: (" + str(lowBinEdge) + ", " + str(highBinEdge) + ")"

for entry in range(lowBinEdge,highBinEdge):
    # Have to grab tree entry first
    tree.GetEntry(entry)

    count   =   count + 1

    if count % 100000 == 0 :
        print  '--------- Processing Event ' + str(count) +'   -- percent complete ' + str(100*count/(highBinEdge-lowBinEdge)) + '% -- '

    doneAlready = False

    for hemis in ['hemis0','hemis1']:
        if hemis == 'hemis0':
            # Load up the ttree values
            tVals = {
                "tau1":tree.tau1_leading,
                "tau2":tree.tau2_leading,
                "tau3":tree.tau3_leading,
                "phi":tree.phi_leading,
                "mass":tree.mass_leading,
                "pt":tree.pt_leading,
                "eta":tree.eta_leading,
                "sjbtag":tree.sjbtag_leading,
                "SDmass":tree.topSDmass_leading,
                "flavor":tree.flavor_leading
            }

            wVals = {
                "tau1":tree.tau1_subleading,
                "tau2":tree.tau2_subleading,
                "tau3":tree.tau3_subleading,
                "phi":tree.phi_subleading,
                "mass":tree.mass_subleading,
                "pt":tree.pt_subleading,
                "eta":tree.eta_subleading,
                "sjbtag":tree.sjbtag_subleading,
                "SDmass":tree.wSDmass_subleading
            }

        if hemis == 'hemis1' and doneAlready == False  :
            wVals = {
                "tau1":tree.tau1_leading,
                "tau2":tree.tau2_leading,
                "tau3":tree.tau3_leading,
                "phi":tree.phi_leading,
                "mass":tree.mass_leading,
                "pt":tree.pt_leading,
                "eta":tree.eta_leading,
                "sjbtag":tree.sjbtag_leading,
                "SDmass":tree.wSDmass_leading
            }

            tVals = {
                "tau1":tree.tau1_subleading,
                "tau2":tree.tau2_subleading,
                "tau3":tree.tau3_subleading,
                "phi":tree.phi_subleading,
                "mass":tree.mass_subleading,
                "pt":tree.pt_subleading,
                "eta":tree.eta_subleading,
                "sjbtag":tree.sjbtag_subleading,
                "SDmass":tree.topSDmass_subleading,
                "flavor":tree.flavor_subleading
            }

        elif hemis == 'hemis1' and doneAlready == True:
            continue

        # Remake the lorentz vectors
        tjet = TLorentzVector()
        tjet.SetPtEtaPhiM(tVals["pt"],tVals["eta"],tVals["phi"],tVals["mass"])

        wjet = TLorentzVector()
        wjet.SetPtEtaPhiM(wVals["pt"],wVals["eta"],wVals["phi"],wVals["mass"])


        weight = 1.0

        dy_val = abs(tjet.Rapidity()-wjet.Rapidity())

        MtopW = (tjet+wjet).M()

        wpt_cut = wpt[0]<wjet.Perp()<wpt[1]
        tpt_cut = tpt[0]<tjet.Perp()<tpt[1]
        dy_cut = dy[0]<=dy_val<dy[1]
            
        if wpt_cut and tpt_cut:
            deltaY.Fill(dy_val,weight)

            if dy_cut:
                if options.pdfweights != "nominal" :
                    if options.pdfweights == 'up':
                        iweight = tree.pdf_weightUp
                    elif options.pdfweights == 'down':
                        iweight = tree.pdf_weightDown
                    weight *= iweight


                # Apply top scale factor and pileup correction to all MC
                # Got rid of uncertainties since they are flat and applied in theta
                weightSFt = 1.0
                if options.set!="data":
                    bin1 = tree.pileBin

                    if options.pileup != 'off':
                        weight *= PilePlot.GetBinContent(bin1)

                    if options.set.find("QCD") == -1:
                        weightSFt = ttagsf # Error done in theta
                        

                tmass_cut = tmass[0]<tVals["SDmass"]<tmass[1]

                if True:#tmass_cut :
                    ht = tjet.Perp() + wjet.Perp()

                    weight*=weightSFt

    # Apply w tagging scale factor for anything that Passes w jet matching requirement and is ST_tW or signal
                    weightSFwup = 1.0
                    weightSFwdown = 1.0
                    if tree.WJetMatchingRequirement == 1:
                        if options.set.find('tW') != -1 or options.set.find('signal') != -1:
                            weightSFwup = (wtagsf + wtagsfsig)*weight
                            weightSFwdown = (wtagsf - wtagsfsig)*weight
                            weight*=wtagsf
                    elif tree.WJetMatchingRequirement == 0:
                        matchingFailed += 1

                    weighttrigup=1.0
                    weighttrigdown=1.0
                    if tname != 'none' and options.set!='data' :
                        #Trigger reweighting done here
                        TRW = Trigger_Lookup( ht , TrigPlot )[0]
                        TRWup = Trigger_Lookup( ht , TrigPlot )[1]
                        TRWdown = Trigger_Lookup( ht , TrigPlot )[2]

                        weighttrigup=weight*TRWup
                        weighttrigdown=weight*TRWdown
                        weight*=TRW

                        weightSFwup*=TRW
                        weightSFwdown*=TRW
                

                    weightSFptup=1.0
                    weightSFptdown=1.0
                    if options.ptreweight == "on" and options.set.find('ttbar') != -1:
                        # ttbar pt reweighting done here
                        if True:#options.extraPtCorrection and ttsubString == '':
                            FlatPtSFFile = open(di+'bstar_theta_PtSF_onTOPgroupCorrection.txt','r')
                            FlatPtSFList = FlatPtSFFile.readlines()
                            extraCorrection = float(FlatPtSFList[0])
                            extraCorrectionUp = float(FlatPtSFList[1])
                            extraCorrectionDown = float(FlatPtSFList[2])
                            # print 'Pt scale correction = ' + str(1+extraCorrection)
                            FlatPtSFFile.close()
                        else:
                            extraCorrection = 0
                            extraCorrectionUp = 0
                            extraCorrectionDown = 0


                        PTW = tree.pt_reweight*(1+extraCorrection)
                        PTWup = tree.pt_reweight*(1+extraCorrection+extraCorrectionUp)
                        PTWdown = tree.pt_reweight*(1+extraCorrection-extraCorrectionDown)

                        weightSFptup=weight*PTWup
                        weightSFptdown=weight*PTWdown
                        weight*=PTW

                        weightSFwup*=PTW
                        weightSFwdown*=PTW

                        weighttrigup*=PTW
                        weighttrigdown*=PTW
            
                    try:
                        tau32val        =   tVals["tau3"]/tVals["tau2"] 
                        tau21val        =   wVals["tau2"]/wVals["tau1"]
                    except:
                        continue

                    tau21_cut =  tau21[0]<=tau21val<tau21[1]
                    tau32_cut =  tau32[0]<=tau32val<tau32[1]

                    SJ_csvval = tVals["sjbtag"]

                    sjbtag_cut = sjbtag[0]<SJ_csvval<=sjbtag[1]

                    CSVMax.Fill(SJ_csvval,weight)

                    Nsubjetiness32.Fill(tau32val,weight)
                    Nsubjetiness21.Fill(tau21val,weight)
                        
                    if type(wmass[0]) is float:
                        wmass_cut = wmass[0]<=wVals["SDmass"]<wmass[1]
                    elif type(wmass[0]) is list:
                        wmass_cut = wmass[0][0]<=wVals["SDmass"]<wmass[0][1] or wmass[1][0]<=wVals["SDmass"]<wmass[1][1] 
                    else:
                        print "wmass type error" 
                        continue

                    FullTop = sjbtag_cut and tau32_cut

                    if tau21_cut:
                        if wmass_cut:
                            # Get the extrapolation uncertainty
                            extrap = ExtrapUncert_Lookup(wjet.Perp(),Wpurity)
                            extrapUp = weight*(1+extrap)
                            extrapDown = weight*(1-extrap)

                            # We've done the preselection and the W and top masses are orthogonal which means
                            # our tagged W can't be a top so we don't have to check the other hemi configuration
                            doneAlready = True

                            if not FullTop:
                                MtwvMtFail.Fill(tjet.M(),MtopW,weight) 


                                MtwvMtFailTrigup.Fill(tjet.M(),MtopW,weighttrigup)
                                MtwvMtFailTrigdown.Fill(tjet.M(),MtopW,weighttrigdown)
                                MtwvMtFailWup.Fill(tjet.M(),MtopW,weightSFwup) 
                                MtwvMtFailWdown.Fill(tjet.M(),MtopW,weightSFwdown)

                                MtwvMtFailTptup.Fill(tjet.M(),MtopW,weightSFptup)
                                MtwvMtFailTptdown.Fill(tjet.M(),MtopW,weightSFptdown) 

                                MtwvMtFailExtrapUp.Fill(tjet.M(),MtopW,extrapUp)
                                MtwvMtFailExtrapDown.Fill(tjet.M(),MtopW,extrapDown)

                                                    
                            if FullTop:
                                #if ((MtopW)>2400):
                                #   goodEvents.append( [ tree.object().id().run(), tree.object().id().luminosityBlock(), tree.object().id().event(),  ] )
                                MtwvMtPass.Fill(tjet.M(),MtopW,weight) 


                                MtwvMtPassTrigup.Fill(tjet.M(),MtopW,weighttrigup)
                                MtwvMtPassTrigdown.Fill(tjet.M(),MtopW,weighttrigdown)
                                MtwvMtPassWup.Fill(tjet.M(),MtopW,weightSFwup) 
                                MtwvMtPassWdown.Fill(tjet.M(),MtopW,weightSFwdown)

                                MtwvMtPassTptup.Fill(tjet.M(),MtopW,weightSFptup)
                                MtwvMtPassTptdown.Fill(tjet.M(),MtopW,weightSFptdown) 

                                MtwvMtPassExtrapUp.Fill(tjet.M(),MtopW,extrapUp)
                                MtwvMtPassExtrapDown.Fill(tjet.M(),MtopW,extrapDown)

                                EtaTop.Fill(tjet.Eta(),weight)
                                EtaW.Fill(wjet.Eta(),weight)
                                
                                PtTop.Fill(tjet.Perp(),weight)
                                PtW.Fill(wjet.Perp(),weight)
                                PtTopW.Fill((tjet+wjet).Perp(),weight)
                                
                                PhiTop.Fill(tjet.Phi(),weight)
                                PhiW.Fill(wjet.Phi(),weight)
                                dPhi.Fill(abs(tjet.Phi()-wjet.Phi()),weight)

                                Mt.Fill(tjet.M(),weight)

                                temp_variables = {  "wpt":wjet.Perp(),
                                                    "wmass":wVals["SDmass"],
                                                    "tpt":tjet.Perp(),
                                                    "tmass":tVals["SDmass"],
                                                    "tau32":tau32val,
                                                    "tau21":tau21val,
                                                    "sjbtag":SJ_csvval,
                                                    "flavor":tVals["flavor"],
                                                    "mtw":MtopW,
                                                    "weight":weight}

                                for tv in tree_vars.keys():
                                    tree_vars[tv][0] = temp_variables[tv]
                                NewTree.Fill()
                                doneAlready = True
                                    

hmatchingFailed.SetBinContent(1,float(matchingFailed/count))

print "fraction of events that failed matching: " + str(float(matchingFailed/count))

f.cd()
f.Write()
f.Close()

print "number of events: " + str(count)



# if options.printEvents:
#   Outf1   =   open("DataEvents"+options.num+".txt", "w")
#   sys.stdout = Outf1
#   for goodEvent in goodEvents :
#       print '{0:12.0f}:{1:12.0f}:{2:12.0f}'.format(
#           goodEvent[0], goodEvent[1], goodEvent[2]
#       )
