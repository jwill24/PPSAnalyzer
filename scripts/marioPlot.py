#!/usr/bin/env python
import os, sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.ticker import MultipleLocator


def make_square_axes(ax):
    ax.set_aspect(1 / ax.get_data_ratio())

fig, ax = plt.subplots()

path_tot = Path([[13500,0],[250,-3.95],[250,3.95],[13500,0]])
patch_tot = PathPatch(path_tot, facecolor='silver')

path_45N = Path([[250,-2.025],[250,-0.96],[2925,1.5],[5100,0.95]])
patch_45N = PathPatch(path_45N, facecolor='yellow', edgecolor='yellow')

path_45F = Path([[250,-0.96],[250,-0.665],[2420,1.68],[2925,1.5]])
patch_45F = PathPatch(path_45F, facecolor='orange', edgecolor='orange')

path_56N = Path([[250,0.53],[250,2.04],[5070,-0.95],[2310,-1.73]])
patch_56N = PathPatch(path_56N, facecolor='yellow', edgecolor='yellow')

path_56F = Path([[250,0.23],[250,0.525],[2310,-1.73],[2000,-1.875]]) 
patch_56F = PathPatch(path_56F, facecolor='orange', edgecolor='orange') 

path_double = Path([[387,-0.215],[950,0.714],[1950,0],[772.5,-0.91]])
patch_double = PathPatch(path_double, facecolor='lime', edgecolor='lime', alpha=0.7)

ax.add_patch(patch_tot)
ax.add_patch(patch_45N)
ax.add_patch(patch_56N)
ax.add_patch(patch_45F)
ax.add_patch(patch_56F)
ax.add_patch(patch_double)
ax.set(xlim=(250,13500), ylim=(-6,6))
ax.set_xscale('log')
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
ax.yaxis.set_minor_locator(MultipleLocator(0.5))
ax.tick_params(direction='in', which='both')
plt.plot([250,13500],[0,0],'black')
plt.xlabel('m$_{\gamma\gamma}$ (GeV)')
plt.ylabel('Y$_{\gamma\gamma}$')
plt.text(5000,6.1,'$\sqrt{s}$ = 13 TeV')
plt.text(251,6.1,'CMS', fontweight='bold')
plt.text(370,6.1,'Preliminary')
make_square_axes(plt.gca())
plt.show()
