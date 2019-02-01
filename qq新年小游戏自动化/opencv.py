import cv2
import numpy as np 
import heapq
import math
def secondLarge(l):
	print('l',l)
	t = heapq.nlargest(2,l)
	print('t',t)
	t = t[-1]
	return l.index(t)
def getOriginPoint(filename):
	im = cv2.imread(filename)
	t = np.array([1/3,1/3,1/3])
	tt = im@t
	imgray = tt.astype('uint8')
	_,imbinary = cv2.threshold(imgray,50,255,cv2.THRESH_BINARY)
	_,contours,hierarchy = cv2.findContours(imbinary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	print(contours[0].shape)
	for i in range(len(contours)):
		contour = contours[i]
		if hierarchy[0][i][2]==-1:
			area = cv2.contourArea(contour)
			radius = math.sqrt(area/math.pi)
			d = contour.max(0)[0][1] - contour.min(0)[0][1]
			print('d',d)
			print('radius',radius)
			print('rate',abs(d-2*radius)/d)
			if (abs(d-2*radius)/d)<0.05:
				r = contour.sum(0)/contour.size*2
				r = r[0]
				return r[0],r[1]+radius*42/47


size = getOriginPoint('backup.png')
print(size)
cv2.waitKey(0)