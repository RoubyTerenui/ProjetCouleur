import numpy as np
import cv2

# Flux vidéo
cap = cv2.VideoCapture(0)
# Inclusion des fichiers haar
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
kernel = np.ones((5,5),np.uint8)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Détection tete/yeux
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = frame[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


   
    
    #median = cv2.medianBlur(gray,29)
    #laplacian = cv2.Laplacian(frame,cv2.CV_64F)
    #sobelx = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)
    #sobely = cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=5)
    
    # Seuillage
    #ret,th1 = cv2.threshold(gray,120,255,cv2.THRESH_BINARY_INV)

    # Espace HSV
    # median = cv2.medianBlur(frame,5)
    # hsv = cv2.cvtColor(median, cv2.COLOR_BGR2LAB)    
    # Define range of people color in HSV ca marche que devant un fond blanc ca 
    #lower_blue = np.array([0,50,50])
    #upper_blue = np.array([255,150,150])
    # Threshold the HSV image to get only blue colors
    #mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)



     # Convertir en niveau de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,255)
    #ret,thresh = cv2.threshold(gray,127,255,0)
    #im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours, -1, (0,0,0), thickness=cv2.FILLED)

    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('laplacian',laplacian)
    #cv2.imshow('thresh',thresh)
    #cv2.imshow('sobelx',sobelx)
    #cv2.imshow('sobely',sobely)
    #cv2.imshow('mask',mask)
    cv2.imshow('edges',edges)
    #cv2.imshow('res',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
