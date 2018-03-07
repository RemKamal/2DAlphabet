import ROOT
from ROOT import *
import os
gROOT.Macro(os.path.expanduser('~/rootlogon.C'))
#################################################################
# This script is to do 2D Alphabet in Combine with dummy shapes.#
# The proceedure is as follows:                                 #
# - Generate data_obs and signal from pdfs (no bkg - pretend    #
#   we're using QCD MC) for both pass and fail distributions    #
#   --- signal should not really exist in fail                  #
#   --- generate bkg fail and data fail from same PDF           #
# - Turn bkg fail into RPH2D                                    #
#   --- Make a RooRealVar for each bin of background            #
#   --- Store them in RooArgList and make RPH2D                 #
#   --- Make a _norm RooRealVar for the RPH2D                   #
# - Create a RooPolyVar as the transfer function                #
#   --- You should know the shape of this based on the PDFs     #
#       used to generate the data pass an fail                  #
# - Create the bkg pass from TF*bkg_fail                        #
# These will then be fed into Combine which will do a bump hunt #
#################################################################

def makeDummyFromPDF(name,distEq,cat,xVar,yVar,printOpt=True):
    # Gaussian
    if distEq == 'gauss':
        meanx = RooConstVar('meanx','meanx',5)
        sigmax = RooConstVar('sigmax','sigmax',1)

        meany = RooConstVar('meany','meany',2.5)
        sigmay = RooConstVar('sigmay','sigmay',0.5)

        dummyPDFx = RooGaussian(name+'x',name+'x',xVar,meanx,sigmax)
        dummyPDFy = RooGaussian(name+'y',name+'y',yVar,meany,sigmay)

        dummyPDF = RooProdPdf(name,name,RooArgList(dummyPDFx,dummyPDFy))

        if cat == 'pass':
            dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),100)
        elif cat == 'fail':
            dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),10)

        dummyRDH = RooDataHist('signal_'+cat,'signal_'+cat,RooArgSet(xVar,yVar),dummyRDS)

        

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
        if cat == 'pass':
            dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),100)
        elif cat == 'fail':
            dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),10)

        dummyRDH = RooDataHist('signal_'+cat+'_smearUp','signal_'+cat+'_smearUp',RooArgSet(xVar,yVar),dummyRDS)

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
        if cat == 'pass':
            dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),100)
        elif cat == 'fail':
            dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),10)

        dummyRDH = RooDataHist('signal_'+cat+'_smearDown','signal_'+cat+'_smearDown',RooArgSet(xVar,yVar),dummyRDS)

    # Generic
    else:
        dummyPDF = RooGenericPdf(name,distEq,RooArgList(xVar,yVar))
        dummyRDS = dummyPDF.generate(RooArgSet(xVar,yVar),50000) # output is a RooDataSet
        dummyRDH = RooDataHist(name+'_'+cat,name+'_'+cat,RooArgSet(xVar,yVar),dummyRDS)


    dummyTH2 = dummyRDS.createHistogram(xVar,yVar,10,5,'',name)

    if printOpt == True:
        print 'Check this is the shape you want for: ' + distEq
        dummyTH2.Draw('lego')
        raw_input('Hit enter to confirm this shape')

    return dummyTH2, dummyRDH


if __name__ == '__main__':
    

    allVars = []

    # Establish our axis variables
    xVar = RooRealVar('myx','myx',0,10)
    yVar = RooRealVar('myy','myy',0,5)


    # We need to make some dummy 2D histograms that we know the form of
    # pass = x^3*y^2, fail = x*y, Rp/f = (ax^2+bx+c)(dy+f) where a*d=1, b=c=f=0
    data_pass_TH2,data_pass_RDH = makeDummyFromPDF('data_obs','(myx**3)*(myy**2)','pass',xVar,yVar,False)
    print 'data pass entries: '+str(data_pass_TH2.GetEntries())
    # bkg_pass_TH2,bkg_pass_RDH = makeDummyFromPDF('mybkg','myx*myy','pass',xVar,yVar,False)
    signal_pass_TH2,signal_pass_RDH = makeDummyFromPDF('signal','gauss','pass',xVar,yVar,False)
    signalUp_pass_TH2,signalUp_pass_RDH = makeDummyFromPDF('signalUp','gaussUp','pass',xVar,yVar,False)
    signalDown_pass_TH2,signalDown_pass_RDH = makeDummyFromPDF('signalDown','gaussDown','pass',xVar,yVar,False)

    data_fail_TH2,data_fail_RDH = makeDummyFromPDF('data_obs','myx*myy','fail',xVar,yVar,False)
    print 'data fail entries: '+str(data_fail_TH2.GetEntries())
    # bkg_fail_TH2,bkg_fail_RDH = makeDummyFromPDF('mybkg','myx*myy','fail',xVar,yVar,False)
    signal_fail_TH2,signal_fail_RDH = makeDummyFromPDF('signal','gauss','fail',xVar,yVar,False)
    signalUp_fail_TH2,signalUp_fail_RDH = makeDummyFromPDF('signalUp','gaussUp','fail',xVar,yVar,False)
    signalDown_fail_TH2,signalDown_fail_RDH = makeDummyFromPDF('signalDown','gaussDown','fail',xVar,yVar,False)

    # testCan = TCanvas('testCan','testCan',1700,700)
    # testCan.Divide(3,1)
    # testCan.cd(1)
    # data_pass_TH2.Draw('lego')
    # testCan.cd(2)
    # data_fail_TH2.Draw('lego')
    # rpf = data_pass_TH2.Clone()
    # rpf.Divide(data_fail_TH2)
    # testCan.cd(3)
    # rpf.Draw('lego')

    # testCan.Print('passfailrpf.root','root')


    # Get some starting guess values for the coefficients of the Rp/f (po1 vs pol2)
    myguesses = {
        "nom":[
            [0.0,0.0],     # nominal, x0 [y0,y1]
            [0.0,0.0],     # nominal, x1
            [0.0,0.001]      # nominal, x2
        ],
        "up":[
            [0.1,0.1],
            [0.1,0.1],
            [0.1,3.]
        ],
        "down":[
            [-0.1,-0.1],
            [-0.1,-0.1],
            [-0.1,0.0]
        ]
    }

    # Store the guesses as RRVs in an easy-to-access dictionary
    polYO = 1
    polXO = 2
    PolyCoeffs = {}
    for yi in range(polYO+1):
        thisXCoeffList = RooArgList()
        for xi in range(polXO+1):
            name = 'polyCoeff_'+'x'+str(xi)+'y'+str(yi)
            PolyCoeffs['x'+str(xi)+'y'+str(yi)] = RooRealVar(name,name,myguesses['nom'][xi][yi],myguesses['down'][xi][yi],myguesses['up'][xi][yi])
            allVars.append(PolyCoeffs['x'+str(xi)+'y'+str(yi)])

    # Now loop through all of our bins
    binListFail = RooArgList()
    binListPass = RooArgList()
    for ybin in range(1,data_fail_TH2.GetYaxis().GetNbins()+1):
        for xbin in range(1,data_fail_TH2.GetXaxis().GetNbins()+1):

            # First make our fail bins into RRVs
            name = 'Fail_bin_'+str(xbin)+'-'+str(ybin)
            binContent = data_fail_TH2.GetBinContent(xbin,ybin)
            binErrUp = binContent + data_fail_TH2.GetBinErrorUp(xbin,ybin)
            binErrDown = binContent - data_fail_TH2.GetBinErrorLow(xbin,ybin)
            binRRV = RooRealVar(name, name, binContent, max(binErrDown,0), max(binErrUp,0))
            # Store the bin
            binListFail.add(binRRV)
            allVars.append(binRRV)

            # Then get bin center and save
            xCenter = data_fail_TH2.GetXaxis().GetBinCenter(xbin)
            yCenter = data_fail_TH2.GetYaxis().GetBinCenter(ybin)

            xConst = RooConstVar("ConstVar_x_"+str(xbin)+'_'+str(ybin),"ConstVar_x_"+str(xbin)+'_'+str(ybin),xCenter)
            yConst = RooConstVar("ConstVar_y_"+str(xbin)+'_'+str(ybin),"ConstVar_y_"+str(xbin)+'_'+str(ybin),yCenter)

            allVars.append(xConst)
            allVars.append(yConst)

            # And now make a polynomial for this bin
            xPolyList = RooArgList()
            for yCoeff in range(polYO+1):
                xCoeffList = RooArgList()

                # Get each x coefficient for this y
                for xCoeff in range(polXO+1):                    
                    xCoeffList.add(PolyCoeffs['x'+str(xCoeff)+'y'+str(yCoeff)])

                # Make the polynomial and save it to the list of x polynomials
                thisXPolyVarLabel = "xPol_y_"+str(yCoeff)+"_Bin_"+str(int(xbin))+"_"+str(int(ybin))
                xPolyVar = RooPolyVar(thisXPolyVarLabel,thisXPolyVarLabel,xConst,xCoeffList)
                xPolyList.add(xPolyVar)
                allVars.append(xPolyVar)

            # Now make a polynomial out of the x polynomials
            thisYPolyVarLabel = "FullPol_Bin_"+str(int(xbin))+"_"+str(int(ybin))
            thisFullPolyVar = RooPolyVar(thisYPolyVarLabel,thisYPolyVarLabel,yConst,xPolyList)

            allVars.append(thisFullPolyVar)


            # Finally make the pass distribution
            formulaArgList = RooArgList(binRRV,thisFullPolyVar)
            thisBinPass = RooFormulaVar('Pass_bin_'+str(xbin)+'-'+str(ybin),'Pass_bin_'+str(xbin)+'-'+str(ybin),"@0*@1",formulaArgList)
            binListPass.add(thisBinPass)
            allVars.append(thisBinPass)


    print "Making RPH2Ds"
    qcd_fail_RPH2D = RooParametricHist2D('qcd_fail','qcd_fail',xVar, yVar, binListFail, data_fail_TH2)
    qcd_pass_RPH2D = RooParametricHist2D('qcd_pass','qcd_pass',xVar, yVar, binListPass, data_fail_TH2)
    print "Making norm"
    qcd_fail_RPH2D_norm = RooAddition('qcd_fail_norm','qcd_fail_norm',binListFail)
    qcd_pass_RPH2D_norm = RooAddition('qcd_pass_norm','qcd_pass_norm',binListPass)

    things2import = [
        data_pass_RDH,
        data_fail_RDH,
        qcd_fail_RPH2D,
        qcd_pass_RPH2D,
        qcd_fail_RPH2D_norm,
        qcd_pass_RPH2D_norm,
        signal_pass_RDH,
        signal_fail_RDH,
        signalUp_pass_RDH,
        signalUp_fail_RDH,
        signalDown_pass_RDH,
        signalDown_fail_RDH
    ]


    print "Making workspace..."
    # Make workspace to save in
    myWorkspace = RooWorkspace("w_test")
    for rdh in things2import:
        print "Importing " + rdh.GetName()
        getattr(myWorkspace,'import')(rdh,RooFit.RecycleConflictNodes())

    # Now save out the RooDataHists
    myWorkspace.writeToFile('base.root',True)  

    
