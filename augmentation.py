from os import listdir
from os.path import isfile, join
from PIL import Image
import skimage
from skimage import io
from skimage.transform import rotate
import matplotlib.pyplot as plt
import numpy as np
import cv2
cropdim=256
cropcount=6
file_path='cropdata/1'
totalnews=0
totalmasks=0
mypath='data/SHG/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
from PIL import Image
intervalofcrop=int((1024-cropdim)/(cropcount-1))
print("Cropping...")
for f in onlyfiles:
    if f.find('.tif')!=-1:
        im = skimage.external.tifffile.imread(mypath+f)
        if f.find('mask')==-1:
            for x in range(0,cropcount):
                for y in range(0,cropcount):
                    img = im[x*intervalofcrop:x*intervalofcrop+cropdim,y*intervalofcrop:y*intervalofcrop+cropdim]
                    skimage.external.tifffile.imsave(file_path + '_' + str(cropcount*cropcount*(int(f[2:2+f[2:].find(".")])-1)+cropcount*x+y) + '.tif', img)
                    totalnews+=1
        else:
            for x in range(0,cropcount):
                for y in range(0,cropcount):
                    img = im[x*intervalofcrop:x*intervalofcrop+cropdim,y*intervalofcrop:y*intervalofcrop+cropdim]
                    skimage.external.tifffile.imsave(file_path + '_' + str(cropcount*cropcount*(int(f[2:2+f[2:].find("_")])-1)+cropcount*x+y) + '_mask.tif', img)
                    totalmasks+=1
print("Cropping done.")
print("Rotating...")
file_path='rotdata/1'
totalnews=0
totalmasks=0
mypath='cropdata/'
degrees_of_rotation=[0,60,90,120,180]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for f in onlyfiles:
    if f.find('.tif')!=-1:
        if f.find('mask')==-1:
            im = skimage.external.tifffile.imread(mypath+f)
            for r in degrees_of_rotation:
                img = (rotate(im,r)*65536).astype(np.uint16)
                skimage.external.tifffile.imsave(file_path + '_' + str(5*int(f[2:2+f[2:].find(".")])+degrees_of_rotation.index(r)) +'.tif', img)
                totalnews+=1
            im = skimage.external.tifffile.imread(mypath+f[:len(f)-4]+"_mask.tif")
            for r in degrees_of_rotation:
                img = (rotate(im,r)*255).astype(np.uint8)
                skimage.external.tifffile.imsave(file_path + '_' + str(5*int(f[2:2+f[2:].find(".")])+degrees_of_rotation.index(r)) + '_mask.tif', img)
                totalmasks+=1
print("Rotating done.")
print("Reflecting...")
file_path='newdata/1'
totalnews=0
totalmasks=0
mypath='rotdata/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for f in onlyfiles:
    if f.find('.tif')!=-1:
        if f.find('mask')==-1:
            im = skimage.external.tifffile.imread(mypath+f)
            img = cv2.flip(im,1)
            skimage.external.tifffile.imsave(file_path + '_' + str(2*int(f[2:2+f[2:].find(".")])) + '.tif', im)
            skimage.external.tifffile.imsave(file_path + '_' + str(2*int(f[2:2+f[2:].find(".")])+1) + '.tif', img)
            totalnews+=2
            im = skimage.external.tifffile.imread(mypath+f[:len(f)-4]+"_mask.tif")
            img = cv2.flip(im,1)
            skimage.external.tifffile.imsave(file_path + '_' + str(2*int(f[2:2+f[2:].find(".")])) + '_mask.tif', im)
            skimage.external.tifffile.imsave(file_path + '_' + str(2*int(f[2:2+f[2:].find(".")])+1) + '_mask.tif', img)
            totalmasks+=2
print("Reflecting done.")