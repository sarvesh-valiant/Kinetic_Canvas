import cv2             #importing the libries
import numpy as np
import time           #importing time for showing frame rate
import os             #to access the UI files
import Chidorix as ch

folderPath = "Header" #importing the UI images
myList = os.listdir(folderPath)
print(myList)


overlayList = []    #storing the images in a list called overlayList


for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}')   #Looping and importing the images

overlayList.append(image)
print(len(overlayList))     #printing the length of the overlayinyList
header = overlayList[0]

cap = cv2.Videocapture(0)   
cap.set(3, 1980)  #determining the width and the height of the images
cap.set(4, 1080)

while True:
    success, img = cap.read() #1.importing image
                             
                              #2.find hand landmarks

                              #3.check which fingers are up

                              #4.if selection mode-two fingers are up

                              #5.If draw mode - index finger is up

                              
img[0:130,0:1980] = header    #setting the header image
    cv2.imshow("Image,img")
    cv2.waitKey(1)