import cropImages as crop

"""Dorsal"""
path = 'Behavior_Flies/Dorsal'
name_type = 'dorsal'

#first box: 
box1_size = [80, 215, 290, 1070]

#second box: 
box2_size = [255, 390, 290, 1070]

#third box:
box3_size = [420, 555, 290, 1070]

#fourth box: 
box4_size = [600, 735, 290, 1070]

#fifth box: 
box5_size = [755, 890, 290, 1070]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""GFP"""
path = 'Behavior_Flies/GFP'
name_type = 'gfp'

#first box: 
box1_size = [110, 240, 300, 1070]

#second box: 
box2_size = [280, 410, 300, 1070]

#third box:
box3_size = [445, 575, 300, 1070]

#fourth box: 
box4_size = [610, 740, 300, 1070]

#fifth box: 
box5_size = [770, 900, 300, 1070]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""EagDN"""
path = 'Behavior_Flies/EagDN'
name_type = 'eagdn'

#first box: 
box1_size = [60, 190, 300, 1060]

#second box: 
box2_size = [210, 340, 300, 1060]

#third box:
box3_size = [390, 520, 300, 1060]

#fourth box: 
box4_size = [550, 680, 300, 1060]

#fifth box: 
box5_size = [720, 850, 300, 1060]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""TNT"""
path = 'Behavior_Flies/TNT'
name_type = 'tnt'

#first box: 
box1_size = [90, 210, 300, 1080]

#second box: 
box2_size = [260, 380, 290, 1070]

#third box:
box3_size = [425, 545, 290, 1070]

#fourth box: 
box4_size = [595, 715, 290, 1070]

#fifth box: 
box5_size = [760, 880, 290, 1070]

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
box1_size = [180, 305, 260, 1030]

#second box: 
box2_size = [350, 475, 265, 1035]

#third box:
box3_size = [510, 635, 270, 1040]

#fourth box: 
box4_size = [675, 795, 270, 1040]

#fifth box: 
box5_size = [] # No Flies

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


"""Hunchback"""
path = 'Behavior_Flies/Hunchback'
name_type = 'hunchback'

#first box: 
box1_size = [70, 200, 310, 1070]

#second box: 
box2_size = [235, 365, 310, 1070]

#third box:
box3_size = [400, 530, 310, 1070]

#fourth box: 
box4_size = [560, 690, 310, 1070]

#fifth box: 
box5_size = [720, 850, 310, 1070]

crop.createVideos(path, name_type, box1_size, box2_size, box3_size, box4_size, box5_size)


 

