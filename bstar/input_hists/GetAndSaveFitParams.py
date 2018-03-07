#############################################################
# Builds dictionary and pickles it for use in Full2D*.py    #
# --------------------------------------------------------- #
# Necessary because of different root versions and a lack   #
# of local combine. I can't open these TF1's on LPC when    #
# they were made on my Mac and I can't run                  #
# RooParametricHist2D on my Mac so the different steps need #
# to be split up.                                           #
#############################################################


import ROOT
from ROOT import *

import pickle

# Got these from BStar13TeV/Alphabet/results/default/MtwvsBkg_QCD_mtfit_quad_cheat_narrow.root
# Ex. p1fit.GetParameter(0) = x1y0
fParameterGuess = TFile.Open('../../../BStar13TeV/Alphabet/results/default/MtwvsBkg_QCD_mtfit_quad_cheat_narrow.root')
print 'test0'
p0fit = fParameterGuess.Get('p0fit')
print 'test1'
p1fit = fParameterGuess.Get('p1fit')
print 'test2'
p2fit = fParameterGuess.Get('p2fit')
myguesses = {
    "nom":[
        [p0fit.GetParameter(0),p0fit.GetParameter(1)],     # nominal, x0 [y0,y1]
        [p1fit.GetParameter(0),p1fit.GetParameter(1)],     # nominal, x1
        [p2fit.GetParameter(0),p2fit.GetParameter(1)]      # nominal, x2
    ]}
myguesses["up"] = [
                    [p0fit.GetParameter(0)+p0fit.GetParError(0)*10, p0fit.GetParameter(1)+p0fit.GetParError(1)*10],     
                    [p1fit.GetParameter(0)+p1fit.GetParError(0)*10, p1fit.GetParameter(1)+p1fit.GetParError(1)*10],     
                    [p2fit.GetParameter(0)+p2fit.GetParError(0)*10, p2fit.GetParameter(1)+p2fit.GetParError(1)*10]   
                ]
myguesses["down"] = [
                    [p0fit.GetParameter(0)-p0fit.GetParError(0)*10, p0fit.GetParameter(1)-p0fit.GetParError(1)*10],     
                    [p1fit.GetParameter(0)-p1fit.GetParError(0)*10, p1fit.GetParameter(1)-p1fit.GetParError(1)*10],     
                    [max(0,p2fit.GetParameter(0)-p2fit.GetParError(0)*10), p2fit.GetParameter(1)-p2fit.GetParError(1)*10]     # x2y0 should be positive since shape in x is concave up and intercept in y is > 0
                ]

print "Made"
print myguesses

pickle.dump( myguesses, open( "myguesses.p", "wb" ) )