import ROOT
from ROOT import *

import math
from math import sqrt

import gc
gc.disable()

# ROOT.gROOT.SetBatch(True)
# ROOT.PyConfig.IgnoreCommandLineOptions = True

testTH1 = TH1F('testTH1','testTH1',10,0,10)

for ix in range(1,testTH1.GetNbinsX()+1):
	valx = 2*ix

	testTH1.SetBinContent(ix,valx)
	testTH1.SetBinError(ix,testTH1.GetBinContent(ix)/4)

xVar = RooRealVar('xVar','xtitle',0,10)

binList = RooArgList()
for xbin in range(1,testTH1.GetXaxis().GetNbins()+1):
    name = 'binVar_'+str(xbin)
    title = 'title_binVar_'+str(xbin)
    binContent = testTH1.GetBinContent(xbin)
    binErrUp = binContent + testTH1.GetBinErrorUp(xbin)
    binErrDown = binContent - testTH1.GetBinErrorLow(xbin)

    binRRV = RooRealVar(name, title, binContent, max(binErrDown,0), max(binErrUp,0))

    binList.add(binRRV)


final = RooParametricHist('test_RPH','test_RPH',xVar, binList, testTH1)
		
myWorkspace = RooWorkspace('myW')

getattr(myWorkspace,'import')(final)
myWorkspace.writeToFile('basetest.root',True) 