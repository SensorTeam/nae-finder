"""
Finds potential eye signals from a .jpg by finding bright spots in the image.
Does not take into account signal duality
Last modified: 17 APR 18
"""

from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import math

####### SET MACROS ####

GRADIUS = 1		# gaussian blur radius, must be odd

THRESH = 120		# minimum brightness

#MINMASKSIZE = 30		# size masking for noise reduction
#MAXMASKSIZE = 500

MINAREA = 10			# refine mask sizes
MAXAREA = 30000

MINCIRCULARITY = 0.5		# between 0 and 1

MAXRADIUS = 20		# max eye radius

#######################


# Returns list of contours refined by size, circularity, and radius
def mask_circles(contours):
	contours_area = []
	contours_circles = []
	contours_radius = []
	# find contours of correct area
	for con in contours:
		area = cv2.contourArea(con)
		if MINAREA < area < MAXAREA:
			contours_area.append(con)
			# find contours of sufficient circularity
			perimeter = cv2.arcLength(con, True)
			if perimeter == 0:
				break
			circularity = 4*math.pi*(area/(perimeter*perimeter))
			if MINCIRCULARITY < circularity < 1.0:
				contours_circles.append(con)
				# find contours of smaller radius			
				(x, y), radius = cv2.minEnclosingCircle(con)
				if radius < MAXRADIUS:
					contours_radius.append(con)
	return contours_radius


# Returns final contours of potential eye signals
def find_eye(image):
	 
	# make a copy of the image and convert it to grayscale
	orig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# apply a Gaussian blur to the image then find the brightest region
	blurred = cv2.GaussianBlur(gray, (GRADIUS, GRADIUS), 0)

	# threshold the image to reveal light regions in the blurred image
	# any pixel with brightness greater than 80 is set to white, everything else set to black
	thresh = cv2.threshold(blurred, THRESH, 255, cv2.THRESH_BINARY)[1]

	# erode and dilate to remove noise
	thresh = cv2.erode(thresh, None, iterations=2)
	thresh = cv2.dilate(thresh, None, iterations=4)

	# connected component analysis
	# mask stores "large" components
	labels = measure.label(thresh, neighbors=8, background=0)
	mask = np.zeros(thresh.shape, dtype="uint8")

	for label in np.unique(labels):
		# if label is background, ignore
		if label == 0:
			continue
		# else construct label mask and count pixels
		labelMask = np.zeros(thresh.shape, dtype="uint8")
		labelMask[labels == label] = 255
		numPixels = cv2.countNonZero(labelMask)

		# if the number of pixels in the component is sufficiently and appropriate size
		# ie large enough to not be noise, small enough to be an eye
		# then add it to our mask of regions
#		if numPixels > MINMASKSIZE and numPixels < MAXMASKSIZE:
		mask = cv2.add(mask, labelMask)

	# find contours
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	cnts_final = mask_circles(cnts)


	# circle around the bright spots on the image
	for con in cnts_final:
		(cX, cY), radius = cv2.minEnclosingCircle(con)
		cv2.circle(image, (int(cX), int(cY)), int(radius+2), (0, 0, 255), 2)
	# save circled image
	cv2.imwrite("output_circled.jpg", image)


	return cnts_final