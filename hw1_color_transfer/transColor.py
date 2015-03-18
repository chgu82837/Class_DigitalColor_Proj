#!/usr/bin/env python
# Require python3

import os, sys
from PIL import Image
# Docs at http://pillow.readthedocs.org/index.html

import numpy as np
import math as m
import statistics as s

if len(sys.argv) < 4:
    print("Usage:")
    print("    python[3] transColor.py <source_img> <target_img> <destination_img> [dev_divider]")
    exit()

if len(sys.argv) == 5:
    dev_divider = float(sys.argv[4])
else:
    dev_divider = 2.5

rgb2LMS = np.dot(
    np.array([0.3897,0.6890,-0.0787,-0.2298,1.1834,0.0464,0,0,1]).reshape(3,3),
    np.array([0.5141,0.3239,0.1604,0.2651,0.6702,0.0641,0.0241,0.1228,0.8444]).reshape(3,3)
)
LMS2lms = np.dot(
    np.array([1/m.sqrt(3),0,0,0,1/m.sqrt(6),0,0,0,1/m.sqrt(2)]).reshape(3,3),
    np.array([1,1,1,1,1,-2,1,-1,0]).reshape(3,3)
)

lms2LMS = np.linalg.inv(LMS2lms)
LMS2rgb = np.linalg.inv(rgb2LMS)

# print("rgb2LMS",rgb2LMS)
# print("LMS2lms",LMS2lms)
# print("lms2LMS",lms2LMS)
# print("LMS2rgb",LMS2rgb)

# print("lms2LMS * LMS2lms",np.dot(lms2LMS,LMS2lms))
# print("LMS2rgb * rgb2LMS",np.dot(LMS2rgb,rgb2LMS))

# exit()

def get_lms(img):
    img_ary = np.array(img)
    tmp = []
    avg = [0,0,0]
    dev = [0,0,0]
    # pix = [[],[],[]]
    for y in range(img.size[0]):
        row = []
        for x in range(img.size[1]):
            tmp_p = []
            for e in np.nditer(img_ary[x,y,0:3]):
                tmp_p.append(float(e) / 255)
            tmp_p = np.array(tmp_p)
            # print(tmp_p)
            tmp_p = np.dot(rgb2LMS,tmp_p)
            # print(tmp_p)
            for i in [0,1,2]:
                tmp_p[i] = m.log(tmp_p[i],10)
            # print(tmp_p)
            tmp_p = np.dot(LMS2lms,tmp_p)
            # print(tmp_p)
            for i in [0,1,2]:
                avg[i] = avg[i] + tmp_p[i]
                # pix[i].append(tmp_p[i])
            # exit()

            row.append(tmp_p)
        tmp.append(row)

    pix_cnt = src_i.size[0] * src_i.size[1]
    for i in [0,1,2]:
        avg[i] = avg[i] / pix_cnt

    # print("pix_cnt",pix_cnt)
    # print("avg",avg,[s.mean(cha) for cha in pix])

    for row in tmp:
        for tmp_p in row:
            for i in [0,1,2]:
                dev[i] = dev[i] + (tmp_p[i] - avg[i]) * (tmp_p[i] - avg[i])

    for i in [0,1,2]:
        dev[i] = m.sqrt(dev[i] / pix_cnt)

    # print("dev",dev,[s.pstdev(cha) for cha in pix])
    # exit()

    return tmp,avg,dev

print("Starting to get infomation of source image...")
src_i = Image.open(sys.argv[1])
src,src_avg,src_dev = get_lms(src_i)
print("src_avg",src_avg)
print("src_dev",src_dev)

print("Starting to get infomation of target image...")
tar_i = Image.open(sys.argv[2])
tar,tar_avg,tar_dev = get_lms(tar_i)
print("tar_avg",tar_avg)
print("tar_dev",tar_dev)

# exit()

print("Starting to process the destination image...")

des_i = Image.new("RGB",src_i.size)
des = np.array(des_i)

for y in range(src_i.size[0]):
    for x in range(src_i.size[1]):
        tmp = [0,0,0]
        for i in [0,1,2]:
            # tmp[i] = src[y][x][i]
            scale = tar_dev[i] / src_dev[i] / dev_divider
            tmp[i] = (src[y][x][i] - src_avg[i]) * scale + src_avg[i]
        tmp = np.dot(lms2LMS,tmp)
        for i in [0,1,2]:
            tmp[i] = m.pow(10,tmp[i])
        tmp = np.dot(LMS2rgb,tmp)
        for i in [0,1,2]:
            des[x,y,i] = int(tmp[i] * 255)
        # print(des[x,y])

# exit()
Image.fromarray(des).save(sys.argv[3])

print("Process completed!")
