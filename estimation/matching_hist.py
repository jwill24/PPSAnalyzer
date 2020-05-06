#!/usr/bin/env python3
from scipy import stats
import math
import numpy as np
import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from scipy.optimize import curve_fit
from scipy.interpolate import make_interp_spline, BSpline

def plotDist(sig,sample,method):
    data_ = True if sample == 'data' else False
    
    # Get experiments
    v = []
    with open(sig+'sigma_'+sample+'_'+method+'.txt', 'r') as f:
        for line in f:
            v.append(float(line.strip()))
    
    # Get mean and range
    if data_: v = [int(x) for x in v]
    mu = sum(v)/len(v)
    s_mu = str(round(mu,2))
    x = np.arange(min(v), max(v))
    print('min:', min(v), 'max:', max(v), 'average:', mu)
    
    # Plot histogram
    sns.set_style('darkgrid')
    plt.hist(v,bins=x,density=True)
    plt.xticks(np.arange(0, round(max(x),0), 2))
    ymin, ymax = plt.gca().get_ylim()
    xmin, xmax = plt.gca().get_xlim()
    distx, disty = xmax-xmin, ymax-ymin
    plt.text(xmin+0.75*distx, ymax+0.03*disty, '$\sqrt{s}$ = 13 TeV', fontsize=15)
    plt.text(xmin, ymax+0.035*disty, 'CMS', fontweight='bold', fontsize=15)
    plt.text(xmin+0.106*distx, ymax+0.035*disty, 'Preliminary', fontsize=15)
    plt.text(xmin+0.81*distx, ymin+0.75*disty, '$\mu$ = '+s_mu)
    
    # Do fits
    if data_:
        pdf_poisson = stats.poisson(mu) 
        # Plot points
        plt.plot(x+0.5, pdf_poisson.pmf(x), 'ro', label='Poisson $\lambda$ = %f'% mu)
        # Plot curve
        xnew = np.linspace(min(x)+0.5, max(x)+0.5, 300)
        spl = make_interp_spline(x+0.5, pdf_poisson.pmf(x), k=3)
        smooth = spl(xnew)
        plt.plot(xnew,smooth,'r')
    else:
        lnspc = np.linspace(min(x), max(x), len(v))
        ag,bg,cg = stats.gamma.fit(v)
        pdf_gamma = stats.gamma.pdf(lnspc, ag, bg, cg) 
        plt.plot(lnspc, pdf_gamma, 'r', label="Gamma")
        
    plt.xlabel(sig+'$\sigma$ matching', fontsize=15)    
    plt.savefig('matching_'+sig+'sigma_'+sample+'_'+method+'.pdf')
    plt.show()
    
    
#plotDist('2','data','singleRP')
#plotDist('3','data','singleRP')
        
#plotDist('2','mc','singleRP')
plotDist('3','mc','singleRP')
    
    

#plotDist('2','data','multiRP')
#plotDist('3','data','multiRP')
        
#plotDist('2','mc','multiRP')
#plotDist('3','mc','multiRP')