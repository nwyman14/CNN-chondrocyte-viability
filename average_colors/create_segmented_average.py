from PIL import Image
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
im = Image.open('mask.tif')
pixy=np.array(im)
pix = np.zeros((im.size[0],im.size[1]), 'uint32')
for y in range(0,im.size[0]):
    for x in range(0,im.size[1]):
        pix[x,y]=pixy[x,y]
countup=256
coloringmode=0
print(im.size)
for y in range(0,im.size[0]):
    for x in range(0,im.size[1]):
        if(x==0):
            if(coloringmode!=0):
                coloringmode=0
                countup+=1
        if(coloringmode==0):
            if(pix[x,y]==255):
                coloringmode=countup
                if(y!=0):
                    if(pix[x,y-1]!=coloringmode and pix[x,y-1]!=0):
                        pix[pix==coloringmode]=pix[x,y-1]
                        coloringmode=pix[x,y-1]
                        pix[x,y]=coloringmode
                    else:
                        pix[x,y]=coloringmode
                else:
                    pix[x,y]=coloringmode
        else:
            if(pix[x,y]==255):
                if(y!=0):
                    if(pix[x,y-1]!=coloringmode and pix[x,y-1]!=0):
                        pix[pix==coloringmode]=pix[x,y-1]
                        coloringmode=pix[x,y-1]
                        pix[x,y]=coloringmode
                    else:
                        pix[x,y]=coloringmode
                else:
                    pix[x,y]=coloringmode
            else:
                countup+=1
                coloringmode=0
print(pix)
imr = Image.open('red.tif')
img = Image.open('green.tif')
ims = Image.open('shg.tif')
ayr=np.array(imr)
ayg=np.array(img)
ays=np.array(ims)
#ayg=ayg-ays
ayg[ayg<0]=0
diffen=1+np.amax(ayr)
rs = np.zeros((np.amax(pix)+1), 'uint32')
gs = np.zeros((np.amax(pix)+1), 'uint32')
rgbArray = np.zeros((im.size[0],im.size[1],3), 'uint8')
cellcount=0
for i in range(256,np.amax(pix)+1):
    if i in pix[:,:]:
        cellcount+=1
cellid = np.zeros((cellcount), 'uint32')
cellx = np.zeros((cellcount), 'uint32')
celly = np.zeros((cellcount), 'uint32')
cellarea = np.zeros((cellcount), 'uint32')
cellpics = np.zeros((cellcount), 'uint32')
cellcount=0
for i in range(256,np.amax(pix)+1):
    if i in pix[:,:]:
        cellid[cellcount]=i
        cellarea[cellcount]=np.sum(pix==i)
        cellcount+=1
pixxx=pix*1024
for y in range(0,im.size[0]):
    for x in range(0,im.size[1]):
        pixxx[x,y]+=x
pixyy=pix*1024
for y in range(0,im.size[0]):
    for x in range(0,im.size[1]):
        pixyy[x,y]+=y
for i in range(0,cellcount):
    cellx[i]=np.average(((pixxx-1024*cellid[i])[(pixxx-1024*cellid[i])>0])[(pixxx-1024*cellid[i])[(pixxx-1024*cellid[i])>0]<1024])
    celly[i]=np.average(((pixyy-1024*cellid[i])[(pixyy-1024*cellid[i])>0])[(pixyy-1024*cellid[i])[(pixyy-1024*cellid[i])>0]<1024])
    cropr=np.array(imr)[int(max(cellx[i]-math.sqrt(cellarea[i]),0)):int(min(cellx[i]+math.sqrt(cellarea[i]),1024)),int(max(celly[i]-math.sqrt(cellarea[i]),0)):int(min(celly[i]+math.sqrt(cellarea[i]),1024))]
    cvarr=cv2.resize(cropr, dsize=(160,160), interpolation=cv2.INTER_CUBIC)
    cropg=np.array(img)[int(max(cellx[i]-math.sqrt(cellarea[i]),0)):int(min(cellx[i]+math.sqrt(cellarea[i]),1024)),int(max(celly[i]-math.sqrt(cellarea[i]),0)):int(min(celly[i]+math.sqrt(cellarea[i]),1024))]
    cvarg=cv2.resize(cropg, dsize=(160,160), interpolation=cv2.INTER_CUBIC)
    cropb=np.array(ims)[int(max(cellx[i]-math.sqrt(cellarea[i]),0)):int(min(cellx[i]+math.sqrt(cellarea[i]),1024)),int(max(celly[i]-math.sqrt(cellarea[i]),0)):int(min(celly[i]+math.sqrt(cellarea[i]),1024))]
    cvarb=cv2.resize(cropb, dsize=(160,160), interpolation=cv2.INTER_CUBIC)
    rgbArray = np.zeros((160,160,3), 'uint8')
    rgbArray[..., 0] = cvarr / np.amax(cvarr) * 255
    rgbArray[..., 1] = cvarg / np.amax(cvarg) * 255
    rgbArray[..., 2] = cvarb / np.amax(cvarb) * 255
    Image.fromarray(rgbArray).save("indcells/"+str(i)+".png")
for i in range(0,cellcount):
    #if(i%10==0):
    print(str(i)+"/"+str(cellcount)+" "+str(int(cellx[i]))+" "+str(int(celly[i])))
    newr=pix*diffen+ayr
    newr[newr<cellid[i]*diffen]=cellid[i]*diffen
    newr[newr>(cellid[i]+1)*diffen]=cellid[i]*diffen
    newr=newr-cellid[i]*diffen
    if(not math.isnan(np.average(newr[newr>0]))):
        rs[cellid[i]]=np.average(newr[newr>0])
    newg=pix*diffen+ayg
    newg[newg<cellid[i]*diffen]=cellid[i]*diffen
    newg[newg>(cellid[i]+1)*diffen]=cellid[i]*diffen
    newg=newg-cellid[i]*diffen
    if(not math.isnan(np.average(newg[newg>0]))):
        gs[cellid[i]]=np.average(newg[newg>0])
    if(i==13 or i==87 or i==137 or i==150 or i==151 or i==173):
        histred,bin= np.histogram(newr[newr>0], bins=100)
        histgreen,bin= np.histogram(newg[newg>0], bins=100)
        center = np.amin(newr[newr>0])+1
        plt.plot(np.arange(1,100), histred[1:],"r",np.arange(1,100), histgreen[1:],"g")
        plt.title('Histogram of Autofluorescence Brightness in Cell')
        plt.xlabel('Relative Frequency')
        plt.ylabel('Red/Green Brightness')
        plt.show()
    
rgbArray = np.zeros((im.size[0],im.size[1],3), 'uint8')
    
for y in range(0,im.size[0]):
    for x in range(0,im.size[1]):
        rgbArray[x,y,0]=rs[pix[x,y]]
        rgbArray[x,y,1]=gs[pix[x,y]]
        rgbArray[x,y,2]=0
im=Image.fromarray(np.uint8(rgbArray))
im.save('coloredmask.png')