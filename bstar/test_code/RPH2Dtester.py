import ROOT
from ROOT import *

import math
from math import sqrt

# ROOT.gROOT.SetBatch(True)
# ROOT.PyConfig.IgnoreCommandLineOptions = True

testTH2 = TH2F('testTH2','testTH2',10,0,10,25,0,25)

for ix in range(1,testTH2.GetNbinsX()+1):
	for iy in range(1,testTH2.GetNbinsY()+1):
		valx = 2*ix
		valy = 3*iy

		testTH2.SetBinContent(ix,iy,valx*valy)
		testTH2.SetBinError(ix,iy,testTH2.GetBinContent(ix,iy)/4)

xVar = RooRealVar('xVar','xtitle',0,10)
yVar = RooRealVar('yVar','ytitle',0,25)

testList = []
binList = RooArgList()
for ybin in range(1,testTH2.GetYaxis().GetNbins()+1):
    for xbin in range(1,testTH2.GetXaxis().GetNbins()+1):
        name = 'binVar_'+str(xbin)+'-'+str(ybin)
        title = 'title_binVar_'+str(xbin)+'-'+str(ybin)
        binContent = testTH2.GetBinContent(xbin,ybin)
        binErrUp = binContent + testTH2.GetBinErrorUp(xbin,ybin)
        binErrDown = binContent - testTH2.GetBinErrorLow(xbin,ybin)
        # print name + ', ' + title + ', ' + str(binContent) + ', ' + str(binErrDown) + ', ' + str(binErrUp)
        binRRV = RooRealVar(name, title, binContent, max(binErrDown,0), max(binErrUp,0))
        
        testList.append(binRRV)

for item in testList:
	binList.add(item)


# Check that binList is non-empty and check type in c++ code


final = RooParametricHist2D('test_RPH2D','test_RPH2D',xVar, yVar, binList, testTH2)
		
myWorkspace = RooWorkspace('myW')

getattr(myWorkspace,'import')(final)
# Now save out the RooDataHists
myWorkspace.writeToFile('basetest.root',True) 
