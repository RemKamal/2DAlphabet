import ROOT
from ROOT import *

#################################################################
# This script is to full test the 2D RDHs in Combine.           #
# The proceedure is as follows:                                 #
# - Generate data_obs, signal, and background from pdfs         #
# - Make a RooRealVar for each bin of background                #
# - Store them in RooArgList and make RPH2D                     #
# - Make a _norm RooRealVar for the RPH2D                       #
# These will then be fed into Combine which will do a bump hunt #
#################################################################

def makeDummyFromPDF(name,distEq,xVar,yVar,printOpt=True):
    # Gaussian
    if distEq == 'gauss':
        meanx = RooConstVar('meanx','meanx',5)
        sigmax = RooConstVar('sigmax','sigmax',1)

        meany = RooConstVar('meany','meany',2.5)
        sigmay = RooConstVar('sigmay','sigmay',0.5)

        dummyPDFx = RooGaussian(name+'x',name+'x',xVar,meanx,sigmax)
        dummyPDFy = RooGaussian(name+'y',name+'y',yVar,meany,sigmay)

        dummyPDF = RooProdPdf(name,name,RooArgList(dummyPDFx,dummyPDFy))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),500)

        dummyRDH = RooDataHist('signal_main','signal_main',RooArgSet(xVar,yVar),dummyRDS)


    # Skewed gaussian up
    elif distEq == 'gaussUp':
        meanx = RooConstVar('meanx','meanx',6)
        sigmax = RooConstVar('sigmax','sigmax',1)
        tailx = RooConstVar('tailx','tailx',0.5)

        meany = RooConstVar('meany','meany',3)
        sigmay = RooConstVar('sigmay','sigmay',0.5)
        taily = RooConstVar('taily','taily',0.5)

        dummyPDFx = RooNovosibirsk(name+'x',name+'x',xVar,meanx,sigmax,tailx)
        dummyPDFy = RooNovosibirsk(name+'y',name+'y',yVar,meany,sigmay,taily)

        dummyPDF = RooProdPdf(name,name,RooArgList(dummyPDFx,dummyPDFy))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),500)

        dummyRDH = RooDataHist('signal_main_smearUp','signal_main_smearUp',RooArgSet(xVar,yVar),dummyRDS)

    # Skewed guassian down
    elif distEq == 'gaussDown':
        meanx = RooConstVar('meanx','meanx',4)
        sigmax = RooConstVar('sigmax','sigmax',1)
        tailx = RooConstVar('tailx','tailx',-0.5)

        meany = RooConstVar('meany','meany',2)
        sigmay = RooConstVar('sigmay','sigmay',0.5)
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


    dummyTH2 = dummyRDS.createHistogram(xVar,yVar,10,5,'',name)

    if printOpt == True:
        print 'Check this is the shape you want for: ' + distEq
        dummyTH2.Draw('lego')
        raw_input('Hit enter to confirm this shape')

    return dummyRDS, dummyTH2, dummyRDH

# def makeRPH2D(thisTH2,name):
#     dumbList = []
#     binList = RooArgList()
#     for ybin in range(1,thisTH2.GetYaxis().GetNbins()+1):
#         for xbin in range(1,thisTH2.GetXaxis().GetNbins()+1):
#             name = str(name)+'_binVar_'+str(xbin)+'-'+str(ybin)
#             title = str(name)+'_binVar_'+str(xbin)+'-'+str(ybin)
#             binContent = thisTH2.GetBinContent(xbin,ybin)
#             binErrUp = binContent + thisTH2.GetBinErrorUp(xbin,ybin)
#             binErrDown = binContent - thisTH2.GetBinErrorLow(xbin,ybin)
#             # print name + ', ' + title + ', ' + str(binContent) + ', ' + str(binErrDown) + ', ' + str(binErrUp)
#             binRRV = RooRealVar(name, title, binContent, max(binErrDown,0), max(binErrUp,0))
            
#             dumbList.append(binRRV)

#     for item in dumbList:
#         binList.add(item)

#     print "Making RPH2D"
#     final = RooParametricHist2D('mybkg','mybkg',xVar, yVar, binList, thisTH2)
#     print "Making norm"
#     norm = RooAddition('mybkg_norm','mybkg_norm',binList)
#     print "Done"

#     return final, norm


# def makeRPH1D(thisTH2,thisname):
#     dumbList = []
#     binList = RooArgList()
#     for xbin in range(1,thisTH2.GetNbinsX()+1):
#         name = str(thisname)+'_binVar_'+str(xbin)
#         title = str(thisname)+'_binVar_'+str(xbin)
#         binContent = thisTH2.GetBinContent(xbin)
#         binErrUp = binContent + thisTH2.GetBinErrorUp(xbin)
#         binErrDown = binContent - thisTH2.GetBinErrorLow(xbin)
#         # print name + ', ' + title + ', ' + str(binContent) + ', ' + str(binErrDown) + ', ' + str(binErrUp)
#         binRRV = RooRealVar(name, title, binContent, max(binErrDown,0), max(binErrUp,0))
        
#         dumbList.append(binRRV)

#     for item in dumbList:
#         binList.add(item)

#     # binList.Print()

#     print "Making RPH2D"
#     final = RooParametricHist('mybkg_main','mybkg_main',xVar, binList, thisTH2)
#     print "Making norm"
#     norm = RooAddition('mybkg_main_norm','mybkg_main_norm',binList)
#     print "Done"

#     return final, norm


if __name__ == '__main__':
    
    # Establish our axis variables
    xVar = RooRealVar('myx','myx',0,10)
    yVar = RooRealVar('myy','myy',0,5)


    # We need to make some dummy 2D histograms that we know the form of
    dataRDS,dataTH2,dataRDH = makeDummyFromPDF('data_obs','myx*myy',xVar,yVar,False)
    bkgRDS,bkgTH2,bkgRDH = makeDummyFromPDF('mybkg','myx*myy',xVar,yVar,False)
    signalRDS,signalTH2,signalRDH = makeDummyFromPDF('signal','gauss',xVar,yVar,False)
    signalUpRDS,signalUpTH2,signalUpRDH = makeDummyFromPDF('signalUp','gaussUp',xVar,yVar,False)
    signalDownRDS,signalDownTH2,signalDownRDH = makeDummyFromPDF('signalDown','gaussDown',xVar,yVar,False)



    # Make the background into a RooParametricHist2D
    dumbList = []
    binList = RooArgList()
    print "Type of bkgTH2 " +str(type(bkgTH2))

    for ybin in range(1,bkgTH2.GetYaxis().GetNbins()+1):
        for xbin in range(1,bkgTH2.GetXaxis().GetNbins()+1):
            name = 'mybkg_binVar_'+str(xbin)+'-'+str(ybin)
            title = 'mybkg_binVar_'+str(xbin)+'-'+str(ybin)
            binContent = bkgTH2.GetBinContent(xbin,ybin)
            binErrUp = binContent + bkgTH2.GetBinErrorUp(xbin,ybin)
            binErrDown = binContent - bkgTH2.GetBinErrorLow(xbin,ybin)
            # print name + ', ' + title + ', ' + str(binContent) + ', ' + str(binErrDown) + ', ' + str(binErrUp)
            binRRV = RooRealVar(name, title, binContent, max(binErrDown,0), max(binErrUp,0))
            
            dumbList.append(binRRV)

    for item in dumbList:
        binList.add(item)

    print "Making RPH2D"
    bkgRPH2D = RooParametricHist2D('mybkg_main','mybkg_main',xVar, yVar, binList, bkgTH2)
    print "Making norm"
    bkgRPH2D_norm = RooAddition('mybkg_main_norm','mybkg_main_norm',binList)




    print "Making workspace..."
    # Make workspace to save in
    myWorkspace = RooWorkspace("w_test")
    for rdh in [xVar,yVar,bkgRPH2D,bkgRPH2D_norm,dataRDH,signalRDH,signalUpRDH,signalDownRDH]:
        print "Importing " + rdh.GetName()
        getattr(myWorkspace,'import')(rdh,RooFit.RecycleConflictNodes())

    # Now save out the RooDataHists
    myWorkspace.writeToFile('base.root',True)  

