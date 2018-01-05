# README
This code is copied from [here](https://github.com/DAZSLE/ZPrimePlusJet/tree/zqqjet2016/fitting/ZqqJet) and will be developed for use in the b* all-hadronic analysis. I will keep change logs here as I commit.

## Change Log

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