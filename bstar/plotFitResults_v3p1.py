import ROOT
from ROOT import *

gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)

# IMPLEMENTS METHOD TO BLIND BUT NOT ACTUALLY BLINDED
# NEED TO REMOVE REFERENCES TO RDH_dataPassFull and TH2_dataPassSig

if __name__ == '__main__':
    allVars = []

    #####################
    #   Get everything  #
    #####################

    # Open up our files and workspaces
    new_file = TFile.Open('MaxLikelihoodFitResult.root')
    new_w = new_file.Get('MaxLikelihoodFitResult')

    old_file = TFile.Open('base.root')      # Need to get the data_obs pass and fail
    old_w = old_file.Get('w_test')          # which is not stored in the output of Combine
                                            # (the sum of the two is stored there)

    # We'll also need at least one of the original TH2s to grab info like binning and var names
    ogFile = TFile.Open('Full2D_input.root')
    tempTH2 = ogFile.Get('data_obs_pass')


    # QCD shapes
    Pdf_QcdFailLow = new_w.pdf('shapeBkg_qcd_failLow')
    Pdf_QcdPassLow = new_w.pdf('shapeBkg_qcd_passLow')
    Pdf_QcdFailHigh = new_w.pdf('shapeBkg_qcd_failHigh')
    Pdf_QcdPassHigh = new_w.pdf('shapeBkg_qcd_passHigh')

    # PDFs
    norm_QcdFailLow = new_w.function('shapeBkg_qcd_failLow__norm')
    norm_QcdPassLow = new_w.function('shapeBkg_qcd_passLow__norm')
    norm_QcdFailHigh = new_w.function('shapeBkg_qcd_failHigh__norm')
    norm_QcdPassHigh = new_w.function('shapeBkg_qcd_passHigh__norm')

    # Data
    RDH_dataFailLow = old_w.data('data_obs_failLow')
    RDH_dataPassLow = old_w.data('data_obs_passLow')
    RDH_dataFailHigh = old_w.data('data_obs_failHigh')
    RDH_dataPassHigh = old_w.data('data_obs_passHigh')
    RDH_dataFailFull = old_w.data('data_obs_fail')          # Need this to reconstruct signal region
    RDH_dataPassFull = old_w.data('data_obs_pass') # Remove after testing

    allVars.extend([Pdf_QcdPassLow,Pdf_QcdFailLow,norm_QcdFailLow, norm_QcdPassLow, RDH_dataPassLow,RDH_dataFailLow])
    allVars.extend([Pdf_QcdPassHigh,Pdf_QcdFailHigh,norm_QcdFailHigh, norm_QcdPassHigh, RDH_dataPassHigh,RDH_dataFailHigh])

    # Vars
    xVar = old_w.var(tempTH2.GetXaxis().GetName())
    xVarLow = new_w.var(tempTH2.GetXaxis().GetName()+'_Low')
    xVarHigh = new_w.var(tempTH2.GetXaxis().GetName()+'_High')
    yVar = new_w.var(tempTH2.GetYaxis().GetName())

    # Python hack
    allVars.extend([xVar,xVarLow,xVarHigh,yVar])

    # Parameters of the fit (store them in python list immediately)
    RAS_rpfParams = new_w.allVars().selectByName('polyCoeff_x*y*',True)
    iter_params = RAS_rpfParams.createIterator()
    PolyCoeffs = {}
    RPV_par = iter_params.Next()
    while RPV_par:
        coeffName = RPV_par.GetName()[RPV_par.GetName().find('x'):] # returns "x#y#"
        PolyCoeffs[coeffName] = RPV_par
        print coeffName + ': ',
        RPV_par.Print()
        allVars.append(RPV_par)
        RPV_par = iter_params.Next()


    #########################
    #   Do some rebuilding  #
    #########################

    # Polynomial Order
    polXO = 0
    polYO = 0
    for param_name in PolyCoeffs.keys():
        # Assuming poly order is a single digit (pretty reasonable I think...)
        tempXorder = int(param_name[param_name.find('x')+1])
        tempYorder = int(param_name[param_name.find('y')+1])
        if tempXorder > polXO:
            polXO = tempXorder
        if tempYorder > polYO:
            polYO = tempYorder

    # Signal region bounds
    sigStart = ogFile.Get('TH1_region_bounds').GetBinLowEdge(1)
    sigEnd = sigStart + ogFile.Get('TH1_region_bounds').GetBinWidth(1)

    # X axis binning
    xlow = tempTH2.GetXaxis().GetXmin()
    xhigh = tempTH2.GetXaxis().GetXmax()
    xBinWidth = ogFile.Get('TH1_region_bounds').GetBinContent(1)            # Hardcoded
    xnbins = int(float(xhigh-xlow)/float(xBinWidth))            # Bins over full x axis
    xnbinsLow = int((sigStart-xlow)/xBinWidth)
    xnbinsHigh = int((xhigh-sigEnd)/xBinWidth)

    # Y axis binning
    ylow = tempTH2.GetYaxis().GetXmin()
    yhigh = tempTH2.GetYaxis().GetXmax()
    ynbins = tempTH2.GetNbinsY()




    #########################
    #   Start making stuff  #
    #########################

    # Should eventually make a loop through a dictionary for this 
    # It's repetitive and your eventually going to have to make more then two processes 

    # Create TH2s that span the full x-axis range from everything

    #
    # Data first
    #
    TH2_dataFailLow = RDH_dataFailLow.createHistogram('data_obsFailLow',xVarLow,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh)))
    TH2_dataPassLow = RDH_dataPassLow.createHistogram('data_obsPassLow',xVarLow,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh)))
    TH2_dataFailHigh = RDH_dataFailHigh.createHistogram('data_obsFailHigh',xVarHigh,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh)))
    TH2_dataPassHigh = RDH_dataPassHigh.createHistogram('data_obsPassHigh',xVarHigh,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh)))

    TH2_dataFailSig = RDH_dataFailFull.createHistogram('data_obsFailFull',xVar,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh)))
    TH2_dataPassSig = RDH_dataPassFull.createHistogram('data_obsPassFull',xVar,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh)))


    TH2_dataFail = TH2F('data_obsFail','data_obsFail',xnbins,xlow,xhigh,ynbins,ylow,yhigh)
    TH2_dataPass = TH2F('data_obsPass','data_obsPass',xnbins,xlow,xhigh,ynbins,ylow,yhigh)

    TH2_dataFail.Add(TH2_dataFailLow)
    TH2_dataFail.Add(TH2_dataFailHigh)
    TH2_dataPass.Add(TH2_dataPassLow)
    TH2_dataPass.Add(TH2_dataPassHigh)

    #
    # Rp/f - Transfer Function
    #

    # Rebuild the RooPolyVar (can't just grab since we have one in each bin stored! Need something over whole space)
    xPolyList = RooArgList()
    for yCoeff in range(polYO+1):
        xCoeffList = RooArgList()

        # Get each x coefficient for this y
        for xCoeff in range(polXO+1):                    
            xCoeffList.add(PolyCoeffs['x'+str(xCoeff)+'y'+str(yCoeff)])

        # Make the RooPolyVar in x and save it to the list of x polynomials
        thisXPolyVarLabel = "xPol_y_"+str(yCoeff)
        xPolyVar = RooPolyVar(thisXPolyVarLabel,thisXPolyVarLabel,xVar,xCoeffList)
        xPolyList.add(xPolyVar)
        allVars.append(xPolyVar)

    # Now make a RooPolyVar out of the x polynomials
    RPV_rpf_func = RooPolyVar("FullPol","FullPol",yVar,xPolyList)
    allVars.append(RPV_rpf_func)

    # And make a histogram from that
    # VERY IMPORTANT NOTE: You need to call RooFit.Scaling(False) here otherwise it will scale each bin by the xBinWidth*yBinWidth and you'll get huge values
    TH2_rpf_func = RPV_rpf_func.createHistogram("Rpf_func",xVar,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh)),RooFit.Scaling(False)) # VERY IMPORTANT NOTE: You need to cal
    print TH2_rpf_func.Integral()

    # And finally get the true Rpf
    TH2_rpf_true = TH2_dataPassSig.Clone()
    TH2_rpf_true.Divide(TH2_dataFailSig)


    #
    # QCD estimate (this is more complicated because of the pdfs)
    #
    dict_Qcd = {} # Initializing storage unit

    for reg in ['fail','pass']:
        # When we do this, it make the hist over the full x-axis range (even though the PDFs are subsets)
        # We need to do this to get the normalized PDF values in the bins of interest - the others won't be save to the final 'full' histogram that combines low and high
        TH2_QcdSig = TH2_dataFailSig.Clone("qcd_passSig")
        TH2_QcdSig.Multiply(TH2_rpf_func)

        # Scale the PDF hists
        if reg == 'fail':
            TH2_QcdLow = Pdf_QcdFailLow.createHistogram("qcd_"+reg+"Low",xVarLow,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh))) 
            TH2_QcdHigh = Pdf_QcdFailHigh.createHistogram("qcd_"+reg+"High",xVarHigh,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh))) 

            TH2_QcdLow.Scale(norm_QcdFailLow.getValV())
            TH2_QcdHigh.Scale(norm_QcdFailHigh.getValV())

        elif reg == 'pass':
            TH2_QcdLow = Pdf_QcdPassLow.createHistogram("qcd_"+reg+"Low",xVarLow,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh))) 
            TH2_QcdHigh = Pdf_QcdPassHigh.createHistogram("qcd_"+reg+"High",xVarHigh,RooFit.Binning(xnbins,xlow,xhigh),RooFit.YVar(yVar,RooFit.Binning(ynbins,ylow,yhigh))) 

            TH2_QcdLow.Scale(norm_QcdPassLow.getValV())
            TH2_QcdHigh.Scale(norm_QcdPassHigh.getValV())

        print TH2_QcdLow.GetBinContent(1,4)

        # Now we need to take the relevant bins of each low and high and save them in two final histograms - one with an estimate in signal and one without
        TH2_Qcd = TH2F('qcd_'+reg,'qcd_'+reg,xnbins,xlow,xhigh,ynbins,ylow,yhigh)
        TH2_Qcd_blind = TH2F('qcd_'+reg+'_blind','qcd_'+reg+'_blind',xnbins,xlow,xhigh,ynbins,ylow,yhigh)

        # Check we've got the same binning just in case
        if TH2_QcdLow.GetNbinsY() != TH2_Qcd.GetNbinsY() or TH2_QcdLow.GetNbinsX() != TH2_Qcd.GetNbinsX():
            print 'Warning binning does not match'
            quit()

        for ybin in range(1,ynbins):
            # First low
            for lowxbin in range(1,xnbinsLow+1):
                TH2_Qcd.SetBinContent(lowxbin,ybin,TH2_QcdLow.GetBinContent(lowxbin,ybin))
                TH2_Qcd_blind.SetBinContent(lowxbin,ybin,TH2_QcdLow.GetBinContent(lowxbin,ybin))

            # Make the estimate in signal region if necessary
            for sigxbin in range(xnbinsLow+1, xnbins - xnbinsHigh+1):
                if reg == 'pass':
                    TH2_Qcd.SetBinContent(sigxbin,ybin,TH2_QcdSig.GetBinContent(sigxbin,ybin))
                elif reg == 'fail':
                    TH2_Qcd.SetBinContent(sigxbin,ybin,TH2_dataFailSig.GetBinContent(sigxbin,ybin))

            # Then high
            for highxbin in range(xnbins - xnbinsHigh + 1,xnbins+1):
                TH2_Qcd.SetBinContent(highxbin,ybin,TH2_QcdHigh.GetBinContent(highxbin,ybin))
                TH2_Qcd_blind.SetBinContent(highxbin,ybin,TH2_QcdHigh.GetBinContent(highxbin,ybin))

        dict_Qcd[reg] = {'qcd':TH2_Qcd, 'qcd_blind':TH2_Qcd_blind}


    TH2_QcdFail = dict_Qcd['fail']['qcd']
    TH2_QcdPass = dict_Qcd['pass']['qcd']

    #################
    #   Plotting    #
    #################

    # Now make some pull surfaces
    pull_Data_Bkg_Fail = TH2_dataFailSig.Clone('pull_Data_Bkg_Fail')
    pull_Data_Bkg_Pass = TH2_dataPassSig.Clone('pull_Data_Bkg_Pass')
    pull_RpfTrue_RpfFunc = TH2_rpf_true.Clone('pull_RpfTrue_RpfFunc')

    pull_Data_Bkg_Fail.Add(TH2_QcdFail,-1)
    pull_Data_Bkg_Pass.Add(TH2_QcdPass,-1)
    pull_RpfTrue_RpfFunc.Add(TH2_rpf_func,-1)

    # And make some ratios
    ratio_Data_Bkg_Fail = TH2_dataFailSig.Clone('ratio_Data_Bkg_Fail')
    ratio_Data_Bkg_Pass = TH2_dataPassSig.Clone('ratio_Data_Bkg_Pass')
    ratio_RpfTrue_RpfFunc = TH2_rpf_true.Clone('ratio_RpfTrue_RpfFunc')

    ratio_Data_Bkg_Fail.Divide(TH2_QcdFail)
    ratio_Data_Bkg_Pass.Divide(TH2_QcdPass)
    ratio_RpfTrue_RpfFunc.Divide(TH2_rpf_func)

    # And some projections onto Mtw
    TH1_QcdPass = TH2_QcdPass.ProjectionY()
    TH1_dataPass = TH2_dataPassSig.ProjectionY()
    TH1_QcdFail = TH2_QcdFail.ProjectionY()
    TH1_dataFail = TH2_dataFailSig.ProjectionY()


    #####################################
    #   Do some naming and labeling     #
    #####################################

    TH2_QcdFail.SetTitle('Background estimate : Fail')
    TH2_QcdPass.SetTitle('Background estimate : Pass')
    TH2_dataFailSig.SetTitle('Data : Fail')
    TH2_dataPass.SetTitle('Data : Pass')

    pull_Data_Bkg_Pass.SetTitle('Data-Bkg Pass')
    pull_Data_Bkg_Fail.SetTitle('Data-Bkg Fail')
    pull_RpfTrue_RpfFunc.SetTitle('True Rp/f minus Fitted Rp/f')

    ratio_Data_Bkg_Pass.SetTitle('Data/Bkg Pass')
    ratio_Data_Bkg_Fail.SetTitle('Data/Bkg Fail')
    ratio_RpfTrue_RpfFunc.SetTitle('True Rp/f over Fitted Rp/f')

    TH2_rpf_true.SetTitle('True R_{P/F} (Data_{pass}/Data_{fail})')
    TH2_rpf_func.SetTitle('Fitted R_{P/F} (from Combine)')

    TH2_rpf_true.RebinY(3)

    #####################################
    #   Save out the interesting stuff  #
    #####################################

    # Print our four 2D distributions (data, bkg, pass, fail)
    DataVBkgCan = TCanvas('DataVBkgCan','DataVBkgCan',1200,1000)
    DataVBkgCan.Divide(2,2)
    DataVBkgCan.cd(1)
    TH2_dataPass.Draw('lego')
    DataVBkgCan.cd(2)
    TH2_dataFailSig.Draw('lego')
    DataVBkgCan.cd(3)
    TH2_QcdPass.Draw('lego')
    DataVBkgCan.cd(4)
    TH2_QcdFail.Draw('lego')


    DataVBkgCan.Print('Plots/Full2Dv3p1_DataVsBkg_results.pdf','pdf')
    DataVBkgCan.Print('Plots/Full2Dv3p1_DataVsBkg_results.root','root')


    # # Print our pulls
    # PullCan = TCanvas('PullCan','PullCan',1800,800)
    # PullCan.Divide(3,1)
    # PullCan.cd(1)
    # pull_Data_Bkg_Fail.Draw('surf')
    # PullCan.cd(2)
    # pull_Data_Bkg_Pass.Draw('surf')
    # PullCan.cd(3)
    # pull_RpfTrue_RpfFunc.Draw('surf')

    # PullCan.Print('Plots/Full2Dv3p1_pull_results.pdf','pdf')
    # PullCan.Print('Plots/Full2Dv3p1_pull_results.root','root')


    # # Print our ratios
    # ratioCan = TCanvas('ratioCan','ratioCan',1800,800)
    # ratioCan.Divide(3,1)
    # ratioCan.cd(1)
    # ratio_Data_Bkg_Fail.Draw('surf')
    # ratioCan.cd(2)
    # ratio_Data_Bkg_Pass.Draw('surf')
    # ratioCan.cd(3)
    # ratio_RpfTrue_RpfFunc.Draw('surf')

    # ratioCan.Print('Plots/Full2Dv3p1_ratio_results.pdf','pdf')
    # ratioCan.Print('Plots/Full2Dv3p1_ratio_results.root','root')


    # Print real and derived Rp/fs
    RpfsCan = TCanvas('RpfsCan','RpfsCan',1800,800)
    RpfsCan.Divide(2,1)
    RpfsCan.cd(1)
    TH2_rpf_true.Draw('lego')
    RpfsCan.cd(2)
    TH2_rpf_func.Draw('surf')

    RpfsCan.Print('Plots/Full2Dv3p1_rpfs.pdf','pdf')
    RpfsCan.Print('Plots/Full2Dv3p1_rpfs.root','root')

    # Print projections (same histo)
    MtwSpace = TCanvas('MtwSpace','MtwSpace',1400,800)
    MtwLegPass = TLegend(0.6,0.75,0.95,0.90)
    MtwLegFail = TLegend(0.6,0.75,0.95,0.90)
    MtwSpace.Divide(2,1)

    MtwSpace.cd(1)
    TH1_QcdPass.SetLineColor(kRed)
    TH1_QcdPass.SetTitle('Data vs Bkg Pass projected onto M_{tw}')
    TH1_QcdPass.Draw('hist e')
    TH1_dataPass.Draw('same hist e')
    MtwLegPass.AddEntry(TH1_QcdPass,'estimate pass','l')
    MtwLegPass.AddEntry(TH1_dataPass,'data pass','l')
    MtwLegPass.Draw()

    MtwSpace.cd(2)
    TH1_QcdFail.SetLineColor(kRed)
    TH1_QcdFail.SetTitle('Data vs Bkg Fail projected onto M_{tw}')
    TH1_QcdFail.Draw('hist e')
    TH1_dataFail.Draw('same hist e')
    MtwLegFail.AddEntry(TH1_QcdFail,'estimate fail','l')
    MtwLegFail.AddEntry(TH1_dataFail,'data fail','l')
    MtwLegFail.Draw()

    MtwSpace.Print('Plots/Full2Dv3p1_mtw.pdf','pdf')

    # And the logy versions
    MtwSpaceLog = TCanvas('MtwSpaceLog','MtwSpaceLog',1400,800)
    MtwSpaceLog.Divide(2,1)

    MtwSpaceLog.cd(1)
    MtwSpaceLog_1.SetLogy()
    TH1_QcdPass.Draw('hist e')
    TH1_dataPass.Draw('same hist e')
    MtwLegPass.Draw()
    MtwSpaceLog.cd(2)
    MtwSpaceLog_2.SetLogy()
    TH1_QcdFail.Draw('hist e')
    TH1_dataFail.Draw('same hist e')
    MtwLegFail.Draw()

    MtwSpaceLog.Print('Plots/Full2Dv3p1_mtw_semilog.pdf','pdf')

