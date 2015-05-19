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
        secret_msg_b = "m" in sys.argv[1]
        for i in range(1,8):
            if str(i) in sys.argv[1]:
                k_value = i
        sys.argv.pop(1)
    else: # Default flog value
        skip_opap = False
        reversing = False
        verbose = False
        secret_msg_b = False

    input_img = sys.argv[1]
    if not reversing:
        result_path = sys.argv[2]
    if secret_msg_b and not reversing:
        secret_msg = sys.argv[3]
    else:
        secret_msg = ""

except Exception as e:
    print("Usage:")
    print("    python[3] conceal.py [-ORmv<k>] <input_img> [result_img] [secret_msg]")
    print("")
    print("    [-LRv] flags:")
    print("    -O : Skip OPAP")
    print("    -R : Reverse the operation, get the secret message from the <input_img>")
    print("    -m : Use a string as the secret message, the [secret_msg] is required when concealing")
    print("   <k> : the k value from `1` - `8`")
    print("    -v : show debug message")
    print("")
    print("Error:")
    print(e)
    print("")
    exit(255)

if k_value >= 8 or k_value <= 0:
    print("k value invalid (valid: 1 - 7)")
    exit(255)

p_max = 255
mask = 2 ** k_value

class MsgSeq():
    def __init__(self, k, msg):
        self.k = k
        self.msg = msg
        self.cnt = 0
        self.mask = ~ ( -1 << k )
        if self.msg:
            self.byteArr = msg.encode()
            self.byte = self.byteArr[0]
            self.byteArr = self.byteArr[1:]
            self.finished = False
            self.decoded = True
        else:
            self.byteArr = []
            self.byte = 0
            self.finished = True
            self.decoded = False
    def next(self):
        if self.finished:
            return 0
        result = self.byte
        self.byte >>= self.k
        self.cnt += self.k

        if self.cnt >= 8:
            if len(self.byteArr):
                nextByte = self.byteArr[0]
            else:
                self.finished = True
                nextByte = 0
            if self.cnt >= 8 + self.k:
                self.cnt -= 8
                result = nextByte >> (self.cnt - self.k)
                self.byte = result >> self.k
                self.byteArr = self.byteArr[1:]
            else:
                shmt_tmp = self.k + 8 - self.cnt
                result |= (nextByte << shmt_tmp) & (-1 << shmt_tmp)
        return result & self.mask

    def put(self,p):
        if self.decoded:
            # raise Exception("Decoded, refuse to put more")
            return
        self.byte |= p << self.cnt
        self.cnt += self.k
        if self.cnt >= 8:
            if self.byte & 255 == 0:
                self.getStr()
            else:
                self.byteArr.append(self.byte & 255)
                self.byte >>= 8
                self.cnt -= 8

    def getStr(self):
        if self.decoded:
            return self.msg
        self.byteArr.append(self.byte & 255)
        self.decoded = True
        # print(self.byteArr)
        self.msg = bytes(self.byteArr).decode().replace("\0","")
        return self.msg

# a = MsgSeq(3,'123')
# b = MsgSeq(3,'')
# c = []
# for x in range(10):
#     c.append(a.next())
# print(c)
# for e in c:
#     b.put(e)
# print(b.getStr(),b.getStr()[0])
# exit()

class RanMsgSeq:
    def __init__(self, k, seed):
        self.k = k
        random.seed(seed)
        self.max = 2 ** k - 1
    def next(self):
        return random.randint(0,self.max)

def conceal(p,s):
    p_ = p_r = p - (p % mask) + s
    if not skip_opap:
        if p_ <= p_max - mask and abs(p_ + mask - p) < abs(p_r - p):
            p_r = p_ + mask
        if p_ >= mask and abs(p_ - mask - p) < abs(p_r - p):
            p_r = p_ - mask
    # print("p",p,"s",s,"r",p_,"p_r",p_r)
    return p_r

# def reveal(p):
#     # print("p",p,"r",p % mask)
#     return p % mask

if secret_msg_b:
    MsgIter = MsgSeq(k_value,secret_msg)
    if verbose:
        reveal = lambda p: print( "%d " % (p % mask),end="") or MsgIter.put(p % mask)
    else:
        reveal = lambda p: MsgIter.put(p % mask)
else:
    MsgIter = RanMsgSeq(k_value,2015)
    reveal = lambda p: print( "%d " % (p % mask),end="")

print("Start processing...")

if reversing:
    print("Reversing the message out ...")
    cover_img = Image.open(input_img)
    cover_ary = np.array(cover_img)
    # result_img = Image.new(cover_img.mode,cover_img.size)
    # result_ary = np.array(result_img)
    for y in range(cover_img.size[0]):
        for x in range(cover_img.size[1]):
            tmp_p = []
            for e in np.nditer(cover_ary[x,y]):
                tmp_p.append(e)
            if len(tmp_p) == 1:
                reveal(tmp_p[0])
            else:
                for i in range(len(tmp_p)):
                   reveal(tmp_p[i])

    if secret_msg_b:
        print("\nMessage revealed:\n=========================================\n",MsgIter.getStr(),"\n=========================================")
    else:
        print("\n=========================================")
else:
    mse = 0
    cover_img = Image.open(input_img)
    cover_ary = np.array(cover_img)
    result_img = Image.new(cover_img.mode,cover_img.size)
    result_ary = np.array(result_img)
    if verbose:
        print("cover_ary:", cover_ary, "result_ary:", result_ary)
        print("=========================================")
    for y in range(cover_img.size[0]):
        for x in range(cover_img.size[1]):
            tmp_p = []
            for e in np.nditer(cover_ary[x,y]):
                tmp_p.append(e)
                # print(e)
            if len(tmp_p) == 1:
                next_val = MsgIter.next()
                if verbose:
                    print("%d " % next_val,end="")
                result_ary[x,y] = conceal(tmp_p[0],next_val)
                mse += (int(result_ary[x,y]) - int(tmp_p[0])) ** 2
            else:
                for i in range(len(tmp_p)):
                    next_val = MsgIter.next()
                    if verbose:
                        print("%d " % next_val,end="")
                    result_ary[x,y,i] = conceal(tmp_p[i],next_val)
                    mse += (int(result_ary[x,y,i]) - int(tmp_p[i])) ** 2
    if verbose:
        print("")
        print("=========================================")
        print("result_ary", result_ary)
    # exit(0)
    print(mse)
    mse /= cover_img.size[0] * cover_img.size[1]
    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * m.log((p_max**2)/mse,10)
    print("MSE =",mse,"PSNR =",psnr)

    Image.fromarray(result_ary,cover_img.mode).save(result_path)

print("Process completed!")
