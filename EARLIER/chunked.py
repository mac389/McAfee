from numpy import *
from scipy import *
from scipy.stats import cumfreq
from numpy.random import shuffle
import matplotlib.pyplot as plt
from matplotlib import rcParams, text
from itertools import combinations_with_replacement
import os
import neuroTools as tech

##################################################################################################		
#--------------------------------------Plotting Options--------------------------------------------
params = {'backend': 'ps',
          'axes.labelsize': 10,
          'text.fontsize': 20,
          'legend.fontsize': 20,
          'xtick.labelsize': 20,
          'ytick.labelsize': 20,
          'text.tex.preamble': [r'\usepackage[font=Large]{caption}',r'\usepackage{tikz}',
								r'\usepackage{amsmath}',r'\usetikzlibrary{arrows}',
								r'\usepackage{mathtools}'],
          'text.usetex': True}
rcParams.update(params)
#-------------------------------------------------------------------------------------------------	
##################################################################################################


#helper functions
def shuffler(array):
	answer = array.copy()
	map(shuffle,answer.transpose())
	#Use transpose because NumPy only shuffles the first axis, here want to shuffle the second
 	return answer
	
#load data
data_extension = '.data'
data = squeeze(loadtxt('ED_times_starting_chunked.data').astype(int))

#load labels
label_extension = '.format'
#label_files = [open(filename).readlines() for filename in os.listdir(".") if item.endswith(label_extension)]
#NEED TO FIX

#bootstrapping, assumes that the data here completely describe (are completely representative thereof) the underlying distribution.
sample_count = data.shape[0]
variable_count = data.shape[1]
jitter_count = 1000

#print array([diff(shuffler(data),axis=1) for jitter in range(jitter_count)]).shape()
#Changed to axis is one from original control.py file
distributions = reshape(array([diff(shuffler(data),axis=1) for jitter in range(jitter_count)]),(sample_count*jitter_count,variable_count))

#generate cdfs

cdfs = array([(cumfreq(distribution)[0:3]) for distribution in distributions.transpose()])
 #-1 because the list of differences of n sample counts will have n-1 members
print cdfs[1]
overview = plt.figure()
ax = overview.add_subplot(111)
for cdf in cdfs:
	xvals = array([ cdf[1] + i*cdf[2] for i in range(10)])
	h, = ax.plot(xvals,cdf[0]/max(cdf[0]),'--.',markersize=30)
	h.set_clip_on(False)
#plt.legend(('CXR','ABD CT','ABD + Chest CT'),'lower right', numpoints=1, fancybox=True, frameon=False, bbox_to_anchor=(1.1,0.2))
tech.adjust_spines(ax,['left','bottom'])
overview.text(0.5, 0.08, r'Weekly Change in Cases', ha='center', va='top', fontsize=30, weight='bold') #xlabel
overview.text(0.02875, 0.5, r'Frequency of Occurrence', ha='center', va='center', rotation='vertical', fontsize=30, weight='bold')
plt.subplots_adjust(top=0.95, bottom =0.18, left=0.15)
plt.savefig('cdf_chunked.png',dpi=300)
