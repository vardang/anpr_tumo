# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:28:42 2020

@author: User
"""

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def nothing(x):
    pass
def plot_side_by_side(image1, image2, title1="", title2="", width=15, height=15, cmap="gray"):
  fig = plt.figure(figsize=[width, height])
  ax1 = fig.add_subplot(121)
  ax1.imshow(image1, cmap=cmap)
  ax1.set(xticks=[], yticks=[], title=title1)

  ax2 = fig.add_subplot(122)
  ax2.imshow(image2, cmap=cmap)
  ax2.set(xticks=[], yticks=[], title=title2)
  
def make_mask(img):
        type=cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        img_bin = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_bin=cv2.adaptiveThreshold(img_bin,255,type,cv2.THRESH_BINARY,7,4)
        img_bin = 255-img_bin  # Invert the image
        # Defining a kernel length
        kernel_length = np.array(img).shape[1]//40      
        verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
        # A kernel of (3 X 3) ones.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Morphological operation to detect verticle lines from an image
        img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
        verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
        alpha = 0.5
        beta = 1.0 - alpha
        # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
        img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
        return img_final_bin

def show_imgs():
    cam = cv2.VideoCapture(0)
    #img=cv2.imread(name)
    cv2.namedWindow('Preprocessing')
    cv2.createTrackbar('Canny', 'Preprocessing',0,1,nothing)
    cv2.createTrackbar('th1', 'Preprocessing',200,200,nothing)
    cv2.createTrackbar('th2', 'Preprocessing',30,300,nothing)

    #cv2.namedWindow('my webcam')
    while True:
        ret_val, img = cam.read()
        
        th1=cv2.getTrackbarPos('th1','Preprocessing')
        th2=cv2.getTrackbarPos('th2','Preprocessing')
        canny=cv2.getTrackbarPos('Canny','Preprocessing')
        if canny==1:
            img=cv2.Canny(img,th1,th2)
        cv2.imshow('Preprocessing',img)
        if cv2.waitKey(1) == 27: 
            break 
    cv2.destroyAllWindows()


show_imgs()
#'auto.jpg'