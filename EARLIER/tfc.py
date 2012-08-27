from numpy import *
from scipy import *
from scipy.stats import cumfreq
from numpy.random import shuffle,random
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

def shuffler(data, jitter_count=10000):
	replicates = tile(data,(jitter_count,1))
	replicates += (random(replicates.shape)*(max(data)-min(data))+min(data))
	map(shuffle,replicates)
	return ravel(diff(replicates,axis=1))

def normed_hist(data):
	n,bins = histogram(data)
	left = bins[:-1]
	width = bins[1]-bins[0]
	pct = n/float(n.sum())
	return (left, pct,width)

	

#load data
doc = array([81.07,70.74,88.92,41.90])
nurse = array([37.85,74.76,110.84,49.31])


#bootstrapping, assumes that the data here completely describe (are completely representative thereof) the underlying distribution.

docs = shuffler(doc)
nurses = shuffler(nurse)

left_docs, pct_docs, width_docs = normed_hist(docs)
left_nurses, pct_nurses, width_nurses = normed_hist(nurses)

overview = plt.figure(figsize =(8.27,11.69)) #Thus instructeth PDM
ax = overview.add_subplot(111)
ax.bar(left_docs,pct_docs,width=width_docs, color='k')
plt.hold(True)
ax.bar(left_nurses,pct_nurses,width=width_nurses, color='k', fill=False)
plt.legend(('Doctors','Nurses'), loc='upper left', frameon=False)

#plt.setp(patches, 'facecolor', 'k', 'alpha', 0.75)
tech.adjust_spines(ax,['left','bottom'])
overview.text(0.5, 0.08, r'Weekly Change in Time to See Provider', ha='center', va='top', fontsize=30, weight='bold') #xlabel
overview.text(0.02875, 0.5, r'Chance of Occurrence', ha='center', va='center', rotation='vertical', fontsize=30, weight='bold')
ax.annotate(r'April 21, 2010',xy=(35,.16), xytext=(36,.18),arrowprops=dict(facecolor='black', shrink=0.05), fontsize=20)
plt.subplots_adjust(top=0.95, bottom =0.18, left=0.15)
plt.savefig('cdf_tfc.jpg',dpi=600)