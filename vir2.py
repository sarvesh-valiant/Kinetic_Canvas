import cv2             # Importing the libraries
import numpy as np
import os              # To access the UI files
import Chidorix as ch

##############################

brushThickness = 15  #assigning a value for brushthickness
eraserThickness = 50 #assigning a value for eraserthickness

##############################

folderPath = "Header"  # Importing the UI images
myList = os.listdir(folderPath)
print(myList)

overlayList = []  # Storing the images in a list called overlayList

# Looping and importing the images
for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}')
    if image is not None:  # Check if the image was read correctly
        overlayList.append(image)

print(len(overlayList))  # Printing the length of the overlayList
header = overlayList[0]  
drawColor = (255, 0, 0)
cap = cv2.VideoCapture(0)  # Correct capitalization for VideoCapture
cap.set(3, 1980)  # Setting the width
cap.set(4, 1080)  # Setting the height

detector = ch.handDetector(detectionCon=0.85)

xp, yp = 0, 0   #setting the values for x previous and y previous
imgCanvas = np.zeros((1080, 1980, 3), np.vint8)

while True:
    success, img = cap.read()  # 1. Importing image
    if not success:
        print("Failed to capture image")
        break  # Break the loop if there's an error

    img = cv2.flip(img, 0)  # Flipping the image vertically

    # 2. Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
         
       # print(lmList)
        x1, y1 = lmList[8][1:]  # Finding the tip of index finger
        x2, y2 = lmList[12][1:]  # Finding the tip of middle finger

        # 3. Check which fingers are up
        fingers = []
        # Example logic to check which fingers are up (this can be adjusted)
        if lmList[8][2] < lmList[6][2]:  # Index finger
            fingers.append(1)
        else:
            fingers.append(0)

        if lmList[12][2] < lmList[10][2]:  # Middle finger
            fingers.append(1)
        else:
            fingers.append(0)

        # 4. If selection mode - two fingers are up
        if sum(fingers) == 2:
            xp, yp = 0, 0 
            print("Selection mode")

 # determining the colors of the brushes
        if y1 < 130:
            if 250< x1 <450:
                header = overlayList[0]
                drawColor = (255, 0, 0)  #red color
            elif 550 < x1 < 750:    
                header = overlayList[1]
                drawColor = (0, 255, 0)  #green color
            elif 800 < x1 < 950:
                 header = overlayList[2]
                 drawColor = (0, 135, 189)  #blue color
            elif 1050 < x1 < 1200:
                 header = overlayList[3]
                 drawColor = (0, 0, 0)     #eraser- black color

      #If it is a selection mode drawing a rectangle           
        cv2.rectangle(img, (x1, y1 - 25), (x2 ,y2 + 25), drawColor, cv2.FILLED)

        # 5. If draw mode - index finger is up
    elif fingers[0] == 1:
            #If it is drawing mode drawing a circle
        cv2.circle(img, (x1, y1), 15, drawColor,cv2.FILLED)
        print("Draw mode")

        if xp == 0 and yp == 0:
           xp, yp = x1, y1

        if drawColor == (0,0,0):
           cv2.line(img, (xp,yp),(x1,y1),drawColor,eraserThickness)
           cv2.line(imgCanvas, (xp,yp),(x1,y1),drawColor,eraserThickness)

        else:
           cv2.line(img, (xp,yp),(x1,y1),drawColor,brushThickness)
           cv2.line(imgCanvas, (xp,yp),(x1,y1),drawColor,brushThickness)

    xp, yp = x1, y1

imgGray = cv2.cvColor(imgCanvas,cv2.COLOR_BRR2GRAY)   
_,imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
img = cv2.bitwise_and(img,imgInv)
img = cv2.bitwise_or(img,imgCanvas)

    #setting the header image
img[0:130, 0:1980] = header
   # img = cv2.addWeighted(img,3.5,imgCanvas,0.5,0)          cv2.imshow("Image", img)  # Corrected the window name and display the image
cv2.imshow("Canvas", imgCanvas) 
cv2.imshow("Inv",imgInv)
cv2.waitKey(1)
