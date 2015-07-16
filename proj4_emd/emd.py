from PIL import Image
from random import *
import sys,os,math
import numpy as np

debug = False
try:

    if sys.argv[1][0] == "-":
        debug = "D" in sys.argv[1]
        sys.argv.pop(1)
    n = int(sys.argv[1])
    infile = sys.argv[2]
    
except Exception as e:
    print("Usage:")
    print("    python[3] emd.py [-D] <n> <image_path>")
    print("")
    print("Option:")
    print("    -D : debug mode (enable verbose)")
    exit(255)

cover_image = Image.open(infile)
if debug:
    print("Cover image:",infile)
if debug:
    print("Cover image format:" , cover_image.format) 
if debug:
    print("Cover image mode:" , cover_image.mode)
if debug:
    print("Cover image size:" ,"%dx%d" % cover_image.size)
cover_image_width = cover_image.size[0]
cover_image_height = cover_image.size[1]

V = cover_image_width
H = cover_image_height
cover_image = cover_image.load()
stego_image = Image.new("L", (H, V))
stego_image = stego_image.load()

s = Random()
s.seed(2015)
secretMessage = []

K = 1                  #Affordable
maxMXC = 0             #Affordable
finalK = 0             #Affordable

W = np.arange(1,n+1,1)                 #weight

print("Starting ...")

THCc = math.log(2*n+1 , 2)
MSEp = ((2*n)/(2*n+1)*math.floor(H*V/n))/(H*V)
Uc = math.floor(H*V/n)
L = math.floor(K*math.log(2*n+1 , 2))
while K <= Uc:
    L = math.floor(K*math.log(2*n+1 , 2))
    if L <= 64:     #Affordable
        MXC = (Uc/K)*L
        if maxMXC < MXC:              #Affordable
            maxMXC = MXC
            finalK = K
            L = math.floor(K*math.log(2*n+1 , 2))
            finalL = L
    K += 1

if debug:
    print('Weight : ',W)
    print("Uc",Uc)

for x in range(0,Uc):
    secretMessage.append(s.randint(0,(n*2)))


def overflow_underflow(pa,index,key):
    global n,W,secretMessage,embNum

    pStego = []
    f = 0
    s = 0
    if key == 0:
        pa[index] = pa[index] - 1
    else:
        pa[index] = pa[index] + 1

    for x in range(0,n):
        f += pa[x] * W[x]
    f = f % (2*n+1)

    s = (secretMessage[embNum]-f+(2*n+1))% (2*n+1)
    if secretMessage[embNum] == f:
        pStego = pa
        return 1
    else:
        if s <= n:
            for x in range(0,n):
                if x != (s-1):
                    pStego.append(pa[x])
                else:
                    pStego.append(pa[x]+1)
            for x in range(0,n):
                if pStego[x] > 255:
                    overflow_underflow(pa,x,0)
            return 1

        else:
            for x in range(0,n):
                if x != (2*n-s):
                    pStego.append(pa[x])
                else:
                    pStego.append(pa[x]-1)
            for x in range(0,n):
                if pStego[x] < 0:
                    overflow_underflow(pa,x,1)
            return 1

indexGroupHead = 0
indexGroupTail = 0
stegoRow = 0
stegoColumn = 0
indexRow = 0
indexColumn = 0
embNum = 0
MSE = 0
tmp = 0
trueMSE = 0
PSNR = 0

for x in range(0,H):
    for y in range(0,V):
        stego_image[x,y] = cover_image[x,y]

while embNum < (math.floor(H*V/n)):
    p = []
    pStego = []
    f = 0
    s = 0
    key = 0
    for x in range(0,n):
        if indexColumn == (V):
            if indexRow < (H - 1):
                indexRow += 1
                indexColumn = 0
        p.append(cover_image[indexRow,indexColumn])
        if indexColumn <= (V-1):
            indexColumn += 1

    for x in range(0,n):
        f += p[x] * W[x]
    f = f % (2*n+1)

    s = (secretMessage[embNum]-f+(2*n+1))% (2*n+1)
    
    if secretMessage[embNum] == f:
        pStego = p
    else:
        if s <= n:
            for x in range(0,n):
                if x != (s-1):
                    pStego.append(p[x])
                else:
                    pStego.append(p[x]+1)
            for x in range(0,n):
                if pStego[x] > 255:
                    key = overflow_underflow(p,x,0)
        else:
            for x in range(0,n):
                if x != (2*n-s):
                    pStego.append(p[x])
                else:
                    pStego.append(p[x]-1)
            for x in range(0,n):
                if pStego[x] < 0:
                    key = overflow_underflow(p,x,1)
        if key == 1:
            pStego = []
            pStego = p

    for x in range(0,n):
        if stegoColumn == (V):
            if stegoRow < (H - 1):
                stegoRow += 1
                stegoColumn = 0
        stego_image[stegoRow,stegoColumn] = pStego[x]
        if stegoColumn <= (V-1):
            stegoColumn += 1

    embNum += 1

for x in range(0,H):
    for y in range(0,V):
        tmp = stego_image[x,y] - cover_image[x,y]
        MSE = MSE + (tmp*tmp)
trueMSE = MSE/(H*V)
PSNR = 10 * math.log(255*255/trueMSE , 10)

print("== Result =========================")
print("EMbed number: ",math.floor(H*V/n))
print("MSE:",trueMSE)
print("PSNR:",PSNR)
