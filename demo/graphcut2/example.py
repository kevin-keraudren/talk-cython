#!/usr/bin/python

import numpy as np
from lib.graphcut import graphcut
import cv2
from time import time

img = cv2.imread( "../lena.png", 0 ).astype('float64')
mask = cv2.imread( "../mask.png", 0 )

start = time()

seg = graphcut( img.copy(), mask.copy(), 10 )

stop = time()
print "Elapsed time:", stop - start, "seconds"

print "writing segmentation to file..."
img[seg==2] = 0
cv2.imwrite( "segmentation.png", img )

seg = seg.astype('float')
seg /= seg.max()
seg *= 255
cv2.imwrite( "final_mask.png", seg )

img = cv2.imread( "../lena.png", 0 ).astype('float64')
mask = cv2.imread( "../mask2.png", 0 )
seg = graphcut( img.copy(), mask.copy(), 10 )
img[seg==2] = 0
cv2.imwrite( "segmentation2.png", img )
