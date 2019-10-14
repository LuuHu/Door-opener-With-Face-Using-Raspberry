from gpiozero import LED
green = LED(16)
blue = LED(20)
red = LED(21)
green.on()
blue.on()
red.on()

import cv2 as cv
import face_recognition as fr
import numpy as np
from gpio import door
from picamera import PiCamera
import picamera.array
import time
import datetime
from tensorflow import keras
from multiprocessing import Pool
import os
from time import sleep
from multiprocessing import Pool

name = ['name0','name1','name2','name3','name4','name5'] # It should owns the same shape with first dim of "coded" in line 58
model = keras.models.Sequential([
    keras.layers.Conv2D(36,(7,7),strides=(2,2),input_shape=(960,540,3)),
    keras.layers.LeakyReLU(),
    keras.layers.MaxPool2D(),

    keras.layers.Conv2D(48,(5,5),strides=(2,2)),
    keras.layers.LeakyReLU(),
    keras.layers.MaxPool2D(),

    keras.layers.Conv2D(60,(5,5)),
    keras.layers.LeakyReLU(),
    keras.layers.MaxPool2D((3,3)),
    keras.layers.BatchNormalization(),

    keras.layers.Conv2D(60,(3,3)),
    keras.layers.LeakyReLU(),
    keras.layers.MaxPool2D(),
    keras.layers.BatchNormalization(),

    keras.layers.Flatten(),
    keras.layers.Dense(18),
    keras.layers.LeakyReLU(),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(7, activation='softmax')
])
model.load_weights('/home/pi/Desktop/doom/Weights/mymodlweights.h5')

camera = PiCamera()
camera.resolution = (960, 720)
camera.rotation = 90
camera.framerate = 5
image = picamera.array.PiRGBArray(camera)
try:
    coded = np.load("codedface.npy")
    coded = coded.tolist()
except Exception:
    print('Error in reading facecode!')

print('prepared !')
green.off()
blue.off()
red.off()

def getreal(img):
    img = cv.resize(img,(540,960))
    fan = model.predict(img[np.newaxis,:])
    fan = fan[0].tolist()
    return fan.index(max(fan))

def vaildation(img):
    facecode = fr.face_encodings(img)
    if len(facecode) != 0:
        res = fr.compare_faces(coded,facecode[0],0.4)
        try:
            ind = res.index(True)
            return ind # The number of the face that was found in the face code
        except Exception:
            return 996 # No matching face
        return res
    else:
        print("No face were found")
        return 997 # no face were found

if __name__=='__main__':
    p = Pool(2)
    while True:
        cur = datetime.datetime.now()
        if cur.hour <= 7:
            print('Non-work time')
            time.sleep(1200)
        blue.on()
        camera.capture(image,'rgb')
        img1 = image.array
        image.truncate(0)
        camera.capture(image,'rgb')
        img2 = image.array
        blue.off()
        image.truncate(0)
        
        level = p.map(vaildation,[img1,img2])   # I decide to use multi-core to process to speed up
        
        if level[0] == 997 or level[1] == 997:
            print("reject level = 1")
            continue  # one of or two pic has no face
        elif level[0] == 996 and level[1] == 996:
            red.on()
            print("unknown face")
            cv.imwrite("unknown//"+str(cur)+"11.jpg",img1[:,:,::-1])
            cv.imwrite("unknown//"+str(cur)+"12.jpg",img2[:,:,::-1])
            print("reject level = 1")
            red.off()
            continue
        elif level[0] == level[1]:
            really0 = getreal(img1)
            really1 = getreal(img2)
            ##### The reason why i use it twice instead of Pool.map is that it may OOM cause the model is quite large, maybe you can design your own model
            print(really0)
            print(really1)
            
            if really0==1 and really1==1:
                print(name[level[0]])
                green.blink(0.5, 0.5)
                print("validation pass")
                door()
                cv.imwrite("known//"+str(cur)+"1.jpg",img1[:,:,::-1])
                cv.imwrite("known//"+str(cur)+"2.jpg",img2[:,:,::-1])
                green.off()
                continue
            else:
                red.on()
                print("reject level = 2")
                print("unknown face")
                cv.imwrite("unknown//"+str(cur)+"21.jpg",img1[:,:,::-1])
                cv.imwrite("unknown//"+str(cur)+"22.jpg",img2[:,:,::-1])
                print("reject level = 1")
                time.sleep(30)
                red.off()
                continue
        else:
            pass
