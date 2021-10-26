
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import alphashape
from matplotlib.patches import Patch
from descartes import PolygonPatch
plt.rcParams.update({
"text.usetex":True,
"font.family":"serif",
"font.serif":["Computer Modern Roman"]
                    })

def openframe(path_to_frame):

    frame=pd.read_csv(path_to_frame,sep=' ')
    
    return frame


def plotterAnalyses(frame,title,path_to_plot):

  
    
    analysis_list=[]
    frame_excluded=frame.loc[frame['SModelS_status']=='Excluded']
    for value in frame_excluded['Analysis']:
        if value=='False':
            continue
      
        if value not in analysis_list:
            analysis_list.append(value)
            
    frame_nonexcluded=frame.loc[frame['SModelS_status']=='Non-excluded']
    plt.plot(frame_nonexcluded['m(N1)'],frame_nonexcluded['m(H+)'],'s',label ='Allowed',color='grey',markersize=10, alpha=0.1,markeredgewidth=0)
    
    frame_almostexcluded=frame_nonexcluded.loc[frame_nonexcluded['r_max']>.5]
    plt.plot(frame_almostexcluded['m(N1)'],frame_almostexcluded['m(H+)'],'s',label ='.5<r<1',color='black',markersize=6)
    
    ##Plotting excluded points by analysis
    
    j=0
    for analysis in analysis_list:
    
        frame_analysis=frame_excluded.loc[frame_excluded['Analysis']==analysis]
        plt.plot(frame_analysis['m(N1)'],frame_analysis['m(H+)'],'s',label =analysis,markersize=6)
        plt.xscale('log')
        plt.xlabel('$ m_{N_{1}}$ (GeV)',fontsize=12)
        plt.ylabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
        j=j+1
    
    plt.legend()
    plt.title(title)
    plt.savefig(path_to_plot)
    plt.close()
    
    
    return
    

def plotterTopo(frame,title,path_to_plot):

  
    
    analysis_list=[]
    frame_excluded=frame.loc[frame['SModelS_status']=='Excluded']
    for value in frame_excluded['Tx']:
        if value=='False':
            continue
      
        if value not in analysis_list:
            analysis_list.append(value)
            
    frame_nonexcluded=frame.loc[frame['SModelS_status']=='Non-excluded']
    plt.plot(frame_nonexcluded['m(N1)'],frame_nonexcluded['m(H+)'],'.',label ='Allowed',color='grey')
    
    frame_almostexcluded=frame_nonexcluded.loc[frame_nonexcluded['r_max']>.5]
    plt.plot(frame_almostexcluded['m(N1)'],frame_almostexcluded['m(H+)'],'.',label ='.5<r<1',color='black')
    
    ##Plotting excluded points by analysis
    
    
    
    j=0
    for analysis in analysis_list:
        
        frame_analysis=frame_excluded.loc[frame_excluded['Tx']==analysis]
     
        plt.plot(frame_analysis['m(N1)'],frame_analysis['m(H+)'],'.',label=analysis)
 
        plt.xscale('log')
        
        j=j+1
    
   
    
  
    
    plt.xlabel('$ m_{N_{1}}$ (GeV)',fontsize=12)
    plt.ylabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
    plt.legend()
    plt.title(title)
    plt.savefig(path_to_plot)
    plt.close()
    
    
    return


def plotterTopoHSCPind(frame,title,path_to_plot):

  
    
    analysis_list=[]
    frame_excluded=frame.loc[frame['SModelS_status']=='Excluded']
    for value in frame_excluded['Tx']:
        if value=='False':
            continue
      
        if value not in analysis_list:
            analysis_list.append(value)
            
    frame_nonexcluded=frame.loc[frame['SModelS_status']=='Non-excluded']
    plt.plot(frame_nonexcluded['m(N1)'],frame_nonexcluded['m(H+)'],'.',label ='Allowed',color='grey',markersize=.5,alpha=.5)
    
    #frame_almostexcluded=frame_nonexcluded.loc[frame_nonexcluded['r_max']>.5]
    #plt.plot(frame_almostexcluded['m(N1)'],frame_almostexcluded['m(H+)'],'.',label ='.5<r<1',color='black')
    
    ##Plotting excluded points by analysis
    
    
    
   
    
        
    frame_analysis=frame_excluded.loc[frame_excluded['Tx']=='TSmuSmuDisp']
     
    plt.plot(frame_analysis['m(N1)'],frame_analysis['m(H+)'],'.',label ='TSmuSmuDisp',markersize=10)
      
    frame_analysis=frame_excluded.loc[(frame_excluded['Tx']=='THSCPM1b,THSCPM8') | (frame_excluded['Tx']=='THSCPM1b,THSCPM2b,THSCPM8,THSCPM9')]
    plt.plot(frame_analysis['m(N1)'],frame_analysis['m(H+)'],'.',label='HSCP (combination)',markersize=10)
    plt.xscale('log')
        
    
    
    frameHSCP1=frame_excluded.loc[frame_excluded['THSCPM1b']>=.8]
    
    plt.plot(frameHSCP1['m(N1)'],frameHSCP1['m(H+)'],'.',label ='THSCPM1b',markersize=10,color='green')
    plt.xscale('log')
    
    plt.xlabel('$ m_{N_{1}}$ (GeV)',fontsize=12)
    plt.ylabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
    plt.legend()
    plt.title(title)
    plt.savefig(path_to_plot)
    plt.close()
    
    
    return


def plotCurvesTopo(frame,title,path_to_plot):
    import numpy as np

    plt.scatter(frame['m(N1)'],frame['m(H+)'],c=frame['r_max'],alpha=1,cmap='jet',vmax=1.2,vmin=.1)
    plt.colorbar(label='$r_{max}$',fontsize=20)
    #clb.label('$$r_{max}$$')
    analysis_list=[]
    frame_excluded=frame.loc[frame['SModelS_status']=='Excluded']
    for value in frame_excluded['Tx']:
        if value=='False':
            continue
      
        if value not in analysis_list:
            analysis_list.append(value)

    color_list=['yellow','grey','white','orange','purple']
   
    
    ####Displaced lepton
    frame_displaced=frame.loc[frame['Disp']>1]
    frame_analysis2d=frame_displaced[['m(N1)','m(H+)']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    hull = ConvexHull(frame_analysis2d,qhull_options='QG4')
    k=0
    for simplex in hull.simplices:
        if k==0:
            plt.plot(frame_analysis2d[simplex, 0], frame_analysis2d[simplex, 1], 'r--',color=color_list[0],label='Displaced leptons',lw=2)
            k=-1
        else:
            plt.plot(frame_analysis2d[simplex, 0], frame_analysis2d[simplex, 1], 'r--',color=color_list[0],lw=2)
                
    
       
    plt.xscale('log')
        
    ##HSCP
    frame_analysis=frame_excluded.loc[frame_excluded['Tx']!='TSmuSmuDisp']
    frame_analysis2d=frame_analysis[['m(N1)','m(H+)']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    hull = ConvexHull(frame_analysis2d,qhull_options='QG4')
    k=0
    for simplex in hull.simplices:
        if k==0:
            plt.plot(frame_analysis2d[simplex, 0], frame_analysis2d[simplex, 1], 'r--',color=color_list[2],label='HSCP',lw=2)
            k=-1
        else:
            plt.plot(frame_analysis2d[simplex, 0], frame_analysis2d[simplex, 1], 'r--',color=color_list[2],lw=2)
                
    
       
    plt.xscale('log')
    
        
        
    plt.legend()
    plt.xlabel('$ m_{N_{1}}$ (GeV)',fontsize=20)
    plt.ylabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=20)
    plt.title(title)
       
        
    plt.savefig(path_to_plot)
    plt.close()
    return
        
    

def plotCurvesTopo2(frame,frameHSCP,title,path_to_plot):
    
    
    frame=frame.loc[frame['MASS37']<900]
    fig, ax = plt.subplots()
    #ax.scatter(frame['m(N1)'],frame['m(H+)'],c=frame['r_max'],alpha=1,cmap='jet',vmax=1.2,vmin=.1)
    #ax.set_xscale('log')
   # plt.colorbar()
    
    ax.set_xlim(left=min(frame['MASS37']),right=max(frame['MASS37']))
    ax.set_ylim(bottom=min(frame['MASS9000006']),top=max(frame['MASS9000006']))
    
    plt.scatter(frame['MASS37'],frame['MASS9000006'],c=frame['r_max'],alpha=1,cmap='jet',vmax=1.2,vmin=.1,s=55)
    cbar=plt.colorbar(label='$r_{max}$')
   
    cbar.set_label(label='$r_{max}$', size=20)
    cbar.ax.tick_params(labelsize=15)
    frame_displaced=frame.loc[frame['Disp']>1]
    frame_analysis2d=frame_displaced[['MASS37','MASS9000006']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    print(frame_analysis2d)
    alpha_shape = alphashape.alphashape(frame_analysis2d, .099)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='pink',fill=False,zorder=20,lw=2,label='Displaced lepton'))
    
    plt.subplots_adjust(bottom=.13)
    plt.subplots_adjust(left=.13)
    
    frame_excluded=frameHSCP.loc[frameHSCP['r_max']>1]
    frame_analysis=frame_excluded.loc[frame_excluded['Tx']!='TSelSelDisp']
    frame_analysis2d=frame_analysis[['MASS37','MASS9000006']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    print(frame_analysis2d)
    alpha_shape = alphashape.alphashape(frame_analysis2d, .09)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='white',fill=False,lw=2,label='HSCP'))
    plt.legend(loc='upper left',framealpha=.6,labelcolor='black',fontsize=15)
    #print(alpha_shape)
   # Patch(alpha_shape,'.',c='yellow')
    plt.yscale('log')
    plt.ylabel('$ m_{N_{1}}$ (GeV)',fontsize=19)
    plt.xlabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=19)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.title(title,fontsize=15)
    plt.savefig(path_to_plot)
    plt.close()
   
    return
 
    
def plotCurvesTopoCtau2(frame,frameHSCP,title,path_to_plot):


    frame=frame.loc[frame['MASS37']<900]
    frame=frame.loc[frame['ctau(37)']<10e5]
    fig, ax = plt.subplots()
    
    
    #ax.scatter(frame['m(N1)'],frame['m(H+)'],c=frame['r_max'],alpha=1,cmap='jet',vmax=1.2,vmin=.1)
    #ax.set_xscale('log')
   # plt.colorbar()
    
    ax.set_xlim(left=min(frame['MASS37']),right=max(frame['MASS37']))
    ax.set_ylim(bottom=9e-3,top=1e3)
    
    plt.scatter(frame['MASS37'],frame['ctau(37)'],c=frame['r_max'],alpha=1,cmap='jet',vmax=1.2,vmin=.1,s=55)
    plt.colorbar(label='$r_{max}$')
    
    frame_displaced=frameHSCP.loc[frameHSCP['Disp']>1]
    frame_analysis2d=frame_displaced[['MASS37','ctau(37)']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    print(frame_analysis2d)
    alpha_shape = alphashape.alphashape(frame_analysis2d, .099)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='pink',fill=False,zorder=20,lw=2,label='Displaced lepton'))
    
    
    frameHSCP['ctau(37)']=frameHSCP['ctau(37)']
    frame_excluded=frameHSCP.loc[frameHSCP['SModelS_status']=='Excluded']
    print('heeelllooooo')
    print(max(frame_excluded['ctau(37)']))
    
    frame_analysis=frame_excluded.loc[frame_excluded['ctau(37)']<10e3]
    frame_analysis2d=frame_excluded[['MASS37','ctau(37)']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    print(frame_analysis2d)
    alpha_shape = alphashape.alphashape(frame_analysis2d, .002)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='white',fill=False,lw=2,label='HSCP'))
    plt.legend(loc='upper left',framealpha=.6,labelcolor='black')
    #print(alpha_shape)
   # Patch(alpha_shape,'.',c='yellow')
    plt.yscale('log')
    plt.ylabel('$ c\\tau_{H^{\\pm}}$ (m)',fontsize=12)
    plt.xlabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
    plt.title(title)
    plt.savefig(path_to_plot)
    plt.close()
   
    return
    

def comparing_compression(frame_comp,frame_nocomp,title,path_to_plot):

    r_ratio=frame_comp['r_max']/frame_nocomp['r_max']
    #plt.scatter(frame_comp['MASS9000006'],frame_comp['MASS37'],c=r_ratio,alpha=1,cmap='jet',vmax=2,s=45)
    print(min(r_ratio))
    fig, ax = plt.subplots()
    
    ax.set_xlim(left=min(frame_comp['MASS37']),right=max(frame_comp['MASS37']))
    ax.set_ylim(bottom=min(frame_comp['MASS9000006']),top=max(frame_comp['MASS9000006']))
    
    frame_comp_excluded=frame_comp.loc[frame_comp['SModelS_status']=='Excluded']
    frame_comp_excluded=frame_comp_excluded[['MASS37','MASS9000006']]
    frame_comp_excluded=frame_comp_excluded.to_numpy()
    print(frame_comp_excluded)
    alpha_shape = alphashape.alphashape(frame_comp_excluded, .099)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='pink',fill=False,zorder=20,lw=2,label='True'))
    
    
   
    frame_nocomp_excluded=frame_nocomp.loc[frame_nocomp['r_max']<1]
    frame_nocomp_excluded=frame_nocomp_excluded[['MASS37','MASS9000006']]
    frame_nocomp_excluded=frame_nocomp_excluded.to_numpy()
 
    alpha_shape = alphashape.alphashape(frame_nocomp_excluded, .1)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='pink',fill=False,zorder=20,lw=2,label='False'))
    
    plt.scatter(frame_comp['MASS37'],frame_comp['MASS9000006'],c=r_ratio,alpha=1,cmap='jet',vmax=3,vmin=.96,s=45)
    plt.yscale('log')
    plt.colorbar(label='$r_{ratio}=r_{True}/r_{False}$')
    plt.ylabel('$m_{N_{1}}$ (GeV)',fontsize=12)
    plt.xlabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
    plt.legend(title='Compression',loc='upper left')
    
   
    
    
    
    plt.title(title)
    
    plt.savefig(path_to_plot)
    plt.close()
    return
    
    
    


    
path_to_frame='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_50_muons_3.txt'
#path_to_frame='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_delta5_muons_compression.txt'
path_to_onlyHSCPframe='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_50_muons_onlyHSCP_3.txt'
title='Fermionic DM, $\\Delta m=50$ GeV, $ H^\pm\\to \\mu ^\pm  N_1$'

#path_to_plot='static_plots/plot_analysis_larger_delta5_electrons_compression.png'
#path_to_plot_topo='static_plots/plot_topo_larger_delta5_muons_compression.png'
path_to_plot_ctau_curves='plots/plot_curves_ctau_delta50_muons_3_lim900.png'
path_to_plot_curves='plots/plot_curves_delta50_muons_3_lim900.png'
frame=openframe(path_to_frame)
HSCPframe=openframe(path_to_onlyHSCPframe)
#plotterAnalyses(frame,title,path_to_plot)
#plotterTopo(frame,title,path_to_plot_topo)
#plotCurvesTopo(frame,title,path_to_plot_curves)
plotCurvesTopo2(frame,HSCPframe,title,path_to_plot_curves)
plotCurvesTopoCtau2(frame,HSCPframe,title,path_to_plot_ctau_curves)
#plotterTopoHSCPind(frame,title,path_to_plot_topo)

'''
path_to_frame='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_5_electrons_2_compression.txt'
path_to_frame_nocomp='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_5_electrons_2_nocompression.txt'
frame_comp=openframe(path_to_frame)
frame_nocomp=openframe(path_to_frame_nocomp)
title='Fermionic DM, $\\Delta m=5$ GeV, $ H^\pm\\to e^\pm N_1$  '
path_to_plot='plots/comparing_compression_electrons.png'
comparing_compression(frame_comp,frame_nocomp,title,path_to_plot)

'''
