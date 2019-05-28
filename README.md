# COBAR
Project for the course Controlling Behaviour in animals and robots 

mainAnalysis.py: 
    script responsible for the whole analysis of the data, which calls cropImages.py and plots.py scripts to perform the image processing and plot the graphs respectively. 

'Behavior_Flies' is a folder containing all the data recorded: inside, there is one folder for each gene, and inside each of these folders ten folders named "GENE_#" where # is the number of the trial. 

'Behavior_Flies_selected' is the folder containing the recorded frames, during stimulation 

'Videos': videos of all the recordinds taken, with indicated centroids and head positions, in blue and red respectively

'boxplots': folder with the boxplots showing the velocities 

'traces': folder containing the graphs of the flies' orientation

noStimAnalysis.py: 
this is a script that performs an image processing algorithm for the detection of the fly centroid and head, in the case of frames taken without light stimulation (dark images)

'noStim_detection.mp4': this is a video showing the ability of detecting centroids and heads even with dark images (no light stimulation)


