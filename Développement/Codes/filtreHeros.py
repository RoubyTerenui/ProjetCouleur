import numpy as np
import cv2
import math

# Flux vidéo
cap = cv2.VideoCapture(0)
# Images
mask = cv2.imread('img/Mask17.png', -1)
mask2 = cv2.imread('img/Mask1.png', -1)
masks = [mask, mask2]
faces_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')

def detectFaces(image):
    faces = faces_cascade.detectMultiScale(image, 1.3, 5)
    return faces

def isBodyPartDetected(bodyPart,i):
    for (x, y, w, h) in bodyPart:
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)        
        i = 1
        break
    return i

def faceIsDetected(faces, mask, frame):
    for (x, y, w, h) in faces:
        [w,h] = resizeRec(x,y,w,h,math.floor(1/6*x))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)            
        maskresized = cv2.resize(mask, (w, h))
        w, h, c = maskresized.shape
        displayMask(x,y,w,h,frame,maskresized,math.floor(1/5*x),math.floor(1/10*x))
    return frame

def resizeRec(x,y,w,h,size):
    if w < x + size: # Redimensionnement du masque car le carré ne prend que le visage et non la tete entiere
        w = w + size
        h = h + size
    return w,h

def displayMask(x,y,w,h,frame,maskresized,newx,newy):    
    findColorPixelTShirt(frame,x,y,w)
    for i in range(0, w):
        for j in range(0, h):
            if maskresized[i, j][3] != 0:
                 if (y + i < 480) & (x + j<640):    
                        frame[y + i-newx, x + j- newy] = maskresized[i, j]

def findColorPixelTShirt(frame,x,y,w):
    pixel = 0
    k=0
    l=0
    moyenne = [0,0,0]
    xpixel = x
    ypixel = y+math.floor(3/2*w)
    px = frame[xpixel,ypixel]
    img = cv2.rectangle(frame,(x,y+math.floor(3/2*w)),(x+50,y+math.floor(3/2*w)+10),(0,0,255),2)
    for i in range(xpixel, xpixel+50):
        for j in range(ypixel, ypixel+math.floor(3/2*w)+10):
            pixel = pixel +1
            for k in range(0, 3):
                moyenne[k] = moyenne[k] + px[k]
                k=k+1
    for l in range(0, 3):
                moyenne[l] = math.floor(moyenne[l]/pixel)
                l=l+1
  
def startCam(cap,mask,faces_cascade):
    while(True):
        # Capture frame-by-frame
        mask = masks[0]
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detectFaces(gray)
        i = 0
        i = isBodyPartDetected(faces,i)      
        if i == 1:
            frame = faceIsDetected(faces, mask, frame)
                        
        if i == 0:
            print("No face found") 

        cv2.imshow('Be a hero !', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

startCam(cap,masks,faces_cascade)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
