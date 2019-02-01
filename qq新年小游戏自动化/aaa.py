import os
from PIL import Image
import time
import math
import cv2
import numpy as np 
import heapq
def getScreenImage(filename='screen.png'):
	os.system('del backup.png')
	os.system('copy {} backup.png'.format(filename))
	os.system('adb shell screencap -p /sdcard/screen.png')
	os.system('adb pull /sdcard/screen.png '+filename)
def getxy(index):
	x = index%720
	y = math.floor(index/720)
	return x,y
def makeOriginalPointBlue(filename):
	im = cv2.imread(filename)
	t = np.array([1/3,1/3,1/3])
	tt = im@t
	imgray = tt.astype('uint8')
	_,imbinary = cv2.threshold(imgray,50,255,cv2.THRESH_BINARY)
	_,contours,hierarchy = cv2.findContours(imbinary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	imcontour = cv2.drawContours(np.zeros(im.shape),contours,-1,(255,255,255),2)
	r = None
	for i in range(len(contours)):
		contour = contours[i]
		if hierarchy[0][i][2]==-1:
			area = cv2.contourArea(contour)
			radius = math.sqrt(area/math.pi)
			d = contour.max(0)[0][1] - contour.min(0)[0][1]
			print('d',d)
			print('radius',radius)
			print('rate',abs(d-2*radius)/d)
			if d>20 and (abs(d-2*radius)/d)<0.15:
				print('mark')
				cv2.drawContours(im,contours,i,(255,255,255),2)
				cv2.namedWindow('contour',cv2.WINDOW_NORMAL)
				cv2.imshow('contour',im)
				cv2.waitKey(0)
				r = contour.sum(0)/contour.size*2
				r = r[0]
	if r is None:
		return None
	return r[0],r[1]+radius*42/47
def makeTargetPointBlue(im,threshold=1280):
	d = im.getdata()
	dd = list(d)
	rx = 0
	ry = 0
	cnt = 0
	for i in range(threshold*720):
		if dd[i]==(227,56,53,255):
			dd[i] = (0,0,255,255)
			cnt += 1
			x,y = getxy(i)
			rx += x
			ry += y
	im.putdata(dd)
	print('threshold',threshold)
	print('cnt',cnt)
	print('rx',rx)
	print('ry',ry)
	rx = math.floor(rx/cnt)
	ry = math.floor(ry/cnt)
	return rx,ry,cnt
def getOriginalPoint(filename):
	im = cv2.imread(filename)
	t = np.array([1/3,1/3,1/3])
	tt = im@t
	imgray = tt.astype('uint8')
	_,imbinary = cv2.threshold(imgray,50,255,cv2.THRESH_BINARY)
	_,contours,hierarchy = cv2.findContours(imbinary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	for i in range(len(contours)):
		contour = contours[i]
		if hierarchy[0][i][2]==-1:
			area = cv2.contourArea(contour)
			radius = math.sqrt(area/math.pi)
			d = contour.max(0)[0][1] - contour.min(0)[0][1]
			#print('d',d)
			#print('radius',radius)
			#print('rate',abs(d-2*radius)/d)
			if d>20 and (abs(d-2*radius)/d)<0.15:
				r = contour.sum(0)/contour.size*2
				r = r[0]
				return r[0],r[1]+radius*42/47
def getTargetPoint(im,threshold=1280):
	d = im.getdata()
	dd = list(d)
	rx = 0
	ry = 0
	cnt = 0
	for i in range(threshold*720):
		if dd[i]==(227,56,53,255):
			cnt += 1
			x,y = getxy(i)
			rx += x
			ry += y
	rx = math.floor(rx/cnt)
	ry = math.floor(ry/cnt)
	return rx,ry,cnt
def calcDistance(x1,y1,x2,y2):
	t1 = abs(x2-x1)
	t2 = abs(y2-y1)
	return math.sqrt(t1*t1+t2*t2)
def touch(time):
	os.system('adb shell input swipe 0 0 0 0 {}'.format(int(time)))


debug = False
a = 30.3
if debug:
	im = Image.open('screen.png')
	im.show()
	ox,oy = makeOriginalPointBlue('screen.png')
	tx,ty,size=makeTargetPointBlue(im,int(oy))
	im.show()
	print(ox,oy,tx,ty,size)
	dis = calcDistance(ox,oy,tx,ty)
	t = a*dis/math.sqrt(size)
	print(t)
	cv2.waitKey(0)
while not debug:
	getScreenImage()
	im = Image.open('screen.png')
	ox,oy = getOriginalPoint('screen.png')
	tx,ty,size = getTargetPoint(im,int(oy))
	dis = calcDistance(ox,oy,tx,ty)
	t = a*dis/math.sqrt(size)
	if size>40 and size<100 and dis>300:
		t *= 0.87
	if size<40:
		t *= 0.84
	print('dis',dis)
	print('size',size)
	with open('record.txt','a+') as f:
		f.write(str(dis)+' '+str(size)+' '+str(t)+'\n')
	print('t',t)
	touch(t)
	time.sleep(3)