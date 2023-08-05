# pyACA
**IN WORK: Currently untested**

Python scripts accompanying the book "An Introduction to Audio Content 
Analysis" (www.AudioContentAnlysis.org)

This package comprises implementations of simple algorithms and features for 
audio content analysis.

Please note that the provided code examples are only intended to showcase 
algorithmic principles – they are not suited to be used without 
parameter optimization and additional algorithmic tuning. More specifically,
the python code might **violate typical python style conventions** in order to
be consistent with the Matlab code at 
https://github.com/alexanderlerch/ACA-Code

The majority of these python sources require the numpy and scipy installed. 
Several functions (such as MFCCs and Gammatone filters) are based on 
implementations in Slaney’s Auditory Matlab Toolbox.

Please feel free to visit http://www.audiocontentanalysis.org/code/
to find the latest versions of this code or to submit comments or code 
that fixes, improves and adds functionality.

The top-level functions are:
- computeFeature: calculates instantaneous features 
- computePitch: calculates a fundamental frequency estimate
- computeKey: calculates a simple key estimate
- computeNoveltyFunction: simple onset detection
- computeBeatHisto: calculates a simple beat histogram

The names of the additional functions follow the following 
conventions:
- Feature*: instantaneous features
- Pitch*: pitch tracking approach
- Novelty*: novelty function computation
- Tool*: additional help functions such as frequency scale 
conversion, dynamic time warping, gammatone filterbank, ...

Example: Computation and plot of the Spectral Centroid

```python
    import numpy as np
    import matplotlib.pyplot as plt 
	import pyACA
  
    # read audio file
    [f_s,afAudioData] = pyACA.ToolReadAudio(cPath)
    #afAudioData = np.sin(2*np.pi * np.arange(f_s*1)*440./f_s)
 
    # compute feature
	cFeatureName = "SpectralCentroid"
    [v,t] = pyACA.computeFeature(cFeatureName, afAudioData, f_s)

    # plot feature output
    plt.plot(t,v)
```


