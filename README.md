# WormWatcher
Machine Learning model to quantify locomotion of celegans from a video 


This is the development page for worm watcher the plan is to use open-cv Scikit and Pandas to give a csv sheet with each row being a worm followed and each column with a Number of a movement 1-4 omega, bend, reversal, and coil 

Then lets also included time the worm was being "watched" so that we arent skewing data for  watching onw woem shorter than another worm 


Lets get midline length of a worm, maybe if a worm is being watched and it does a bodybend/reversal then lets take a pic 
run it through exodtong worm machine code and add length as a column to this 

Then once we have this working lets get R graphs to populate from these quantifications IE number of moves by AGE


so to start lets get a script that takes a video of worms then converts to binary accuratly (@sherc1 Ill get you a video by midweek)


    Here are videos https://drive.google.com/drive/folders/1SM3szGu3VzXV3p9ug1t-6cQdsUrYTZor?usp=sharing




Updates thus far 
* Cropper Crops video with a gui for user 
* Convert to grayscaler script not very useful tbh video kinda already in grayscale
* Boxer.py This is the meat thus far Boxes video live for editing quit with q, need to refine overlapping boxes, boxes length of existence, yada yada
* Added Requirement.txt 

Plan 
* Export these boxes into a new video one for each
* Make a weights file for a worm movement?
* Script to count based on these
* Script to combine all scripts into a black box program
