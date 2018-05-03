import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import math
import os
    
camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("Be a Hero !")
screen = pygame.display.set_mode([1070,565])
# Flux vidéo
cap = cv2.VideoCapture(0)
# Images
specs = cv2.imread('img/thuglifespecs.png', -1)
cigar = cv2.imread('img/cigar.png',-1)
mask1 = cv2.imread('img/Mask1.png', -1)
mask2 = cv2.imread('img/Mask2.png', -1)
mask3 = cv2.imread('img/Mask3.png', -1)
mask4 = cv2.imread('img/Mask4.png', -1)
mask5 = cv2.imread('img/Mask5.png', -1)
mask6 = cv2.imread('img/Mask6.png', -1)
mask7 = cv2.imread('img/Mask7.png', -1)
mask8 = cv2.imread('img/Mask8.png', -1)
mask9 = cv2.imread('img/Mask9.png', -1)
mask10 = cv2.imread('img/Mask10.png', -1)
mask11 = cv2.imread('img/Mask11.png', -1)
mask12 = cv2.imread('img/Mask12.png', -1)
mask13 = cv2.imread('img/Mask13.png', -1)
mask14 = cv2.imread('img/Mask14.png', -1)
mask15 = cv2.imread('img/Mask15.png', -1)
mask16 = cv2.imread('img/Mask16.png', -1)
mask17 = cv2.imread('img/Mask17.png', -1)
mask18 = cv2.imread('img/Mask18.png', -1)
masks = [mask1, mask2, mask3, mask4, mask5, mask6, mask7, mask8, mask9, mask10, mask11, mask12, mask13, mask14, mask15, mask16, mask17, mask18]

mouth_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_mcs_mouth.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascades/frontalEyes.xml')
faces_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
#Boutons
boutonMask1 = pygame.image.load("img/Mask1.png").convert_alpha()
boutonMask1Area = pygame.Rect((663, 93), (79, 97))
boutonMask2 = pygame.image.load("img/Mask2.png").convert_alpha()
boutonMask2Area = pygame.Rect((751, 0), (104, 96))
boutonMask3 = pygame.image.load("img/Mask3.png").convert_alpha()
boutonMask3Area = pygame.Rect((855, 0), (106, 92))
boutonMask4 = pygame.image.load("img/Mask4.png").convert_alpha()
boutonMask4Area = pygame.Rect((765, 93), (79, 97))
boutonMask5 = pygame.image.load("img/Mask5.png").convert_alpha()
boutonMask5Area = pygame.Rect((657, 190), (78, 107))
boutonMask6 = pygame.image.load("img/Mask6.png").convert_alpha()
boutonMask6Area = pygame.Rect((867, 93), (73, 95))
boutonMask7 = pygame.image.load("img/Mask7.png").convert_alpha()
boutonMask7Area = pygame.Rect((759, 190), (85, 100))
boutonMask8 = pygame.image.load("img/Mask8.png").convert_alpha()
boutonMask8Area = pygame.Rect((963, 93), (79, 96))
boutonMask9 = pygame.image.load("img/Mask9.png").convert_alpha()
boutonMask9Area = pygame.Rect((871, 190), (89, 108))
boutonMask10 = pygame.image.load("img/Mask10.png").convert_alpha()
boutonMask10Area = pygame.Rect((961, 0), (103, 86))
boutonMask11 = pygame.image.load("img/Mask11.png").convert_alpha()
boutonMask11Area = pygame.Rect((648, 298), (95, 75))
boutonMask12 = pygame.image.load("img/Mask12.png").convert_alpha()
boutonMask12Area = pygame.Rect((977, 190), (86, 94))
boutonMask13 = pygame.image.load("img/Mask13.png").convert_alpha()
boutonMask13Area = pygame.Rect((856, 298), (115, 97))
boutonMask14 = pygame.image.load("img/Mask14.png").convert_alpha()
boutonMask14Area = pygame.Rect((979, 298), (79, 90))
boutonMask15 = pygame.image.load("img/Mask15.png").convert_alpha()
boutonMask15Area = pygame.Rect((640, 395), (70, 91))
boutonMask16 = pygame.image.load("img/Mask16.png").convert_alpha()
boutonMask16Area = pygame.Rect((752, 298), (96, 86))
boutonMask17 = pygame.image.load("img/Mask17.png").convert_alpha()
boutonMask17Area = pygame.Rect((640, 0), (111, 93))
boutonMask18 = pygame.image.load("img/Mask18.png").convert_alpha()
boutonMask18Area = pygame.Rect((710, 395), (88, 93))
boutonSave = pygame.image.load("img/save.png").convert_alpha()
boutonSaveArea = pygame.Rect((100, 480), (302, 83))
boutonReset = pygame.image.load("img/reset.png").convert_alpha()
boutonResetArea = pygame.Rect((410, 480), (83, 83))
boutonTL = pygame.image.load("img/tl.jpg").convert_alpha()
boutonTLArea = pygame.Rect((800, 395), (100, 83))
blue= [78, 200, 238]
green= [77, 179, 72]
black= [50, 50, 50]
red= [205, 35, 39]
yellow= [250, 209, 7]
purple= [125, 71, 153]
white= [235, 236, 237]
color = [blue, green, black, red, yellow, purple, white]

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

def faceIsDetected(faces, mask, frame,TL,numeroMask):
    for (x, y, w, h) in faces:
        [w,h,newx,newy] = resizeRec(x,y,w,h,numeroMask)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        maskresized = cv2.resize(mask, (w, h))
        w, h, c = maskresized.shape
        displayMask(x,y,w,h,frame,maskresized,newx,newy,TL)
    return frame

def eyesIsDetected(x,y,w,h,ex,ey,ew,eh,frame,TL,faces,image):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)            
    image2 = cv2.resize(image, (ew, eh))
    ew, eh, c = image2.shape
    ey=y+ey
    ex=x+ex
    for (x, y, w, h) in faces:
        displayMask(ex,ey,ew,eh,frame,image2,0,0,TL)
    return frame

def mouthIsDetected(x,y,w,h,mx,my,mw,mh,frame,TL,faces,image):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    image2 = cv2.resize(image,(mw,mh))
    mw,mh,c = image2.shape
    my=y+w-mw
    mx=x+h-mh-math.floor(mw/2)        
    for (x, y, w, h) in faces:
        displayMask(mx,my,mw,mh,frame,image2,0,0,TL)
    return frame

def resizeRec(x,y,w,h,numeroMask):
    if numeroMask == 1:
        wResize = 0
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = 0
    if numeroMask == 2:
        wResize = math.floor(1/4*x)
        hResize = math.floor(1/4*x)
        newx = math.floor(1/5*x)
        newy = math.floor(1/8*x)
    if numeroMask == 3:
        wResize = math.floor(1/6*x)
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = math.floor(1/10*x)
    if numeroMask == 4:
        wResize = 0
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = 0
    if numeroMask == 5:
        wResize = math.floor(1/15*x)
        hResize = math.floor(1/3*x)
        newx = math.floor(1/4*x)
        newy = math.floor(1/20*x)
    if numeroMask == 6:
        wResize = 0
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = 0
    if numeroMask == 7:
        wResize = math.floor(1/10*x)
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = math.floor(1/15*x)
    if numeroMask == 8:
        wResize = 0
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = 0
    if numeroMask == 9:
        wResize = -math.floor(1/30*x)
        hResize = math.floor(1/8*x)
        newx = math.floor(1/4*x)
        newy = 0
    if numeroMask == 10:
        wResize = math.floor(1/6*x)
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = math.floor(1/10*x)
    if numeroMask == 11:
        wResize = -math.floor(1/10*x)
        hResize = -math.floor(1/10*x)
        newx = math.floor(1/15*x)
        newy = -math.floor(1/15*x)
    if numeroMask == 12:
        wResize = math.floor(1/15*x)
        hResize = math.floor(1/10*x)
        newx = math.floor(1/6*x)
        newy = math.floor(1/25*x)
    if numeroMask == 13:
        wResize = math.floor(1/5*x)
        hResize = math.floor(1/6*x)
        newx = math.floor(1/4*x)
        newy = math.floor(1/10*x)
    if numeroMask == 14:
        wResize = 0
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = 0
    if numeroMask == 15:
        wResize = 0
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = 0
    if numeroMask == 16:
        wResize = -math.floor(1/10*x)
        hResize = -math.floor(1/10*x)
        newx = math.floor(1/15*x)
        newy = -math.floor(1/15*x)
    if numeroMask == 17:
        wResize = math.floor(1/5*x)
        hResize = math.floor(1/6*x)
        newx = math.floor(1/4.5*x)
        newy = math.floor(1/10*x)
    if numeroMask == 18:
        wResize = math.floor(1/20*x)
        hResize = math.floor(1/6*x)
        newx = math.floor(1/5*x)
        newy = math.floor(1/25*x)
    if w < x + wResize: # Redimensionnement du masque car le carré ne prend que le visage et non la tete entiere
        w = w + wResize
        h = h + hResize
    return w,h,newx,newy

def displayMask(x,y,w,h,frame,maskresized,newx,newy,TL):
    if TL == False:
        moyenne = findColorPixelTShirt(frame,x,y,w)
        giveColorPixelTShirt(moyenne)
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
    ypixel = y+math.floor(4/3*w)
    px = frame[xpixel,ypixel]
    img = cv2.rectangle(frame,(x,y+math.floor(4/3*w)),(x+50,y+math.floor(4/3*w)+10),(0,0,255),2)
    for i in range(xpixel, xpixel+50):
        for j in range(ypixel, ypixel+math.floor(3/2*w)+10):
            pixel = pixel +1
            for k in range(0, 3):
                moyenne[k] = moyenne[k] + px[k]
                k=k+1
    for l in range(0, 3):
                moyenne[l] = math.floor(moyenne[l]/pixel)
                l=l+1
    return moyenne

def giveColorPixelTShirt(moyenne):
    allcolor = 0
    colormin=0
    color2 =[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    whichColor=0
    for i in range(0, 7):
        allcolor=0
        for j in range(0, 3):
            color2[i][j] = abs(moyenne[j]-color[i][j])
            allcolor = allcolor + color2[i][j]
        if i == 0:            
            colormin = allcolor
        else:            
            if colormin > allcolor:
                colormin = allcolor
                whichColor = i 


def thugLife(faces,frame,i,TL):
    for (x, y, w, h) in faces:
        rectangle = frame[y:y+h, x:x+w]
        eyes = detectFaces(rectangle)
        i = isBodyPartDetected(eyes,i)
        if i == 1:
            for (ex,ey,ew,eh) in eyes: 
               frame = eyesIsDetected(x,y,w,h,ex,ey,ew,eh,frame,TL,faces,specs)
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
                frame = mouthIsDetected(x,y,w,h,mx,my,mw,mh,frame,TL,faces,cigar)
        if i == 0:
            print("No mouth found")
    return frame
    
def startCam(cap,mask,faces_cascade,specs,cigar):
    try:
        display = False
        TL = False
        bufferImage = []
        nbImage = 0
        wResize = 0
        hResize = 0
        newx = 0
        newy = 0
        numeroMask = 0
        while True:            
            ret, frame = camera.read()		
            screen.fill([255,255,255])
            if display == True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detectFaces(gray)
                i = 0
                i = isBodyPartDetected(faces,i)      
                if i == 1:                    
                    if TL == True:
                        frame = thugLife(faces,frame,i,TL)
                    else:
                        frame = faceIsDetected(faces, mask, frame,TL,numeroMask)
                if i == 0:
                    print("No face found")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0,0))
            screen.blit(boutonMask1, (663,93))
            screen.blit(boutonMask2, (751,0))
            screen.blit(boutonMask3, (855,0))
            screen.blit(boutonMask4, (765,93))
            screen.blit(boutonMask5, (657,190))
            screen.blit(boutonMask6, (867,93))
            screen.blit(boutonMask7, (759,190))
            screen.blit(boutonMask8, (963,93))
            screen.blit(boutonMask9, (871,190))
            screen.blit(boutonMask10, (961,0))
            screen.blit(boutonMask11, (648,310))
            screen.blit(boutonMask12, (977,200))
            screen.blit(boutonMask13, (856,298))
            screen.blit(boutonMask14, (979,298))
            screen.blit(boutonMask15, (640,395))
            screen.blit(boutonMask16, (752,305))
            screen.blit(boutonMask17, (640,0))
            screen.blit(boutonMask18, (710,395))
            screen.blit(boutonSave, (100,480))
            screen.blit(boutonReset, (410,480))
            screen.blit(boutonTL, (800,395))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    sys.exit(0)
                elif event.type == MOUSEBUTTONUP: # quand je relache le bouton
                    if event.button == 1: # 1= clique gauche
                        if boutonMask1Area.collidepoint(event.pos):
                            numeroMask = 1
                            TL = False
                            display = True
                            mask = masks[0]
                        if boutonMask2Area.collidepoint(event.pos):
                            numeroMask = 2
                            TL = False
                            display = True
                            mask = masks[1]
                        if boutonMask3Area.collidepoint(event.pos):
                            numeroMask = 3
                            TL = False
                            display = True
                            mask = masks[2]
                        if boutonMask4Area.collidepoint(event.pos):
                            numeroMask = 4
                            TL = False
                            display = True
                            mask = masks[3]
                        if boutonMask5Area.collidepoint(event.pos):
                            numeroMask = 5
                            TL = False
                            display = True
                            mask = masks[4]
                        if boutonMask6Area.collidepoint(event.pos):
                            numeroMask = 6
                            TL = False
                            display = True
                            mask = masks[5]
                        if boutonMask7Area.collidepoint(event.pos):
                            numeroMask = 7
                            TL = False
                            display = True
                            mask = masks[6]
                        if boutonMask8Area.collidepoint(event.pos):
                            numeroMask = 8
                            TL = False
                            display = True
                            mask = masks[7]
                        if boutonMask9Area.collidepoint(event.pos):
                            numeroMask = 9
                            TL = False
                            display = True
                            mask = masks[8]
                        if boutonMask10Area.collidepoint(event.pos):
                            numeroMask = 10
                            display = True
                            mask = masks[9]
                        if boutonMask11Area.collidepoint(event.pos):
                            numeroMask = 11
                            TL = False
                            display = True
                            mask = masks[10]
                        if boutonMask12Area.collidepoint(event.pos):
                            numeroMask = 12
                            TL = False
                            display = True
                            mask = masks[11]
                        if boutonMask13Area.collidepoint(event.pos):
                            numeroMask = 13
                            TL = False
                            display = True
                            mask = masks[12]
                        if boutonMask14Area.collidepoint(event.pos):
                            numeroMask = 14
                            TL = False
                            display = True
                            mask = masks[13]
                        if boutonMask15Area.collidepoint(event.pos):
                            numeroMask = 15
                            TL = False
                            display = True
                            mask = masks[14]
                        if boutonMask16Area.collidepoint(event.pos):
                            numeroMask = 16
                            TL = False
                            display = True
                            mask = masks[15]
                        if boutonMask17Area.collidepoint(event.pos):
                            numeroMask = 17
                            TL = False
                            display = True
                            mask = masks[16]
                            son = pygame.mixer.Sound("sound/flash.wav")
                            son.play()
                        if boutonMask18Area.collidepoint(event.pos):
                            numeroMask = 18
                            TL = False
                            display = True
                            mask = masks[17]
                        if boutonSaveArea.collidepoint(event.pos):
                            nbImage = nbImage + 1
                            try: 
                                os.makedirs("ImageSaved")
                            except OSError:
                                if not os.path.isdir("ImageSaved"):
                                    Raise
                            pygame.image.save(frame, "ImageSaved/image"+str(nbImage)+".jpg")
                        if boutonResetArea.collidepoint(event.pos):
                            display = False
                        if boutonTLArea.collidepoint(event.pos):
                            display = True
                            TL = True
    except (KeyboardInterrupt,SystemExit):
        cap.release()
        pygame.quit()
        cv2.destroyAllWindows()


startCam(cap,masks,faces_cascade,specs,cigar)

