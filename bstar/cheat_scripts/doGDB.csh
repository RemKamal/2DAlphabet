cp CombineCode/RooParametricHist2D.h ../../HiggsAnalysis/CombinedLimit/interface/
cp CombineCode/RooParametricHist2D.cxx ../../HiggsAnalysis/CombinedLimit/src/
source scramIt.csh
gdb -ex r --args python Full2Dv1.py
