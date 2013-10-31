#!/usr/bin/python

import numpy as np
from lib import graphcut
import itertools
import cv2
import math
from time import time

img = cv2.imread( "../lena.png", 0 ).astype('float64')
mask = cv2.imread( "../mask.png", 0 )

start = time()

nb_pixels = img.shape[0]*img.shape[1]

G = graphcut.PyGraph(nb_pixels,nb_pixels*(8+2))
G.add_node(nb_pixels)

def index( i, j, img ):
    return j + img.shape[1]*i

r = [-1,0, 1]
neighbourhood = []
for a,b in itertools.product(r,r):
    if abs(a)+abs(b) != 0:  
        neighbourhood.append((a,b))

        
std = 10

print "Noise std:", std

print "building graph..."
        
for i in xrange(img.shape[0]):
    for j in xrange(img.shape[1]):
        for a,b in neighbourhood:
            if ( 0 <= i+a < img.shape[0]
                 and 0 <= j+b < img.shape[1] ):
                    dist = math.sqrt( a**2 + b**2 )
                    if img[i,j] < img[i+a,j+b]:
                        w = 1.0/dist
                    else:
                        w = np.exp(-(img[i,j] - img[i+a,j+b])**2/(2.0*std**2))/dist
                    G.add_edge( index(i,j,img),
                                index(i+a,j+b,img),
                                w,
                                0 )

print "linking to source and sink..."
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if mask[i,j] == 1:
            G.add_tweights(index(i,j,img),1000,0)
        elif mask[i,j] == 2:
            G.add_tweights(index(i,j,img),0,1000)

print "computing maxflow..."
print G.maxflow()

print "transcription of segmentation..."
seg = np.zeros(img.shape)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
            seg[i,j] = G.what_segment(index(i,j,img)) + 1

stop = time()
print "Elapsed time:", stop - start, "seconds"

print "writing segmentation to file..."
img[seg==2] = 0
cv2.imwrite( "segmentation.png", img )

seg = seg.astype('float')
seg /= seg.max()
seg *= 255
cv2.imwrite( "final_mask.png", seg )


