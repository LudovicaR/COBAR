import numpy as np

import cropImages as crop
import plots 

"""Dorsal"""
path = 'Behavior_Flies_selected/Dorsal'
name_type = 'dorsal'

#first box: 
box1_size = [80, 200, 300, 1050]

#second box: 
box2_size = [250, 380, 300, 1050]

#third box:
box3_size = [420, 540, 300, 1050]

#fourth box: 
box4_size = [600, 700, 300, 1050]

#fifth box: 
box5_size = [770, 870, 300, 1050]

# average size of the lanes (in pixels)
size_1_x = np.mean([box1_size[1]-box1_size[0], 
                      box2_size[1]-box2_size[0], 
                      box3_size[1]-box3_size[0], 
                      box4_size[1]-box4_size[0], 
                      box5_size[1]-box5_size[0]])

size_1_y = np.mean([box1_size[3]-box1_size[2], 
                      box2_size[3]-box2_size[2], 
                      box3_size[3]-box3_size[2], 
                      box4_size[3]-box4_size[2], 
                      box5_size[3]-box5_size[2]])


# to generate the .csv files with the centroids and head positions
#crop.analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""GFP"""
path = 'Behavior_Flies_selected/GFP'
name_type = 'gfp'

#first box: 
box1_size = [120, 240, 300, 1050]

#second box: 
box2_size = [280, 410, 300, 1050]

#third box:
box3_size = [445, 570, 300, 1050]

#fourth box: 
box4_size = [615, 730, 300, 1050]

#fifth box: 
box5_size = [785, 890, 300, 1050]

# average size of the lanes (in pixels)
size_2_x = np.mean([box1_size[1]-box1_size[0], 
                      box2_size[1]-box2_size[0], 
                      box3_size[1]-box3_size[0], 
                      box4_size[1]-box4_size[0], 
                      box5_size[1]-box5_size[0]])

size_2_y = np.mean([box1_size[3]-box1_size[2], 
                      box2_size[3]-box2_size[2], 
                      box3_size[3]-box3_size[2], 
                      box4_size[3]-box4_size[2], 
                      box5_size[3]-box5_size[2]])

# to generate the .csv files with the centroids and head positions
#crop.analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""EagDN"""
path = 'Behavior_Flies_selected/EagDN'
name_type = 'eagdn'

#first box: 
box1_size = [70, 180, 300, 1050]

#second box: 
box2_size = [215, 340, 300, 1050]

#third box:
box3_size = [390, 520, 300, 1050]

#fourth box: 
box4_size = [550, 680, 300, 1050]

#fifth box: 
box5_size = [730, 835, 300, 1050]

# average size of the lanes (in pixels)
size_3_x = np.mean([box1_size[1]-box1_size[0], 
                      box2_size[1]-box2_size[0], 
                      box3_size[1]-box3_size[0], 
                      box4_size[1]-box4_size[0], 
                      box5_size[1]-box5_size[0]])

size_3_y = np.mean([box1_size[3]-box1_size[2], 
                      box2_size[3]-box2_size[2], 
                      box3_size[3]-box3_size[2], 
                      box4_size[3]-box4_size[2], 
                      box5_size[3]-box5_size[2]])

# to generate the .csv files with the centroids and head positions
#crop.analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""TNT"""
path = 'Behavior_Flies_selected/TNT'
name_type = 'tnt'

#first box: 
box1_size = [90, 210, 295, 1080]

#second box: 
box2_size = [260, 380, 295, 1075]

#third box:
box3_size = [425, 555, 300, 1075]

#fourth box: 
box4_size = [595, 715, 300, 1075]

#fifth box: 
box5_size = [760, 880, 300, 1070]

# average size of the lanes (in pixels)
size_4_x = np.mean([box1_size[1]-box1_size[0], 
                      box2_size[1]-box2_size[0], 
                      box3_size[1]-box3_size[0], 
                      box4_size[1]-box4_size[0], 
                      box5_size[1]-box5_size[0]])

size_4_y = np.mean([box1_size[3]-box1_size[2], 
                      box2_size[3]-box2_size[2], 
                      box3_size[3]-box3_size[2], 
                      box4_size[3]-box4_size[2], 
                      box5_size[3]-box5_size[2]])

# to generate the .csv files with the centroids and head positions
#crop.analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""ShalRNA"""
path = 'Behavior_Flies_selected/ShalRNA'
name_type = 'shalrna'

#first box: 
box1_size = [85, 210, 305, 1080]

#second box: 
box2_size = [255, 390, 305, 1075]

#third box:
box3_size = [425, 555, 305, 1075]

#fourth box: 
box4_size = [590, 715, 305, 1075]

#fifth box: 
box5_size = [760, 880, 305, 1075]

# average size of the lanes (in pixels)
size_5_x = np.mean([box1_size[1]-box1_size[0], 
                      box2_size[1]-box2_size[0], 
                      box3_size[1]-box3_size[0], 
                      box4_size[1]-box4_size[0], 
                      box5_size[1]-box5_size[0]])

size_5_y = np.mean([box1_size[3]-box1_size[2], 
                      box2_size[3]-box2_size[2], 
                      box3_size[3]-box3_size[2], 
                      box4_size[3]-box4_size[2], 
                      box5_size[3]-box5_size[2]])

# to generate the .csv files with the centroids and head positions
#crop.analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""IMPTNT"""
path = 'Behavior_Flies_selected/IMPTNT'
name_type = 'imptnt'

#first box: 
box1_size = [180, 305, 260, 1035]

#second box: 
box2_size = [350, 475, 265, 1035]

#third box:
box3_size = [510, 635, 270, 1035]

#fourth box: 
box4_size = [675, 795, 270, 1035]

#fifth box: 
box5_size = [] # No Flies

# average size of the lanes (in pixels)
size_6_x = np.mean([box1_size[1]-box1_size[0], 
                      box2_size[1]-box2_size[0], 
                      box3_size[1]-box3_size[0], 
                      box4_size[1]-box4_size[0]])

size_6_y = np.mean([box1_size[3]-box1_size[2], 
                      box2_size[3]-box2_size[2], 
                      box3_size[3]-box3_size[2], 
                      box4_size[3]-box4_size[2]])

# to generate the .csv files with the centroids and head positions
#crop.analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""Hunchback"""
path = 'Behavior_Flies_selected/Hunchback'
name_type = 'hunchback'

#first box: 
box1_size = [70, 195, 300, 1050]

#second box: 
box2_size = [235, 365, 300, 1050]

#third box:
box3_size = [400, 530, 300, 1050]

#fourth box: 
box4_size = [565, 685, 300, 1050]

#fifth box: 
box5_size = [730, 845, 300, 1050]

# average size of the lanes (in pixels)
size_7_x = np.mean([box1_size[1]-box1_size[0], 
                      box2_size[1]-box2_size[0], 
                      box3_size[1]-box3_size[0], 
                      box4_size[1]-box4_size[0], 
                      box5_size[1]-box5_size[0]])

size_7_y = np.mean([box1_size[3]-box1_size[2], 
                      box2_size[3]-box2_size[2], 
                      box3_size[3]-box3_size[2], 
                      box4_size[3]-box4_size[2], 
                      box5_size[3]-box5_size[2]])

# to generate the .csv files with the centroids and head positions
#crop.analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)

# average size of all the lanes, for all the different genetic strains
# this is an approximation used to calculate the velocity in mm/s instead of 
# pixels/s, which is a more informative measure 
avg_size_x = np.mean([size_1_x, size_2_x, size_3_x, size_4_x, size_5_x, size_6_x, size_7_x])
avg_size_y = np.mean([size_1_y, size_2_y, size_3_y, size_4_y, size_5_y, size_6_y, size_7_y])


## Create the plots with the flies velocities 

plots.velocity_analysis("Dorsal",10)
plots.velocity_analysis("GFP",10)
plots.velocity_analysis("EagDN",10)
plots.velocity_analysis("TNT",10)
plots.velocity_analysis("ShalRNA",10)
plots.velocity_analysis("IMPTNT",10)
plots.velocity_analysis("Hunchback",10)


