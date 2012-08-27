from numpy import *
from scipy import *
from scipy.stats import cumfreq
from numpy.random import shuffle,random
import matplotlib.pyplot as plt
from matplotlib import rcParams, text
from matplotlib.ticker import FormatStrFormatter
from itertools import combinations_with_replacement
import os
import neuroTools as tech

##################################################################################################		
#--------------------------------------Plotting Options--------------------------------------------
params = {'backend': 'ps',
          'axes.labelsize': 10,
          'font.weight': 'bold',
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

#load data
data = array([3,7,8,4])


#bootstrapping, assumes that the data here completely describe (are completely representative thereof) the underlying distribution.
sample_count = data.shape[0]
variable_count = 1
jitter_count = 1000

replicates = tile(data,(jitter_count,1))
replicates += (random(replicates.shape)*(max(data)-min(data))+min(data))
map(shuffle,replicates)
distribution = ravel(diff(replicates,axis=1))
cdf = cumfreq(distribution)

n,bins = histogram(distribution)
left = bins[:-1]
width = bins[1]-bins[0]
pct = n/float(n.sum())

overview = plt.figure(figsize =(8.27,11.69)) #Thus instructeth PDM
ax = overview.add_subplot(111)
xvals = linspace(cdf[1],cdf[1]+10*cdf[2],num=10) #By default cumfreq divides into 10 bins
ax.bar(left,pct,width=width, color='k', alpha=0.75)
#plt.setp(patches, 'facecolor', 'k', 'alpha', 0.75)
tech.adjust_spines(ax,['left','bottom'])
overview.text(0.55, 0.08, r'\noindent Weekly Change in\\Chest X-rays ', ha='center', va='top', fontsize=30, weight='bold') #xlabel
overview.text(0.02875, 0.5, r'Chance of Occurrence', ha='center', va='center', rotation='vertical', fontsize=30, weight='bold')
ax.annotate(r'April 21, 2010',xy=(25,.16), xytext=(25,.17),arrowprops=dict(facecolor='black', shrink=0.05), fontsize=20)
formatter = FormatStrFormatter('$\mathbf{%g}$')
ax.xaxis.set_major_formatter(formatter)
plt.subplots_adjust(top=0.95, bottom =0.18, left=0.15)
plt.savefig('walkout.jpg',dpi=1200)
