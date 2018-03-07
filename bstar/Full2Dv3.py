import ROOT
from ROOT import *
import os
import pickle
gROOT.Macro(os.path.expanduser('~/rootlogon.C'))
#################################################################
# This script is to do 2D Alphabet in Combine with QCD MC.      #
# The proceedure is as follows:                                 #
# - Get QCD MC and a signal MC that has already been made to    #
#   certain specifications                                      #
#   --- Axis names are set to the desired RRV names and ranges  #
#   --- Has set_bin_uncertUp/Down naming scheme                 # 
# - Make a RDH and corresponding RRVs from the TH2s             #
# - Turn bkg fail into RPH2D                                    #
#   --- Make a RooRealVar for each bin of background            #
#   --- Store them in RooArgList and make RPH2D                 #
#   --- Make a _norm RooRealVar for the RPH2D                   #
# - Create a RooPolyVar as the transfer function                #
#   --- You should know the shape of this based on the PDFs     #
#       used to generate the data pass an fail                  #
# - Create the bkg pass from TF*bkg_fail                        #
# These will then be fed into Combine which will do the fit     #
#################################################################
# To-do                                                         #
# -----                                                         #
# - Make poly orders as options and code this generalization    #
#################################################################

def makeRDH(myTH2,RAL_vars):
    name = myTH2.GetName()
    thisRDH = RooDataHist(name,name,RAL_vars,myTH2)
    return thisRDH


# For this to work, you must have your TH2 axes properly named (not TITLED!)
def getRRVs(myTH2):
    xname = myTH2.GetXaxis().GetName()
    yname = myTH2.GetYaxis().GetName()
    xlow = myTH2.GetXaxis().GetXmin()
    xhigh = myTH2.GetXaxis().GetXmax()
    ylow = myTH2.GetYaxis().GetXmin()
    yhigh = myTH2.GetYaxis().GetXmax()

    xRRV = RooRealVar(xname,xname,xlow,xhigh)
    yRRV = RooRealVar(yname,yname,ylow,yhigh)

    return xRRV,yRRV

#########################
#       Start Here      #
#########################
if __name__ == '__main__':
    allVars = []

    # Open our files and get the TH2s of interest
    inFile = TFile.Open('Full2D_input.root')
    TH2_data_pass = inFile.Get('data_obs_pass')
    TH2_data_fail = inFile.Get('data_obs_fail')
    TH2_signalRH1200_pass = inFile.Get('signalRH1200_pass')
    TH2_signalRH1200_fail = inFile.Get('signalRH1200_fail')
    TH2_signalRH1200_pass_WUp = inFile.Get('signalRH1200_pass_WUp')
    TH2_signalRH1200_fail_WUp = inFile.Get('signalRH1200_fail_WUp')
    TH2_signalRH1200_pass_WDown = inFile.Get('signalRH1200_pass_WDown')
    TH2_signalRH1200_fail_WDown = inFile.Get('signalRH1200_fail_WDown')


    # Establish our axis variables
    xVar,yVar = getRRVs(TH2_data_pass) # only have to do this once (make sure this TH2 has correct axis names!)
    varList = RooArgList(xVar,yVar)

    # Convert to RooDataHists
    RDH_data_pass = makeRDH(TH2_data_pass,varList)
    RDH_data_fail = makeRDH(TH2_data_fail,varList)
    RDH_signalRH1200_pass = makeRDH(TH2_signalRH1200_pass,varList)
    RDH_signalRH1200_fail = makeRDH(TH2_signalRH1200_fail,varList)
    RDH_signalRH1200_pass_WUp = makeRDH(TH2_signalRH1200_pass_WUp,varList)
    RDH_signalRH1200_fail_WUp = makeRDH(TH2_signalRH1200_fail_WUp,varList)
    RDH_signalRH1200_pass_WDown = makeRDH(TH2_signalRH1200_pass_WDown,varList)
    RDH_signalRH1200_fail_WDown = makeRDH(TH2_signalRH1200_fail_WDown,varList)

    things2import = [   RDH_data_pass, 
                        RDH_data_fail, 
                        RDH_signalRH1200_pass, 
                        RDH_signalRH1200_fail, 
                        RDH_signalRH1200_pass_WUp, 
                        RDH_signalRH1200_fail_WUp,
                        RDH_signalRH1200_pass_WDown,
                        RDH_signalRH1200_fail_WDown]


#############################################################################################
# Everything from here on is only dealing with the QCD estimate - everything else is done   #
#############################################################################################

    # Get some starting guess values for the coefficients of the Rp/f (po1 vs pol2)
    # In the future, this info should just be saved in inFile to keep things generic
    # For now, this is a hack to fix a bug. Read GetAndSaveFitParams.py for more.
    myguesses = pickle.load(open( "myguesses.p", "rb" ))

    # Store the guesses as RRVs in an easy-to-access dictionary
    polYO = 1
    polXO = 2
    PolyCoeffs = {}
    for yi in range(polYO+1):
        thisXCoeffList = RooArgList()
        for xi in range(polXO+1):
            name = 'polyCoeff_'+'x'+str(xi)+'y'+str(yi)
            PolyCoeffs['x'+str(xi)+'y'+str(yi)] = RooRealVar(name,name,myguesses['nom'][xi][yi],myguesses['down'][xi][yi],myguesses['up'][xi][yi])
            allVars.append(PolyCoeffs['x'+str(xi)+'y'+str(yi)])

    # Now loop through all of our bins to...
    # - make each fail bin into a RRV
    # - derive a RooFormulaVar for each pass bin
    binListFail = RooArgList()
    binListPass = RooArgList()
    for ybin in range(1,TH2_data_fail.GetYaxis().GetNbins()+1):
        for xbin in range(1,TH2_data_fail.GetXaxis().GetNbins()+1):
            # First make our fail bins into RRVs
            name = 'Fail_bin_'+str(xbin)+'-'+str(ybin)

            # Mask out anything in the signal region by making a RRV with value from 0 to 1000000
            if TH2_data_fail.GetXaxis().GetBinLowEdge(xbin+1) > 150 and TH2_data_fail.GetXaxis().GetBinLowEdge(xbin) < 190:
                binRRV = RooRealVar(name, name, binContent, 0, 100000)
                print 'Creating masked bin ' + name
            else:
                binContent = TH2_data_fail.GetBinContent(xbin,ybin)
                binErrUp = binContent + TH2_data_fail.GetBinErrorUp(xbin,ybin)*5
                binErrDown = binContent - TH2_data_fail.GetBinErrorLow(xbin,ybin)*5
                binRRV = RooRealVar(name, name, binContent, max(binErrDown,0), max(binErrUp,0))
            
            # Store the bin
            binListFail.add(binRRV)
            allVars.append(binRRV)

            # Then get bin center and save
            xCenter = TH2_data_fail.GetXaxis().GetBinCenter(xbin)
            yCenter = TH2_data_fail.GetYaxis().GetBinCenter(ybin)

            xConst = RooConstVar("ConstVar_x_"+str(xbin)+'_'+str(ybin),"ConstVar_x_"+str(xbin)+'_'+str(ybin),xCenter)
            yConst = RooConstVar("ConstVar_y_"+str(xbin)+'_'+str(ybin),"ConstVar_y_"+str(xbin)+'_'+str(ybin),yCenter)

            allVars.append(xConst)
            allVars.append(yConst)

            # And now make a polynomial for this bin
            xPolyList = RooArgList()
            for yCoeff in range(polYO+1):
                xCoeffList = RooArgList()

                # Get each x coefficient for this y
                for xCoeff in range(polXO+1):                    
                    xCoeffList.add(PolyCoeffs['x'+str(xCoeff)+'y'+str(yCoeff)])

                # Make the polynomial and save it to the list of x polynomials
                thisXPolyVarLabel = "xPol_y_"+str(yCoeff)+"_Bin_"+str(int(xbin))+"_"+str(int(ybin))
                xPolyVar = RooPolyVar(thisXPolyVarLabel,thisXPolyVarLabel,xConst,xCoeffList)
                xPolyList.add(xPolyVar)
                allVars.append(xPolyVar)

            # Now make a polynomial out of the x polynomials
            thisYPolyVarLabel = "FullPol_Bin_"+str(int(xbin))+"_"+str(int(ybin))
            thisFullPolyVar = RooPolyVar(thisYPolyVarLabel,thisYPolyVarLabel,yConst,xPolyList)

            allVars.append(thisFullPolyVar)


            # Finally make the pass distribution
            formulaArgList = RooArgList(binRRV,thisFullPolyVar)
            thisBinPass = RooFormulaVar('Pass_bin_'+str(xbin)+'-'+str(ybin),'Pass_bin_'+str(xbin)+'-'+str(ybin),"@0*@1",formulaArgList)
            binListPass.add(thisBinPass)
            allVars.append(thisBinPass)


    print "Making RPH2Ds"
    RPH2D_qcd_fail = RooParametricHist2D('qcd_fail','qcd_fail',xVar, yVar, binListFail, TH2_data_fail)
    RPH2D_qcd_pass = RooParametricHist2D('qcd_pass','qcd_pass',xVar, yVar, binListPass, TH2_data_fail)
    RPH2D_qcd_fail_norm = RooAddition('qcd_fail_norm','qcd_fail_norm',binListFail)
    RPH2D_qcd_pass_norm = RooAddition('qcd_pass_norm','qcd_pass_norm',binListPass)


    things2import.extend([
        RPH2D_qcd_fail,
        RPH2D_qcd_pass,
        RPH2D_qcd_fail_norm,
        RPH2D_qcd_pass_norm,
    ])


    print "Making workspace..."
    # Make workspace to save in
    myWorkspace = RooWorkspace("w_test")
    for rdh in things2import:
        print "Importing " + rdh.GetName()
        getattr(myWorkspace,'import')(rdh,RooFit.RecycleConflictNodes())

    # Now save out the RooDataHists
    myWorkspace.writeToFile('base.root',True)  

    

