# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 16:23:11 2021

@author: Manan garg
"""

import numpy as np
import cv2
import time

cap=cv2.VideoCapture(0)
time.sleep(2)

while True:
    ret,background=cap.read()
    if ret==True:
        break

while True:
    ret,img=cap.read()

    if ret==False:
        break

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #HSV- Hue Saturation Value

    lower_red=np.array([0,120,70]) # red ,darkness, brightness
    upper_red=np.array([10,255,255])
    mask1=cv2.inRange(hsv,lower_red,upper_red) #Separating the cloak part

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1=mask1+mask2

    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2) #Noise removal
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    mask2=cv2.bitwise_not(mask1)

    res1=cv2.bitwise_and(background, background, mask=mask1) #Used for segmentation of the color
    res2=cv2.bitwise_and(img, img, mask=mask2) #Used to substitute the cloak part
    final_output=cv2.addWeighted(res1,1,res2,1,0) # 1*res1+1*res2+0

    cv2.imshow("Eureka!!",final_output)
    cv2.imshow("Original",img)
    k=cv2.waitKey(10) & 0xFF
    if k==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()