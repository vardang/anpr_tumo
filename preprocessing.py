# =============================================================================
# import cv2
# import os
# import numpy as np
# import matplotlib.pyplot as plt
# 
# def nothing(x):
#     pass
# img = cv2.imread("ex.png")
# 
# while img.isOpened():
# 	flag, frame = img.read()
# 	if not flag:
# 		break
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	canny = cv2.Canny(gray,100,200)
# 	cv2.imshow('frame', frame)
# 	cv2.imshow('gray', gray)
# 	cv2.imshow('canny', canny)
# 
# 	key_pressed = cv2.waitKey(1)
# 
# 	if key_pressed == 27:
# 		break
# 
# cap.release()
# cv2.destroyAllWindows()
# 
# =============================================================================
import numpy as np
import cv2
import pytesseract

def cut_plate(image,cnts):
#detecting plate
    plate = None
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        edges_count = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(edges_count) == 4:
            x,y,w,h = cv2.boundingRect(c)
            plate = image[y:y+h, x:x+w]
            break
    
    cv2.imwrite("plate.png", plate)
#predicting plate numbers
#should be modyfied and upgrated
    conf=('-l eng --oem 3 --psm 8')
    text = pytesseract.image_to_string(plate, config=conf)
    font = cv2.FONT_HERSHEY_SIMPLEX
    x,y,w,h=cv2.boundingRect(c)
    cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2)
    cv2.putText(image, text, (x-int(w/4),y+2*h+5), font, 1, (255,0,0), 2)
#    print(text)
    return (image)

def run(imgpath):
    def nothing(x):
        pass
    cv2.namedWindow('Preprocessing')
    cv2.resizeWindow('Preprocessing', 300,800)
    cv2.createTrackbar('Canny', 'Preprocessing',0,1,nothing)
    cv2.createTrackbar('b', 'Preprocessing',33,50,nothing)
    cv2.createTrackbar('th1', 'Preprocessing',200,200,nothing)
    cv2.createTrackbar('b1', 'Preprocessing',95,200,nothing)
    cv2.createTrackbar('th2', 'Preprocessing',126,300,nothing)
    cv2.createTrackbar('b2', 'Preprocessing',172,200,nothing)
    
    
    img = cv2.imread(imgpath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray= cv2.bilateralFilter(gray, 33,95, 172)
    while(1):
        im=img.copy()
        wimg = gray
        canny=cv2.getTrackbarPos('Canny','Preprocessing')    #set 1 to see contours
    #change Trackbars' poses to get the best parameters
        th1=cv2.getTrackbarPos('th1','Preprocessing')
        th2=cv2.getTrackbarPos('th2','Preprocessing')
        b=cv2.getTrackbarPos('b','Preprocessing')
        b1=cv2.getTrackbarPos('b1','Preprocessing')
        b2=cv2.getTrackbarPos('b2','Preprocessing')
        wimg=cv2.bilateralFilter(wimg, b,b1, b2)
        if canny==1:
            wimg=cv2.Canny(wimg,th1,th2)
        im2,cnts, new = cv2.findContours(wimg.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        _ = cv2.drawContours(im, cnts,-1, (255,0,255),2)
        k = cv2.waitKey(2) & 0xFF
        if k == 27:
            break
        if k==13:
            cv2.setTrackbarPos('Canny','Preprocessing',0)
            im=cut_plate(img,cnts)
        cv2.imshow('Preprocessing',im)
    cv2.destroyAllWindows()

run("E:/Desktop/AOByte/auto.jpg")
