import glob

import pandas as pd
import numpy as np
from numpy import linalg as LA

import matplotlib.pyplot as plt
import seaborn as sns

import cv2

def findCentroid(img, file):
    
    print(file)
    
    # convert the image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # find the number of rows and columns of the image 
    img_rows = img.shape[0]
    img_cols = img.shape[1]
    
    # to find the average of half of the image 
    img_mean = np.uint8(np.mean(img[0:700,:]))
    
    threshold_img = np.zeros_like(img)

    for i in range(1,img_rows): 
        for j in range(1,img_cols):
            if img[i,j] <= img_mean*0.70:
                threshold_img[i,j] = 255
    
    kernel = np.ones((3,3), np.uint8)
    img_erosion = cv2.erode(threshold_img, kernel, iterations=5)
    
    wings_img = np.zeros_like(img)

    for i in range(1,img_rows): 
        for j in range(1,img_cols):
            if img[i,j] <= img_mean*0.90 and img[i,j] >= img_mean*0.50:
                wings_img[i,j] = 255
                
    wings_erosion = cv2.erode(wings_img, kernel, iterations=2)
    
    output = cv2.connectedComponentsWithStats(img_erosion, 4, cv2.CV_32S)

    x_centroid = int(output[3][1][0])
    y_centroid = int(output[3][1][1])
    
    if x_centroid-55 > 0:
        part_left = wings_erosion[10:110,(x_centroid-55):x_centroid]
        part_left_track = img_erosion[10:110,(x_centroid-55):x_centroid]
    else:
        part_left = wings_erosion[10:110,:x_centroid]
        part_left_track = img_erosion[10:110,:x_centroid]
        
    if x_centroid+55 < len(wings_erosion):
        part_right = wings_erosion[10:110,x_centroid:x_centroid+55]
        part_right_track = img_erosion[10:110,x_centroid:x_centroid+55]
    else:
        part_right = wings_erosion[10:110,x_centroid:]
        part_right_track = img_erosion[10:110,x_centroid:]
    
    white_left = 0
    
    for i in range(part_left.shape[0]): 
        for j in range(part_left.shape[1]):
            if part_left[i,j] >= 50 :
                white_left = white_left + 1
    
    print('Part left scored : ' + str(white_left) + ' white pixels.')
    
    white_right = 0
    
    for i in range(part_right.shape[0]): 
        for j in range(part_right.shape[1]):
            if part_right[i,j] >= 50 :
                white_right = white_right + 1
    
    print('Part right scored : ' + str(white_right) + ' white pixels.')
    
    x_head = 0
    y_head = 0
    
    if white_left < white_right:
        print('Head is in part left')
        for i in range(0,part_left.shape[1]): 
            for j in range(0,part_left.shape[0]):
                if part_left_track[j,i] == 255 and (x_head == 0 and y_head == 0):
                    x_head = j
                    y_head = i
                    print("head is in part left : ["+ str(x_head) + ", " + str(y_head) + "]")

    else:
        print('Head is in part right')
        for i in reversed(range(0,part_right.shape[1])): 
            for j in reversed(range(0,part_left.shape[0])):
                if part_right_track[j,i] == 255 and (x_head == 0 and y_head == 0):
                    x_head = j
                    y_head = i
                    print("head is in part right : ["+ str(x_head) + ", " + str(y_head) + "]")
    
    return x_centroid, y_centroid, x_head, y_head



def analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size):
    
    folders = [f for f in sorted(glob.glob(path + "/**"))]
    
    for folder in folders: 
        
        # to save this data frame in a csv file
        
        files = [f for f in sorted(glob.glob(folder + "/**"))]
        
        centroidsDf = pd.DataFrame(np.zeros([len(files), 11]),columns=["frame", "fly1_x", "fly1_y", "fly2_x", "fly2_y", "fly3_x", "fly3_y", "fly4_x", "fly4_y", "fly5_x", "fly5_y"]);
        headsDf = pd.DataFrame(np.zeros([len(files), 11]),columns=["frame", "fly1_x", "fly1_y", "fly2_x", "fly2_y", "fly3_x", "fly3_y", "fly4_x", "fly4_y", "fly5_x", "fly5_y"]);
        
        img_array1 = []
        img_array2 = []
        img_array3 = []
        img_array4 = []
        img_array5 = []

        for file in files:
            
            centroidsDf["frame"][files.index(file)] = files.index(file)+1
            headsDf["frame"][files.index(file)] = files.index(file)+1
            
            img = cv2.imread(file)
            
            ## FLY 1 ##

            box1 = img[box1_size[0]:box1_size[1], box1_size[2]:box1_size[3]]
            
            img_array1.append(box1)
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box1, file)
            
            centroidsDf["fly1_x"][files.index(file)] = x_centroid
            centroidsDf["fly1_y"][files.index(file)] = y_centroid
            
            headsDf["fly1_x"][files.index(file)] = x_head
            headsDf["fly1_y"][files.index(file)] = y_head
            
            ## FLY 2 ##
            
            box2 = img[box2_size[0]:box2_size[1], box2_size[2]:box2_size[3]]
            img_array2.append(box2)
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box2, file)
            
            centroidsDf["fly2_x"][files.index(file)] = x_centroid
            centroidsDf["fly2_y"][files.index(file)] = y_centroid
            
            headsDf["fly2_x"][files.index(file)] = x_head
            headsDf["fly2_y"][files.index(file)] = y_head
            
            ## FLY 3 ##
            
            box3 = img[box3_size[0]:box3_size[1], box3_size[2]:box3_size[3]]
            img_array3.append(box3)
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box3, file)
            
            centroidsDf["fly3_x"][files.index(file)] = x_centroid
            centroidsDf["fly3_y"][files.index(file)] = y_centroid
            
            headsDf["fly3_x"][files.index(file)] = x_head
            headsDf["fly3_y"][files.index(file)] = y_head
            
            ## FLY 4 ##
            
            box4 = img[box4_size[0]:box4_size[1], box4_size[2]:box4_size[3]]
            img_array4.append(box4)
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box4, file)
            
            centroidsDf["fly4_x"][files.index(file)] = x_centroid
            centroidsDf["fly4_y"][files.index(file)] = y_centroid
            
            headsDf["fly4_x"][files.index(file)] = x_head
            headsDf["fly4_y"][files.index(file)] = y_head
            
            ## FLY 5 ##
            
            if (box5_size != []):
                box5 = img[box5_size[0]:box5_size[1], box5_size[2]:box5_size[3]]
                img_array5.append(box5)
                
                # image processing to get the centroid and head positions
                x_centroid, y_centroid, x_head, y_head = findCentroid(box5, file)
                
                centroidsDf["fly5_x"][files.index(file)] = x_centroid
                centroidsDf["fly5_y"][files.index(file)] = y_centroid
                
                headsDf["fly5_x"][files.index(file)] = x_head
                headsDf["fly5_y"][files.index(file)] = y_head
        
        centroidsDf.to_csv(folder+"/centroids.csv", index = None, header=True)
        headsDf.to_csv(folder+"/heads.csv", index = None, header=True)

        ## CREATE THE VIDEOS ##

#        height, width, _ = box1.shape
#        size = (width,height)
#        out = cv2.VideoWriter('./Videos/'+name_type+'1_' + str(folders.index(folder))+ '_' + str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
#        for i in range(len(img_array1)):
#            out.write(img_array1[i])
#        out.release()
#        
#        height, width, _ = box2.shape
#        size = (width,height)
#        out = cv2.VideoWriter('./Videos/'+name_type+'2_' + str(folders.index(folder))+ '_' + str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
#        for i in range(len(img_array2)):
#            out.write(img_array2[i])
#        out.release()
#        
#        height, width, _ = box3.shape
#        size = (width,height)
#        out = cv2.VideoWriter('./Videos/'+name_type+'3_' + str(folders.index(folder))+ '_' +str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
#        for i in range(len(img_array3)):
#            out.write(img_array3[i])
#        out.release()
#        
#        height, width, _ = box4.shape
#        size = (width,height)
#        out = cv2.VideoWriter('./Videos/'+name_type+'4_' + str(folders.index(folder))+ '_' + str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
#        for i in range(len(img_array4)):
#            out.write(img_array4[i])
#        out.release()
#        
#        if (box5_size != []):
#            height, width, _ = box5.shape
#            size = (width,height)
#            out = cv2.VideoWriter('./Videos/'+name_type+'5_' + str(folders.index(folder))+ '_' +str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
#            for i in range(len(img_array5)):
#                out.write(img_array5[i])
#            out.release()
        
        
def velocity_calculator(points):
    
    diff=points[-1]-points[0]
    
    time=8*len(points)/56

    v_x=diff[0]/time
    v_y=diff[1]/time
    velocities=[v_x,v_y]

    velocity = LA.norm(velocities)

    return velocity, v_x, v_y

    

