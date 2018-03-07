#################################################################
# This script is to do 2D Alphabet in Combine with QCD MC.      #
# It also has a masked signal region that is made by splitting  #
# the jet mass axis into 2 RPH2Ds.                              #
#                                                               #
# Will have 4 'bins' passLow, passHigh, failLow, failHigh       #
#                                                               #
# The proceedure is as follows:                                 #
# - Get QCD MC and a signal MC that has already been made to    #
#   certain specifications                                      #
#   --- Axis names are set to the desired RRV names and ranges  #
#   --- Has set_bin_uncertUp/Down naming scheme                 # 
# - Make a RDH and corresponding RRVs from the TH2s             #
# - Turn bkg fail into two RPH2Ds - one low mass, one high      #
#   --- Make a RooRealVar for each bin of background            #
#   --- Store them in RooArgList and make RPH2D                 #
#   --- Make a _norm RooRealVar for each RPH2D                  #
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

import ROOT
from ROOT import *
import os
import pickle
from optparse import OptionParser

gROOT.Macro(os.path.expanduser('~/rootlogon.C'))


def makeRDH(myTH2,RAL_vars):
    name = myTH2.GetName().replace('TH2_','')
    thisRDH = RooDataHist(name,name,RAL_vars,myTH2)
    ####### TESTING CODE ########
    # print str(myTH2.GetNbinsX()) + ', ' + str(myTH2.GetXaxis().GetXmin()) + ', ' + str(myTH2.GetXaxis().GetXmax())
    # testhist = thisRDH.createHistogram(name+'_test',RAL_vars.at(0),RooFit.Binning(myTH2.GetNbinsX(),myTH2.GetXaxis().GetXmin(),myTH2.GetXaxis().GetXmax()),RooFit.YVar(RAL_vars.at(1),RooFit.Binning(myTH2.GetNbinsY(),myTH2.GetYaxis().GetXmin(),myTH2.GetYaxis().GetXmax())))
    # testhist.Draw('lego')
    # raw_input('waiting ' + name)
    #############################
    return thisRDH


# For this to work, you must have your TH2 axes properly named (not TITLED!)
def getRRVs(myTH2):
    band = ''
    if myTH2.GetName().find('Low') != -1:
        band = '_Low'
    elif myTH2.GetName().find('High') != -1:
        band = '_High'

    xname = myTH2.GetXaxis().GetName()+band
    yname = myTH2.GetYaxis().GetName()
    xlow = myTH2.GetXaxis().GetXmin()
    xhigh = myTH2.GetXaxis().GetXmax()
    ylow = myTH2.GetYaxis().GetXmin()
    yhigh = myTH2.GetYaxis().GetXmax()

    xRRV = RooRealVar(xname,xname,xlow,xhigh)
    yRRV = RooRealVar(yname,yname,ylow,yhigh)

    return xRRV,yRRV


def getFileContents(thisFile):
    # Going to organize the contents of the input file into a dictionary that we can access and add to easily
    distDict = {}
    
    # Get the keys
    keysInFile = thisFile.GetListOfKeys()
    iterator = keysInFile.MakeIterator()    # Make an iterator
    key = keysInFile.First()                # Grab the first key
    # While a key exists
    while key != None :  
        # If we have a TH2F...
        if key.ReadObj().ClassName() == 'TH2F':
            # Make an inner dictionary for the key
            histName = key.ReadObj().GetName()
            distDict[histName] = {}

            # Grab and store the TH2
            distDict[histName]['TH2_Full'] = key.ReadObj()

            # Store the process, category, and possible systematic in the inner dictionary
            if key.ReadObj().GetName().split('_')[0] == 'data':
                distDict[histName]['process'] = 'data_obs'
                distDict[histName]['cat'] = key.ReadObj().GetName().split('_')[2]
                try:
                    distDict[histName]['syst'] = key.ReadObj().GetName().split('_')[3]
                except:
                    distDict[histName]['syst'] = None

            else:
                distDict[histName]['process'] = key.ReadObj().GetName().split('_')[0]
                distDict[histName]['cat'] = key.ReadObj().GetName().split('_')[1]
                try:
                    distDict[histName]['syst'] = key.ReadObj().GetName().split('_')[2]
                except:
                    distDict[histName]['syst'] = None
        # If we don't have a TH2F...
        else:
            print 'Object ' + key.ReadObj().GetName() + ' is not a TH2F'

        # Go to the next key
        key = iterator.Next()

    return distDict

def copyHistWithNewXbounds(thisHist,copyName,newBinWidthX,xNewBinsLow,xNewBinsHigh):
    # Make a copy with the same Y bins but new x bins
    nBinsY = thisHist.GetNbinsY()
    yBinsLow = thisHist.GetYaxis().GetXmin()
    yBinsHigh = thisHist.GetYaxis().GetXmax()
    nNewBinsX = int((xNewBinsHigh-xNewBinsLow)/float(newBinWidthX))
    histCopy = TH2F(copyName,copyName,nNewBinsX,xNewBinsLow,xNewBinsHigh,nBinsY,yBinsLow,yBinsHigh)
    
    histCopy.GetXaxis().SetName(thisHist.GetXaxis().GetName())
    histCopy.GetYaxis().SetName(thisHist.GetYaxis().GetName())


    # Loop through the old bins
    # ASSUMES nOldBinsX > nNewBinsX
    for binY in range(1,nBinsY+1):
        # print 'Bin y: ' + str(binY)
        for newBinX in range(1,nNewBinsX+1):
            newBinContent = 0
            newBinXlow = histCopy.GetXaxis().GetBinLowEdge(newBinX)
            newBinXhigh = histCopy.GetXaxis().GetBinUpEdge(newBinX)

            # print '\t New bin x: ' + str(newBinX) + ', ' + str(newBinXlow) + ', ' + str(newBinXhigh)
            for oldBinX in range(1,thisHist.GetNbinsX()+1):
                if thisHist.GetXaxis().GetBinLowEdge(oldBinX) >= newBinXlow and thisHist.GetXaxis().GetBinUpEdge(oldBinX) <= newBinXhigh:
                    # print '\t \t Old bin x: ' + str(oldBinX) + ', ' + str(thisHist.GetXaxis().GetBinLowEdge(oldBinX)) + ', ' + str(thisHist.GetXaxis().GetBinUpEdge(oldBinX))
                    # print '\t \t Adding content ' + str(thisHist.GetBinContent(oldBinX,binY))
                    newBinContent += thisHist.GetBinContent(oldBinX,binY)

            # print '\t Setting content ' + str(newBinContent)
            histCopy.SetBinContent(newBinX,binY,newBinContent)


    return histCopy


#########################
#       Start Here      #
#########################
if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option('-w', '--xwidth', metavar='F', type='int', action='store',
                      default   =   20,
                      dest      =   'xwidth',
                      help      =   'width of your x bins')
    parser.add_option('-l', '--xlow', metavar='F', type='int', action='store',
                      default   =   50,
                      dest      =   'xlow',   
                      help      =   'Lower bound in x')
    parser.add_option('-u', '--xup', metavar='F', type='int', action='store',
                      default   =   360,
                      dest      =   'xup',
                      help      =   'Upper bound in x')

    (options, args) = parser.parse_args()


    allVars = []
    allDists = {}

    #################
    #   Get stuff   #
    #################

    # Open our files and get the TH2s of interest
    inFile = TFile.Open('Full2D_input.root')
    dDists = getFileContents(inFile)

    # Establish our axis variables
    xVar,yVar = getRRVs(dDists['data_obs_pass']['TH2_Full']) # only have to do this once (make sure this TH2 has correct axis names!)
    varList = RooArgList(xVar,yVar)

    # Get signal region bin walls and the 'content' which is the bin widths in x
    sigStart = inFile.Get('TH1_region_bounds').GetBinLowEdge(1)
    sigEnd = sigStart + inFile.Get('TH1_region_bounds').GetBinWidth(1)
    xBinWidth = inFile.Get('TH1_region_bounds').GetBinContent(1)



    #########################
    #   Make RooDataHists   #
    #########################
    subVarsMade = False
    for distKey in dDists.keys():
        histToSplit = dDists[distKey]['TH2_Full']   # Grab the hist we want to split into high and low categories

        # Clone into high and low and give it the same name but replace the category (pass/fail) with passLow/FailLow and passHigh/failHigh
        lowName = 'TH2_' + distKey.replace(dDists[distKey]['cat'],dDists[distKey]['cat']+'Low')
        highName = 'TH2_' + distKey.replace(dDists[distKey]['cat'],dDists[distKey]['cat']+'High')

        histLowX  = copyHistWithNewXbounds(histToSplit, lowName, xBinWidth,  options.xlow,sigStart)         # Need to make bins generic/as an option
        histHighX = copyHistWithNewXbounds(histToSplit, highName, xBinWidth, sigEnd,options.xup)         # Third argument is bin WIDTH not nbins


        dDists[distKey]['TH2_Low'] = histLowX                           # Won't use this but saving anyway
        dDists[distKey]['TH2_High'] = histHighX                         # Won't use this but saving anyway

        # On first pass through, make low and high x RRVs
        # If we don't do this, the xVar will change its binning to match the TH2 dimensions
        # when making the RDH. If the xVar bins go to the low x band, then when you call 
        # to make the high x RDH the xVar will change its binning to the next nearest bin
        # and so only one of the high mass bins will fill (the one next to the blinded region). 

        if subVarsMade == False:
            xVarLow = getRRVs(histLowX)[0]
            xVarHigh = getRRVs(histHighX)[0]
            allVars.extend([xVarLow,xVarHigh])
            lowVarList = RooArgList(xVarLow,yVar)
            highVarList = RooArgList(xVarHigh,yVar)
            subVarsMade = True

        # Convert to RooDataHists
        dDists[distKey]['RDH_Full'] = makeRDH(histToSplit,varList)      # Won't use this but saving anyway
        dDists[distKey]['RDH_Low']  = makeRDH(histLowX,lowVarList)
        dDists[distKey]['RDH_High'] = makeRDH(histHighX,highVarList)

        ####### TESTING CODE ########
        # testhist = dDists[distKey]['RDH_Low'].createHistogram(distKey+'_Low',xVar,RooFit.Binning(histLowX.GetNbinsX(),histLowX.GetXaxis().GetXmin(),histLowX.GetXaxis().GetXmax()),RooFit.YVar(yVar,RooFit.Binning(histLowX.GetNbinsY(),histLowX.GetYaxis().GetXmin(),histLowX.GetYaxis().GetXmax())))
        # testhist.Draw('lego')
        # raw_input('waiting')
        #############################

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
    dDists['qcd_fail'] = {}
    dDists['qcd_pass'] = {}
    for iband, TH2_data_fail in enumerate([dDists['data_obs_fail']['TH2_Low'],dDists['data_obs_fail']['TH2_High']]):
        if iband == 0:   
            sband = 'Low'
            xVarBand = xVarLow
        elif iband == 1:
            sband = 'High'
            xVarBand = xVarHigh
        binListFail = RooArgList()
        binListPass = RooArgList()

        for ybin in range(1,TH2_data_fail.GetNbinsY()+1):
            for xbin in range(1,TH2_data_fail.GetNbinsX()+1):
                # First make our fail bins into RRVs
                name = 'Fail'+sband+'_bin_'+str(xbin)+'-'+str(ybin)

                binContent = TH2_data_fail.GetBinContent(xbin,ybin)
                binErrUp = binContent + TH2_data_fail.GetBinErrorUp(xbin,ybin)*5
                binErrDown = binContent - TH2_data_fail.GetBinErrorLow(xbin,ybin)*5
                binRRV = RooRealVar(name, name, binContent, max(binErrDown,0), max(binErrUp,0))
                
                # Store the bin
                binListFail.add(binRRV)
                allVars.append(binRRV)

                # Then get bin center and assign it to a RooConstVar
                xCenter = TH2_data_fail.GetXaxis().GetBinCenter(xbin)
                yCenter = TH2_data_fail.GetYaxis().GetBinCenter(ybin)

                xConst = RooConstVar("ConstVar_"+sband+"_x_"+str(xbin)+'_'+str(ybin),"ConstVar_"+sband+"_x_"+str(xbin)+'_'+str(ybin),xCenter)
                yConst = RooConstVar("ConstVar_"+sband+"_y_"+str(xbin)+'_'+str(ybin),"ConstVar_"+sband+"_y_"+str(xbin)+'_'+str(ybin),yCenter)

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
                    thisXPolyVarLabel = "xPol_"+sband+"_y_"+str(yCoeff)+"_Bin_"+str(int(xbin))+"_"+str(int(ybin))
                    xPolyVar = RooPolyVar(thisXPolyVarLabel,thisXPolyVarLabel,xConst,xCoeffList)
                    xPolyList.add(xPolyVar)
                    allVars.append(xPolyVar)

                # Now make a polynomial out of the x polynomials
                thisYPolyVarLabel = "FullPol_"+sband+"_Bin_"+str(int(xbin))+"_"+str(int(ybin))
                thisFullPolyVar = RooPolyVar(thisYPolyVarLabel,thisYPolyVarLabel,yConst,xPolyList)

                allVars.append(thisFullPolyVar)


                # Finally make the pass distribution
                formulaArgList = RooArgList(binRRV,thisFullPolyVar)
                thisBinPass = RooFormulaVar('Pass'+sband+'_bin_'+str(xbin)+'-'+str(ybin),'Pass'+sband+'_bin_'+str(xbin)+'-'+str(ybin),"@0*@1",formulaArgList)
                binListPass.add(thisBinPass)
                allVars.append(thisBinPass)


        print "Making RPH2Ds for " + sband
        dDists['qcd_fail']['RPH2D_fail'+sband]          = RooParametricHist2D('qcd_fail'+sband,'qcd_fail'+sband,xVarBand, yVar, binListFail, TH2_data_fail)
        dDists['qcd_fail']['RPH2D_fail'+sband+'_norm']  = RooAddition('qcd_fail'+sband+'_norm','qcd_fail'+sband+'_norm',binListFail)
        dDists['qcd_pass']['RPH2D_pass'+sband ]         = RooParametricHist2D('qcd_pass'+sband,'qcd_pass'+sband,xVarBand, yVar, binListPass, TH2_data_fail)
        dDists['qcd_pass']['RPH2D_pass'+sband+'_norm']  = RooAddition('qcd_pass'+sband+'_norm','qcd_pass'+sband+'_norm',binListPass)

        dDists['qcd_fail']['xbins_'+sband] = TH2_data_fail.GetNbinsX()
        dDists['qcd_fail']['ybins_'+sband] = TH2_data_fail.GetNbinsY()
        


    print "Making workspace..."
    # Make workspace to save in
    myWorkspace = RooWorkspace("w_test")
    for key in dDists.keys():
        for subkey in dDists[key].keys():
            if subkey not in ['cat','process','syst'] and subkey.find('TH2') == -1 and subkey.find('bins_') == -1:
                rooObj = dDists[key][subkey]
                print "Importing " + rooObj.GetName()
                getattr(myWorkspace,'import')(rooObj,RooFit.RecycleConflictNodes())

    getattr(myWorkspace,'import')(xVar,RooFit.RecycleConflictNodes())   # Won't ever be imported by something that needs it

    # Now save out the RooDataHists
    myWorkspace.writeToFile('base.root',True)  

    
    # Finally do some minor card prep
    card_template = open('card_2Dv3p1.tmp','r')
    card_new = open('card_2Dv3p1.txt','w')
    card_new.write(card_template.read())
    card_template.close()
    card_new.write('\n')
    flatParamLines = []
    for sband in ['Low','High']:
        for ix in range(1,dDists['qcd_fail']['xbins_'+sband]+1):
            for iy in range(1,dDists['qcd_fail']['ybins_'+sband]+1):
                flatParamLines.append('Fail'+sband+'_bin_'+str(ix)+'-'+str(iy)+' flatParam \n')
    card_new.writelines(flatParamLines)
    card_new.close()

