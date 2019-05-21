import glob

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import cv2
#import numpy as np
#from matplotlib import pyplot as plt

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
    
    clean_threshold = threshold_img
    
    kernel = np.ones((3,3), np.uint8)
    img_erosion = cv2.erode(threshold_img, kernel, iterations=5)
    
    clean_erosion = img_erosion
    
    wings_img = np.zeros_like(img)

    for i in range(1,img_rows): 
        for j in range(1,img_cols):
            if img[i,j] <= img_mean*0.90 and img[i,j] >= img_mean*0.50:
                wings_img[i,j] = 255
                
    clean_wings = wings_img
    wings_erosion = cv2.erode(wings_img, kernel, iterations=2)
    clean_wings_erosion = wings_erosion
    
    img_sample = img_erosion
    output = cv2.connectedComponentsWithStats(img_sample, 4, cv2.CV_32S)
    label_img = output[1].astype(np.uint8)
    
    x_centroid = int(output[3][1][0])
    y_centroid = int(output[3][1][1])
    
    ### CENTROID COORDINATES ###
    #centroid = np.array(x_centroid, y_centroid)
    
    part_left = wings_erosion[10:110,(x_centroid-60):x_centroid]
    part_right = wings_erosion[10:110,x_centroid:x_centroid+60]
    part_left_track = img_erosion[10:110,(x_centroid-60):x_centroid]
    part_right_track = img_erosion[10:110,x_centroid:x_centroid+60]
    
    axis_x =  part_left.shape[1] 
    axis_y =  part_left.shape[0] 
    
    white_left = 0
    
    for i in range(axis_y): 
        for j in range(axis_x):
            if part_left[i,j] >= 50 :
                white_left = white_left + 1
    
    print('Part left scored : ' + str(white_left) + ' white pixels.')
    
    image_length_two =  part_right.shape[1]
    image_height_two =  part_right.shape[0]
    
    white_right = 0
    
    for i in range(axis_y): 
        for j in range(axis_x):
            if part_right[i,j] >= 50 :
                white_right = white_right + 1
    
    print('Part right scored : ' + str(white_right) + ' white pixels.')
    
    if white_left < white_right :
        print('Head is in part left')
    else :
        print('Head is in part right')

    head = []
    
    if white_left < white_right:
        print('Head is in part left')
        for i in range(0,axis_x): 
            for j in range(0,axis_y):
                if part_left_track[j,i] == 255 and head == []:
                    head.append(np.array([i,j]))
                    print("head is in part left : "+ str(np.array([i,j])))
                    img_head = cv2.circle(img[10:110,(x_centroid-60):x_centroid],(head[0][0],head[0][1]), 7, (255,255,255), -1)
                    plt.imshow(img_head)
                    plt.show()
    else:
        for i in reversed(range(0,axis_x)): 
            for j in reversed(range(0,axis_y)):
                if part_right_track[j,i] == 255 and head == []:
                    head.append(np.array([i,j]))
                    print("head is in part right : "+ str(np.array([i,j])))
                    img_head = cv2.circle(img[10:110,x_centroid:x_centroid+60],(head[0][0],head[0][1]), 7, (255,255,255), -1)
                    plt.imshow(img_head)
                    plt.show()



def analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size):
    
    # initiailze data frame --> gene 
    geneDf = pd.DataFrame(np.zeros([50, 5]),columns=["gene", "trial", "fly", "centroid", "head"]);
    geneDf = geneDf.astype("object")
    geneDf["gene"] = name_type
    
    folders = [f for f in sorted(glob.glob(path + "/**"))]
    
    for folder in folders: 

        # initialize data frame --> trial
        geneDf["trial"][5*folders.index(folder):5*(folders.index(folder)+1)] = np.repeat(folders.index(folder)+1, 5)
        geneDf["fly"][5*folders.index(folder):5*(folders.index(folder)+1)] = [1, 2, 3, 4, 5]
        
        files = [f for f in sorted(glob.glob(folder + "/**"))]
        img_array1 = []
        centroid_1 = []
        img_array2 = []
        centroid_2 = []
        img_array3 = []
        centroid_3 = []
        img_array4 = []
        centroid_4 = []
        img_array5 = []
        centroid_5 = []
        for file in files:
            img = cv2.imread(file)

            box1 = img[box1_size[0]:box1_size[1], box1_size[2]:box1_size[3]]
            # image processing to get centroid 
            # add centroid to data frame
            img_array1.append(box1)
            
            findCentroid(box1, file)
            
            centroid_1.append([]) # to be completed with output of image processing functions 
            
            cv2.imwrite(file+"_1.jpg", box1);
            
            box2 = img[box2_size[0]:box2_size[1], box2_size[2]:box2_size[3]]
            img_array2.append(box2)
            
            box3 = img[box3_size[0]:box3_size[1], box3_size[2]:box3_size[3]]
            img_array3.append(box3)
            
            box4 = img[box4_size[0]:box4_size[1], box4_size[2]:box4_size[3]]
            img_array4.append(box4)
            
            if (box5_size != []):
                box5 = img[box5_size[0]:box5_size[1], box5_size[2]:box5_size[3]]
                img_array5.append(box5)
            
        ## Remember to convert the lists with all the centroids in np.arrays 
        #np.asarray()
        
        geneDf["centroid"][5*folders.index(folder):5*(folders.index(folder)+1)] = [
                centroid_1, centroid_2, centroid_3, centroid_4, centroid_5]
        
        height, width, _ = box1.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'1_' + str(folders.index(folder))+ '_' + str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
        for i in range(len(img_array1)):
            out.write(img_array1[i])
        out.release()
        
        height, width, _ = box2.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'2_' + str(folders.index(folder))+ '_' + str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
        for i in range(len(img_array2)):
            out.write(img_array2[i])
        out.release()
        
        height, width, _ = box3.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'3_' + str(folders.index(folder))+ '_' +str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
        for i in range(len(img_array3)):
            out.write(img_array3[i])
        out.release()
        
        height, width, _ = box4.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'4_' + str(folders.index(folder))+ '_' + str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
        for i in range(len(img_array4)):
            out.write(img_array4[i])
        out.release()
        
        if (box5_size != []):
            height, width, _ = box5.shape
            size = (width,height)
            out = cv2.VideoWriter('./Videos/'+name_type+'5_' + str(folders.index(folder))+ '_' +str(files.index(file)) + '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
            for i in range(len(img_array5)):
                out.write(img_array5[i])
            out.release()
    
    return geneDf

