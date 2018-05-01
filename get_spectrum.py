"""
Returns matrix of pixel and intensity for eye spectrums
"""

import math
import numpy as np
import cv2


# Returns the spectrum (pixel v intensity) for an eye given the left and right boundaries
# Intensity is total intensity all pixels in that row
# Image must be grayscale
def eye_spectrum(eye, left, right, image):
	spectrum = []
	[x, y, extL, extR, extT, extB] = eye
#	numpix = right - left
	# for each row in the image until just above the top of the eye
	for i in range(0, extT[1]-(extB[1]-extT[1])):
		intensity = 0
		# for each pixel in section containing spectrum
		for j in range(left, right):
			# if pixel is bright enough
			if image[i][j] > 10:
				# get brightness imagegray[i][j]
				intensity += image[i][j]
#		# average out the brightness for the row
#		ave_intensity = intensity / numpix
		spectrum.append([i, intensity])
	return spectrum


# Calls eye_spectrum() for each eye
	# pair = [eye1, eye2]
	# eye1 = [x, y, extL, extR, extT, extB]
def get_spectrum(pair, image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	eye1, eye2 = pair
	
	width1, width2 = eye1[3][0]-eye1[2][0], eye2[3][0]-eye2[2][0]
	cen = math.floor( (eye1[0]+eye2[0]) / 2 )

	spec1 = eye_spectrum(eye1, math.floor(eye1[2][0]-width1), cen, gray)
	spec2 = eye_spectrum(eye2, cen, math.ceil(eye2[3][0]+width2)+1, gray)
	return [spec1, spec2]
