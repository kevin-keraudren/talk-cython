#!/usr/bin/python

import irtk
import cv2

mask = irtk.imread("mask.nii",dtype='uint8')
irtk.imwrite("mask.png",mask)

img = irtk.Image( cv2.imread("lena.png",0) )

irtk.imshow( img, mask,
             filename="initialisation.png",
             colors={1:(255,0,0),2:(0,255,0)},
             opacity=1.0 )

mask2 = irtk.imread("mask2.nii",dtype='uint8')
irtk.imwrite("mask2.png",mask2)
irtk.imshow( img, mask2,
             filename="initialisation2.png",
             colors={1:(255,0,0),2:(0,255,0)},
             opacity=1.0 )
