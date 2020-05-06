import sys
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.ticker as mtick
#import seaborn as sns

def plot(sig):
    # Get experiments
    v = []
    #e, two, three = [], [], []
    with open('convergence_data_singleRP.txt', 'r') as f:
        for line in f:
            vec = line.strip('[]\n')
            first, second, third = vec.split(',')
            #e.append(int(first)), two.append(float(third)), three.append(float(second))
            v.append( [int(first),float(second),float(third)] )

    df = pd.DataFrame(v, columns=['e','three','two'])
    #sns.set_style('darkgrid')
    #sns.set_style('ticks')
    
    if sig == 'three':
        mu = 8.99
        s_sig = '3'
        ymin, ymax = 2, 14
    elif sig == 'two':
        mu = 4.26749
        s_sig = '2'
        ymin, ymax = 0, 8
    
    
    fig, ax=plt.subplots()
    ax.grid()
    #sns.scatterplot(x='e', y='three', data=df)
    ax.scatter(df['e'],df[sig])
    ax.axhline(y=mu, color='r', linestyle='-')
    ax.set_xscale("log")
    
    
    fig.set_size_inches(15, 5)
    
   
    #ax.xaxis.set_minor_locator(mtick.LogLocator(base=10, subs=(1,2,3,4,5,6,7,8,9)))
    ax.set_axisbelow(True)
    ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    
    plt.ylabel(s_sig+'$\sigma$ matching', fontsize=15)
    plt.xlabel('Experiments',fontsize=15)
    
    plt.ylim(ymin,ymax)
    plt.savefig(s_sig+'sigma_convergence.pdf')
    plt.show()
    
    
plot('three')

#plot('two')
