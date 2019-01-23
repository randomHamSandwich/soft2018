class Entitet:
    def __init__(self,x,y,eID,age):
        self.x = x
        self.y = y
        self.eID = eID
        self.age = age
        self.previusPositionsX= []
        self.previusPositionsY= []
        self.noMatchAge=0
        self.isMatchedCurrentFrame = False


    def updateXY(self,xx,yy):
        self.previusPositionsX.append(self.x)
        self.previusPositionsY.append(self.y)
        if(len(self.previusPositionsX))>=4:
            self.previusPositionsX.pop(0)
            self.previusPositionsY.pop(0)
        self.x=xx
        self.y=yy
    def incAge(self):
        self.age += 1
    def predictNextPosition(self):
        #xNovo-xStaro
       # return (self.x,self.y)
       if len(self.previusPositionsX )== 0:
            return (self.x,self.y)
       if len(self.previusPositionsX)== 1:
            pomeraj= (self.x-self.previusPositionsX[0]
                      , self.y-self.previusPositionsY[0])
            
            return (self.x+pomeraj[0], self.y+pomeraj[1])
        
       if len(self.previusPositionsX )== 2:
            pomeraj= (((self.x-self.previusPositionsX[1])*2+(self.previusPositionsX[1]-self.previusPositionsX[0]))/3
                      , ((self.y-self.previusPositionsY[1])*2+(self.previusPositionsY[1]-self.previusPositionsY[0]))/3)
            
            return (self.x+pomeraj[0], self.y+pomeraj[1])       
        
       if len(self.previusPositionsX )== 3:
            pomeraj= (((self.x-self.previusPositionsX[2])*3+(self.previusPositionsX[2]-self.previusPositionsX[1])*2+(self.previusPositionsX[1]-self.previusPositionsX[0]))/6
                      , ((self.y-self.previusPositionsY[2])*3+(self.previusPositionsY[2]-self.previusPositionsY[1])*2+(self.previusPositionsY[1]-self.previusPositionsY[0]))/6)
            
            return (self.x+pomeraj[0], self.y+pomeraj[1])       
                    
        

import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt 
matplotlib.rcParams['figure.figsize'] = 16,12
video= r"C:\spyderSoft\soft2018\video1.mp4"


cap = cv2.VideoCapture(video)
w = cap.get(3) #get width nasheg prozora
h = cap.get(4) #get height naseg prozora

frameCountX = int(5*w/7)
frameCountY = int(h/20)
fameCount = 0

#konture u ovom frejmu
peopleCountX=int(w/50)
peopleCountY=int(h/20)
peopleCount=0

countX=peopleCountX
countY=peopleCountY+40
count=[] # koliko je izbrojano ljudi

idEnt=0

contours_entiteta = [] # konture trenutnog frejma
entiteti = []

isFirstFrame= True ;

#y=kx+n BT za border top
kBT=0
nBT=0

#tacka a i tacka b topBordera
topBorderA =[]
topBorderB =[]

fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True) #Create the background substractor

while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    fgmask = fgbg.apply(frame) #Use the substractor
    ret,imBin = cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)   
    try:     
        if isFirstFrame:
           # print("xxxxxxxxxxxxxxxxXXXXXXXXXXXXXXXxxxxxxxxxx")
            ploting = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, frame0_bin = cv2.threshold(img_frame_gray, 145, 255, cv2.THRESH_BINARY) # ret je vrednost praga, image_bin je binarna slika
 
            #BT=border top
            kernelBT = np.ones((2, 10))
            imBin_dilate= cv2.dilate(frame0_bin,kernelBT, 1)

            img, contoursBT, hierarchyBT = cv2.findContours(imBin_dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours_entitetaBT = [] #ovde ce biti samo konture koje jesu ljudi
            for contourBT in contoursBT: # za svaku konturu
                centerBT, sizeBT, angleBT = cv2.minAreaRect(contourBT) # pronadji pravougaonik minimalne povrsine koji ce obuhvatiti celu konturu
                cXBT,cYBT,cWBT,cHBT = cv2.boundingRect(contourBT)
                widthBT, heightBT = sizeBT
                if widthBT/20> heightBT and widthBT>200  : # da li je gornja granica
                    contours_entitetaBT.append(contourBT) 
                    #print(angleBT)
                    #cv2.circle(ploting, (int(round(cXBT)),int(round(cYBT))), 1, (0,255,0), 2, 8, 0)
                    cv2.circle(ploting, (int(round(cXBT+cWBT)),int(round(cYBT))), 1, (255,255,255), 2, 8, 0)
                    cv2.circle(ploting, (int(round(cXBT)),int(round(cYBT+cHBT))), 1, (0,255,255), 2, 8, 0)
                    #cv2.circle(ploting, (int(round(cXBT+cWBT)),int(round(cYBT+cHBT))), 1, (0,255,0), 2, 8, 0)
                    topBorderA.append(cXBT)
                    topBorderA.append(cYBT+cHBT)
                    topBorderB.append(cXBT+cWBT)
                    topBorderB.append(cYBT)
                    
                    #k=(y2-y1)/(x2-x1)
                    #n=y1-k*x1
                    kBT=(cYBT-cYBT-cHBT)/(cXBT+cWBT-cXBT)
                    nBT=cYBT-kBT*(cXBT+cWBT)
                    #print("sdadsdsadsds ", kBT)
              
 #           ii=200
  #          while ii < 600:
   #             cv2.circle(ploting, (ii,int(round(kBT*ii+nBT))), 1, (0,255,0), 2, 8, 0)     
    #            ii=ii+1
            
            #print(str(len(contours_entitetaBT)))
            cv2.drawContours(ploting, contours_entitetaBT, -1, (255, 0, 0), 1)
            plt.imshow(ploting)
        
        #ispis frejmova
        fameCount = fameCount+1
        text = "Frame " + str(fameCount)
        cv2.putText(frame, text ,(frameCountX,frameCountY),cv2.FONT_HERSHEY_DUPLEX
                    ,1,(255,0,0),1,cv2.LINE_AA)
        
        
        #uklanjanje shuma
        kernel = np.ones((3, 3))
        imBin_erode= cv2.erode(imBin,kernel, 1)
        imBin_open= cv2.dilate(imBin_erode,kernel, 1)
        #erosion = cv2.erode(img,kernel,iterations = 1)
        # kernel = np.ones((5, 5)) # drugi kernel istestiraj sta daje najbolje rezultate
        imBin_open_dilate= cv2.dilate(imBin_open,kernel, 1)
        imBin_closed= cv2.erode(imBin_open_dilate,kernel, 1)
        
        #pronalazenje kontura
        img, contours, hierarchy = cv2.findContours(imBin_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_entiteta = [] #ovde ce biti samo konture koje jesu ljudi
        for contour in contours: # za svaku konturu
            center, size, angle = cv2.minAreaRect(contour) # pronadji pravougaonik minimalne povrsine koji ce obuhvatiti celu konturu
            cX,cY,cW,cH = cv2.boundingRect(contour)
            
            width, height = size
#            if width>5 and height >5 and width<70 and height <70   : # uslov da kontura jeste covek Implementiraj granijice implementiraj da li je novi covek
            if cW>5 and cH >5 and cW<70 and cH <70 and kBT*center[0]+nBT < center[1]-2  : # velicina da jeste potencijalno covek, y dobijeno uvrsavanje x treba da bude manje od nashg y da bi bilo ispod linije
                contour = cv2.convexHull(contour) #sve konture da budu konveksne da  NEMAMO KONKAVNIH
                contours_entiteta.append(contour) # jeste covek dodaj
                cv2.circle(frame, (int(round(center[0])),int(round(center[1]))), 1, (0,255,0), 2, 8, 0)
                
        #resetuj match za ovaj frame
        for entitet in entiteti:
            entitet.isMatchedCurrentFrame= False
        
        jeNovEntitet =True
        for ccc in contours_entiteta:
            for entitet in entiteti:
                center, size, angle = cv2.minAreaRect(ccc)
#                if abs(entitet.x-center[0]) <= 15 and abs(entitet.y-center[1]) <= 15: 
                predXY = entitet.predictNextPosition()
                if abs(predXY[0]-center[0]) <= 15 and abs(predXY[1]-center[1]) <= 15 and entitet.noMatchAge<50:      
                    entitet.incAge()
                    entitet.updateXY(center[0],center[1])
                    jeNovEntitet = False
                    entitet.isMatchedCurrentFrame= True
                    entitet.noMatchAge=0
                    break 
                
                
            if jeNovEntitet:
                eTemp = Entitet(center[0],center[1],idEnt,0)
                entiteti.append(eTemp)
                idEnt= idEnt+1
        
        
        for entitet in entiteti:
            if entitet.isMatchedCurrentFrame== False:
                entitet.noMatchAge = entitet.noMatchAge+1
            
        for en in entiteti:
            if en.noMatchAge>=50:
                en.x=-1
                en.y=-1
                en.previusPositionsX=[]
                en.previusPositionsY=[]
                
            if en.age > 16:
                if en not in count:
                   count.append(en)
       

                
        #ispis broja ljuci. Trenutno ispisuje samo broj kontura u tom frejmu
        peopleCount = len(contours_entiteta)
        text = "Kontura u frame:"  + str(peopleCount)
        cv2.putText(frame, text ,(peopleCountX,peopleCountY),cv2.FONT_HERSHEY_DUPLEX
                    ,1,(0,0,255),1,cv2.LINE_AA)
        

        text = "count: "  +str(len(count))
        cv2.putText(frame, text ,(countX,countY),cv2.FONT_HERSHEY_DUPLEX
                    ,1,(0,0,255),1,cv2.LINE_AA)
        
        
        cv2.drawContours(frame, contours_entiteta, -1, (255, 0, 0), 1)
        cv2.line(frame, (topBorderA[0], topBorderA[1]), (topBorderB[0], topBorderB[1]), (255,0,0), 2)

        #cv2.line(frame, (30, 50), (60, 50), (255,0,0), 2)
        cv2.imshow('originalna',frame)
        #cv2.imshow('Binarna',imBin)
        #cv2.imshow('closed', imBin_closed)
        
        isFirstFrame = False
    except Exception as e: 
        #print(e)
        #nema vishe frejmova ili greshka
        break
    
    #exit  ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
print( "na snimku", video ," je izbrojano: ",str(len(count))," ljudi")
cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows
