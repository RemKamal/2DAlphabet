import ROOT
from ROOT import *

gROOT.SetBatch(kTRUE)

allVars = []

#####################
#	Get everything	#
#####################

# Open up our files and workspaces
new_file = TFile.Open('MaxLikelihoodFitResult.root')
new_w = new_file.Get('MaxLikelihoodFitResult')

old_file = TFile.Open('base.root')		# Need to get the data_obs pass and fail
old_w = old_file.Get('w_test')			# which is not stored in the output of Combine
										# (the sum of the two is stored there)

# Get the QCD shapes
Pdf_QcdFail = new_w.pdf('shapeBkg_qcd_fail')
Pdf_QcdPass = new_w.pdf('shapeBkg_qcd_pass')

# Get scales of PDFS
norm_QcdFail = new_w.function('shapeBkg_qcd_fail__norm')
norm_QcdPass = new_w.function('shapeBkg_qcd_pass__norm')

# and the data
RDH_dataFail = old_w.data('data_obs_fail')
RDH_dataPass = old_w.data('data_obs_pass')

# and the vars
xVar = new_w.var('myx')
yVar = new_w.var('myy')

# and the parameters of the fit (store them in python list immediately)
RAS_rpfParams = new_w.allVars().selectByName('polyCoeff_x*y*',True)
iter_params = RAS_rpfParams.createIterator()
PolyCoeffs = {}
RPV_par = iter_params.Next()
while RPV_par:
	coeffName = RPV_par.GetName()[RPV_par.GetName().find('x'):] # retruns "x#y#"
	PolyCoeffs[coeffName] = RPV_par
	allVars.append(RPV_par)
	RPV_par = iter_params.Next()


# While we're here, let's figure out the order of our polynomials
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

print "Order of polynomial is x" + str(polXO) + "y" + str(polYO)

# Python hack
allVars.extend([Pdf_QcdPass,Pdf_QcdFail,norm_QcdFail, norm_QcdPass, RDH_dataPass,RDH_dataFail,xVar,yVar])


#########################
#	Start making stuff	#
#########################

# Create TH2s from everything
TH2_dataFail = RDH_dataFail.createHistogram('data_obsFail',xVar,RooFit.Binning(10,0,10),RooFit.YVar(yVar,RooFit.Binning(5,0,5)))
TH2_dataPass = RDH_dataPass.createHistogram('data_obsPass',xVar,RooFit.Binning(10,0,10),RooFit.YVar(yVar,RooFit.Binning(5,0,5)))

TH2_QcdFail = Pdf_QcdFail.createHistogram("qcd_fail",xVar,RooFit.Binning(10,0,10),RooFit.YVar(yVar,RooFit.Binning(5,0,5))) 
TH2_QcdPass = Pdf_QcdPass.createHistogram("qcd_pass",xVar,RooFit.Binning(10,0,10),RooFit.YVar(yVar,RooFit.Binning(5,0,5))) # Get plotting warnings here - doesn't seem to make a difference
# Scale the PDF hists
TH2_QcdFail.Scale(norm_QcdFail.getValV())
TH2_QcdPass.Scale(norm_QcdPass.getValV())

# Rebuild the RooPolyVar (can't just grab since we have one in each bin stored! Need something over whole space)
# And now make a polynomial for this bin
xPolyList = RooArgList()
for yCoeff in range(polYO+1):
    xCoeffList = RooArgList()

    # Get each x coefficient for this y
    for xCoeff in range(polXO+1):                    
        xCoeffList.add(PolyCoeffs['x'+str(xCoeff)+'y'+str(yCoeff)])

    # Make the polynomial and save it to the list of x polynomials
    thisXPolyVarLabel = "xPol_y_"+str(yCoeff)
    xPolyVar = RooPolyVar(thisXPolyVarLabel,thisXPolyVarLabel,xVar,xCoeffList)
    xPolyList.add(xPolyVar)
    allVars.append(xPolyVar)

# Now make a polynomial out of the x polynomials
RPV_rpf_func = RooPolyVar("FullPol","FullPol",yVar,xPolyList)
allVars.append(RPV_rpf_func)

# And make a histogram from that
TH2_rpf_func = RPV_rpf_func.createHistogram("Rpf_func",xVar,RooFit.Binning(10,0,10),RooFit.YVar(yVar,RooFit.Binning(5,0,5))) 

# And finally get the true Rpf
TH2_rpf_true = TH2_dataPass.Clone()
TH2_rpf_true.Divide(TH2_dataFail)

# Now make some pull surfaces
pull_Data_Bkg_Fail = TH2_dataFail.Clone('pull_Data_Bkg_Fail')
pull_Data_Bkg_Pass = TH2_dataPass.Clone('pull_Data_Bkg_Pass')
pull_RpfTrue_RpfFunc = TH2_rpf_true.Clone('pull_RpfTrue_RpfFunc')

pull_Data_Bkg_Fail.Add(TH2_QcdFail,-1)
pull_Data_Bkg_Pass.Add(TH2_QcdPass,-1)
pull_RpfTrue_RpfFunc.Add(TH2_rpf_func,-1)


# Finally make some ratios
ratio_Data_Bkg_Fail = TH2_dataFail.Clone('ratio_Data_Bkg_Fail')
ratio_Data_Bkg_Pass = TH2_dataPass.Clone('ratio_Data_Bkg_Pass')
ratio_RpfTrue_RpfFunc = TH2_rpf_true.Clone('ratio_RpfTrue_RpfFunc')

ratio_Data_Bkg_Fail.Divide(TH2_QcdFail)
ratio_Data_Bkg_Pass.Divide(TH2_QcdPass)
ratio_RpfTrue_RpfFunc.Divide(TH2_rpf_func)


#####################################
# 	Save out the interesting stuff	#
#####################################

# Print our four 2D distributions (data, bkg, pass, fail)
DataVBkgCan = TCanvas('DataVBkgCan','DataVBkgCan',1200,1000)
DataVBkgCan.Divide(2,2)
DataVBkgCan.cd(1)
TH2_QcdFail.Draw('lego')
DataVBkgCan.cd(2)
TH2_QcdPass.Draw('lego')
DataVBkgCan.cd(3)
TH2_dataFail.Draw('lego')
DataVBkgCan.cd(4)
TH2_dataPass.Draw('lego')

DataVBkgCan.Print('Plots/Full2Dv2_DataVsBkg_results.pdf','pdf')
DataVBkgCan.Print('Plots/Full2Dv2_DataVsBkg_results.root','root')


# Print our pulls
PullCan = TCanvas('PullCan','PullCan',1800,800)
PullCan.Divide(3,1)
PullCan.cd(1)
pull_Data_Bkg_Fail.Draw('surf')
PullCan.cd(2)
pull_Data_Bkg_Pass.Draw('surf')
PullCan.cd(3)
pull_RpfTrue_RpfFunc.Draw('surf')

PullCan.Print('Plots/Full2Dv2_pull_results.pdf','pdf')
PullCan.Print('Plots/Full2Dv2_pull_results.root','root')


# Print our ratios
ratioCan = TCanvas('ratioCan','ratioCan',1800,800)
ratioCan.Divide(3,1)
ratioCan.cd(1)
ratio_Data_Bkg_Fail.Draw('surf')
ratioCan.cd(2)
ratio_Data_Bkg_Pass.Draw('surf')
ratioCan.cd(3)
ratio_RpfTrue_RpfFunc.Draw('surf')

ratioCan.Print('Plots/Full2Dv2_ratio_results.pdf','pdf')
ratioCan.Print('Plots/Full2Dv2_ratio_results.root','root')


# Print real and derived Rp/fs
RpfsCan = TCanvas('RpfsCan','RpfsCan',1800,800)
RpfsCan.Divide(2,1)
RpfsCan.cd(1)
TH2_rpf_true.Draw('surf')
RpfsCan.cd(2)
TH2_rpf_func.Draw('surf')

RpfsCan.Print('Plots/Full2Dv2_rpfs.pdf','pdf')
RpfsCan.Print('Plots/Full2Dv2_rpfs.root','root')



