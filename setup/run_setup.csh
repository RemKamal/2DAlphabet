cp RooParametricHist2D.cxx $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/src/
cp RooParametricHist2D.h $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/interface/

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/src/

sed '/RooParametricHist.h/ a\#include "HiggsAnalysis/CombinedLimit/interface/RooParametricHist2D.h"' classes.h
sed '/RooParametricHist/ a\	<class name="RooParametricHist2D" />' classes_def.xml

scramv1 b clean; scramv1 b
cd $CMSSW_BASE/2DAlphabet