import ROOT
from ROOT import *

import math
from math import sqrt

# ROOT.gROOT.SetBatch(True)
# ROOT.PyConfig.IgnoreCommandLineOptions = True

def makeRPH2DBinList(thisTH2,thisname):
    testList = []
    binList = RooArgList()
    for ybin in range(1,thisTH2.GetYaxis().GetNbins()+1):
        for xbin in range(1,thisTH2.GetXaxis().GetNbins()+1):
            name = str(thisname)+'_binVar_'+str(xbin)+'-'+str(ybin)
            title = str(thisname)+'_binVar_'+str(xbin)+'-'+str(ybin)
            binContent = thisTH2.GetBinContent(xbin,ybin)
            binErrUp = binContent + thisTH2.GetBinErrorUp(xbin,ybin)
            binErrDown = binContent - thisTH2.GetBinErrorLow(xbin,ybin)
            # print name + ', ' + title + ', ' + str(binContent) + ', ' + str(binErrDown) + ', ' + str(binErrUp)
            binRRV = RooRealVar(name, title, binContent, max(binErrDown,0), max(binErrUp,0))
            
            testList.append(binRRV)

    for item in testList:
        binList.add(item)

    return binList

if __name__ == '__main__':

    testTH2 = TH2F('testTH2','testTH2',10,0,10,25,0,25)

    for ix in range(1,testTH2.GetNbinsX()+1):
    	for iy in range(1,testTH2.GetNbinsY()+1):
    		valx = 2*ix
    		valy = 3*iy

    		testTH2.SetBinContent(ix,iy,valx*valy)
    		testTH2.SetBinError(ix,iy,testTH2.GetBinContent(ix,iy)/4)

    xVar = RooRealVar('xVar','xtitle',0,10)
    yVar = RooRealVar('yVar','ytitle',0,25)

    myWorkspace = RooWorkspace('myW')

    finalBins = makeRPH2DBinList(testTH2,'test')
    final = RooParametricHist2D('mybkg','mybkg',xVar, yVar, finalBins, testTH2)
    norm = RooAddition('mybkg_norm','mybkg_norm',finalBins)

    getattr(myWorkspace,'import')(final)
    getattr(myWorkspace,'import')(norm)


    # Now save out the RooDataHists
    myWorkspace.writeToFile('basetest.root',True) 
