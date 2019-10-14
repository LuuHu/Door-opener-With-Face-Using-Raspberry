import face_recognition as fr
import numpy as np
import cv2 as cv

def addface(img):
    facecode = fr.face_encodings(img,num_jitters=3)
    if len(facecode) == 1:
        try:
            coded = np.load("codedface.npy")
            coded = coded.tolist()
        except Exception:
            coded = []
        #print(facecode)
        coded.append(facecode[0])
        coded = np.array(coded)
        print(coded.shape)
        np.save('codedface.npy',coded)
    else:
        print("None or multi face!\nChange another image")

pic = cv.imread('XXX.jpg')  
#This is the picture name you wanna to add
pic = cv.cvtColor(pic,cv.COLOR_BGR2RGB)
addface(pic)
