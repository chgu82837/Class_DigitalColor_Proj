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
    print("    python[3] transColor.py [-ROMbav] <source_img> <target_img> <destination_img> [source_avg_r source_avg_g source_avg_b source_dev_r source_dev_g source_dev_b]")
    print("")
    print("    [-ROMbav] flags:")
    print("    -R : reverse the operation, source_img will be treated as the converted img, flag M will be enable, flag b,a will be disabled and source_avg and source_dev is required")
    print("    -O : disable log at convertion")
    print("    -M : disable lms at convertion (Use pure RGB to convert) (Also disable log)")
    print("    -b : use boundary to convert instead of statistics method")
    print("    -a : adjust the result to source boundary")
    print("    -v : show debug message")
    exit()

# Default flog value
reversing = False
disable_log = False
disable_lms = False
use_boundary_method = False
enable_boundary_adjust = False
verbose = False

if sys.argv[1][0] == "-":
    reversing = "R" in sys.argv[1]
    disable_log = "O" in sys.argv[1]
    disable_lms = "M" in sys.argv[1]
    use_boundary_method = "b" in sys.argv[1]
    enable_boundary_adjust = "a" in sys.argv[1]
    verbose = "v" in sys.argv[1]
    sys.argv.pop(1)

if reversing:
    disable_lms = True
    use_boundary_method = False
    enable_boundary_adjust = False
    if len(sys.argv) < 10:
        print("To reverse, the source_avg and source_dev is required")
        exit()

src_avg_f = False
src_dev_f = False

if len(sys.argv) >= 10:
    source_info = sys.argv[4].split(",")
    if float(sys.argv[4]) > 1:
        src_avg_f = [float(e) / 255 for e in sys.argv[4:7]]
        src_dev_f = [float(e) / 255 for e in sys.argv[7:10]]
    else:
        src_avg_f = [float(e) for e in sys.argv[4:7]]
        src_dev_f = [float(e) for e in sys.argv[7:10]]

# print(src_avg_f,src_dev_f)
# exit()

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

if verbose:
    print("Showing convertion matrix:")
    print("rgb2LMS",rgb2LMS)
    print("LMS2lms",LMS2lms)
    print("lms2LMS",lms2LMS)
    print("LMS2rgb",LMS2rgb)

    print("lms2LMS * LMS2lms",np.dot(lms2LMS,LMS2lms))
    print("LMS2rgb * rgb2LMS",np.dot(LMS2rgb,rgb2LMS))

    # exit()

log_min = m.log(1/255,10)
p_max = 255

def get_lms(img):
    img_ary = np.array(img)
    tmp = []
    avg = [0,0,0]
    dev = [0,0,0]
    max_v = [-100,-100,-100]
    min_v = [100,100,100]
    log_too_small = 0

    for y in range(img.size[0]):
        row = []
        for x in range(img.size[1]):
            tmp_p = []
            for e in np.nditer(img_ary[x,y,0:3]):
                tmp_p.append(float(e) / 255)
            tmp_p = np.array(tmp_p)

            if not disable_lms:
                tmp_p = np.dot(rgb2LMS,tmp_p)

                if not disable_log:
                    for i in [0,1,2]:
                        if tmp_p[i] <= 0:
                            if verbose:
                                print("input too small:",tmp_p[i],"at",{'x':x,'y':y,'i':i})
                            log_too_small += 1
                            tmp_p[i] = log_min
                        else:
                            tmp_p[i] = m.log(tmp_p[i],10)
                    tmp_p = np.dot(LMS2lms,tmp_p)

            for i in [0,1,2]:
                avg[i] = avg[i] + tmp_p[i]
                max_v[i] = max(max_v[i],tmp_p[i])
                min_v[i] = min(min_v[i],tmp_p[i])

            row.append(tmp_p)
        tmp.append(row)

    print("There are %d pixels that value is underflow (<= 0) when doing log, use value %f instead" % (log_too_small,log_min))

    pix_cnt = src_i.size[0] * src_i.size[1]
    for i in [0,1,2]:
        avg[i] = avg[i] / pix_cnt

    for row in tmp:
        for tmp_p in row:
            for i in [0,1,2]:
                dev[i] = dev[i] + (tmp_p[i] - avg[i]) * (tmp_p[i] - avg[i])

    for i in [0,1,2]:
        dev[i] = m.sqrt(dev[i] / pix_cnt)

    return tmp,avg,dev,max_v,min_v

print("Starting to get infomation of source image...")
src_i = Image.open(sys.argv[1])
src,src_avg,src_dev,src_max,src_min = get_lms(src_i)
print("src_avg",src_avg)
print("src_dev",src_dev)
print("src_max",src_max)
print("src_min",src_min)

print("Starting to get infomation of target image...")
tar_i = Image.open(sys.argv[2])
tar,tar_avg,tar_dev,tar_max,tar_min = get_lms(tar_i)
print("tar_avg",tar_avg)
print("tar_dev",tar_dev)
print("tar_max",tar_max)
print("tar_min",tar_min)

# exit()

if src_avg_f and src_dev_f:
    print("Using given source avg and dev...")
    src_avg = src_avg_f
    src_dev = src_dev_f

print("Starting to process the destination image...")

des_i = Image.new("RGB",src_i.size)
des = np.array(des_i)

des_tmp = []

if enable_boundary_adjust:
    res_max = [-100,-100,-100]
    res_min = [100,100,100]

if use_boundary_method: # ================= boundary method ======================
    print("Using boundary method ...")
    inte_ratio = [0]

    for i in [1,2]:
        inte_ratio.append((tar_max[i] - tar_min[i]) / (src_max[i] - src_min[i]))

    print("inte_ratio:",inte_ratio)

    for y in range(src_i.size[0]):
        des_r_tmp = []
        for x in range(src_i.size[1]):
            tmp = [src[y][x][0],0,0]
            for i in [1,2]:
                tmp[i] = tar_min[i] + (src[y][x][i] - src_min[i]) * inte_ratio[i]

                if enable_boundary_adjust:
                    res_max[i] = max(res_max[i],tmp[i])
                    res_min[i] = min(res_min[i],tmp[i])
            des_r_tmp.append(tmp)
        des_tmp.append(des_r_tmp)

else: # ================== statistics method ======================
    scale = []
    if reversing:
        for i in [0,1,2]:
            scale.append(src_dev[i] / tar_dev[i])# / dev_divider
    else:
        for i in [0,1,2]:
            scale.append(tar_dev[i] / src_dev[i])# / dev_divider
    
    print("Using statistics method ...")
    for y in range(src_i.size[0]):
        des_r_tmp = []
        for x in range(src_i.size[1]):
            tmp = [0,0,0]
            for i in [0,1,2]:
                # tmp[i] = src[y][x][i]
                tmp[i] = (src[y][x][i] - src_avg[i]) * scale[i] + src_avg[i]

                if enable_boundary_adjust:
                    res_max[i] = max(res_max[i],tmp[i])
                    res_min[i] = min(res_min[i],tmp[i])
            des_r_tmp.append(tmp)
        des_tmp.append(des_r_tmp)
# ================== convertion done ======================

if enable_boundary_adjust:
    print("res_max:",res_max)
    print("res_min:",res_min)

if enable_boundary_adjust:
    print("Starting to adjust result boundary to source boundary ...")
    adj_inte_ratio = []
    for i in [0,1,2]:
        adj_inte_ratio.append((src_max[i] - src_min[i]) / (res_max[i] - res_min[i]))
    for y in range(src_i.size[0]):
        for x in range(src_i.size[1]):
            for i in [0,1,2]:
                des_tmp[y][x][i] = src_min[i] + (des_tmp[y][x][i] - res_min[i]) * adj_inte_ratio[i]

# ================= convert back =========================

too_big = 0
too_small = 0
mse = 0.0
mse_n = 0

for y in range(src_i.size[0]):
    for x in range(src_i.size[1]):
        tmp = des_tmp[y][x]

        if not disable_lms:
            if not disable_log:
                tmp = np.dot(lms2LMS,tmp)
                for i in [0,1,2]:
                    tmp[i] = m.pow(10,tmp[i])
            tmp = np.dot(LMS2rgb,tmp)
        for i in [0,1,2]:
            if tmp[i] > 1:
                if verbose:
                    print("final result too big:",tmp[i],"at",{'x':x,'y':y,'i':i},"... Auto fix to 1")
                too_big += 1
                tmp[i] = 1
            if tmp[i] < 0:
                if verbose:
                    print("final result too small:",tmp[i],"at",{'x':x,'y':y,'i':i},"... Auto fix to 0")
                too_small += 1
                tmp[i] = 0
            des[x,y,i] = int(tmp[i] * 255)
            src_tmp = int(src[y][x][i] * 255)
            mse += (des[x,y,i] - src_tmp) ** 2
            mse_n += 1
        # print(des[x,y])

print("There are %d value overflow ... Auto fix to 1" % too_big)
print("There are %d value underflow ... Auto fix to 0" % too_small)

mse /= mse_n
psnr = 10 * m.log((p_max**2)/mse,10)

print("MSE between source and destination is %f\nPSNR between source and destination is %f" % (mse,psnr))

# exit()
Image.fromarray(des).save(sys.argv[3])

print("Process completed!")
