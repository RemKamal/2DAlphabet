import ROOT
from ROOT import *

#################################################################
# This script is to test Combine's ability to read 2D RDHs.     #
# It creates four different distributions to play with:         #
# - data_obs generated from a pdf (<<<<<infinite events)        #
# - background generated from same pdf (<<<<<infinite events)   #
# - signal (gaussian in the middle)                             #
# - skewed signal to left and right to have shape uncert.       #
# These will then be fed into Combine which will do a bump hunt #
#################################################################


def makeDummyFromPDF(name,distEq,xVar,yVar,printOpt=True):
    # Gaussian
    if distEq == 'gauss':
        meanx = RooConstVar('meanx','meanx',15)
        sigmax = RooConstVar('sigmax','sigmax',2)

        dummyPDF = RooGaussian(name+'x',name+'x',xVar,meanx,sigmax)
        dummyRDS = dummyPDF.generate(RooArgSet(xVar),1000)
        dummyRDH = RooDataHist('signal_main','signal_main',RooArgSet(xVar),dummyRDS)


    # Skewed gaussian up
    elif distEq == 'gaussUp':
        meanx = RooConstVar('meanx','meanx',17)
        sigmax = RooConstVar('sigmax','sigmax',2)
        tailx = RooConstVar('tailx','tailx',0.5)

        dummyPDF = RooNovosibirsk(name+'x',name+'x',xVar,meanx,sigmax,tailx)
        dummyRDS = dummyPDF.generate(RooArgSet(xVar),1000)
        dummyRDH = RooDataHist('signal_main_smearUp','signal_main_smearUp',RooArgSet(xVar),dummyRDS)

    # Skewed guassian down
    elif distEq == 'gaussDown':
        meanx = RooConstVar('meanx','meanx',12)
        sigmax = RooConstVar('sigmax','sigmax',2)
        tailx = RooConstVar('tailx','tailx',-0.5)

        dummyPDF = RooNovosibirsk(name+'x',name+'x',xVar,meanx,sigmax,tailx)
        dummyRDS = dummyPDF.generate(RooArgSet(xVar),1000)
        dummyRDH = RooDataHist('signal_main_smearDown','signal_main_smearDown',RooArgSet(xVar),dummyRDS)

    # Generic
    else:
        dummyPDF = RooGenericPdf(name,distEq,RooArgList(xVar))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar),50000) # output is a RooDataSet

        dummyRDH = RooDataHist(name+'_main',name+'_main',RooArgSet(xVar),dummyRDS)


    # dummyTH2 = dummyRDS.createHistogram(xVar,yVar,35,1,'',name)
    dummyTH2 = None
    # if printOpt == True:
    #     print 'Check this is the shape you want for: ' + distEq
    #     dummyTH2.Draw('lego')
    #     raw_input('Hit enter to confirm this shape')


    # dummyTH1 = dummyTH2.ProjectionX(name+'_main')

    return dummyRDS,dummyTH2,dummyRDH

if __name__ == '__main__':
    
    # Establish our axis variables
    xVar = RooRealVar('x','x',0,35)
    yVar = RooRealVar('y','y',0,1)

    # We need to make some dummy 2D histograms that we know the form of
    dataRDS,dataTH2,dataRDH = makeDummyFromPDF('data_obs','x',xVar,yVar,False)
    bkgRDS,bkgTH2,bkgRDH = makeDummyFromPDF('mybkg','x',xVar,yVar,False)
    signalRDS,signalTH2,signalRDH = makeDummyFromPDF('signal','gauss',xVar,yVar,False)
    signalUpRDS,signalUpTH2,signalUpRDH = makeDummyFromPDF('signalUp','gaussUp',xVar,yVar,False)
    signalDownRDS,signalDownTH2,signalDownRDH = makeDummyFromPDF('signalDown','gaussDown',xVar,yVar,False)

    # # Print out the signals for later review
    # totCan = TCanvas('totCan','totCan',1400,500)
    # totCan.Divide(3,1)
    # totCan.cd(1)
    # signalTH2.Draw()
    # totCan.cd(2)
    # signalUpTH2.Draw()
    # totCan.cd(3)
    # signalDownTH2.Draw()
    # totCan.Print('SignalPlots.root','root')

    # Make workspace to save in
    myWorkspace = RooWorkspace('myW')
    # myframe = xVar.frame()
    for rdh in [xVar,dataRDH,bkgRDH,signalRDH,signalUpRDH,signalDownRDH]:
        getattr(myWorkspace,'import')(rdh)

    # Now save out the RooDataHists
    myWorkspace.writeToFile('base.root',True)

    # outfile = TFile('base.root','recreate')
    # for hist in [dataTH2,bkgTH2,signalTH2,signalUpTH2,signalDownTH2]:
    #     hist.Write()

    # outfile.Close()    

