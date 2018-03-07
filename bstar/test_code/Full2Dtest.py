import ROOT
from ROOT import *

#################################################################
# This script is to test the feasibility of the Full2D plan.    #
# It assumes a pass distribution of x^3*y^2 and fail of x*y     #
# which gives an Rp/f of x^2*y (these are arbitrary choices).   #
# The idea is to guess the pass when you know the fail and      #
# the form of the Rp/f                                          #
#################################################################


def makeDummies():
    # First we need to setup a random number generator
    randGenerator = TRandom3() # Sets up an instance of the generator
    randGenerator.SetSeed(0)

    # Do different axis binning to distinguish the two directions easily
    pass_TH2 = TH2F('pass_TH2','pass_TH2',25,0,25,10,0,10)
    fail_TH2 = TH2F('fail_TH2','fail_TH2',25,0,25,10,0,10)

    # We also need to define our distributions via TF1's that we sample from
    passDistx = TF1('passDistx','x**3',0,25)
    passDisty = TF1('passDisty','x**2',0,10)

    failDistx = TF1('failDistx','x',0,25)
    failDisty = TF1('failDisty','x',0,10)


    # We have 250 bins so let's fill the histograms with 10000 random values
    for i in range(10000):
        passxrand = passDistx.GetRandom()
        passyrand = passDisty.GetRandom()

        failxrand = failDistx.GetRandom()
        failyrand = failDisty.GetRandom()

        pass_TH2.Fill(passxrand,passyrand)
        fail_TH2.Fill(failxrand,failyrand)

        if (i+1)%100 == 0:
            print 'Generating point ' + str(i+1) + '\r',

    return (pass_TH2,fail_TH2)


def makePoly(xRRV,yRRV):
    # I've kept this very simple since we have pol2 in x and pol1 in y
    # This means there should be 6 constants (x2y will be 1 and all else should be 0!)
    Nx = 2
    Ny = 1

    varList = {}

    thesePol1D = RooArgList()
    for n in range(Nx+1):
        these1Dcoefficients = RooArgList()
        for m in range(Ny+1):
            thisVar = 'x'+str(n)+'y'+str(m)
            thisVal = 0
            thismin = -10 # Make big bounds to really test the fit
            thismax = 10

            # Save the coefficient
            thisRooVar = RooRealVar(thisVar,thisVar,thisVal,thismin,thismax)
            varList[thisVar] = thisRooVar #... in a general dictionary
            these1Dcoefficients.add(thisRooVar)

        thisPol1D = RooPolyVar('x'+str(n),'x'+str(n),xRRV,these1Dcoefficients)
        thesePol1D.add(thisPol1D)

    full2Dpol = RooPolyVar('Rpf','Rpf',yRRV,thesePol1D)

    return full2Dpol

if __name__ == '__main__':
    
    # We need to make some dummy 2D histograms that we know the form of
    passDummy,failDummy = makeDummies()

    # Establish our axis variables
    xVar = RooRealVar('x','x',0,25)
    yVar = RooRealVar('y','y',0,10)

    # Now we need to turn these into RooDataHists
    passRDH = RooDataHist('pass','pass',RooArgList(xVar,yVar),passDummy)
    failRDH = RooDataHist('fail','fail', RooArgList(xVar,yVar),failDummy)

    # Build a polynomial for the transfer function
    Rpf = makePoly(xVar,yVar)

    # Make our estimate
    passRFV = RooFormulaVar('est','est','@0*@1',RooArgList(failRDH,Rpf))




