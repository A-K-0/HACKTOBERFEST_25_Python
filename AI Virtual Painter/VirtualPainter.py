import cv2
import numpy as np
import time 
import os
import handtrackingModuleEnhanced as htme

#########################################
brushThickness = 15
eraserThickness = 100
#########################################

folderPath=r"G:\MY PROJECTS\OPENCV PROJECTS\ADVANCED\AI Virtual Painter\Headers"
myList=os.listdir(folderPath)
# print(myList)
overlayList=[]

for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header= overlayList[0]
drawColor = (255,0,255)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
imgCanvas = np.zeros((720,1280,3),np.uint8)

detector= htme.handDetector(detectionCon=0.85)
xp,yp=0,0
while True:
    # import image
    success, img = cap.read()
    img = cv2.flip(img,1)

    # find hand landmarks
    img = detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)

    if len(lmList)!=0:
        # print(lmList)

        # tip of index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        # checking which fingers are up
        fingers=detector.fingersUp()
        #print(fingers)

        # if selection mode - 2 fingers up 
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            print("Selection Mode")
            # checking for the click
            if y1<125:
                if 250<x1<450:
                    header=overlayList[0]
                    drawColor=(255,0,255)
                elif 550<x1<750:
                    header=overlayList[1]
                    drawColor=(255,0,0)
                elif 800<x1<950:
                    header=overlayList[2]
                    drawColor=(0,255,0)
                elif 1050<x1<1200:
                    header=overlayList[3]
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        # if drawing mode - index finger up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp=x1,y1

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgGray = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgGray)
    img= cv2.bitwise_or(img,imgCanvas)           

    # setting the header image
    img[0:125,0:1280]=header
    #img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    #cv2.imshow("Canvas", imgCanvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()