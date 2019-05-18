import glob

import cv2
#import numpy as np
#from matplotlib import pyplot as plt

def createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size):
    
    folders = [f for f in sorted(glob.glob(path + "/**"))]
    
    for folder in folders: 
        files = [f for f in sorted(glob.glob(folder + "/**"))]
        img_array1 = []
        img_array2 = []
        img_array3 = []
        img_array4 = []
        img_array5 = []
        for file in files:
            img = cv2.imread(file)
    
            box1 = img[box1_size[0]:box1_size[1], box1_size[2]:box1_size[3]]
            img_array1.append(box1)
            
            box2 = img[box2_size[0]:box2_size[1], box2_size[2]:box2_size[3]]
            img_array2.append(box2)
            
            box3 = img[box3_size[0]:box3_size[1], box3_size[2]:box3_size[3]]
            img_array3.append(box3)
            
            box4 = img[box4_size[0]:box4_size[1], box4_size[2]:box4_size[3]]
            img_array4.append(box4)
            
            if (box5_size != []):
                box5 = img[box5_size[0]:box5_size[1], box5_size[2]:box5_size[3]]
                img_array5.append(box5)
            
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

