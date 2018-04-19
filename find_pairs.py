"""
Refines contours by finding ones that are matched with pairs
Takes as input an image and its respective contours from find_eye.py
Returns array of details if points
"""
import cv2
import numpy as np 
import math


# find pairs

def find_pairs(image, cnts):
	pair_det = []
	con_det = []
	con_pairs = []
	for con in cnts:
		(x, y) = find_centre(con)
		extL = tuple(con[con[:,:,0].argmin()][0])
		extR = tuple(con[con[:,:,0].argmax()][0])
		extT = tuple(con[con[:,:,1].argmin()][0])
		extB = tuple(con[con[:,:,1].argmax()][0])
		con_det.append([x, y, extL, extR, extT, extB])
	# compare with every contour after itself
	for i in range(0, len(cnts)-1):
		con1 = con_det[i]
		x1 = con1[0]
		y1 = con1[1]
		w1 = con1[3][0]-con1[2][0]
		h1 = con1[5][1]-con1[4][1]
		for j in range(i+1, len(cnts)):
			con2 = con_det[j]
			x2 = con2[0]
			y2 = con2[1]
			w2 = con2[3][0]-con2[2][0]
			h2 = con2[5][1]-con2[4][1]
			# same height and width (within 1.5)
			if 0.67*w2 < w1 < 1.5*w2 and 0.67*h2 < h1 < 1.5*h2:
				#print("size")
				# angle of orientation < 30 deg
				theta = math.degrees(math.atan((y2-y1) / (x2-x1)))
				if -30 < theta < 30:
				#	print("angle")
					# x not more than 7 times the average eye width across
					maxdist = (w1+w2) / 2 * 7
					if abs(x2-x1) < maxdist:
				#		print("dist")
						# add eyes to list of pairs
						pair_det.append([con_det[i], con_det[j]])
						con_pairs.append([cnts[i], cnts[j]])
	pairs = [con_pairs, pair_det]
	return pairs

# find the approximate centre of each shape
def find_centre(con):
	M = cv2.moments(con)
	x = int(M["m10"] / M["m00"])
	y = int(M["m01"] / M["m00"])
	return (x, y)
