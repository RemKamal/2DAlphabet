import ROOT
from ROOT import *

# Grab and store your files - key names should match what you want combine to see
dictFiles = {
    'data_obs':         TFile.Open('rootfiles/TW2DalphabetQCD_Trigger_nominal_none_PSET_default.root'),
    'signalRH1200':     TFile.Open('rootfiles/TW2DalphabetweightedsignalRH1200_Trigger_nominal_none_PSET_default.root')
}

outfile = TFile('../Full2D_input.root','recreate')

# Need a dummy histogram to store sideband and signal bounds in TAxis
TH1_region_bounds = TH1F('TH1_region_bounds','TH1_region_bounds',1,150,190)
TH1_region_bounds.SetBinContent(1,20)   # This is a way to store the bin width of the x bins easily
TH1_region_bounds.Write()

# Loop through keys and pass and fail
for dataset in dictFiles.keys():
    for cat in ['Pass','Fail']:

        # Lower case cat
        lcat = cat.lower()

        # Grab the file
        thisFile = dictFiles[dataset]
        # Get and clone the pass/fail hist
        thisHist = thisFile.Get('MtwvMt'+cat).Clone()

        # Set names, titles, labels
        thisHist.SetName(dataset+'_'+lcat)
        thisHist.SetTitle(dataset+'_'+lcat)
        thisHist.GetXaxis().SetName('jetmass')
        thisHist.GetXaxis().SetTitle('jetmass')
        thisHist.GetYaxis().SetName('resmass')
        thisHist.GetYaxis().SetTitle('resmass')

        # Default 60 bins in Mt and 35 bins in Mtw
        thisHist.RebinX(6)

        # Write out
        outfile.cd()
        thisHist.Write()

        # If dealing with signal
        if dataset.find('signal') != -1:
            shapeUncerts = ['W']
            # Loop through shape uncertainties and do the same
            for u in shapeUncerts:
                thisHistUp = thisFile.Get('MtwvMt'+cat+u+'up').Clone()

                thisHistUp.SetName(dataset+'_'+lcat+'_'+u+'Up')
                thisHistUp.SetTitle(dataset+'_'+lcat+'_'+u+'Up')
                thisHistUp.GetXaxis().SetName('jetmass')
                thisHistUp.GetXaxis().SetTitle('jetmass')
                thisHistUp.GetYaxis().SetName('resmass')
                thisHistUp.GetYaxis().SetTitle('resmass')

                thisHistUp.RebinX(6)

                thisHistDown = thisFile.Get('MtwvMt'+cat+u+'down').Clone()

                thisHistDown.SetName(dataset+'_'+lcat+'_'+u+'Down')
                thisHistDown.SetTitle(dataset+'_'+lcat+'_'+u+'Down')
                thisHistDown.GetXaxis().SetName('jetmass')
                thisHistDown.GetXaxis().SetTitle('jetmass')
                thisHistDown.GetYaxis().SetName('resmass')
                thisHistDown.GetYaxis().SetTitle('resmass')

                thisHistDown.RebinX(6)

                outfile.cd()
                thisHistUp.Write()
                thisHistDown.Write()
