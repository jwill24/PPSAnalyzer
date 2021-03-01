import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
from matplotlib import rc
import math

plt.rc('font',family='Helvetica')
plt.rcParams.update()

#rc('text', usetex=True)

def make_square_axes(ax):
    ax.set_aspect(1 / ax.get_data_ratio())

z1 = np.linspace(-0.8e-12, 0.8e-12, 100)
z2 = np.linspace(-1.6e-12, 1.6e-12, 100)

#z1 = np.linspace(-0.6e-12, 0.6e-12, 100)
#z2 = np.linspace(-1.2e-12, 1.2e-12, 100)

z1,z2 = np.meshgrid(z1,z2)

#obs = (3.51442 * 1e22 * z1 ** 2) + (2 * 1.46434 * 1e22 * z1 * z2) + (8.05388 * 1e21 * z2 ** 2) - 1.08365 # 2016 old
#exp = (3.51442 * 1e22 * z1 ** 2) + (2 * 1.46434 * 1e22 * z1 * z2) + (8.05388 * 1e21 * z2 ** 2) - 1.25596 # 2016 old

obs = (2.5001 * 1e25 * z1 ** 2) + (2 * 1.04167 * 1e25 * z1 * z2) + (6.59021 * 1e24 * z2 ** 2) - 2.07947 # 2016 new
exp = (2.5001 * 1e25 * z1 ** 2) + (2 * 1.04167 * 1e25 * z1 * z2) + (6.59021 * 1e24 * z2 ** 2) - 2.48835 # 2016 new

#obs = (2.5001 * 1e25 * z1 ** 2) + (2 * 1.04167 * 1e25 * z1 * z2) + (6.59021 * 1e24 * z2 ** 2) - 2.07947 # Run2
#exp = (5.6000 * 1e25 * z1 ** 2) + (2 * 2.3333 * 1e25 * z1 * z2) + (1.2833 * 1e25 * z2 ** 2) - 0.101 # Run2

levels = np.linspace(z2.min(), z2.max(), 100)

fig,ax = plt.subplots(1)

# 2016 Limits (observed, expected)
ax.contour(z1, z2, obs, [0], colors='black')
ax.contour(z1, z2, exp, [0], linestyles='dashed', colors='black')
ax.contourf(z1, z2, obs, [0], levels = [0,100], colors='#7e9acf')
ax.plot(0,0,marker='x',color='black', markersize=14, markeredgewidth=6) # sm marker
custom_lines = [Line2D([], [], color='black', marker='x', linestyle='None', markersize=14, markeredgewidth=6),
                Line2D([0], [0], color='black', lw=2),
                Line2D([0], [0], linestyle='dashed', color='black', lw=2),
                ]
ax.legend(custom_lines, ['Standard Model', 'Observed 95% CL', 'Expected 95% CL'], loc='lower left', bbox_to_anchor=(0.02,0.02), facecolor='none', frameon=False, fontsize=18)

for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1.5)

plt.xlim(-0.8e-12,0.8e-12)
plt.ylim(-1.6e-12,1.6e-12)
ax.xaxis.set_minor_locator(MultipleLocator(0.5e-13))
ax.yaxis.set_minor_locator(MultipleLocator(1.e-13))
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
ax.tick_params(direction='in', which='major', length=18, width=1.0)
ax.tick_params(direction='in', which='minor', length=9, width=1.0)
ax.set_xticks([-0.75e-12, -0.5e-12, -0.25e-12, 0, 0.25e-12, 0.5e-12, 0.75e-12])
ax.set_xticklabels(['-0.75', '-0.5', '-0.25', '0', '0.25', '0.5', '0.75'], fontsize=20)
ax.set_yticks([-1.5e-12, -1.e-12, -0.5e-12, 0, 0.5e-12, 1.e-12, 1.5e-12])
ax.set_yticklabels(['-1.5', '-1', '-0.5', '0', '0.5', '1', '1.5'], fontsize=20)
plt.xlabel(r'$\zeta_{1}$ ($\times$10$^{-12}$) (GeV$^{-4}$)', horizontalalignment='right', x=1.0, fontsize=20, labelpad=20)
plt.ylabel(r'$\zeta_{2}$ ($\times$10$^{-12}$) (GeV$^{-4}$)', horizontalalignment='right', y=1.0, fontsize=20, labelpad=20)
#ax.text(3.4e-13,1.65e-12,'9.4 fb$^{-1}$ (13 TeV)', fontsize=10) 
#ax.text(2.6e-13,1.25e-12,'CMS-TOTEM', fontweight='bold', fontsize=13)
ax.text(3.7e-13,1.65e-12,'9.4 fb$^{-1}$ (13 TeV)', fontsize=20)
ax.text(3.42e-13,1.34e-12,'CMS-TOTEM', fontweight='bold', fontsize=24)
ax.text(4.63e-13,1.23e-12,'Preliminary', fontsize=20)
make_square_axes(plt.gca())
plt.savefig('aqgc_limit.png')
plt.show()


# RunII comparison
#ax.contour(z1, z2, obs, [0], colors='#8E0103')
#ax.contour(z1, z2, exp, [0], colors='#d7263d')
#ax.contourf(z1, z2, exp, [0], levels = [0,100], colors='#009ffd', alpha=0.6)
#custom_lines = [Line2D([0], [0], color='#8E0103', lw=2),
#                Line2D([0], [0], color='#d7263d', lw=2)]
#ax.legend(custom_lines, ['Previous Limit', 'Expected 95% CL'], loc="lower left", facecolor='none', frameon=False)


#plt.xlim(-0.6e-12,0.6e-12)
#plt.ylim(-1.2e-12,1.2e-12)
#ax.xaxis.set_minor_locator(MultipleLocator(0.5e-13))
#ax.yaxis.set_minor_locator(MultipleLocator(1.e-13))
#ax.xaxis.set_ticks_position('both')
#ax.yaxis.set_ticks_position('both')
#ax.tick_params(direction='in', which='major', length=9, width=0.8)
#ax.tick_params(direction='in', which='minor', length=4, width=0.8)
#ax.set_xticks([-0.5e-12, -0.25e-12, 0, 0.25e-12, 0.5e-12])
#ax.set_xticklabels(['-0.5', '-0.25', '0', '0.25', '0.5'])
#ax.set_yticks([-1.e-12, -0.5e-12, 0, 0.5e-12, 1.e-12])
#ax.set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
#plt.xlabel(r'$\zeta_{1}$ ($\times$10$^{-12}$) (GeV$^{-4}$)', horizontalalignment='right', x=1.0, fontsize=12)
#plt.ylabel(r'$\zeta_{2}$ ($\times$10$^{-12}$) (GeV$^{-4}$)', horizontalalignment='right', y=1.0, fontsize=12)
#ax.text(9.7e-12,30.5e-12,'$\sqrt{s}$ = 13 TeV')
#ax.text(1.63e-13,1.23e-12,'102.7 fb$^{-1}$ (13 TeV)', fontsize=11)
#ax.text(-0.6e-12,1.23e-12,'CMS', fontweight='bold', fontsize=13)
#ax.text(-0.45e-12,1.23e-12,'Preliminary', fontsize=12)
##ax.text(2.6e-13,1.01e-12,'CMS', fontweight='bold', fontsize=13)
##ax.text(2.6e-13,.89e-12,'Preliminary', fontsize=13)
#make_square_axes(plt.gca())
#plt.savefig('aqgc_limit_comparison.png')
#plt.show()

