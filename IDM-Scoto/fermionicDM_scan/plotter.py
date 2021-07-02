
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import alphashape
from matplotlib.patches import Patch
from descartes import PolygonPatch


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
    plt.colorbar(label='$r_{max}$')
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
    plt.xlabel('$ m_{N_{1}}$ (GeV)',fontsize=12)
    plt.ylabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
    plt.title(title)
       
        
    plt.savefig(path_to_plot)
    plt.close()
    return
        
    

def plotCurvesTopo2(frame,frameHSCP,title,path_to_plot):


    fig, ax = plt.subplots()
    #ax.scatter(frame['m(N1)'],frame['m(H+)'],c=frame['r_max'],alpha=1,cmap='jet',vmax=1.2,vmin=.1)
    #ax.set_xscale('log')
   # plt.colorbar()
    
    ax.set_xlim(left=min(frame['m(H+)']),right=max(frame['m(H+)']))
    ax.set_ylim(bottom=min(frame['m(N1)']),top=max(frame['m(N1)']))
    
    plt.scatter(frame['m(H+)'],frame['m(N1)'],c=frame['r_max'],alpha=1,cmap='jet',vmax=1.2,vmin=.1)
    plt.colorbar(label='$r_{max}$')
    
    frame_displaced=frameHSCP.loc[frameHSCP['Disp']>1]
    frame_analysis2d=frame_displaced[['m(H+)','m(N1)']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    print(frame_analysis2d)
    alpha_shape = alphashape.alphashape(frame_analysis2d, .05)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='pink',fill=False,zorder=20,lw=2,label='Displaced lepton'))
    
    
    
    frame_excluded=frameHSCP.loc[frameHSCP['SModelS_status']=='Excluded']
    frame_analysis=frame_excluded.loc[frame_excluded['Tx']!='TSmuSmuDisp']
    frame_analysis2d=frame_analysis[['m(H+)','m(N1)']]
    frame_analysis2d=frame_analysis2d.to_numpy()
    print(frame_analysis2d)
    alpha_shape = alphashape.alphashape(frame_analysis2d, .05)
    print(alpha_shape)
    ax.add_patch(PolygonPatch(alpha_shape, alpha=1,ec='white',fill=False,lw=2,label='HSCP'))
    plt.legend(loc='upper left',framealpha=.6,labelcolor='black')
    #print(alpha_shape)
   # Patch(alpha_shape,'.',c='yellow')
    plt.yscale('log')
    plt.ylabel('$ m_{N_{1}}$ (GeV)',fontsize=12)
    plt.xlabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
    plt.title(title)
    plt.savefig(path_to_plot)
    plt.close()
   
    return
 
    
  
    

   


    
path_to_frame='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_delta5_muons_compression.txt'
#path_to_frame='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_delta5_muons_compression.txt'
path_to_onlyHSCPframe='/Users/humberto/Documents/work/Scoto-IDM/smodels-dev/smodels/frame_delta5_muons_compression_onlyHSCP.txt'
title='Fermionic DM, $\\Delta m=5$ GeV, $ H^\pm\\to \\mu^\pm N_1$  '

path_to_plot='static_plots/plot_analysis_larger_delta5_electrons_compression.png'
path_to_plot_topo='static_plots/plot_topo_larger_delta5_muons_compression.png'
path_to_plot_curves='plots/plot_curves_intersections_delta5_muons.png'
frame=openframe(path_to_frame)
HSCPframe=openframe(path_to_onlyHSCPframe)
#plotterAnalyses(frame,title,path_to_plot)
#plotterTopo(frame,title,path_to_plot_topo)
#plotCurvesTopo(frame,title,path_to_plot_curves)
plotCurvesTopo2(frame,HSCPframe,title,path_to_plot_curves)
#plotterTopoHSCPind(frame,title,path_to_plot_topo)
