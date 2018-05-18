"""
Returns matrix of pixel and intensity for eye spectrums
"""

import math
import numpy as np
import cv2


# only get the most relevant parts of the spectrum
def calibrate(spec, green500):
	# calibrate using points at 0nm (the point source) and 500nm
	wav = []
	intensities = []
	# calculate the conversion
	conv = green500/500
	# for each wavelength, find the associated pixel and intensity
	for w in range(400,721):
		pix = round(w*conv)
		adjust = spec[0][0]
		i = spec[pix-adjust][1]
		intensities.append(i)
		wav.append([w, i])
	# standardise to percentages
	max_intensity = max(intensities)
	for val in wav:
		val[1] = val[1]/max_intensity
	# smoothing
	
	return wav

# convert RGB to HSV and return hue
def get_hue(colour):
	rr,gg,bb = colour
	r,g,b = rr/255, gg/255, bb/255
	M = max(r,g,b)
	m = min(r,g,b)
	c = M - m
	if c == 0:
		hue = 0
	elif M == r:
		#g, b = int(round(g)), int(round(b))
		hue = ((g-b)/c)%6
	elif M == g:
		hue = (b-r)/c + 2
	elif M == b:
		hue = (r-g)/c + 4
	hue = hue*60
	return hue


UPPERBOUND = 0
LOWERBOUND = 1300
# Returns the spectrum (pixel v intensity) for an eye given the left and right boundaries
# Intensity is total intensity all pixels in that row
def eye_spectrum(eye, left, right, image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	spectrum = []
	rgb = []
	[x, y, extL, extR, extT, extB] = eye
	# for each row in the image until just above the top of the eye
	####### CHANGE RANGE VALUES AFTER CALIBRATION - CAN BE CENTRE OF EYE + KNOWN VALUE TO AVOID NOISE
	for i in range(UPPERBOUND, LOWERBOUND):  # extT[1]-(extB[1]-extT[1])
		numpix, intensity, tot_r, tot_g, tot_b = 0, 0, 0, 0, 0
		# for each pixel in section containing spectrum
		for j in range(left, right):
			# if pixel is bright enough
			if gray[i][j] > 10:
				numpix += 1
				# get brightness
				intensity += gray[i][j]
				b,g,r = image[i,j]
				tot_r += r
				tot_g += g
				tot_b += b
		# spectrum is indexed from 0 at the centre of the eye
		spectrum.insert(0, [y-i, intensity])
		if numpix != 0:
			fin_r, fin_g, fin_b = tot_r/numpix, tot_g/numpix, tot_b/numpix
		else:
			fin_r, fin_g, fin_b = 0, 0, 0
		rgb.insert(0, [fin_r, fin_g, fin_b])
	# get hue from rgb
	H = []
	for colour in rgb:
		hue = get_hue(colour)
		H.append(hue)
	# wave 500nm = 154 degrees hue
	# find the row pertaining to that green
	greenidx = (np.abs(np.asarray(H)-154)).argmin()
	green500 = spectrum[greenidx][0]
	# calibrate each rgb with wavelength using green
	final_spec = calibrate(spectrum, green500)
	return final_spec


# Calls eye_spectrum() for each eye
	# pair = [eye1, eye2]
	# eye1 = [x, y, extL, extR, extT, extB]
def get_spectrum(pair, image):
	eye1, eye2 = pair

	width1, width2 = eye1[3][0]-eye1[2][0], eye2[3][0]-eye2[2][0]
	cen = math.floor( (eye1[0]+eye2[0]) / 2 )

	spec1 = eye_spectrum(eye1, math.floor(eye1[2][0]-width1), cen, image)
	spec2 = eye_spectrum(eye2, cen, math.ceil(eye2[3][0]+width2)+1, image)
	return [spec1, spec2]
