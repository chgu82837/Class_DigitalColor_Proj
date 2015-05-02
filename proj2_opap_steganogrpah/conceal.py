#!/usr/bin/env python
# Require python3

import os, sys, random
from PIL import Image
# Docs at http://pillow.readthedocs.org/index.html

import numpy as np
import math as m
import statistics as s

try:
    k_value = 3
    if sys.argv[1][0] == "-":
        skip_opap = "O" in sys.argv[1]
        reversing = "R" in sys.argv[1]
        verbose = "v" in sys.argv[1]
        for i in range(1,8):
            if str(i) in sys.argv[1]:
                k_value = i
        sys.argv.pop(1)
    else: # Default flog value
        skip_opap = False
        reversing = False
        verbose = False

    cover_path = sys.argv[1]
    result_path = sys.argv[2]
    secret_msg = False
    if len(sys.argv) > 3:
        secret_msg = False # sys.argv[3] Not implemented yet

except Exception as e:
    print("Usage:")
    print("    python[3] conceal.py [-ORv<k>] <cover_img> <result_img> [secret_msg]")
    print("")
    print("    [-LRv] flags:")
    print("    -O : Skip OPAP")
    print("    -R : Reverse the operation, get the secret message from the <result_img> and output <cover_img> (Not implemented yet)")
    print("   <k> : the k value from `1` - `8`")
    print("    -v : show debug message")
    exit(255)

random.seed(2015)
p_max = 255

def nextMsgSeq(k):
    return random.randint(0,2 ** k - 1)

def conceal(k,p,s):
    p_ = p - (p % 2**k) + s
    if not skip_opap:
        p_c = [p_] # p candidates
        if p_ <= p_max - 2**k:
            p_c.append(p_ + 2**k)
        if p_ >= 2**k:
            p_c.append(p_ - 2**k)
        for p__ in p_c:
            if (p__ - p)**2 < (p_ - p)**2:
                p_ = p__
    if(verbose):
        print("p",p,"s",s,"r",p_)
    return p_

if reversing:
    pass
else:
    mse = 0
    cover_img = Image.open(cover_path)
    cover_ary = np.array(cover_img)
    result_img = Image.new(cover_img.mode,cover_img.size)
    result_ary = np.array(result_img)
    if verbose:
        print("cover_ary:", cover_ary, "result_ary:", result_ary)
    # exit(0)
    for y in range(cover_img.size[0]):
        for x in range(cover_img.size[1]):
            tmp_p = []
            for e in np.nditer(cover_ary[x,y]):
                tmp_p.append(e)
                # print(e)
            if len(tmp_p) == 1:
                result_ary[x,y] = conceal(k_value,tmp_p[0],nextMsgSeq(k_value))
                mse += (int(result_ary[x,y]) - int(tmp_p[0])) ** 2
            else:
                for i in range(len(tmp_p)):
                    result_ary[x,y,i] = conceal(k_value,tmp_p[i],nextMsgSeq(k_value))
                    mse += (int(result_ary[x,y,i]) - int(tmp_p[i])) ** 2
    if verbose:
        print("result_ary", result_ary)
    # exit(0)
    mse /= cover_img.size[0] * cover_img.size[1]
    psnr = 10 * m.log((p_max**2)/mse,10)
    print("MSE =",mse,"PSNR =",psnr)

    Image.fromarray(result_ary,cover_img.mode).save(result_path)

print("Process completed!")
