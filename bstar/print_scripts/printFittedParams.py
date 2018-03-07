import ROOT
from ROOT import *

file = TFile.Open('MaxLikelihoodFitResult.root')
myw = file.Get('MaxLikelihoodFitResult')

for i in range(3):
	for j in range(2):
		print "polyCoeff_x"+str(i)+"y"+str(j)
		myw.var("polyCoeff_x"+str(i)+"y"+str(j)).Print()