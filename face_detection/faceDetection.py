# USAGE
# Specify the name of the person
#     python3 faceDetection.py -n Josh

## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

import numpy as np
import cv2
import os
import argparse
from sense_hat import SenseHat

sense = SenseHat()

g = (0,255,0)
b = (0,0,255)
r = (255,0,0)
c = (0,0,0)

# display a box on the LED matrix
def faceLED():
    face = [
        g, g, g, g, g, g, g, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, c, c, c, c, c, c, g,
        g, g, g, g, g, g, g, g
    ]
    sense.set_pixels(face)

# display eyes on the LED matrix
def eyeLED():
    # left eye
    sense.set_pixel(1,2,b)
    sense.set_pixel(1,3,b)
    sense.set_pixel(2,2,b)
    sense.set_pixel(2,3,b)
    # right eye
    sense.set_pixel(5,2,b)
    sense.set_pixel(5,3,b)
    sense.set_pixel(6,2,b)
    sense.set_pixel(6,3,b)

# display smile on the LED matrix
def smileLED():
    sense.set_pixel(2,5,r)
    sense.set_pixel(3,5,r)
    sense.set_pixel(4,5,r)
    sense.set_pixel(5,5,r)
    sense.set_pixel(2,6,r)
    sense.set_pixel(3,6,r)
    sense.set_pixel(4,6,r)
    sense.set_pixel(5,6,r)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
    help="The name/id of this person you are recording")
ap.add_argument("-i", "--dataset", default='dataset',
    help="path to input directory of faces + images")
args = vars(ap.parse_args())

# use name as folder name
name = args["name"]
folder = './dataset/{}'.format(name)

# Create a new folder for the new name
if not os.path.exists(folder):
    os.makedirs(folder)

# Load face, eyes and smile cascades
faceCascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
smileCascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_smile.xml')
eyeCascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

img_counter = 0
face_counter = 0
smile_counter = 0

while img_counter <= 20:
    ret, img = cap.read()

    if not ret:
        print("Camera did not connect")
        break
    # flip image if upside down
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
        )

    # if a face is detected display box on sense hat
    if len(faces) > 0:
        faceLED()
    else:
        sense.clear((0,0,0))

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        eyes = eyeCascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.5,
                minNeighbors=5,
                minSize=(5, 5)
            )

        smile = False
        
        # loop if eyes are detected
        for (ex, ey, ew, eh) in eyes:
            eyeLED()    # display eyes on sense hat

            # if a smile hasn't already been detected check
            if not smile:
                smile = smileCascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.5,
                    minNeighbors=15,
                    minSize=(25, 25)
                )
                # loop if smile is detected
                for (xx, yy, ww, hh) in smile:
                    smileLED()  # display smile on sense hat
                    # if more smile images are needed save image
                    if(smile_counter <= 10):
                        img_name = "{}/{:04}.jpg".format(folder,img_counter)
                        cv2.imwrite(img_name, img[y:y+h,x:x+w])
                        print("{} smile written!".format(img_name))
                        smile_counter += 1
                    smile = True
                    break
            # if no smile was detected and still need more face images save image
            if(face_counter <= 10 and not smile):
                img_name = "{}/{:04}.jpg".format(folder,img_counter)
                cv2.imwrite(img_name, img[y:y+h,x:x+w])
                print("{} face written!".format(img_name))
                face_counter += 1
                break
        
        img_counter = face_counter + smile_counter  # calculate total images saved

    key = input("Press q to quit or ENTER to continue: ")
    if key == 'Q':
        break

cap.release()
cv2.destroyAllWindows()
