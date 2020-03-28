from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

def plotPoisson(sig, min_, max_):
  v = []
  with open(sig+'sigma.txt', 'r') as f:
    for line in f:
      v.append(int(line.strip()))

  average = sum(v)/len(v)
  v_new = [x+0.5 for x in v]

  sns.set_style('darkgrid')
  ax = sns.distplot( v, kde=False, color='darkturquoise', bins=np.arange(min_, max_),norm_hist=True ) # plot hist
  ax2 = sns.distplot( v_new, fit=stats.gamma, kde=False, hist=False, fit_kws={'color':'lightcoral'} ) # plot fit
  ax.xaxis.set_major_locator(MaxNLocator(integer=True))
  plt.figtext( .75, .75, '$\lambda$ = '+str(average), fontsize=12  )
  plt.xlim(min_,max_)
  plt.ylabel('P(X=x)')
  plt.xlabel('Matching at '+sig+'$\sigma$')
  plt.show()

#plotPoisson('2',0,14)
plotPoisson('3',3,25)
