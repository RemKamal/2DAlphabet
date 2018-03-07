import ROOT
from ROOT import *

xvar = RooRealVar('x','x',-1,-1)

xproxy = RooRealProxy('xproxy','xproxy',xvar)

# print xproxy.min()
print xproxy.min('5')
