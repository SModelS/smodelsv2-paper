#!/usr/bin/env python3

import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import alphashape
from descartes import PolygonPatch
#Direct input
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})
path="/home/alguero/Work/smodelsv2-paper/IDM-Scoto/scalar_DM_scenario/plots"
df = pd.read_csv("scalarDataFermions.csv")
df['topo'] = df['topo'].apply(lambda x: x.replace("'", ""))
df['topo'] = df['topo'].apply(lambda x: x.replace("[", ""))
df['topo'] = df['topo'].apply(lambda x: x.replace("]", ""))
df=df.sort_values(by='rmax', ascending=True)

excl = df[df['rmax'] > 1]
compressed = excl[excl['mA0']-excl['mHc']<5]
df = df[df['mA0']-df['mHc']>5]
ald = df[~(df['rmax'] > 1)]
near = df[(0.5 < df['rmax']) & (df['rmax'] < 1.)]
dt = df[df['rmaxDT']>1]
hscp = df[df['rmaxHSCP']>1]
analyses = excl.ana.unique()
topos = excl.bestTx.unique()

fig, ax = plt.subplots()
ax = plt.gca()
plt.scatter(df['mHc'],df['deltaM'],c=df['rmax'],alpha=1,cmap='jet',vmax=1.2,vmin=.1, s=20)
plt.scatter(compressed['mHc'],compressed['deltaM'],c=compressed['rmax'],alpha=1,cmap='jet',vmax=1.2,vmin=.1, s=20)
cb = plt.colorbar()
cb.set_label(label=r'$r_{\rm{max}}$', fontsize=20)
cb.ax.tick_params(labelsize=15)
ax.tick_params(axis='both', labelsize=15)

###Disappearing tracks
frame_analysis2d=dt[['mHc','deltaM']]
frame_analysis2d=frame_analysis2d.to_numpy()
alpha_shape = alphashape.alphashape(frame_analysis2d, .001)
ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='pink',fill=False,zorder=20,lw=2,label='disappearing tracks'))

####Disappearing tracks with fermions
# frame_analysis2d=dtf[['mHc','deltaM']]
# frame_analysis2d=frame_analysis2d.to_numpy()
# alpha_shape = alphashape.alphashape(frame_analysis2d, .001)
# ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='black',ls='--',fill=False,zorder=20,lw=2,label='DT fermions excl.'))


####HSCP
frame_analysis2d=hscp[['mHc','deltaM']]
frame_analysis2d=frame_analysis2d.to_numpy()
alpha_shape = alphashape.alphashape(frame_analysis2d, .001)
ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='white',fill=False,zorder=20,lw=2,label='HSCP'))

lgd = plt.legend(loc='upper right',fontsize=18, facecolor='#d9e6f2', framealpha = 1.),

# plt.text(200, 0.1, "HSCP exclusion", color='white', fontsize=15, ha='left', va='center')
# plt.annotate(xy=(150, 0.2), xytext=(405, 0.35), s="disappearing tracks\nexclusion", color='black', fontsize=15,
#              arrowprops={'arrowstyle':'->'}, ha='left', va='center')

plt.ylim(0.053,0.4)
plt.xlim(101,750)
# plt.yscale('log')
# plt.title(r"Scalar dark matter, $\mathregular{H^\pm \to (\pi^\pm\;\rm{or}\;ff') H^0}$",fontsize = 15)
plt.title('Scalar DM, CMS efficiency map', fontsize = 15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel(r'$\Delta m = m_{H^\pm} - m_{H^0}$ (GeV)',fontsize = 19)
plt.xlabel(r'$m_{H^\pm}$ (GeV)',fontsize = 19)
plt.tight_layout()
file = os.path.join(path, "fermionDeltaM.png")
plt.savefig(file)
# plt.show()

fig, ax = plt.subplots()
ax = plt.gca()
plt.scatter(df['mHc'],df['dHc'],c=df['rmax'],alpha=1,cmap='jet',vmax=1.2,vmin=.1, s=20)
plt.scatter(compressed['mHc'],compressed['dHc'],c=compressed['rmax'],alpha=1,cmap='jet',vmax=1.2,vmin=.1, s=20)
cb = plt.colorbar()
cb.set_label(label=r'$r_{\rm{max}}$', fontsize=20)
cb.ax.tick_params(labelsize=15)
ax.tick_params(axis='both', labelsize=15)

####Disappearing tracks
frame_analysis2d=dt[['mHc','dHc']]
frame_analysis2d=frame_analysis2d.to_numpy()
alpha_shape = alphashape.alphashape(frame_analysis2d, .01)
ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='pink',fill=False,zorder=20,lw=2,label='disappearing tracks'))

####Disappearing tracks with fermions
# frame_analysis2d=dtf[['mHc','dHc']]
# frame_analysis2d=frame_analysis2d.to_numpy()
# alpha_shape = alphashape.alphashape(frame_analysis2d, .01)
# ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='black',ls='--',fill=False,zorder=20,lw=2,label='dis. tracks fermions eff.'))

####HSCP
frame_analysis2d=hscp[['mHc','dHc']]
frame_analysis2d=frame_analysis2d.to_numpy()
# Function for varying the alpha parameter
def alf(ind, r):
    if any(frame_analysis2d[ind][:,0] < 200) and any(frame_analysis2d[ind][:,1] < 7):
        return .05
#     elif any(frame_analysis2d[ind][:,0] < 280) and any(frame_analysis2d[ind][:,1] < 10):
#         return .0002
    elif any(frame_analysis2d[ind][:,0] < 380) and any(frame_analysis2d[ind][:,1] < 10):
        return .3
    else:
        return .008

alpha_shape = alphashape.alphashape(frame_analysis2d, alf)
ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='white',fill=False,zorder=20,lw=2,label='HSCP'))

lgd = plt.legend(loc='lower right', fontsize=18, facecolor='#d9e6f2', framealpha = 1.)

# plt.text(175, 100, "HSCP exclusion", color='white', fontsize=15, ha='left', va='center')
# plt.annotate(xy=(150, 0.1), xytext=(300, 0.7), s="disappearing tracks\nexclusion", color='white', fontsize=15,
#              arrowprops={'arrowstyle':'->', 'color':'white'}, ha='left', va='center')

plt.ylim(5e-3,1e3)
plt.xlim(101,710)
plt.yscale('log')
# plt.title(r"Scalar dark matter, $\mathregular{H^\pm \to (\pi^\pm\;\rm{or}\;ff') H^0}$",fontsize = 25)
plt.ylabel(r'$c\tau_{H^\pm}$ (m)',fontsize = 20)
plt.xlabel(r'$m_{H^\pm}$ (GeV)',fontsize = 20)
plt.title('Scalar DM, CMS efficiency map', fontsize = 15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
file = os.path.join(path, "fermionWidth.png")
plt.savefig(file)
# plt.show()
