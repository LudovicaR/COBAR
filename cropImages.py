import glob

import pandas as pd
import numpy as np

import cv2

def findCentroid(img, file):
    """Function that detects the centroid and the head position of the fly by applying image processing techniques."""
    
    print(file)
    
    # convert the image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # find the number of rows and columns of the image 
    img_lin = img.shape[0]
    img_col = img.shape[1]
    
    # to find the average of half of the image 
    img_mean = np.uint8(np.mean(img[0:700,:]))
    
    threshold_img = np.zeros_like(img)
    
    # we set a threshold to detect the fly's body at 70% of the average
    for i in range(1,img_lin): 
        for j in range(1,img_col):
            if img[i,j] <= img_mean*0.70:
                threshold_img[i,j] = 255
    
    clean_threshold = threshold_img

    # erosion applied to remove unwanted details, like the lanes borders 
    kernel = np.ones((3,3), np.uint8)
    img_erosion = cv2.erode(threshold_img, kernel, iterations=5)

    clean_erosion = img_erosion
    
    wings_img = np.zeros_like(img)

    # thresholding to detect the fly's body with wings 
    for i in range(1,img_lin): 
        for j in range(1,img_col):
            if img[i,j] <= img_mean*0.90 and img[i,j] >= img_mean*0.50:
                wings_img[i,j] = 255
                
    clean_wings = wings_img
    
    # erosion and dilation to the the fly's body and wings 
    wings_erosion = cv2.erode(wings_img, kernel, iterations=2)
    clean_wings_erosion = wings_erosion
    wings_erode_dilate = cv2.dilate(clean_erosion, kernel, iterations=10)
    
    final_img = np.zeros_like(img)

    for i in range(1,img_lin): 
        for j in range(1,img_col):
            if wings_erode_dilate[i,j] == 255 and clean_wings[i,j] == 255 :
                final_img[i,j] = 255
    
    # final image with only the fly's wings
    final_img = final_img - clean_threshold
    
    img_sample = img_erosion

    # the centroid detection by using connected components 
    output = cv2.connectedComponentsWithStats(img_sample, 4, cv2.CV_32S) 
    
    x_centroid = int(output[3][1][0])
    y_centroid = int(output[3][1][1])
    
    remove_value = False
    add_value = False
    
    # we segment the image in two, based on the location of the centroid
    # we take a small square of pixels, to have a more precise detection
    # this squre is 55 x 55 pixels around the centroid 
    # (if the fly is not at the border)
    if x_centroid-55 > 0:
        part_left = final_img[30:100,(x_centroid-55):x_centroid]
        part_left_track = img_erosion[30:100,(x_centroid-55):x_centroid]
        remove_value = True
    else:
        part_left = final_img[30:100,:x_centroid]
        part_left_track = img_erosion[30:100,:x_centroid]
        
    if x_centroid+55 < len(final_img):
        part_right = final_img[30:100,x_centroid:x_centroid+55]
        part_right_track = img_erosion[30:100,x_centroid:x_centroid+55]
        add_value = True
    else:
        part_right = final_img[30:100,x_centroid:]
        part_right_track = img_erosion[30:100,x_centroid:]
    
    axis_left_x =  part_left_track.shape[0] 
    axis_left_y =  part_left_track.shape[1]
    
    # we count the number of white pixels in the left part of the image
    white_left = 0
    
    for i in range(axis_left_x): 
        for j in range(axis_left_y):
            if part_left[i,j] >= 50 :
                white_left = white_left + 1
    
    print('Part left scored : ' + str(white_left) + ' white pixels.')
    
    axis_right_x =  part_right_track.shape[0]
    axis_right_y =  part_right_track.shape[1]

    # we count the number of white pixels in the right part of the image
    white_right = 0
    
    for i in range(axis_right_x): 
        for j in range(axis_right_y):
            if part_right[i,j] >= 50 :
                white_right = white_right + 1
    
    print('Part right scored : ' + str(white_right) + ' white pixels.')
    
    x_head = 0
    y_head = 0
    
    # the part having the smallest number of white pixels corresponds to the head
    
    if white_left < white_right:
        print('Head is in part left')
        for i in range(0,axis_left_x): 
            for j in range(0,axis_left_y):
                if part_left_track[i,j] == 255 and x_head == 0:
                    
                    if remove_value:
                        x_head = i+x_centroid-55
                    else:
                        x_head = i+x_centroid

                    y_head = j
                    print("head is in part left : "+ str(np.array([i,j])))
    else:
        axis_x =  part_right_track.shape[1]
        axis_y =  part_right_track.shape[0]
        for i in reversed(range(0,axis_x)): 
            for j in reversed(range(0,axis_y)):
                if part_right_track[j,i] == 255 and x_head == 0:
                    
                    if add_value:
                        x_head = i+x_centroid+55
                    else:
                        x_head = i+x_centroid
                    
                    x_head = i+x_centroid
                    y_head = j
                    print("head is in part right : "+ str(np.array([i,j])))
    
    return x_centroid, y_centroid, x_head, y_head


def analyzeImages(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size):
    """Function that performs the images' analysis, for which centroids and head positions are found.
    It stores all the points in csv files and creates videos with indicated the position of the centroid and head on the fly's body.
    """
    
    folders = [f for f in sorted(glob.glob(path + "/**"))]
    
    for folder in folders: 
        
        # to save this data frame in a csv file
        
        files = [f for f in sorted(glob.glob(folder + "/**" + ".jpg"))]
        
        centroidsDf = pd.DataFrame(np.zeros([len(files), 11]),columns=["frame", "fly1_x", "fly1_y", "fly2_x", "fly2_y", "fly3_x", "fly3_y", "fly4_x", "fly4_y", "fly5_x", "fly5_y"]);
        headsDf = pd.DataFrame(np.zeros([len(files), 11]),columns=["frame", "fly1_x", "fly1_y", "fly2_x", "fly2_y", "fly3_x", "fly3_y", "fly4_x", "fly4_y", "fly5_x", "fly5_y"]);
        
        img_array1 = []
        img_array2 = []
        img_array3 = []
        img_array4 = []
        img_array5 = []

        for file in files:
            
            print(file)
            
            centroidsDf["frame"][files.index(file)] = files.index(file)+1
            headsDf["frame"][files.index(file)] = files.index(file)+1
            
            img = cv2.imread(file)
            
            ## FLY 1 ##

            box1 = img[box1_size[0]:box1_size[1], box1_size[2]:box1_size[3]]
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box1, file)   
            
            # add the centroid and head locations on the image 
            box1 = cv2.circle(box1, (x_centroid, y_centroid), 7, (255, 0, 0), -1)
            box1 = cv2.circle(box1, (x_head, y_head), 7, (0, 0, 255), -1)
            img_array1.append(box1)
            
            # add the positions in the final data frame
            centroidsDf["fly1_x"][files.index(file)] = x_centroid
            centroidsDf["fly1_y"][files.index(file)] = y_centroid
            
            headsDf["fly1_x"][files.index(file)] = x_head
            headsDf["fly1_y"][files.index(file)] = y_head
            
            ## FLY 2 ##
            
            box2 = img[box2_size[0]:box2_size[1], box2_size[2]:box2_size[3]]
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box2, file)
            
            # add the centroid and head locations on the image 
            box2 = cv2.circle(box2, (x_centroid, y_centroid), 7, (255, 0, 0), -1)
            box2 = cv2.circle(box2, (x_head, y_head), 7, (0, 0, 255), -1)
            img_array2.append(box2)
            
            # add the positions in the final data frame 
            centroidsDf["fly2_x"][files.index(file)] = x_centroid
            centroidsDf["fly2_y"][files.index(file)] = y_centroid
            
            headsDf["fly2_x"][files.index(file)] = x_head
            headsDf["fly2_y"][files.index(file)] = y_head
            
            ## FLY 3 ##

            box3 = img[box3_size[0]:box3_size[1], box3_size[2]:box3_size[3]]
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box3, file)
            
            # add the centroid and head locations on the image 
            box3 = cv2.circle(box3, (x_centroid, y_centroid), 7, (255, 0, 0), -1)
            box3 = cv2.circle(box3, (x_head, y_head), 7, (0, 0, 255), -1)
            img_array3.append(box3)

            # add the positions in the final data frame
            centroidsDf["fly3_x"][files.index(file)] = x_centroid
            centroidsDf["fly3_y"][files.index(file)] = y_centroid
            
            headsDf["fly3_x"][files.index(file)] = x_head
            headsDf["fly3_y"][files.index(file)] = y_head
            
            ## FLY 4 ##
            
            box4 = img[box4_size[0]:box4_size[1], box4_size[2]:box4_size[3]]
            
            # image processing to get the centroid and head positions
            x_centroid, y_centroid, x_head, y_head = findCentroid(box4, file)
            
            # add the centroid and head locations on the image 
            box4 = cv2.circle(box4, (x_centroid, y_centroid), 7, (255, 0, 0), -1)
            box4 = cv2.circle(box4, (x_head, y_head), 7, (0, 0, 255), -1)
            img_array4.append(box4)
            
            # add the positions in the final data frame
            centroidsDf["fly4_x"][files.index(file)] = x_centroid
            centroidsDf["fly4_y"][files.index(file)] = y_centroid
            
            headsDf["fly4_x"][files.index(file)] = x_head
            headsDf["fly4_y"][files.index(file)] = y_head
            
            ## FLY 5 ##
            
            # the fifth fly is not present in all the genetic strains 
            if (box5_size != []):
                box5 = img[box5_size[0]:box5_size[1], box5_size[2]:box5_size[3]]
                
                # image processing to get the centroid and head positions
                x_centroid, y_centroid, x_head, y_head = findCentroid(box5, file)
                
                # add the centroid and head locations on the image 
                box5 = cv2.circle(box5, (x_centroid, y_centroid), 7, (255, 0, 0), -1)
                box5 = cv2.circle(box5, (x_head, y_head), 7, (0, 0, 255), -1)
                img_array5.append(box5)
                
                # add the positions in the final data frame
                centroidsDf["fly5_x"][files.index(file)] = x_centroid
                centroidsDf["fly5_y"][files.index(file)] = y_centroid
                
                headsDf["fly5_x"][files.index(file)] = x_head
                headsDf["fly5_y"][files.index(file)] = y_head
        
        # save the data frame in a .csv file, 
        # one for the centroids and one for the heads
        centroidsDf.to_csv(folder+"/centroids.csv", index = None, header=True)
        headsDf.to_csv(folder+"/heads.csv", index = None, header=True)
        
        
        ## CREATE THE VIDEOS ##
        
        height, width, _ = box1.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'_1_' + str(folders.index(folder)+1)+ '.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 1.5, size)
        for i in range(len(img_array1)):
            out.write(img_array1[i])
        out.release()
        
        height, width, _ = box2.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'_2_' + str(folders.index(folder)+1)+ '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1.5, size)
        for i in range(len(img_array2)):
            out.write(img_array2[i])
        out.release()
        
        height, width, _ = box3.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'_3_' + str(folders.index(folder)+1)+ '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1.5, size)
        for i in range(len(img_array3)):
            out.write(img_array3[i])
        out.release()
        
        height, width, _ = box4.shape
        size = (width,height)
        out = cv2.VideoWriter('./Videos/'+name_type+'_4_' + str(folders.index(folder)+1)+ '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1.5, size)
        for i in range(len(img_array4)):
            out.write(img_array4[i])
        out.release()
        
        if (box5_size != []):
            height, width, _ = box5.shape
            size = (width,height)
            out = cv2.VideoWriter('./Videos/'+name_type+'_5_' + str(folders.index(folder)+1)+ '.mp4' ,cv2.VideoWriter_fourcc(*'DIVX'), 1.5, size)
            for i in range(len(img_array5)):
                out.write(img_array5[i])
            out.release()
        