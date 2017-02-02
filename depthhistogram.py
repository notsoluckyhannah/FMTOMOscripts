import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sources=pd.read_csv('sourceswa.in',names=['lat','lon','dep'],skiprows=1,index_col=None,header=None,sep=' ')
info=sources.ix[::3,:]
try1=np.array(info,dtype='float')
try2=try1[:,2]
plt.hist(try2)
fig=plt.gcf()
plt.show()


	
