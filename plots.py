import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


def reformatCsv(folder, flies_to_remove):
    """Function responsible of creating new csv files that only take into account informative recordings.
    These recordings that are discarded are stored in the 'flies_to_remove' vector. 
    This choice is based on the visual inspection of all the recordins taken.
    """
    
    # flies_to_remove = ['fly1_x','fly1_y','fly2_x','fly2_y','fly3_x','fly3_y', ,'fly4_x', 'fly4_y','fly5_x','fly5_y']
    
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    centroids[flies_to_remove]=np.nan
    heads[flies_to_remove]=np.nan
    
    # create new csv files where the flies that are not useful for the results have been removed
    centroids.to_csv(folder+ "centroids_sorted.csv", index=False)
    heads.to_csv(folder+ "heads_sorted.csv", index=False)
    

def velocity_calculator(df_centroids):
    """Function that calculates the velocity of each fly.
    'df' is the data frame that contains all the detected centroids"""
    
    if df_centroids.shape[1] == 11:
        flies_x = ['fly1_x', 'fly2_x', 'fly3_x', 'fly4_x', 'fly5_x']
        flies_y = ['fly1_y', 'fly2_y', 'fly3_y', 'fly4_y', 'fly5_y']
    else:
        flies_x = ['fly1_x', 'fly2_x', 'fly3_x', 'fly4_x']
        flies_y = ['fly1_y', 'fly2_y', 'fly3_y', 'fly4_y']
        
    # the time interval in which we applied the stimulation
    stim_time = 8
    
    # maximal number of frames recorded during stimulation 
    max_frames = 56
    
    # the actual stimulation time for this particular set of recordings
    time=stim_time*df_centroids.shape[0]/max_frames
    
    # create the vector with all the time points (one for each frame)
    time_points=range(0,df_centroids[flies_x].shape[0], 5)
    
    # initialize the velocities vectors 
    v_x=[]
    v_y=[]
    #velocities=[]
    
    # calculate the velocities, by using the centroids and the calculated times
    for t in range(len(time_points)): 
        if ((t+1)>=len(time_points))==False:
            first_centroid_x = df_centroids[flies_x].iloc[time_points[t]]
            second_centroid_x = df_centroids[flies_x].iloc[time_points[t+1]]
            diff_x=second_centroid_x-first_centroid_x

            first_centroid_y = df_centroids[flies_y].iloc[time_points[t]]
            second_centroid_y = df_centroids[flies_y].iloc[time_points[t+1]]
            diff_y=second_centroid_y-first_centroid_y

            v_x.append(diff_x/time)
            v_y.append(diff_y/time)
    
    velocity_per_fly=[]
    for fly in range(5):
        for vel in range(0,len(v_x)):
            velocity_per_fly.append(np.sqrt(v_x[vel][fly]**2+\
                                            v_y[vel][fly]**2))
    
    return velocity_per_fly, v_x, v_y


def velocity_boxplots(df, velocity_ID, gene_name, num_trials):
    """Function to create boxplots for the flies velocities."""
    
    plt.figure(figsize=(15, 7))
    plt.rcParams['font.size'] = 16
    ax=sns.boxplot(x="fly", y=velocity_ID, data=df)
    plt.xlabel('Flies')
    plt.ylabel(velocity_ID+"(in pixels/second)")
    plt.title('%s for every fly, Gene %s for %s trial(s).png' %(velocity_ID, gene_name , num_trials))
    plt.savefig('Boxplot_%s_%s for %s trial(s).png' %(gene_name, velocity_ID, num_trials))
    #plt.show()


def velocity_analysis(gene_name, num_trials):
    """Function that calls the 'velocity_boxplots' and generate the plots for all the trials for a specific gene strain"""
    
    flies = np.array([1,2,3,4,5])
    struct_df = {'fly':np.tile(flies,num_trials)}
    df_vel = pd.DataFrame(struct_df).reset_index().drop('index', 1)

    all_velocities=[]
    all_vx=[]
    all_vy=[]

    for trial in range(num_trials):
        if trial==0:
            centroids = pd.read_csv("Behavior_Flies_selected/" + str(gene_name)+"/"+str(gene_name)+"_"+str(trial+1)+"/centroids_sorted.csv")

            velocity_per_fly, v_x, v_y = velocity_calculator(centroids)
            
            for speeds in range(0,len(velocity_per_fly),len(v_x)):
                    all_velocities.append(np.nanmean(velocity_per_fly[0+speeds:speeds+len(v_x)]))
            all_vx.append(np.nanmean(v_x,axis=0))
            all_vy.append(np.nanmean(v_y,axis=0))

        else:
            centroids = pd.read_csv("Behavior_Flies_selected/" + str(gene_name)+"/"+str(gene_name)+"_"+str(trial+1)+"/centroids_sorted.csv")

            velocity_per_fly, v_x, v_y = velocity_calculator(centroids)

            for speeds in range(0,len(velocity_per_fly),len(v_x)):
                all_velocities.append(np.nanmean(velocity_per_fly[0+speeds:speeds+len(v_x)]))
            all_vx.append(np.nanmean(v_x,axis=0))
            all_vy.append(np.nanmean(v_y,axis=0))
    
    #print(all_vx[0])      
    df_vel['v_x']=np.concatenate(all_vx)
    df_vel['v_y']=np.concatenate(all_vy)
    df_vel['velocity']=all_velocities

    velocity_boxplots(df_vel, "velocity",gene_name, num_trials)
    velocity_boxplots(df_vel, "v_x",gene_name, num_trials)
    velocity_boxplots(df_vel, "v_y",gene_name, num_trials)
    
    