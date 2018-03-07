#include "TH1.h"
#include "TH1F.h"
#include "RooArgList.h"
#include "RooAbsCollection.h"
#include "RooRealVar.h"
#include "HiggsAnalysis/CombinedLimit/interface/RooParametricHist.h"
#include "TCanvas.h"
#include <stdio.h>
#include <math.h>

using namespace std;

int RPH1Dtester() {

	TH1F *testTH2 = new TH1F("testTH2","testTH2",10,0,10);

	int valx;

	for (int ix=1; ix < testTH2->GetNbinsX()+1; ++ix) {
		// for (int iy=1; iy < testTH2->GetNbinsY()+1; ++iy) {
			valx = 2*ix;

			testTH2->SetBinContent(ix,valx);
			testTH2->SetBinError(ix,testTH2->GetBinContent(ix)/4);

		// }
	}

	RooRealVar *xVar = new RooRealVar("xVar","xtitle",0,10);

	RooArgList *binList = new RooArgList();

	string name;
	string title;

	// for (int ybin=1; ybin < testTH2->GetNbinsY()+1; ++ybin) {
	for (int xbin=1; xbin < testTH2->GetNbinsX()+1; ++xbin) {
		name = "binVar_"+to_string(xbin); //+"-"+to_string(ybin);
   		title = "title_binVar_"+to_string(xbin); //+"-"+to_string(ybin);

   		float binContent = testTH2->GetBinContent(xbin);//,ybin);
   		float binErrUp = binContent + testTH2->GetBinError(xbin);//,ybin);
   		float binErrDown = binContent - testTH2->GetBinError(xbin);//,ybin);

   		RooRealVar *binRRV = new RooRealVar(name.c_str(), title.c_str(), binContent, max(binErrDown,float(0)), max(binErrUp,float(0)));

   		binList->add(*binRRV);

	}
	// }

	RooParametricHist *final = new RooParametricHist("test_RPH2D","test_RPH2D", *xVar, *binList, *testTH2);

	TH1 *newTH2 = final->createHistogram("xVar",10);

	cout << newTH2->GetBinContent(1) << endl;

	TCanvas *totCan = new TCanvas("c","c",1400,800);

	totCan->Divide(2,1);
	totCan->cd(1);
	newTH2->Draw("E");
	totCan->cd(2);
	testTH2->Draw("E");

	cout << "press any key to exit...";

	return 0;

}