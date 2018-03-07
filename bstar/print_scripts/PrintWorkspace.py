import ROOT
from ROOT import *

myf = TFile.Open('../base.root')
myw = myf.Get('w_test')
myw.Print()
