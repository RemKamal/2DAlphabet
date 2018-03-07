#!/usr/bin/env python

### COMMENT SCHEME ###

#########################################
# Function Description at Definition    #
# ----------------------------------    #
# Input     - ...                       #
# Output    - ...                       #
#########################################

#-----------------------#
# RooFit notes -> ...   #
#-----------------------#

#  ---------------
# | Function name |
#  ---------------
# Description at first call
# Input is ...
# Output is ...

# Keyword 'NOTE' used to make comments about things to revisit
# The number following 'NOTE' denotes catagories of fixes. Those with the same number should be addressed at the same time
# 0 - Need to produce input with proper naming scheme
# 1 - Index for processes
# 2 - Built in scale factors in a list that relies on proper ordering
# 3 - Replacing 'l' and 'p' with more descriptive names
# 4 - Scale hist relying on obscure pass and type IDs
# 5 - Deleting self._lEff* and anything tied to them
# 6 - Read and understand 'hist'
# 7 -
# 8 - Analysis specific fixes to remove
# 9 - Remove signal interpolation
# 10 - Make zeroth order guesses for mlfit_param


import ROOT as r,sys,math,array,os
from ROOT import TFile, TTree, TChain, gPad, gDirectory
from multiprocessing import Process
from optparse import OptionParser
from operator import add
import math
import sys
import time
import array
r.gROOT.Macro(os.path.expanduser('~/rootlogon.C'))
# including other directories
sys.path.insert(0, '../.')
from tools import *
from hist import *

# Set the scale factors
TT_SF = 0.83
W_SF = 1.35
DY_SF = 1.45
W_SF = 1.35
V_SF = 0.891
V_SF_ERR = 0.066

# -------------------------------------------------------------------------------------
def main(options,args):
    #########################################################
    # The main function which just initializes              #
    # - input and output directories                        #
    # - input root file                                     #
    # then loads the histograms and builds the workspaces   #
    #########################################################
    idir = options.idir
    odir = options.odir

    input_file  = r.TFile(options.input);

    #  ----------------
    # | loadHistograms |
    #  ----------------
    # Load and scale histograms for 5 different sets (data, wqq, zqq, qcdmc, tqq+stqq)
    # Input - input_file
    #       - psuedo and pseudo15 are options that default to FALSE
    #       --- Just used to do closure tests with data = MC
    # Ouput - two lists (pass_hists,fail_hists)
    (hpass,hfail) = loadHistograms(input_file,options.pseudo,options.pseudo15);

    #build the workspacees
    dazsleRhalphabetBuilder(hpass,hfail,input_file);

## -------------------------------------------------------------------------------------
def loadHistograms(input_file,pseudo,pseudo15):
    #########################################################################################
    # Loads histograms and scales by tagging scale factors depending on the process         #
    # ------------------------------------------------------------------------------        #
    # Input     - input file                                                                #
    #           - True/False to turn on/off data = QCD MC                                   #
    #                                                                                       #
    # Output    - list of passing histograms (in hard coded order)                          #
    #           - list of failing histograms (in hard coded order)                          #
    #                                                                                       #
    # NOTE1                                                                                 #
    # I (Lucas) don't like how this is done because it's relying on ambigous codes (0,1,2)  #
    # to determine what scale factors to apply - making it hard to quickly know what        #
    # you're doing and to explain it to someone else.                                       #
    #                                                                                       #
    # Naming the histogram objects with indexes from 0 to 4 suffers from                    #
    # same issue and should be changed. (0:Data,1:wqq,2:zqq,3:qcdmc,4:tqq+stqq)             #
    #########################################################################################

    # Initialize lists
    hpass = [];
    hfail = [];

    # Grab and scale the first group (wqq)
    lHP1 = input_file.Get("wqq_pass_matched")
    print 'wqq_pass ', lHP1.Integral() 
    lHF1 = input_file.Get("wqq_fail_matched")
    scaleHists(lHP1,0,1)
    scaleHists(lHF1,0,2)
    print 'wqq_fail ', lHF1.Integral() 

    # Grab and scale the second ground (zqq)
    lHP2 = input_file.Get("zqq_pass_matched")
    print 'zqq_pass ', lHP2.Integral()
    lHF2 = input_file.Get("zqq_fail_matched")
    scaleHists(lHP2,1,1)
    scaleHists(lHF2,1,2)
    print 'zqq_fail ', lHF2.Integral()
    
    input_file.cd()
    
    # Grab (no scale) the third group (qcd MC)
    lHP3 = input_file.Get("qcd_pass")
    print 'qcd_pass ', lHP3.Integral()
    lHF3 = input_file.Get("qcd_fail")
    print 'qcd_fail ', lHF3.Integral()

    # Grab and scale the fourth group (tqq)
    lHP4 = input_file.Get("tqq_pass")
    lHP4.Scale(0.83)
    print 'tqq_pass ', lHP4.Integral()
    lHF4 = input_file.Get("tqq_fail")
    lHF4.Scale(1./(1-0.1*0.17))
    # Also have to do top pT dependent SF
    # NOTE2 - I (Lucas) also don't like how this is hardcoded in
    scale=[1.0,0.8,0.75,0.7,0.6,0.5,0.5]
    for i0 in range(1,lHF4.GetNbinsX()+1):
        for i1 in range(1,lHF4.GetNbinsY()+1):
            lHP4.SetBinContent(i0,i1,lHP4.GetBinContent(i0,i1)*scale[i1])
            lHF4.SetBinContent(i0,i1,lHF4.GetBinContent(i0,i1)*scale[i1])
    print 'tqq_pass 2 ', lHP4.Integral()

    # From documentation:
    # By default when an histogram is created, it is added to the list of histogram objects in the current directory in memory.
    # Remove reference to this histogram from current directory and add reference to new directory dir. dir can be 0 in which case the histogram does not belong to any directory.
    lHP3.SetDirectory(0)
    lHF3.SetDirectory(0)
    lHP4.SetDirectory(0)
    lHF4.SetDirectory(0)

    # Grab the stqq contribution and add it into tqq AFTER tqq has been scaled
    lTHP4 = input_file.Get("stqq_pass")
    lTHF4 = input_file.Get("stqq_fail")
    lHP4.Add(lTHP4)
    lHF4.Add(lTHF4)

    print 'tqq_fail ', lHF4.Integral()
    print 'total mc pass ', lHP1.Integral()+lHP2.Integral()+lHP3.Integral()+lHP4.Integral()
    print 'total mc fail ', lHF1.Integral()+lHF2.Integral()+lHF3.Integral()+lHF4.Integral()
  
    # If True, we want data = MC
    if pseudo:
        lHP0 = lHP3.Clone("data_obs_pass")
        lHF0 = lHF3.Clone("data_obs_fail")
        lHF0.Add(lHF1)
        lHF0.Add(lHF2)
        lHF0.Add(lHF4)
        lHP0.Add(lHP1)
        lHP0.Add(lHP2)
        lHP0.Add(lHP4)
        print 'pass ', lHP0.Integral()
        print 'fail ', lHF0.Integral()

    # Similar to pseudo with some scale change that I (Lucas) don't have to worry about
    elif pseudo15:
        lHF0 = lHF3.Clone("data_obs_fail")
        lHP0 = lHF3.Clone("data_obs_pass");
        lHP0.Scale(0.05);
        #lHP1.Scale(1.2)
        #lHP2.Scale(1.5)
        #lHP4.Scale(1.5)
        lHP0.Add(lHP1)
        lHP0.Add(lHP2)
        lHP0.Add(lHP4)
        lHF0.Add(lHF1)
        lHF0.Add(lHF2)
        lHF0.Add(lHF4)
    # Otherwise grab the real data distributions
    else:
        lHP0 = input_file.Get("data_obs_pass")
        lHF0 = input_file.Get("data_obs_fail")

    # Put each scaled histogram in the output lists
    # Extend just appends each item in the list argument to the list it's called on
    hpass.extend([lHP0,lHP1,lHP2,lHP3,lHP4])
    hfail.extend([lHF0,lHF1,lHF2,lHF3,lHF4])

    # Now time to do the signals
    # Same idea - grab, scale, setdirectory, append - except these get initialized DIRECTLY to the output lists
    masses=[50,75,100,125,150,200,250,300]
    for mass in masses:
        hpass.append(input_file.Get("zqq"+str(mass)+"_pass_matched"))
        hfail.append(input_file.Get("zqq"+str(mass)+"_fail_matched"))
        scaleHists(hpass[len(hpass)-1],1,1)
        scaleHists(hfail[len(hfail)-1],1,2)
        hpass[len(hpass)-1].SetDirectory(0)
        hfail[len(hfail)-1].SetDirectory(0)

    # Quick print to debug
    for lH in (hpass+hfail):
        lH.SetDirectory(0)
        print lH.GetName(), lH.Integral()

    # Done
    return (hpass,hfail);

### -------------------------------------------------------------------------------------
def scaleHists(iHist,iType,iPassId):
    #########################################################
    # Takes in a hist specified by type and pass ID and     #
    # outputs that hist scaled by the value determined      #
    # the type and pass ID.                                 #
    # ----------------------------------------------------- #
    # NOTE4                                                 #
    # I'm not going to try to parse through this because    #
    # I plan to totally replace it.                         #
    #########################################################

    if iPassId == 1:
        iHist.Scale(V_SF)
    #if iPassId == 2:
            #iHist.Scale(1./(1.-0.11*(0.3/0.7)))
        #iHist.Scale(1.009)
    if iType == 0:
        iHist.Scale(DY_SF)

    if iType == 0 and iPassId > 0: #w boson
        #wscale=[1.0,1.05,1.05,1.25,1.25,1.25,1.0]
        wscale=[1.0,1.0,1.0,1.20,1.25,1.25,1.0]
        for i0 in range(1,iHist.GetNbinsX()+1):
            for i1 in range(1,iHist.GetNbinsY()+1):
                iHist.SetBinContent(i0,i1,iHist.GetBinContent(i0,i1)*wscale[i1])
    if iType == 1 and iPassId > 0: 
        # correcting Z *was scaled by W_SF*
        iHist.Scale(DY_SF/W_SF)

## -------------------------------------------------------------------------------------
class dazsleRhalphabetBuilder: 

    def __init__( self, hpass, hfail, inputfile ): 

        # Initialize some instance variables - denoted with underscore
        self._hpass = hpass;
        self._hfail = hfail;
        self._inputfile = inputfile;

        self._outputName = "base.root";
        self._outfile_validation = r.TFile("validation.root","RECREATE");

        self._mass_nbins = 60;
        self._mass_lo    = 30;
        self._mass_hi    = 330;
        print "number of mass bins and lo/hi: ", self._mass_nbins, self._mass_lo, self._mass_hi;
        self._pt_nbins = hpass[0].GetYaxis().GetNbins();
        self._pt_lo = hpass[0].GetYaxis().GetBinLowEdge( 1 );
        self._pt_hi = hpass[0].GetYaxis().GetBinUpEdge( self._pt_nbins );


        # polynomial order for fit
        self._poly_lNP = 3; # 3rd order in pT
        self._poly_lNR = 4; # 4th order in rho


        # define RooRealVars - NOTE3 - 'l' denotes what? Not Roo object since 'p' is used later on
        #---------------------------------------------------#
        # RooRealVar        -> Variable     x               #
        # RooAbsReal        -> Function     f(x)            #
        # RooFormulaVar     -> Base class of RooAbsReal     #
        # RooAbsPdf         -> PDF          f(x)            #
        # RooArgSet         -> space point  x               #
        # RooRealIntegral   -> Integral(f(x),x,xmin,xmax)   #
        # RooAbsData        -> list of space points         #
        #---------------------------------------------------#

        self._lMSD    = r.RooRealVar("x","x",self._mass_lo,self._mass_hi)
        self._lMSD.setBins(self._mass_nbins)        
        self._lPt     = r.RooRealVar("pt","pt",self._pt_lo,self._pt_hi);
        self._lPt.setBins(self._pt_nbins)
        self._lRho    = r.RooFormulaVar("rho","log(x*x/pt/pt)",r.RooArgList(self._lMSD,self._lPt))

        # NOTE5 - Cris is pretty sure that these efficiencies can be done away with - they get used but not
        #        for anything that gets saved out.
        self._lEff    = r.RooRealVar("veff"      ,"veff"      ,0.5 ,0.,1.0)
        self._lEffQCD = r.RooRealVar("qcdeff"    ,"qcdeff"    ,0.1 ,0.,1.0)
        self._lDM     = r.RooRealVar("dm","dm", 0.,-10,10)
        self._lShift  = r.RooFormulaVar("shift",self._lMSD.GetName()+"-dm",r.RooArgList(self._lMSD,self._lDM)) 

        self._allVars = [];
        self._allShapes = [];
        self._allData = [];
        self._allPars = [];

        self.polyArray = []

        #  ----------------------
        # | buildPolynomialArray |
        #  ----------------------
        # Build polynomial array with n (= (order in pt)*(order in rho)) parameters
        # Input empty list, polynomial order rho, polynomial order pt, rho string, pt string,  
        # Output is a filled polyArray
        self.buildPolynomialArray(self.polyArray,self._poly_lNR,self._poly_lNP,"r","p",-1.0,1.0)

        self.LoopOverPtBins();


    # Keeping this as a separate function rather than merging with __init__ to separate the 'defining' from the 'doing' 
    def LoopOverPtBins(self):

        print "number of pt bins = ", self._pt_nbins;
        # loop over 5 pt bins, cat 1: pt500-600, cat 2: pt600-700, cat 3: pt700-800, cat 4: pt800-900, cat5: pt900-1000
        for ipt in range(1,self._pt_nbins+1):
            print "------- pT bin number ",ipt      
            
            # 1d histograms in each pT bin (in the order... data, w, z, qcd, top, signals)
            hpass_inPtBin = [];
            hfail_inPtBin = [];

            # NOTE0 - This block is important because it starts to define the naming scheme kept throughout the code.
            # Specifically, the pt bins are called 'cat's and are given an index based on the bin number.
            # Each 'cat' corresponds to a different process/set and that order is hard coded in.
            # I (Lucas) don't like this because I can't just look at it and know the pt bin walls
            # However, this is pretty ingrained in the code and would take a decent chunk of work to change
            # correctly for very little reward. Will probably leave it.
            
            # h dimensions are pT (y) vs mass (x)
            for ih,h in enumerate(self._hpass):
                # proj defined in ../tools.py
                # - Creates a TH1F in mass, loops over the x-axis bins of h (mass), skips over anything outside
                #   of _mass_lo and _mass_hi, and sets the bin content and error of the new TH1F for the mass bin in the ipt bin
                tmppass_inPtBin = proj("cat",str(ipt),h,self._mass_nbins,self._mass_lo,self._mass_hi)

                # Remove low mass and high mass (cat 1 if m>185, cat 2 if m>220 or m<50, cat 3 if m>260 or m<55, cat4 if m>310 or m<65, cat5 if m<65)
                # NOTE8 - not sure why this for loop is necessary
                for i0 in range(1,self._mass_nbins+1):
                    if ((i0 > 31 or i0 < 0) and ipt == 1) or ((i0 > 38 or i0 < 4) and ipt == 2) or ((i0 > 46 or i0 < 5) and ipt == 3) or ((i0 > 56 or i0 < 7) and ipt == 4) or (i0 < 7 and ipt == 5):
                        tmppass_inPtBin.SetBinContent(i0,0);
                hpass_inPtBin.append( tmppass_inPtBin )
            
            # Same idea but with the fails
            for ih,h in enumerate(self._hfail):
                tmpfail_inPtBin = proj("cat",str(ipt),h,self._mass_nbins,self._mass_lo,self._mass_hi); 
                # remove low mass and high mass (cat 1 if m>185, cat 2 if m>220 or m<50, cat 3 if m>260 or m<55, cat4 if m>310 or m<65, cat5 if m<65)
                # NOTE8
                for i0 in range(1,self._mass_nbins+1):
                    if ((i0 > 31 or i0 < 0) and ipt == 1) or ((i0 > 38 or i0 < 4) and ipt == 2) or ((i0 > 46 or i0 < 5) and ipt == 3) or ((i0 > 56 or i0 < 7 ) and ipt == 4) or (i0 < 7 and ipt == 5):
                        tmpfail_inPtBin.SetBinContent(i0,0);
                hfail_inPtBin.append( tmpfail_inPtBin ) 
            
            #  -----------------
            # | workspaceInputs |
            #  -----------------
            # Input passing and fail histograms for this pt bin and the pt category name string
            # Ouput three lists
            # - Data pass and fail as RooDataHists
            # - totp, totf, ewkp, and ewkf as RooAddPdfs
            # - All MC pass and fail as RooDataHists 
            (thisDatas,thisPdfs,thisHists) = self.workspaceInputs(hpass_inPtBin,hfail_inPtBin,"cat"+str(ipt))
            
            # Get approximate pt bin value
            # NOTE3 - Pt falls exponentially so the mean of the bin is left of the center of the bin! Need to change this since I'm going to used Mtw, not pt
            approx_pt = self._hpass[0].GetYaxis().GetBinLowEdge(ipt)+self._hpass[0].GetYaxis().GetBinWidth(ipt)*0.3;
            

            #  ------------
            # | makeRhalph |
            #  ------------
            # Sets up the RooParametricHists that can float nicely in combine.
            # Input list of fail histos in this pt bin (no QCD MC), same for pass, approximate pt bin value, and the string category  
            # Output is list of RooParametricHist ordered [pass,fail] which are also saved in workspaces and written out
            lParHists = self.makeRhalph([hfail_inPtBin[0],hfail_inPtBin[1],hfail_inPtBin[2],hfail_inPtBin[4]],[hpass_inPtBin[0],hpass_inPtBin[1],hpass_inPtBin[2],hpass_inPtBin[4]],approx_pt,"cat"+str(ipt))           
            
            # Get signals and SM backgrounds
            lPHists=[thisHists[0],thisHists[1],thisHists[2],thisHists[3]]
            lFHists=[thisHists[4],thisHists[5],thisHists[6],thisHists[7]]

            #  ------------
            # | getSignals |
            #  ------------
            # Runs rooTheHistFunc for each of the signals (just Roo's everything)
            # Input list of fail histos in this pt bin (no QCD MC), same for pass, and the string category  
            # Output is rooTheHistFunc output for all signals
            lPHists.extend(self.getSignals(hpass_inPtBin,hfail_inPtBin,"cat"+str(ipt))[0])
            lFHists.extend(self.getSignals(hpass_inPtBin,hfail_inPtBin,"cat"+str(ipt))[1])
            
            #  ---------------
            # | makeWorkspace |
            #  ---------------
            # Combines everything in this pt bin and writes the final workspaces to the output file for combine to read
            # Input output file name, single item list of RooDataHist (Data pass/fail), all MC RooDataHists, list of all vars, catagory sting, boolean for mass shift 
            # Output is full workspaces written to file
            self.makeWorkspace(self._outputName,[thisDatas[0]],lPHists,self._allVars,"pass_cat"+str(ipt),True)
            self.makeWorkspace(self._outputName,[thisDatas[1]],lFHists,self._allVars,"fail_cat"+str(ipt),True)

        # Write and close to finish!
        self._outfile_validation.Write();
        self._outfile_validation.Close();
            
    def workspaceInputs(self, iHP,iHF, iBin):
        #####################################################
        # Creates the inputs for the workspace by           #
        # 'converting' to RooFit objects.                   # 
        # ------------------------------------------------- #
        # Input     - pass histo list for one pt bin        #
        #           - fail histo list for one pt bin        #
        #           - string for pt bin                     #
        #                                                   #
        # Output    - 3 lists                               #
        #           --- RooDataHist: Data  pass and fail    #
        #           --- RooAddPdf: totp, totf, ewkp, ewkf   #
        #           --- RooDataHist: All MC pass and fail   #
        #                                                   #
        #####################################################

        #-------------------------------------------------------#
        # RooCategory works exactly how it looks                #
        # - define an observable by name ("sample")             #
        # - define subcategory types by name and value          #
        #                                                       #
        # RooDataHist       -> THist (but can associate         #
        #                       RooRealVar with it via          # 
        #                       RooArgList)                     #
        # RooHistPdf        -> probablity density function      #
        #                       sampled from a multidimensional #
        #                       histogram                       #
        # RooSimultaneous   -> facilitates simultaneous fitting #
        #                       of multiple PDFs to subsets of  #
        #                       a given dataset                 #
        #-------------------------------------------------------#

        # Define the categories
        lCats = r.RooCategory("sample","sample") 
        lCats.defineType("pass",1) 
        lCats.defineType("fail",0)

        # Construct the RooDataHists from the data TH1 and tie it to the mass variable
        # (we know it's data because data is index 0 in the hpass/hfail lists) 
        lPData = r.RooDataHist("data_obs_pass_"+iBin,"data_obs_pass_"+iBin,r.RooArgList(self._lMSD),iHP[0])
        lFData = r.RooDataHist("data_obs_fail_"+iBin,"data_obs_fail_"+iBin,r.RooArgList(self._lMSD),iHF[0])
        # Same as above but combine the pass and fail
        lData  = r.RooDataHist("comb_data_obs","comb_data_obs",r.RooArgList(self._lMSD),r.RooFit.Index(lCats),r.RooFit.Import("pass",lPData),r.RooFit.Import("fail",lFData)) 

        #  ----------------
        # | rooTheHistFunc |
        #  ----------------
        # Makes the PDFs from the pass and fail hists for the pt bin for a specific process/set
        # Input pass and fail histos for the set, string defining set, string defining pt bin
        # Ouput of rooTheHistFunc is a list = [ RooHistPdf pass,    
        #                                       RooHistPdf fail,    
        #                                       RooExtendPdf pass,  
        #                                       RooExtendPdf fail,  
        #                                       RooDataHist pass,   
        #                                       RooDataHist fail]   
        
        lW    = self.rooTheHistFunc([iHP[1],iHF[1]],"wqq",iBin)
        lZ    = self.rooTheHistFunc([iHP[2],iHF[2]],"zqq",iBin)
        ltop  = self.rooTheHistFunc([iHP[4],iHF[4]],"tqq",iBin)     
        lQCD  = self.rooTheHistFunc([iHP[3],iHF[3]],"qcd",iBin)

        # Construct full PDFs (effectively just adding the EWK parts together it seems)
        lTotP = r.RooAddPdf("tot_pass"+iBin,"tot_pass"+iBin,r.RooArgList(lQCD[0]))
        lTotF = r.RooAddPdf("tot_fail"+iBin,"tot_fail"+iBin,r.RooArgList(lQCD[1]))
        lEWKP = r.RooAddPdf("ewk_pass"+iBin,"ewk_pass"+iBin,r.RooArgList(lW[2],lZ[2],ltop[2]))
        lEWKF = r.RooAddPdf("ewk_fail"+iBin,"ewk_fail"+iBin,r.RooArgList(lW[3],lZ[3],ltop[3]))
        
        # Construct simultaneous fit object with the catagories
        lTot  = r.RooSimultaneous("tot","tot",lCats) 
        # Add the pdfs for each catagory to the RooSimultaneous
        lTot.addPdf(lTotP,"pass") 
        lTot.addPdf(lTotF,"fail")     

        # Save out
        self._allData.extend([lPData,lFData])
        self._allShapes.extend([lTotP,lTotF,lEWKP,lEWKF])

        ## find out which to make global
        ## RooDataHist (data), then RooAbsPdf (qcd,ewk+top), then RooDataHist of each ewk+top
        return ([lPData,lFData],
            [lTotP,lTotF,lEWKP,lEWKF],
            [lW[4],lZ[4],ltop[4],lQCD[4],lW[5],lZ[5],ltop[5],lQCD[5]])        

    def makeRhalph(self,iHFs,iHPs,iPt,iCat):
        #####################################################
        # Sets up the RooParametricHists that can float     #
        # nicely in combine.                                #
        # ------------------------------------------------- #
        # Input     - fhists for all sets BUT QCD MC        #
        #           - phists for all sets BUT QCD MC        #
        #           - approximate pt bin val                #
        #           - catagory string                       #
        #                                                   #
        # Output    - RooParametricHists [pass,fail]        #
        #           - Writes the above to workspaces        #
        #             which get saved to a file             #
        #####################################################

        print "---- [makeRhalph]"   

        # Initialize some constants
        lName = "qcd";
        lUnity = r.RooConstVar("unity","unity",1.);
        lZero  = r.RooConstVar("lZero","lZero",0.);

        # Fix some RooVars that we already initialized with a range (the top pt and the qcd eff)
        self._lPt.setVal(iPt)
        self._lEffQCD.setVal(0.05)
        self._lEffQCD.setConstant(False)

        

        # Initialize some arg lists to store the bin values
        lPassBins = r.RooArgList()
        lFailBins = r.RooArgList()

        # Now build the function by going through the mass bins. 
        # Remember that we're inside a pt bin right now so when we call buildPolynomialArray,
        # this makes a 2D function where one dimension (pt) is constant
        for i0 in range(1,self._mass_nbins+1):
            # Set the mass RooVar to value of the mass bin for the data fail hist
            self._lMSD.setVal(iHFs[0].GetXaxis().GetBinCenter(i0)) 

            #  -------------------
            # | buildRooPolyArray |
            #  -------------------
            # Creates the rho RooPolyVar (basically a polynomial function) for this pt bin
            # Input value of pt and rho RooVars, unity constant (1), zero constant (0), and the polynomial array 
            # Output is a 2D RooPolyVar
            lPass = self.buildRooPolyArray(self._lPt.getVal(),self._lRho.getVal(),lUnity,lZero,self.polyArray)

            # Initialize some counting of event yeilds in the fail distributions
            pSum = 0 # Data - ewk
            pRes = 0 # Ewk

            # For each failed histos (except QCD MC)
            for i1 in range(0,len(iHFs)):
                # Add the content of the failed histo at this mass bin for data and subtract all else
                pSum = pSum + iHFs[i1].GetBinContent(i0) if i1 == 0 else pSum - iHFs[i1].GetBinContent(i0); # subtract W/Z from data
                # If not data, add bin content to pRes
                if i1 > 0 : pRes += iHFs[i1].GetBinContent(i0)
            if pSum < 0: pSum = 0

            # Need to make some bounds for pSum to float between so create a large uncertainty
            # 10 sigma range + 10 events
            pUnc = math.sqrt(pSum)*10.+10
            pUnc += pRes

            # Define the failing var
            pFail = r.RooRealVar(lName+"_fail_"+iCat+"_Bin"+str(i0),lName+"_fail_"+iCat+"_Bin"+str(i0),pSum,max(pSum-pUnc,0),max(pSum+pUnc,0))
            # Define the passing var based on the failing (make sure it can't go negative)
            lArg = r.RooArgList(pFail,lPass,self._lEffQCD)
            pPass = r.RooFormulaVar(lName+"_pass_"+iCat+"_Bin"+str(i0),lName+"_pass_"+iCat+"_Bin"+str(i0),"@0*max(@1,0)*@2",lArg)
            
            # For each passed histo (except QCD MC)
            pSumP = 0
            for i1 in range(0,len(iHPs)):
                    # Add the content of the passed histo at this mass bin for data and subtract all else
                    pSumP = pSumP + iHPs[i1].GetBinContent(i0) if i1 == 0 else pSumP - iHPs[i1].GetBinContent(i0); # subtract W/Z from data 
            # Make sure we don't have negative values
            if pSumP < 0: pSumP = 0

            # if the number of events in the failing is small remove the bin from being free in the fit
            if pSum < 5 and pSumP < 5:
                pFail = r.RooRealVar(lName+"_pass_"+iCat+"_Bin"+str(i0),lName+"_pass_"+iCat+"_Bin"+str(i0),pSum ,0.,max(pSum,0.1))
                pFail.setConstant(True)
                pPass = r.RooRealVar(lName+"_pass_"+iCat+"_Bin"+str(i0),lName+"_pass_"+iCat+"_Bin"+str(i0),pSumP,0.,max(pSumP,0.1))
                pPass.setConstant(True)

            # Record the RooVar for the bin to the array
            lPassBins.add(pPass)
            lFailBins.add(pFail)
            self._allVars.extend([pPass,pFail])
            self._allPars.extend([pPass,pFail])

        #-------------------------------------------------------------------------------------------------------------------------------#
        # Basics of how to use RooParametricHist                                                                                        #
        # --------------------------------------                                                                                        #
        # 1. Get/make your TH1 data set                                                                                                 #
        # 2. Turn it into a RooDataHist and import it into the workspace                                                                #
        # 3. In the signal region, the background process should be floating so create one RooRealVar per bin to allow the yeild        #
        #    in each bin to float                                                                                                       #
        # 4. Put each of these in one RooArgList                                                                                        #
        # 5. Construct using syntax:                                                                                                    #
        #    RooParametricHist(name, title, RooRealVar (the 1D variable), RooArgList (per bin yields), the TH1 (just used for binning)) #
        # 6. Make a _norm term which should be the sum of the yields (RooAddition object - thats how combine likes to play with pdfs)   #
        #-------------------------------------------------------------------------------------------------------------------------------#


        # Make the RooParametricHist (from Combine) for this pt bin
        lPass  = r.RooParametricHist(lName+"_pass_"+iCat,lName+"_pass_"+iCat,self._lMSD,lPassBins,iHFs[0])
        lFail  = r.RooParametricHist(lName+"_fail_"+iCat,lName+"_fail_"+iCat,self._lMSD,lFailBins,iHFs[0])
        lNPass = r.RooAddition(lName+"_pass_"+iCat+"_norm",lName+"_pass_"+iCat+"_norm",lPassBins)
        lNFail = r.RooAddition(lName+"_fail_"+iCat+"_norm",lName+"_fail_"+iCat+"_norm",lFailBins)
        self._allShapes.extend([lPass,lFail,lNPass,lNFail])
        
        # Now write the workspace with the RooParamHist
        lWPass = r.RooWorkspace("w_pass_"+str(iCat))
        lWFail = r.RooWorkspace("w_fail_"+str(iCat))
        getattr(lWPass,'import')(lPass,r.RooFit.RecycleConflictNodes())     # This just imports objects into the workspace and 
        getattr(lWPass,'import')(lNPass,r.RooFit.RecycleConflictNodes())    # RecycleConflictNodes just connects the imported expression
        getattr(lWFail,'import')(lFail,r.RooFit.RecycleConflictNodes())     # to a already existing nodes.
        getattr(lWFail,'import')(lNFail,r.RooFit.RecycleConflictNodes())

        # If in category 1 (wqq)...
        if iCat.find("1") > -1:
            # Write the workspace to file and RECREATE
            lWPass.writeToFile("ralpha"+self._outputName.replace(".root","_"+str(self._poly_lNP)+str(self._poly_lNR)+"_pt.root"))
        else:
            # Else, write the workspace to file and DO NOT RECREATE (that's what the False is for)
            lWPass.writeToFile("ralpha"+self._outputName.replace(".root","_"+str(self._poly_lNP)+str(self._poly_lNR)+"_pt.root"),False)

        lWFail.writeToFile("ralpha"+self._outputName.replace(".root","_"+str(self._poly_lNP)+str(self._poly_lNR)+"_pt.root"),False)
        return [lPass,lFail]                    

    def makeWorkspace(self,iOutput,iDatas,iFuncs,iVars,iCat="cat0",iShift=True):
        
        #####################################################################
        # Creates the final output workspace for this pt bin                #
        # ----------------------------------------------------------------- #
        # Input     - output file name (string)                             #
        #           - single item list of RooDataHist (Data pass/fail)      #
        #           - list of all MC RooDataHists                           #
        #           - list of all vars                                      #
        #           - catagory sting                                        #
        #           - boolean for mass shift                                #
        #                                                                   #
        # Output    - Full workspace written to file                        #
        #####################################################################

        # Initialize the full workspace
        lW = r.RooWorkspace("w_"+str(iCat))

        # Get the pT bin
        ipt = iCat[-1:];

        # Initialize and switch to validation file
        sigMassesForInterpolation = [];
        shapeForInterpolation_central = [];
        shapeForInterpolation_scaleUp = [];
        shapeForInterpolation_scaleDn = [];
        shapeForInterpolation_smearUp = [];
        shapeForInterpolation_smearDn = [];
        shapeForInterpolation_effUp   = [];
        shapeForInterpolation_effDn   = [];
        self._outfile_validation.cd();          

        # Loop through list of all MC RooDataHists
        for pFunc in iFuncs:
            # For this MC RooDataHist, set the pt bin and some strings
            ptbin = ipt;
            process = pFunc.GetName().split("_")[0];
            cat     = pFunc.GetName().split("_")[1];
            mass    = 0.;
            # iShift = True so 'if process is ewk'
            if iShift and ("wqq" in process or "zqq" in process):

                # Set the mass for the process
                if process == "wqq": mass = 80.;
                elif process == "zqq": mass = 91.;
                # elif process == "tqq": raw_input('AHHH TQQ CALLED');  this should never occur based on the prior if statement
                else: mass = float(process[3:])

                # get the matched and unmatched hist
                tmph_matched = self._inputfile.Get(process+"_"+cat+"_matched");         # NOTE0 - need to match this naming scheme
                tmph_unmatched = self._inputfile.Get(process+"_"+cat+"_unmatched");
                
                # NOTE4 - Again, going to scale with these ambiguous codes. Will change this.
                procid = 0 if "wqq" in process else 1
                passid = 1 if "pass" in cat    else 2 
                # scale unmatched and matched hists only once
                if int(ipt) == 1 :
                    scaleHists(tmph_matched,procid,passid)
                    scaleHists(tmph_unmatched,procid,0)#passid)
                
                # NOTE0 - Variable names and hists grabbed do not match!!! Keep for now but replace with 
                if process == "tqq":
                    tmph_matched = self._inputfile.Get(process+"_"+cat+"_unmatched");
                    tmph_unmatched = self._inputfile.Get(process+"_"+cat+"_matched");

                # Create the mass projections
                tmph_mass_matched = proj("cat",str(ipt),tmph_matched,self._mass_nbins,self._mass_lo,self._mass_hi);
                tmph_mass_unmatched = proj("cat",str(ipt),tmph_unmatched,self._mass_nbins,self._mass_lo,self._mass_hi);

                # again,get rid of very low or high mass bins according to pT cat
                for i0 in range(1,self._mass_nbins+1):
                    print pFunc.GetName()
                    # NOTE8
                    if ((i0 > 31 or i0 < 0) and int(ipt) == 1) or ((i0 > 38 or i0 < 4) and int(ipt) == 2) or ((i0 > 46 or i0 < 5) and int(ipt) == 3) or ((i0 > 56 or i0 < 7) and int(ipt) == 4) or ( i0 < 7 and int(ipt) == 5):
                        tmph_mass_matched.SetBinContent(i0,0);
                        tmph_mass_unmatched.SetBinContent(i0,0);

                if pFunc.GetName() == "zqq300_pass_cat5": # bork the last 2 bins!
                    tmph_mass_matched.SetBinContent(59,0.);
                    tmph_mass_matched.SetBinContent(59,0.);     # NOTE8 - this block should be removed as it's an analysis specific fix
                    tmph_mass_unmatched.SetBinContent(60,0.);
                    tmph_mass_unmatched.SetBinContent(60,0.);
                    
                #
                # Next several lines smear and shift the MC
                #

                # smear/shift the matched
                # hist_container is a class instance of `hist` from ../hist.py
                # NOTE6 - I'm just going to trust this works
                hist_container = hist( [mass],[tmph_mass_matched] );
                mass_shift = 1.0;
                mass_shift_unc = 0.15; # 5 (23?) sigma shift!  Change the card accordingly
                res_shift = 1.1;
                res_shift_unc = 0.4; # 5 sigma shift! 
                
                # get new central value
                shift_val = mass - mass*mass_shift;
                tmp_shifted_h = hist_container.shift( tmph_mass_matched, shift_val); # shifts all hists
                
                # get new central value and new smeared value
                smear_val = res_shift - 1.;
                tmp_smeared_h =  hist_container.smear( tmp_shifted_h[0] , smear_val) # smears first hist 
                hmatched_new_central = tmp_smeared_h[0];
                if smear_val <= 0.: hmatched_new_central = tmp_smeared_h[1];
                
                # get shift up/down
                shift_unc = mass*mass_shift*mass_shift_unc;
                hmatchedsys_shift = hist_container.shift( hmatched_new_central, shift_unc);
                
                # get res up/down
                hmatchedsys_smear = hist_container.smear( hmatched_new_central, res_shift_unc); 
                hmatchedsys_eff   = hist_container.smear( hmatched_new_central, 0.);    
                
                # Apply efficiency scale factor
                if "pass" in cat:
                    hmatchedsys_eff[0].Scale(1.1)
                    hmatchedsys_eff[1].Scale(0.9)
                else:
                    hmatchedsys_eff[0].Scale(0.98)
                    hmatchedsys_eff[1].Scale(1.02)

                # Name the new shifted/smeared hist the same as the original
                # NOTE8 - Again these are all specific to this analysis' signal and will probably be done away with
                hmatched_new_central.SetName(pFunc.GetName());
                if mass == 50 and int(ipt) > 2:
                    hmatchedsys_shift[1] = hmatched_new_central.Clone("zqq50"+str(cat)+"_"+str(ipt)+"tmpScaleDn")
                if (mass == 50 and int(ipt) > 3) or (mass == 250 and int(ipt) < 2): # basically 50 GeV is 1 event
                    pInt = hmatched_new_central.Integral()+0.01
                    hmatched_new_central.Add(tmph_mass_unmatched); hmatched_new_central.Scale(pInt/hmatched_new_central.Integral());
                    hmatchedsys_shift[0].Add(tmph_mass_unmatched); hmatchedsys_shift[0].Scale(pInt/hmatchedsys_shift[0].Integral());
                    hmatchedsys_shift[1].Add(tmph_mass_unmatched); hmatchedsys_shift[1].Scale(pInt/hmatchedsys_shift[1].Integral());
                    hmatchedsys_smear[0].Add(tmph_mass_unmatched); hmatchedsys_smear[0].Scale(pInt/hmatchedsys_smear[0].Integral());
                    hmatchedsys_smear[1].Add(tmph_mass_unmatched); hmatchedsys_smear[1].Scale(pInt/hmatchedsys_smear[1].Integral());
                    hmatchedsys_eff  [0].Add(tmph_mass_unmatched); hmatchedsys_eff  [0].Scale(pInt/hmatchedsys_eff  [0].Integral());
                    hmatchedsys_eff  [1].Add(tmph_mass_unmatched); hmatchedsys_eff  [1].Scale(pInt/hmatchedsys_eff  [1].Integral());

                # Name some of the up/down histograms created
                if process == "tqq":
                    hmatchedsys_shift[0].SetName(pFunc.GetName()+"_tscaleUp");
                    hmatchedsys_shift[1].SetName(pFunc.GetName()+"_tscaleDown");
                else:
                    hmatchedsys_shift[0].SetName(pFunc.GetName()+"_scaleUp");
                    hmatchedsys_shift[1].SetName(pFunc.GetName()+"_scaleDown");
                hmatchedsys_smear[0].SetName(pFunc.GetName()+"_smearUp");
                hmatchedsys_smear[1].SetName(pFunc.GetName()+"_smearDown");
                if "zqq" in process:
                    hmatchedsys_eff  [0].SetName(pFunc.GetName()+"_effUp");
                    hmatchedsys_eff  [1].SetName(pFunc.GetName()+"_effDown");
                if "wqq" in process:
                    hmatchedsys_eff  [0].SetName(pFunc.GetName()+"_effUp");
                    hmatchedsys_eff  [1].SetName(pFunc.GetName()+"_effDown");
                
                # Organize into a list
                hout = [hmatched_new_central,hmatchedsys_shift[0],hmatchedsys_shift[1],hmatchedsys_smear[0],hmatchedsys_smear[1],hmatchedsys_eff[0],hmatchedsys_eff[1]];
    
                # Organize the signals into their own lists
                if mass > 0 and mass != 80. and mass != 91.:# and mass != 250. and mass != 300.: 
                    sigMassesForInterpolation.append(mass);     
                    shapeForInterpolation_central.append(hmatched_new_central) 
                    shapeForInterpolation_scaleUp.append(hmatchedsys_shift[0]) 
                    shapeForInterpolation_scaleDn.append(hmatchedsys_shift[1])  
                    shapeForInterpolation_smearUp.append(hmatchedsys_smear[0])  
                    shapeForInterpolation_smearDn.append(hmatchedsys_smear[1])  
                    shapeForInterpolation_effUp  .append(hmatchedsys_eff[0])  
                    shapeForInterpolation_effDn  .append(hmatchedsys_eff[1])  

                # For each of the nominal and up/down hists
                for h in hout:
                    # again,get rid of very low or high mass bins according to pT cat
                    # NOTE8 - Still too specific for b* most likely
                    for i0 in range(1,self._mass_nbins+1):
                        if ((i0 > 31 or i0 < 0) and int(ipt) == 1) or ((i0 > 38 or i0 < 4) and int(ipt) == 2) or ((i0 > 46 or i0 < 5) and int(ipt) == 3) or ((i0 > 56 or i0 < 7) and int(ipt) == 4) or ( i0 < 7 and int(ipt) == 5):
                            h.SetBinContent(i0,0);
                    
                    # Write the histogram   
                    h.Write();
                    # Make a RooDataHist from it
                    tmprdh = RooDataHist(h.GetName(),h.GetName(),r.RooArgList(self._lMSD),h)
                    # Import it into the final workspace for the pt bin
                    getattr(lW,'import')(tmprdh, r.RooFit.RecycleConflictNodes())
                    # If a scale uncertainty...
                    if h.GetName().find("scale") > -1:
                        # Replace 'scale' with 'scalept' in the histo name, convert to Roo, import to workspace
                        pName=h.GetName().replace("scale","scalept")
                        tmprdh = RooDataHist(pName,pName,r.RooArgList(self._lMSD),h)
                        getattr(lW,'import')(tmprdh, r.RooFit.RecycleConflictNodes())

            # If not shifting, just import it to the workspace!
            else: 
                getattr(lW,'import')(pFunc,r.RooFit.RecycleConflictNodes())
                

        # Up to this point in this function, there's been nothing done but 'shift it if you need to, otherwise just save it to the new workspace'

        # do the signal interpolation
        # NOTE9 - Most likely will be removed
        print "---------------------------------------------------------------"
        print len(sigMassesForInterpolation), sigMassesForInterpolation
        print iCat

        # Make this hist objects for each nominal and up/down hists
        morphedHistContainer_central = hist(sigMassesForInterpolation,shapeForInterpolation_central);
        morphedHistContainer_scaleUp = hist(sigMassesForInterpolation,shapeForInterpolation_scaleUp);
        morphedHistContainer_scaleDn = hist(sigMassesForInterpolation,shapeForInterpolation_scaleDn);
        morphedHistContainer_smearUp = hist(sigMassesForInterpolation,shapeForInterpolation_smearUp);
        morphedHistContainer_smearDn = hist(sigMassesForInterpolation,shapeForInterpolation_smearDn);
        morphedHistContainer_effUp   = hist(sigMassesForInterpolation,shapeForInterpolation_effUp);
        morphedHistContainer_effDn   = hist(sigMassesForInterpolation,shapeForInterpolation_effDn);

        interpolatedMasses = [55.,60.0,65.,70.,
                      80.,85.,90.0,95.,
                      105.,110.0,115.,120.,
                      130.,135.0,140.,145.,
                      155.,160.,165.0,170.,
                      175.,180.0,185.,190.,195.,
                      205.,210.,215.,220.,225.,
                      230.,235.,240,245.,
                      255.,260.,265.,270.,275.,
                      280.,285.,290.,295.]

        # For each interpolated mass...
        for m in interpolatedMasses:
            # Initialize a backwards list index (-1 is last item in list)
            mid=-1
            # Change mid depending for high masses
            if m > 200 and  int(ipt) == 1:
                mid=len(sigMassesForInterpolation)-3
            if m > 250 and  int(ipt) == 2:
                mid=len(sigMassesForInterpolation)-2

            # If you didn't change mid...
            if mid != -1:
                # Clone object at [-1] (no morphing)
                htmp_central = shapeForInterpolation_central[mid].Clone("tmp"+str(m)+"scaleup")
                htmp_scaleUp = shapeForInterpolation_scaleUp[mid].Clone("tmp"+str(m)+"scaleup")
                htmp_scaleDn = shapeForInterpolation_scaleDn[mid].Clone("tmp"+str(m)+"scaledn")
                htmp_smearUp = shapeForInterpolation_smearUp[mid].Clone("tmp"+str(m)+"smearup")
                htmp_smearDn = shapeForInterpolation_smearDn[mid].Clone("tmp"+str(m)+"smeardn")
                htmp_effUp   = shapeForInterpolation_effUp  [mid].Clone("tmp"+str(m)+"effup")
                htmp_effDn   = shapeForInterpolation_effDn  [mid].Clone("tmp"+str(m)+"effdn")
                # And scale to very small if above 200 (and not in 1th pt catagory)
                if m > 200:
                    htmp_central.Scale(0.001)
                    htmp_scaleUp.Scale(0.001)
                    htmp_scaleDn.Scale(0.001)
                    htmp_smearUp.Scale(0.001)
                    htmp_smearDn.Scale(0.001)
                    htmp_effUp  .Scale(0.001)
                    htmp_effDn  .Scale(0.001)
            # If you did change mid...
            else:
                # Morph everything
                htmp_central = morphedHistContainer_central.morph(m);
                htmp_scaleUp = morphedHistContainer_scaleUp.morph(m);
                htmp_scaleDn = morphedHistContainer_scaleDn.morph(m);
                htmp_smearUp = morphedHistContainer_smearUp.morph(m);
                htmp_smearDn = morphedHistContainer_smearDn.morph(m);
                htmp_effUp   = morphedHistContainer_effUp  .morph(m);
                htmp_effDn   = morphedHistContainer_effDn  .morph(m);

            # Set some new names for your temp histograms
            htmp_central.SetName("zqq%i_%s" % (int(m),iCat));
            htmp_scaleUp.SetName("zqq%i_%s_scaleUp" % (int(m),iCat)); 
            htmp_scaleDn.SetName("zqq%i_%s_scaleDown" % (int(m),iCat));
            htmp_smearUp.SetName("zqq%i_%s_smearUp" % (int(m),iCat));
            htmp_smearDn.SetName("zqq%i_%s_smearDown" % (int(m),iCat));
            htmp_effUp  .SetName("zqq%i_%s_effUp"    % (int(m),iCat));
            htmp_effDn  .SetName("zqq%i_%s_effDown"  % (int(m),iCat));

            # NOTE8 - another analysis specific fix that gets rid of signal at the high/low ends
            if iCat == "pass_cat5" and m < 125 and m > 100: self.signalChopper(htmp_central,m);

            # Redefine hout (from the previous for loop) and save the signal histogs
            hout = [htmp_central,htmp_scaleUp,htmp_scaleDn,htmp_smearUp,htmp_smearDn,htmp_effUp,htmp_effDn];
            
            # For each one...
            for h in hout:
                print h.GetName()
                # NOTE8 - again with the 'set bin to zero'
                for i0 in range(1,self._mass_nbins+1):
                    if (i0 > 31 and int(ipt) == 1) or ((i0 > 38 or i0 < 4) and int(ipt) == 2) or ((i0 > 46 or i0 < 5) and int(ipt) == 3) or ( (i0 < 7 or i0 > 56) and int(ipt) == 4) or ( i0 < 7 and int(ipt) == 5):
                        h.SetBinContent(i0,0);
                # Write it out, make a Roo it, and import to workspace
                h.Write();
                tmprdh = RooDataHist(h.GetName(),h.GetName(),r.RooArgList(self._lMSD),h)
                getattr(lW,'import')(tmprdh, r.RooFit.RecycleConflictNodes())
                
                # Replace 'scale' with 'scalept' in the histo name, convert to Roo, import to workspace
                if h.GetName().find("scale") > -1:
                    pName=h.GetName().replace("scale","scalept")
                    tmprdh = RooDataHist(pName,pName,r.RooArgList(self._lMSD),h)
                    getattr(lW,'import')(tmprdh, r.RooFit.RecycleConflictNodes())

        # For each data histogram (just one right now)
        for pData in iDatas:
            # Import to the workspace
            getattr(lW,'import')(pData,r.RooFit.RecycleConflictNodes())

        # If NOT in 'pass_cat1'...
        if iCat.find("pass_cat1") == -1:
            # Do NOT recreate when writing
            lW.writeToFile(iOutput,False)
        else:
            # Otherwise recreate
            lW.writeToFile(iOutput) 
    


    ####################
    # 'Dead end' tools #
    ####################

    def buildPolynomialArray(self, iVars,iNVar0,iNVar1,iLabel0,iLabel1,iXMin0,iXMax0):

        #########################################################################
        # Fills empty list with RooVars, each corresponding to a polynomial     #
        # coefficient in two dimensions.                                        #
        # --------------------------------------------------------------------- #
        # Input     - iVars = empty list                                        #
        #           - iNVar0, iNVar1 = polynomial order                         #
        #           - iLabel0, iLabel1 = string to denote variable              #
        #           - iXMin0, iXMax0 = -1, 1 to bound the coefficients          #
        #                                                                       #
        # Output    - appends RooVars to iVar list                              #
        #########################################################################

        ## form of polynomial
        ## (p0r0 + p1r0 * pT + p2r0 * pT^2 + ...) + 
        ## (p0r1 + p1r1 * pT + p2r1 * pT^2 + ...) * rho + 
        ## (p0r2 + p1r2 * pT + p2r2 * pT^2 + ...) * rho^2 + ...
        

        # NOTE10 - mlfit_param.root is the initial 'guess' values for the fit and is generated
        # by Combinewith the -M MaxLikelihoodFit option. Each time you run this script, make the cards,
        # and run Combine, mlfit_param.root is made. The zeroth iteration is done by making manual guesses.
        # I (Lucas) will need to do this most likely.

        lFile = r.TFile("mlfit_param.root")
        lFit  = r.RooFitResult(lFile.Get("fit_b")) # Set to the background only
        self._lEffQCD.setVal(lFit.floatParsFinal().find("qcdeff").getVal())

        for i0 in range(iNVar0+1):
            for i1 in range(iNVar1+1):
                # Build the RooRealVar inputs for this (i0,i1) pair
                pVar = iLabel1+str(i1)+iLabel0+str(i0);
                pXMin = iXMin0
                pXMax = iXMax0
                pVal  = math.pow(10,-min(i1,2)) # Could be 1, 0.1, or 0.01

                # If we're on the first pt order...
                if i1 == 0:
                    # Make a specific starting value (1, 10^-0.5=0.32, 10^-1=0.1, ... 0.1)
                    pVal  = math.pow(10,-min(int(i0*0.5),1))

                # NOTE8 - The above seems highly specific and will probably need to change for b*

                # Guess 0 for p0r0 and for all else, grab the value from lFit
                # NOTE10 - not sure what the difference between pCent != 0 and pVar is
                pCent = 0 if pVar == "p0r0" else lFit.floatParsFinal().find(pVar).getVal()
                pRooVar = r.RooRealVar(pVar,pVar,pCent,pXMin*pVal,pXMax*pVal)

                iVars.append(pRooVar)
        lFile.Close()

    def buildRooPolyArray(self,iPt,iRho,iQCD,iZero,iVars):
        
        #########################################################################
        # Creates the RooPolyVar (basically a polynomial function) for this pt  #
        # bin given the input RooVars and polyarray (iVars)                     #
        # --------------------------------------------------------------------- #
        # Input     - pt and rho RooVars                                        #
        #           - unity constant (1)                                        #
        #           - zero constant (0)                                         #
        #           - polynomial coefficent array                               #
        #                                                                       #
        # Output    - RooPolyVar for rho                                        #
        #########################################################################

        #---------------------------------------------------------------#
        # RooPolyVar    -> Like a RooFormulaVar except the polynomial   #
        #                   coeffieicents are given as input            #
        #---------------------------------------------------------------#

        # Initialize 
        lPt  = r.RooConstVar("Var_Pt_" +str(iPt)+"_"+str(iRho), "Var_Pt_" +str(iPt)+"_"+str(iRho),(iPt))
        lRho = r.RooConstVar("Var_Rho_"+str(iPt)+"_"+str(iRho), "Var_Rho_"+str(iPt)+"_"+str(iRho),(iRho))
        lRhoArray = r.RooArgList()
        lNCount=0

        # For each rho polynomial coefficient...
        for pRVar in range(0,self._poly_lNR+1):

            # Make a temp arguments list
            lTmpArray = r.RooArgList()

            # For each pt polynomial coefficient...
            for pVar in range(0,self._poly_lNP+1):
                if lNCount == 0: lTmpArray.add(iQCD); # Set first constant (e.g. p0r0) to 1
                else: lTmpArray.add(iVars[lNCount]) # Otherwise set it to value in the polynomial array
                lNCount=lNCount+1
            
            # Store the label to keep things from getting too messy
            pLabel="Var_Pol_Bin_"+str(round(iPt,2))+"_"+str(round(iRho,3))+"_"+str(pRVar)

            # Make the RooPolyVar for THIS RHO (have only iterated through pt)
            pPol = r.RooPolyVar(pLabel,pLabel,lPt,lTmpArray)
            # Add it into our storage
            lRhoArray.add(pPol);
            self._allVars.append(pPol)

        # Again, store the label to keep it clean
        lLabel="Var_RhoPol_Bin_"+str(round(iPt,2))+"_"+str(round(iRho,3))

        # Make the RooPolyVar in 2D (lRhoArray is a list of lists)
        lRhoPol = r.RooPolyVar(lLabel,lLabel,lRho,lRhoArray)

        # Save out and return
        self._allVars.extend([lPt,lRho,lRhoPol])
        return lRhoPol

    def rooTheHistFunc(self,iH,iLabel="w",iBin="_cat0"):

        #########################################################################
        # Makes the PDFs from the pass and fail hists for the pt bin for a      #
        # specific process/set                                                  #
        # --------------------------------------------------------------------- #
        # Input     - list of pass and fail histos for                          #
        #               a process in a pt bin (2 items)                         #
        #           - string for process                                        #
        #           - string for pt bin                                         #
        #                                                                       #
        # Output    - appends new RooRealVar and two RooForumalVars             #
        #               to _allVars list                                        #
        #           - appends list of RooHistPdf, RooDataHist, and RooExtendPdf # 
        #               to _allShapes list                                      #
        #           - returns items appended to _allShapes list                 #
        #########################################################################

        # Normalization 
        # -------------
        # Create a normalization variable for the total yield that floats between x0 and x5
        lNTot   = r.RooRealVar (iLabel+"norm"+iBin,iLabel+"norm"+iBin,(iH[0].Integral()+iH[1].Integral()),0.,5.*(iH[0].Integral()+iH[1].Integral()))
        # Create normalization variables (based on an input - so a function) for the pass and fail yields (no bounds since the input variable is bounded)
        lNPass  = r.RooFormulaVar(iLabel+"fpass"+iBin ,iLabel+"norm"+iBin+"*(veff)"  ,r.RooArgList(lNTot,self._lEff))
        lNFail  = r.RooFormulaVar(iLabel+"fqail"+iBin ,iLabel+"norm"+iBin+"*(1-veff)",r.RooArgList(lNTot,self._lEff))
        
        # Shapes
        # ------
        # Create RooDataHists for pass and fail histos for this specific process and pt bin
        # -> Remeber that 'Data' is not data here! It's a stand in for whatever process you're looking at (iLabel)
        lPData  = r.RooDataHist(iLabel+"_pass_"+iBin,iLabel+"_pass_"+iBin, r.RooArgList(self._lMSD),iH[0])
        lFData  = r.RooDataHist(iLabel+"_fail_"+iBin,iLabel+"_fail_"+iBin, r.RooArgList(self._lMSD),iH[1]) 
        # Build pdfs - Need lShift here to float the SHAPE
        lP      = r.RooHistPdf (iLabel+"passh"+iBin,iLabel+"passh"+iBin, r.RooArgList(self._lShift),r.RooArgList(self._lMSD),lPData,0)
        lF      = r.RooHistPdf (iLabel+"failh"+iBin,iLabel+"failh"+iBin, r.RooArgList(self._lShift),r.RooArgList(self._lMSD),lFData,0)

        # Combined
        # --------
        # Extended likelihood from normalization and shape above
        lEP     = r.RooExtendPdf(iLabel+"_passe_" +iBin,iLabel+"pe" +iBin,lP,lNPass)
        lEF     = r.RooExtendPdf(iLabel+"_faile_" +iBin,iLabel+"fe" +iBin,lF,lNFail)
        
        lHist   = [lP,lF,lEP,lEF,lPData,lFData]
        self._allVars.extend([lNTot,lNPass,lNFail])
        self._allShapes.extend(lHist)
        return lHist    

    def getSignals(self,iHP,iHF,iBin):

        #########################################################################
        # Runs rooTheHistFunc on all of the signals and saves the outputs       #
        # to a list                                                             #
        # --------------------------------------------------------------------- #
        # Input     - fhists for all sets BUT QCD MC                            #
        #           - phists for all sets BUT QCD MC                            #
        #           - string category                                           #
        #                                                                       #
        # Output    - rooTheHistFunc output for all signals                     #
        #########################################################################

        #getting signals - skip data+MC (first 5 elm in iHP and iHF)
        lPSigs  = []
        lFSigs  = []
        lPHists = [] 
        lFHists = [] 
        lVars=[50,75,100,125,150,200,250,300]
        # For each signal mass...
        for i0 in range(0,len(lVars)):
            # Roo everything (get hists and PDFs)
            lSig = self.rooTheHistFunc([iHP[i0+5],iHF[i0+5]],"zqq"+str(lVars[i0]),iBin)
            lPSigs.append(lSig[4])
            lFSigs.append(lSig[5])

        # Return lists 
        return (lPSigs,lFSigs)  

    def signalChopper(self,h,m):
        for i in range(1,h.GetNbinsX()+1):
            if h.GetBinCenter(i) > m + 1.5*math.sqrt(m): h.SetBinContent(i,0.);

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-i','--idir', dest='idir', default = 'data/',help='directory with data', metavar='idir')
    parser.add_option('-o','--odir', dest='odir', default = 'plots/',help='directory to write plots', metavar='odir')
    parser.add_option('--pseudo', action='store_true', dest='pseudo', default =False,help='data = MC', metavar='isData')
    parser.add_option('--pseudo15', action='store_true', dest='pseudo15', default =False,help='data = MC (fail) and fail*0.05 (pass)', metavar='isData')
    parser.add_option('--input', dest='input', default = 'histInputs/hist_1DZqq-dataReRecoSpring165eff-3481-Gridv130-final.root',help='directory with data', metavar='idir')

    (options, args) = parser.parse_args()

    import tdrstyle
    tdrstyle.setTDRStyle()
    r.gStyle.SetPadTopMargin(0.10)
    r.gStyle.SetPadLeftMargin(0.16)
    r.gStyle.SetPadRightMargin(0.10)
    r.gStyle.SetPalette(1)
    r.gStyle.SetPaintTextFormat("1.1f")
    r.gStyle.SetOptFit(0000)
    r.gROOT.SetBatch()
    
    main(options,args)
