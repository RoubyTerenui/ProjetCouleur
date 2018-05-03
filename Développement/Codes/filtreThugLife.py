import numpy as np
import cv2
import math

# Flux vidéo
cap = cv2.VideoCapture(0)
# Images
specs = cv2.imread('img/thuglifespecs.png', -1)
cigar = cv2.imread('img/cigar.png',-1)
mouth_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_mcs_mouth.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascades/frontalEyes.xml')
faces_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

def detectFaces(image):
    faces = faces_cascade.detectMultiScale(image, 1.3, 5)
    return faces

def detectEyes(image):
    eyes = eyes_cascade.detectMultiScale(image)
    return eyes

def detectMouths(image):
    mouth = mouth_cascade.detectMultiScale(image)
    return mouth

def isBodyPartDetected(bodyPart,i):
    for (x, y, w, h) in bodyPart:        
        i = 1
        break
    return i

def displayMask(x,y,w,h,frame,maskresized,newx,newy):
    for i in range(0, w):
        for j in range(0, h):
            if maskresized[i, j][3] != 0:
                 if (y + i < 480) & (x + j<640):    
                        frame[y + i-newx, x + j- newy] = maskresized[i, j]
                        
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detectFaces(gray)    
    i = 0
    for (x, y, w, h) in faces:
        rectangle = frame[y:y+h, x:x+w]
        eyes = detectFaces(rectangle)
        i = isBodyPartDetected(eyes,i)
        if i == 1:
            for (ex,ey,ew,eh) in eyes: 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)            
                specs2 = cv2.resize(specs, (ew, eh))
                ew, eh, c = specs2.shape
                ey=y+ey
                ex=x+ex
                for (x, y, w, h) in faces:
                    displayMask(ex,ey,ew,eh,frame,specs2,0,0)
        if i == 0:
            print("No eyes found")

    ## For Cigar
    i = 0    
    for (x, y, w, h) in faces:
        rectangle = frame[y+math.floor(h/2):y+h, x:x+w]
        mouth = detectMouths(rectangle)
        i = isBodyPartDetected(mouth,i)  
        if i == 1:
            for (mx,my,mw,mh) in mouth: 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                cigar2 = cv2.resize(cigar,(mw,mh))
                mw,mh,c = cigar2.shape
                my=y+w-mw
                mx=x+h-mh-math.floor(mw/2)        
                for (x, y, w, h) in faces:
                    displayMask(mx,my,mw,mh,frame,cigar2,0,0)

        if i == 0:
            print("No mouth found")
                    
    # Display the resulting frame
    cv2.imshow('ThugLife', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
