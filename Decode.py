import numpy as np
import cv2
from numpy import save
from numpy import savez_compressed
from numpy import load

infoArr = load("npyArr_WHB.npy")
Prob = load("npyArr_Probs.npy")
Codes = load("npyArr_Codes.npy")

Pixels = []

Width = infoArr[0]
Height = infoArr[1]
blockSize = infoArr[-1]
Resolution = int(Width)*Height
FX = [0.0]*256

def calcPixels(k):
    L_1 = 0
    U_1 = 1
    fx_1 = 0

    for i in range(blockSize):
        added = False
        for index in range(len(Prob)):
            if (index-1)<0:
                fx_1=0.0
            else:
                fx_1 = FX[index-1]
            newL = L_1 + ((U_1-L_1)*fx_1)
            newU = L_1 + ((U_1-L_1)*FX[index])
            if k >= newL and k < newU:
                L_1=newL
                U_1=newU
                Pixels.append(index)
                added=True
                break

        #to handle problems of float precision
        if not added :
                Pixels.append(255)

        if len(Pixels) == Resolution:
            return

def main():

    print("Block size:"+str(blockSize))
    print("Data type:"+str(Codes.dtype))
    print("Image Resolution:"+str(Width)+"*"+str(Height))
    print("Wait few moments")

    for j in range(len(FX)):
        for i in range(j+1):
            FX[j]+=Prob[i]

    for i in Codes:
        calcPixels(i)


    pixels_npy = np.array(Pixels)
    matrixPixels = pixels_npy.reshape(Height, Width)

    cv2.imwrite("file_out.jpg",matrixPixels)

    print("Done")

if __name__ == "__main__":
        main()


