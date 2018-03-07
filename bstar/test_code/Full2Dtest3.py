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

        meany = RooConstVar('meany','meany',10)
        sigmay = RooConstVar('sigmay','sigmay',2)

        dummyPDFx = RooGaussian(name+'x',name+'x',xVar,meanx,sigmax)
        dummyPDFy = RooGaussian(name+'y',name+'y',yVar,meany,sigmay)

        dummyPDF = RooProdPdf(name,name,RooArgList(dummyPDFx,dummyPDFy))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),500)

        dummyRDH = RooDataHist('signal_main','signal_main',RooArgSet(xVar,yVar),dummyRDS)


    # Skewed gaussian up
    elif distEq == 'gaussUp':
        meanx = RooConstVar('meanx','meanx',17)
        sigmax = RooConstVar('sigmax','sigmax',2)
        tailx = RooConstVar('tailx','tailx',0.5)

        meany = RooConstVar('meany','meany',12)
        sigmay = RooConstVar('sigmay','sigmay',2)
        taily = RooConstVar('taily','taily',0.5)

        dummyPDFx = RooNovosibirsk(name+'x',name+'x',xVar,meanx,sigmax,tailx)
        dummyPDFy = RooNovosibirsk(name+'y',name+'y',yVar,meany,sigmay,taily)

        dummyPDF = RooProdPdf(name,name,RooArgList(dummyPDFx,dummyPDFy))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),500)

        dummyRDH = RooDataHist('signal_main_smearUp','signal_main_smearUp',RooArgSet(xVar,yVar),dummyRDS)

    # Skewed guassian down
    elif distEq == 'gaussDown':
        meanx = RooConstVar('meanx','meanx',12)
        sigmax = RooConstVar('sigmax','sigmax',2)
        tailx = RooConstVar('tailx','tailx',-0.5)

        meany = RooConstVar('meany','meany',8)
        sigmay = RooConstVar('sigmay','sigmay',2)
        taily = RooConstVar('taily','taily',-0.5)

        dummyPDFx = RooNovosibirsk(name+'x',name+'x',xVar,meanx,sigmax,tailx)
        dummyPDFy = RooNovosibirsk(name+'y',name+'y',yVar,meany,sigmay,taily)

        dummyPDF = RooProdPdf(name,name,RooArgList(dummyPDFx,dummyPDFy))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),500)

        dummyRDH = RooDataHist('signal_main_smearDown','signal_main_smearDown',RooArgSet(xVar,yVar),dummyRDS)

    # Generic
    else:
        dummyPDF = RooGenericPdf(name,distEq,RooArgList(xVar,yVar))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),50000) # output is a RooDataSet
        dummyRDH = RooDataHist(name+'_main',name+'_main',RooArgSet(xVar,yVar),dummyRDS)


    dummyTH2 = dummyRDS.createHistogram(xVar,yVar,35,25,'',name)

    if printOpt == True:
        print 'Check this is the shape you want for: ' + distEq
        dummyTH2.Draw('lego')
        raw_input('Hit enter to confirm this shape')

    return dummyRDS,dummyTH2,dummyRDH

if __name__ == '__main__':
    
    # Establish our axis variables
    xVar = RooRealVar('x','x',0,35)
    yVar = RooRealVar('y','y',0,25)

    # We need to make some dummy 2D histograms that we know the form of
    dataRDS,dataTH2,dataRDH = makeDummyFromPDF('data_obs','x*y',xVar,yVar,False)
    bkgRDS,bkgTH2,bkgRDH = makeDummyFromPDF('mybkg','x*y',xVar,yVar,False)
    signalRDS,signalTH2,signalRDH = makeDummyFromPDF('signal','gauss',xVar,yVar,False)
    signalUpRDS,signalUpTH2,signalUpRDH = makeDummyFromPDF('signalUp','gaussUp',xVar,yVar,False)
    signalDownRDS,signalDownTH2,signalDownRDH = makeDummyFromPDF('signalDown','gaussDown',xVar,yVar,False)

    # Print out the signals for later review
    totCan = TCanvas('totCan','totCan',1400,1000)
    totCan.Divide(3,2)
    totCan.cd(1)
    signalTH2.Draw('lego')
    totCan.cd(2)
    signalUpTH2.Draw('lego')
    totCan.cd(3)
    signalDownTH2.Draw('lego')
    totCan.cd(4)
    dataTH2.Draw('lego')
    totCan.cd(5)
    bkgTH2.Draw('lego')

    totCan.Print('SignalPlots.root','root')


    # Make workspace to save in
    myWorkspace = RooWorkspace('myW')
    for rdh in [xVar,dataRDH,bkgRDH,signalRDH,signalUpRDH,signalDownRDH]:
        getattr(myWorkspace,'import')(rdh)
    # Now save out the RooDataHists
    myWorkspace.writeToFile('base.root',True)    

