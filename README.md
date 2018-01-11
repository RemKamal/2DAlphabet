# README
This code is copied from [here](https://github.com/DAZSLE/ZPrimePlusJet/tree/zqqjet2016/fitting/ZqqJet) and will be developed for use in the b* all-hadronic analysis. I will keep change logs here as I commit.

## How Ralphabet Builder Works (Phibb version)
1. Before beginning, one must input a single root file which contains all of the 2D histograms that will be analyzed. Their names should follow the syntax 'process_cut_cat'+matchString where cat is either pass or fail and matchString = '_matched' or ''.
2. The LoadHistograms() function can then be used to load, scale, and organize the histograms from this file and store them in two dictionaries - one for pass and one for fail.
3. Now you can initialize an instance of the RhalphabetBuilder() class with the input file and newly created dictionaries as inputs and call the run() function to build rhalphabet.
4. The run() function only calls LoopOverPtBins(). The following subpoints explain what happens for each pt bin.
    1. Project the 2D pass/fail histograms onto their own 1D mass histograms for the pt bin.
    2. Input these 1D mass histograms into GetWorkspaceInputs() which 'converts' non-signal MC and data to RooDataHists.
    3. Call MakeRhalphabet() which estimates the QCD pass distribution for the pt bin and creates the RooParametricHists for pass and fail. Thus, both the pass and fail can float bin-by-bin in combine.
        * In order to estimate the pass distribution, we build a RooPolyVar in (rho, pt) for this specific (mass,pt) bin and then do pass = fail * QCD_efficiency * polynomial.
        * The fail distribution can float between its uncertainty and the polynomial can float given the initial coefficient values and bounds.
    4. Call GetSignalInputs() to convert signal MC to RooDataHists (analog to GetWorkspaceInputs - these could be merged actually)
    5. Call MakeWorkspace() to combine everything in this pt bin and write the final workspaces to the output file for combine to read.
        * This includes getting the systematic histograms, scaling them, and projecting onto mass for this pt bin
        * Also smears and shifts MC masses
        * Finally, 'converts' systematics and smear and shift hists to RooDataHists and writes EVERYTHING to the final workspace
      

## Change Log

### 1/11/18
Full comments in rhalphabet_builder_Phibb.py. This will become the primary version now.

### 1/5/18
Full comments in buildRhalphabet.py added. Any comment starting with `NOTE` is something that I'll have to come back to and/or resolve.

| Old | New |
|-----|-----|
| `f` | `input_file` |
|`self._nptbins` | `self._pt_nbins` |
|`pPt` | `approx_pt` |
| `if i1 == 0:`									| `if i1 == 0:` |
|	`pVal  = math.pow(10,-i1-min(int(i0*0.5),1))` |	`pVal  = math.pow(10,-min(int(i0*0.5),1))` |
| `hpass.extend([lHP0,lHP1,lHP2])` <br> `hfail.extend([lHF0,lHF1,lHF2])` <br> `hpass.extend([lHP3,lHP4])` <br> `hfail.extend([lHF3,lHF4])` | `hpass.extend([lHP0,lHP1,lHP2,lHP3,lHP4])` <br> `hfail.extend([lHF0,lHF1,lHF2,lHF3,lHF4])` |
| `elif process == "tqq": mass = 80.;` | --- |

* Removed `fHists` since it wasn't being used for anything
* Some reordering for my own sanity
