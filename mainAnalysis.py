import os
os.mkdir('Videos')

import cropImages as crop

"""Dorsal"""
path = 'Behavior_Flies/Dorsal'
name_type = 'dorsal'

#first box: 
box1_size = [85, 210, 290, 1070]

#second box: 
box2_size = [255, 390, 290, 1070]

#third box:
box3_size = [420, 555, 300, 1070]

#fourth box: 
box4_size = [615, 710, 300, 1060]

#fifth box: 
box5_size = [770, 875, 300, 1060]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""GFP"""
path = 'Behavior_Flies/GFP'
name_type = 'gfp'

#first box: 
box1_size = [110, 240, 300, 1070]

#second box: 
box2_size = [280, 410, 300, 1070]

#third box:
box3_size = [445, 575, 300, 1060]

#fourth box: 
box4_size = [615, 735, 300, 1060]

#fifth box: 
box5_size = [780, 895, 300, 1060]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""EagDN"""
path = 'Behavior_Flies/EagDN'
name_type = 'eagdn'

#first box: 
box1_size = [70, 180, 300, 1060]

#second box: 
box2_size = [215, 340, 300, 1060]

#third box:
box3_size = [390, 520, 300, 1060]

#fourth box: 
box4_size = [550, 680, 300, 1060]

#fifth box: 
box5_size = [730, 835, 300, 1060]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""TNT"""
path = 'Behavior_Flies/TNT'
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

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""ShalRNA"""
path = 'Behavior_Flies/ShalRNA'
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

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""IMPTNT"""
path = 'Behavior_Flies/IMPTNT'
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

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""Hunchback"""
path = 'Behavior_Flies/Hunchback'
name_type = 'hunchback'

#first box: 
box1_size = [70, 195, 310, 1070]

#second box: 
box2_size = [235, 365, 310, 1070]

#third box:
box3_size = [400, 530, 310, 1070]

#fourth box: 
box4_size = [565, 685, 310, 1070]

#fifth box: 
box5_size = [730, 845, 310, 1070]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


 

