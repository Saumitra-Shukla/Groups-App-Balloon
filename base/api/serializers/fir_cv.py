import imutils
import cv2
 
image=cv2.imread('index.jpeg')
h,w,d=image.shape
print('width=%d, height= %d, depth= %d' % (h,w,d))
cv2.imshow("image",image)
cv2.waitkey(0)