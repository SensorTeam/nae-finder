from find_eye import *
import argparse

########
import math
########

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

contours = find_eye(image)

pairs = find_pairs(image, contours)

# find pairs

def find_pairs(image, cnts):
	pairs = []
	con_det = []
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
		w1 = con1[3]-con1[2]
		h1 = con1[5]-con1[4]
		for j in range(i+1, len(cnts)):
			con2 = con_det[j]
			x2 = con2[0]
			y2 = con2[1]
			w2 = con2[3]-con2[2]
			h2 = con2[5]-con2[4]
			# same height and width (within 1.5)
			if 0.67*x2 < x1 < 1.5*x2 and 0.67*y2 < x1 < 1.5*y2:
				# angle of orientation < 30 deg
				theta = atan((y2-y1) / (x2-x1))
				if degrees(theta) < 30:
					# x not more than 5 times the average eye width across
					maxdist = (w1+w2) / 2 * 5
					if abs(x2-x1) < maxdist:
						# add eyes to list of pairs
						pairs.append([con_det[i], con_det[j]])

# find the approximate centre
def find_centre(con):
	# compute the centre of the contour
	M = cv2.moments(con)
	x = int(M["m10"] / M["m00"])
	y = int(M["m01"] / M["m00"])
	return (x, y)

find_pairs(image, contours)