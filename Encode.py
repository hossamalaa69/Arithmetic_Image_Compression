import os

import numpy as np
import cv2
from numpy import save
from numpy import savez_compressed
from numpy import load


while True:
    print("Enter image director with extension:")
    imgPath = str(input())
    if os.path.isfile(imgPath):
        break
    else:
        print("Invalid image path, Please make sure you're entering valid data")

while True:
    print("Enter block size:")
    blockSize = int(input())
    if blockSize>0:
        break
    else:
        print("Invalid block size, Please make sure you're entering positive integer")

while True:
    print("Enter data type, i.e.(float16,float32,float64):")
    dataType = str(input())
    if dataType=='float16' or dataType=='float32' or dataType=='float64':
        break
    else:
        print("Invalid data type, Please make sure you're entering valid data")


Pixels = []

Codes = []

Prob = [0.0] * 256
np_Prob = np.array(Prob,dtype=dataType)

FX = [0.0] * 256
np_FX = np.array(FX,dtype=dataType)


def calcCode(k):

    L=0
    U=1

    srt = blockSize*k
    end = (blockSize*(k+1))

    for i in range(srt, end):
        if (Pixels[i]-1)<0:
            fx_1=0
        else:
            fx_1= np_FX[Pixels[i] - 1]

        newL = L + ((U - L)*fx_1)
        newU = L + ((U-L)*np_FX[Pixels[i]])
        L=newL
        U=newU

    tag_code = (L+U)/2

    if tag_code>1:
        tag_code=1

    Codes.append(tag_code)

def main():

    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

    print("Wait few moments")

    # read image and store in Pixels array
    rows, cols = img.shape

    for i in range(rows):
        for j in range(cols):
            Pixels.append(img[i, j])

    for i in Pixels:
        np_Prob[i] += 1.0

    for i in range(len(np_Prob)):
        np_Prob[i] = np_Prob[i] / len(Pixels)

    for j in range(len(np_FX)):
        for i in range(j+1):
            np_FX[j] += np_Prob[i]

    if len(Pixels) % blockSize > 0:
        x = len(Pixels) % blockSize
        for i in range(blockSize - x):
            Pixels.append(0)

    lenDic = int(len(Pixels) / blockSize)

    for k in range(lenDic):
        calcCode(k)

    arrInfo =[]
    arrInfo.append(cols)
    arrInfo.append(rows)
    arrInfo.append(blockSize)
    npyArr_info = np.array(arrInfo,dtype=np.uint16)

    np_Codes = np.array(Codes,dtype=dataType)

    save('npyArr_Codes.npy', np_Codes)
    save('npyArr_Probs.npy', np_Prob)
    save('npyArr_WHB.npy', npyArr_info)

    print("Done")

if __name__ == "__main__":
        main()