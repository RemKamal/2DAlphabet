import ROOT
from ROOT import *

#################################################################
# This script is to test the feasibility of a 2nd Full2D plan.  #
# It assumes a pass distribution of x^3*y^2 and fail of x*y     #
# which gives an Rp/f of x^2*y (these are arbitrary choices).   #
# The idea is to build the Rp/f with a blinded signal region    #
# in Mt and then fit it                                         #
#################################################################


if __name__ == '__main__':
    
    # Get some QCD MC to test with 
    filepass = TFile.Open('TWrhalphabetdata_Trigger_nominal_none_PSET_rate_default.root')
    filefail = TFile.Open('TWrhalphabetdata_Trigger_nominal_none_PSET_rate_default.root')

    THpass = filepass.Get('MtwvMtPass')
    THf = filefail.Get('MtwvMtFail')

    THpass.RebinX(2)
    THf.RebinX(2)

    THpass.RebinY(5)
    THf.RebinY(5)

    # Divide to get the ratio
    myRpf = THpass.Clone('myRpf')
    myRpf.Divide(THf)

    # Blind points in top mass signal region
    for xbin in range(myRpf.GetNbinsX()):
        for ybin in range(myRpf.GetNbinsY()):
            globalBin = myRpf.GetBin(xbin,ybin)
            xbinCenter = myRpf.GetXaxis().GetBinCenter(xbin)
            # if xbinCenter > 105 and xbinCenter < 210:
            #     myRpf.SetBinContent(xbin,ybin,0)
            if False:#myRpf.GetBinContent(globalBin) > 5:
                myRpf.SetBinContent(xbin,ybin,0)

    myRpf.Draw('lego')
    raw_input('waiting')

    # Establish our axis variables
    mtVar = RooRealVar('mt','mt',50,350)
    mtwVar = RooRealVar('mtw','mtw',500,4000)

    # Now we need to turn it into RooDataHist
    RpfRDH = RooDataHist('RpfRDH','RpfRDH',RooArgList(mtVar,mtwVar),myRpf)

    # Make some coefficients (5)
    a0 = RooRealVar('a0','a0',0,0.1)
    a1 = RooRealVar('a1','a1',-0.001,0.001)
    a2 = RooRealVar('a2','a2',-0.00001,0.00001)

    b0 = RooRealVar('b0','b0',0.1,0.3)
    b1 = RooRealVar('b1','b1',-0.0001,0)

    # Build a pdf to fit with
    Rpf = RooGenericPdf('RpfPDF','(a0+a1*mt+a2*mt**2)(b0+b1*mtw)',RooArgList(mtVar,mtwVar,a0,a1,a2,b0,b1))

    # Do the fit
    Rpf.fitTo(RpfRDH)

    # Plot
    hRpfPdf = Rpf.createHistogram('mt,mtw',20,20)

    c1 = TCanvas('c1','c1',800,700)
    c1.cd()

    # myRpf.Draw('lego')
    hRpfPdf.Draw('surf')
    raw_input('waiting')