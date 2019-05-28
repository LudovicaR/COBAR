import numpy as np
import cv2
import glob

import matplotlib as plt

folder = "Behavior_Flies/GFP/GFP_3"

files = [f for f in sorted(glob.glob(folder + "/**" + ".jpg"))] 

img_array = []

for file in files[0:21]: # we just take the frames without stimulation 
    img = cv2.imread(file)
    img_original = img[280:410, 300:1050]
    
    img = img_original
    
    # image processing to get the centroid and head positions
    
    # convert the image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    # find the number of rows and columns of the image 
    img_lin = img.shape[0]
    img_col = img.shape[1]
        
    # to find the average of half of the image 
    img_mean = np.uint8(np.mean(img[0:700,:]))
        
    threshold_img = np.zeros_like(img)
    
    for i in range(1,img_lin): 
        for j in range(1,img_col):
            if img[i,j] <= img_mean*0.70:
                threshold_img[i,j] = 255
    
    clean_threshold = threshold_img
    
    kernel = np.ones((3,3), np.uint8)
    img_erosion = cv2.erode(threshold_img, kernel, iterations=7)
    
    clean_erosion = img_erosion
    
    wings_img = np.zeros_like(img)
    
    for i in range(1,img_lin):     
        for j in range(1,img_col):
            if img[i,j] <= img_mean*0.90 and img[i,j] >= img_mean*0.50:
                wings_img[i,j] = 255
                
    clean_wings = wings_img
    
    wings_erosion = cv2.erode(wings_img, kernel, iterations=2)
    clean_wings_erosion = wings_erosion
    
    wings_erode_dilate = cv2.dilate(clean_erosion, kernel, iterations=10)
    
    final_img = np.zeros_like(img)
    
    for i in range(1,img_lin): 
        for j in range(1,img_col):
            if wings_erode_dilate[i,j] == 255 and clean_wings[i,j] == 255 and wings_erode_dilate[i,j] == 255 :
                final_img[i,j] = 255 
                    
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
                    y_head = j
                    print("head is in part right : "+ str(np.array([i,j])))
                    
    
    # add images with centroid and head positions to create video
    
    img_original = cv2.circle(img_original, (x_centroid, y_centroid), 7, (255, 0, 0), -1)
    img_original = cv2.circle(img_original, (x_head, y_head), 7, (0, 0, 255), -1)
    img_array.append(img_original)

## CREATE THE VIDEOS ##
        
height, width, _ = img_original.shape
size = (width,height)
out = cv2.VideoWriter('noStim_detection.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 1.5, size)
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()