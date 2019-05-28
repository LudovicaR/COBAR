import pandas as pd
import numpy as np
from math import atan, degrees

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
    

def velocity_calculator(df_centroids, pixels_x, pixels_y):
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
            # we find the distance covered  in x and convert it in mm
            size_lane_x = 3.5
            diff_x=(second_centroid_x-first_centroid_x)*(size_lane_x/pixels_x)

            first_centroid_y = df_centroids[flies_y].iloc[time_points[t]]
            second_centroid_y = df_centroids[flies_y].iloc[time_points[t+1]]
            # we find the distance covered in y and convert it in mm
            size_lane_y = 22
            diff_y=(second_centroid_y-first_centroid_y)*(size_lane_y/pixels_y)

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
    plt.ylabel(velocity_ID+"(in mm/second)")
    plt.title('%s for every fly, Gene %s for %s trial(s).png' %(velocity_ID, gene_name , num_trials))
    plt.savefig('Boxplot_%s_%s for %s trial(s).png' %(gene_name, velocity_ID, num_trials))
    #plt.show()


def velocity_analysis(gene_name, num_trials, pixels_x, pixels_y):
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

            velocity_per_fly, v_x, v_y = velocity_calculator(centroids, pixels_x, pixels_y)
            
            for speeds in range(0,len(velocity_per_fly),len(v_x)):
                    all_velocities.append(np.nanmean(velocity_per_fly[0+speeds:speeds+len(v_x)]))
            all_vx.append(np.nanmean(v_x,axis=0))
            all_vy.append(np.nanmean(v_y,axis=0))

        else:
            centroids = pd.read_csv("Behavior_Flies_selected/" + str(gene_name)+"/"+str(gene_name)+"_"+str(trial+1)+"/centroids_sorted.csv")

            velocity_per_fly, v_x, v_y = velocity_calculator(centroids, pixels_x, pixels_y)

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
    
def orientation_graph(df, fly_index, gene_name):
    
    plt.figure(figsize=[22,3.5])

    plt.gcf().subplots_adjust(bottom=0.2)
    
    fly_x='fly'+str(fly_index)+'_x'
    fly_y='fly'+str(fly_index)+'_y'
    
    ypix=122
    xpix=760 
    
    o_x=(df[fly_x]*22)/xpix
    o_y=(df[fly_y]*3.5)/ypix
    
    #plt.gca().invert_yaxis()
    for i in range(0, len(o_x), 1):
        if i == 0:
            plt.plot(o_x[i:i+2],o_y[i:i+2], 'go-')
            
        elif i == (len(o_x)-1) :
            plt.plot(o_x[i:i+2],o_y[i:i+2], 'bo-')
        else: 
            plt.plot( o_x[i:i+2],o_y[i:i+2], 'ro-')

    plt.ylabel('Y coordinate of the centroid')
    plt.xlabel('X coordinate of the centroid')
    
    plt.title('%s: Trace for fly #%s' %(gene_name, fly_index))
    plt.savefig('%s_Trace_for_fly_#%s.png' %(gene_name, fly_index))
    plt.show()

def get_cardinal(head_x, head_y, centroid_x, centroid_y):
    directions = {0:"N", 45:"NE", 90:"E", 135:"SE", 180:"S",
              225:"SW", 270:"W", 315:"NW", 360:"N"}
    
    dx, dy = head_x - centroid_x, head_y - centroid_y
    #dx, dy = a[0]-b[0], a[1]-b[1]
    all_directions=[]
    diff=dy/dx
    i=0
    for d in diff:
        if dx.empty:
            orientation = "N"
        else: 
            angle = degrees(atan(d))+90 #+90 to take into account TKinters coordinate system.      
            if dx[i] > 0:
                angle += 180
            orientation = directions[min(directions, key=lambda x: abs(x-angle))]

        all_directions.append(orientation)
        i+=1
    return all_directions

def orientation_piechart(df_orientation, fly_index,gene_name):
    
    plt.figure()
    
    E = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'E'])
    SE = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'SE'])
    NE = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'NE'])
    N = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'N'])
    W = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'W'])
    NW = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'NW'])
    SW = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'SW'])
    S = len(df_orientation['Orientation'][df_orientation['Orientation'] == 'S'])
    
    orient_labels={'W':[W], 'NW': [NW], 'N':[N], 'NE':[NE], 'E':[E],'SE':[SE], 'S':[S], 'SW':[SW]}
    directions=pd.DataFrame(data=orient_labels)
    #colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    # Data to plot
    
    print(directions.iloc[0][directions.iloc[0]!=0].index.tolist())
    labels = directions.iloc[0][directions.iloc[0]!=0].index.tolist()
    sizes = directions.iloc[0][directions.iloc[0]!=0].tolist()
    #colors_to_use = colors[len(directions.iloc[0][directions.iloc[0]!=0])]
    

    # Plot
    plt.rcParams['font.size'] = 16
    plt.pie(sizes, labels=labels,
                    autopct='%1.1f%%', startangle=140)
    
    plt.title('%s: Orientation for fly #%s' %(gene_name, fly_index) )

    plt.axis('equal')
    plt.savefig('%s_Orientation_Pie_Chart_for_fly_#%s.png' %(gene_name, fly_index))
    plt.show()

def generate_orientation_plots():
    """ ... """
    
    ## first plot for the Dorsal factor
    folder = "Behavior_Flies_selected/Dorsal/Dorsal_2/"
    fly_num = 2
    gene_name="Dorsal"
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    
    # plots showing the movement of the fly on the lane 
    orientation_graph(heads, fly_num,gene_name)
    
    all_directions = get_cardinal(centroids["fly"+str(fly_num)+"_x"], centroids["fly"+str(fly_num)+"_x"],\
                                 heads["fly"+str(fly_num)+"_x"],heads["fly"+str(fly_num)+"_y"])
    df_orientation=pd.DataFrame(data=all_directions, columns=['Orientation'])
    
    # plots the orientation of the fly's head 
    orientation_piechart(df_orientation,fly_num,gene_name)
    
    ## second plot for the eagdn factor
    folder = "Behavior_Flies_selected/EagDN/EagDN_4/"
    fly_num = 4
    gene_name="EagDN"
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    
    # plots showing the movement of the fly on the lane 
    orientation_graph(heads, fly_num,gene_name)
    
    all_directions = get_cardinal(centroids["fly"+str(fly_num)+"_x"], centroids["fly"+str(fly_num)+"_x"],\
                                 heads["fly"+str(fly_num)+"_x"],heads["fly"+str(fly_num)+"_y"])
    df_orientation=pd.DataFrame(data=all_directions, columns=['Orientation'])
    
    # plots the orientation of the fly's head 
    orientation_piechart(df_orientation,fly_num,gene_name)
    
    ## third plot for the gfp factor
    folder = "Behavior_Flies_selected/GFP/GFP_9/"
    fly_num = 2
    gene_name="GFP"
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    
    # plots showing the movement of the fly on the lane 
    orientation_graph(heads, fly_num,gene_name)
    
    all_directions = get_cardinal(centroids["fly"+str(fly_num)+"_x"], centroids["fly"+str(fly_num)+"_x"],\
                                 heads["fly"+str(fly_num)+"_x"],heads["fly"+str(fly_num)+"_y"])
    df_orientation=pd.DataFrame(data=all_directions, columns=['Orientation'])
    
    # plots the orientation of the fly's head 
    orientation_piechart(df_orientation,fly_num,gene_name)
    
    ## fourth plot for the hunchback factor
    folder = "Behavior_Flies_selected/Hunchback/Hunchback_7/"
    fly_num = 3
    gene_name="Hunchback"
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    
    # plots showing the movement of the fly on the lane 
    orientation_graph(heads, fly_num,gene_name)
    
    all_directions = get_cardinal(centroids["fly"+str(fly_num)+"_x"], centroids["fly"+str(fly_num)+"_x"],\
                                 heads["fly"+str(fly_num)+"_x"],heads["fly"+str(fly_num)+"_y"])
    df_orientation=pd.DataFrame(data=all_directions, columns=['Orientation'])
    
    # plots the orientation of the fly's head 
    orientation_piechart(df_orientation,fly_num,gene_name)
    
    ## fifth plot for the imptnt factor
    folder = "Behavior_Flies_selected/IMPTNT/IMPTNT_4/"
    fly_num = 2
    gene_name="IMPTNT"
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    
    # plots showing the movement of the fly on the lane 
    orientation_graph(heads, fly_num,gene_name)
    
    all_directions = get_cardinal(centroids["fly"+str(fly_num)+"_x"], centroids["fly"+str(fly_num)+"_x"],\
                                 heads["fly"+str(fly_num)+"_x"],heads["fly"+str(fly_num)+"_y"])
    df_orientation=pd.DataFrame(data=all_directions, columns=['Orientation'])
    
    # plots the orientation of the fly's head 
    orientation_piechart(df_orientation,fly_num,gene_name)
    
    ## sixth plot for the shalrna factor
    folder = "Behavior_Flies_selected/ShalRNA/ShalRNA_5/"
    fly_num = 3
    gene_name="ShalRNA"
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    
    # plots showing the movement of the fly on the lane 
    orientation_graph(heads, fly_num,gene_name)
    
    all_directions = get_cardinal(centroids["fly"+str(fly_num)+"_x"], centroids["fly"+str(fly_num)+"_x"],\
                                 heads["fly"+str(fly_num)+"_x"],heads["fly"+str(fly_num)+"_y"])
    df_orientation=pd.DataFrame(data=all_directions, columns=['Orientation'])
    
    # plots the orientation of the fly's head 
    orientation_piechart(df_orientation,fly_num,gene_name)
    
    ## seventh plot for the tnt factor
    folder = "Behavior_Flies_selected/TNT/TNT_3/"
    fly_num = 5
    gene_name="TNT"
    centroids = pd.read_csv(folder+"centroids.csv")
    heads = pd.read_csv(folder+"heads.csv")
    
    # plots showing the movement of the fly on the lane 
    orientation_graph(heads, fly_num,gene_name)
    
    all_directions = get_cardinal(centroids["fly"+str(fly_num)+"_x"], centroids["fly"+str(fly_num)+"_x"],\
                                 heads["fly"+str(fly_num)+"_x"],heads["fly"+str(fly_num)+"_y"])
    df_orientation=pd.DataFrame(data=all_directions, columns=['Orientation'])
    
    # plots the orientation of the fly's head 
    orientation_piechart(df_orientation,fly_num,gene_name)
    
    
 
    