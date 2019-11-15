import numpy as np
import cv2
from matplotlib import pyplot as plt
 
img = cv2.imread('../model.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
 
# Step 1
rect = (100,0,250,150)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,1,cv2.GC_INIT_WITH_RECT)

# Step 2
newmask = cv2.imread('../mark3.png',0)
''' 
length = newmask.shape
for x in range(newmask.shape[0]):
    for y in range(newmask.shape[1]):
        if newmask[x][y] == [0,0,0] :
            mask[x][y] = 0
        elif newmask[x][y] == [255,255,255] :
            mask[x][y] = 1s
 '''

""" mask[newmask == [0,0,0]] = 0
mask[newmask == [255,255,255]] = 1 

cv2.grabCut(img,mask,None,bgdModel,fgdModel,1,cv2.GC_INIT_WITH_MASK) """
 
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

plt.imshow(img)
plt.colorbar()
plt.show()

img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  
cv2.imwrite("../result.png",img)
