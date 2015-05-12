#!/usr/bin/env python
# Require python3

import os, sys
from PIL import Image
# Docs at http://pillow.readthedocs.org/index.html

import numpy as np
import math as m
import statistics as s

if len(sys.argv) < 3:
    print("Usage:")
    print("    python[3] mse_psnr.py <img1> <img2>")
    print("")
    exit(255)

img1 = Image.open(sys.argv[1])
img2 = Image.open(sys.argv[2])

if img1.size != img2.size:
    print("The size of two image is different. Aborting...")
    exit(255)

if img1.mode != img2.mode:
    print("Warning: the mode of two img is different\n",img1.mode,img2.mode)

mse = 0.0
mse_n = 0

img1_ary = np.array(img1)
img2_ary = np.array(img2)

p_max = 255

print("Calculation started")

for y in range(img1.size[0]):
    for x in range(img1.size[1]):
        for e in range(0,3):
            mse += (float(img1_ary[x,y,e]) - float(img2_ary[x,y,e])) ** 2
            mse_n += 1

mse /= mse_n
psnr = 10 * m.log((p_max**2)/mse,10)

print("MSE between these two images is %f\nPSNR between these two images is %f" % (mse,psnr))
