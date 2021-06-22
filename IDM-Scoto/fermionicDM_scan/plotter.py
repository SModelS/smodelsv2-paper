
import matplotlib.pyplot as plt
import pandas as pd






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
    plt.plot(frame_nonexcluded['m(N1)'],frame_nonexcluded['m(H+)'],'.',label ='Allowed',color='grey')
    
    frame_almostexcluded=frame_nonexcluded.loc[frame_nonexcluded['r_max']>.5]
    plt.plot(frame_almostexcluded['m(N1)'],frame_almostexcluded['m(H+)'],'.',label ='.5<r<1',color='black')
    
    ##Plotting excluded points by analysis
    
    j=0
    for analysis in analysis_list:
    
        frame_analysis=frame_excluded.loc[frame_excluded['Analysis']==analysis]
        plt.plot(frame_analysis['m(N1)'],frame_analysis['m(H+)'],'.',label =analysis)
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
        plt.plot(frame_analysis['m(N1)'],frame_analysis['m(H+)'],'.',label =analysis)
        plt.xscale('log')
        
        j=j+1
    
    
    plt.xlabel('$ m_{N_{1}}$ (GeV)',fontsize=12)
    plt.ylabel('$ m_{H^{\\pm}}$ (GeV)',fontsize=12)
    plt.legend()
    plt.title(title)
    plt.savefig(path_to_plot)
    plt.close()
    
    
    return
    
path_to_frame='data_frames/frame_delta5_electrons.txt'
title='Fermionic DM - $ \\Delta $ 5 (GeV) - $ H^{\\pm} -> e, N_{1} $  '

path_to_plot='static_plots/plot_analysis_larger_delta5_electrons.png'
path_to_plot_topo='static_plots/plot_topo_larger_delta5_electrons.png'
frame=openframe(path_to_frame)
plotterAnalyses(frame,title,path_to_plot)
plotterTopo(frame,title,path_to_plot_topo)
