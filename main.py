# Locates the eyes and extracts data from images, one normal and one with spectrum
# Adds eye to training database with label

from find_eye import *
from find_pairs import *
from get_colour import *
from get_spectrum import *
import argparse
import matplotlib.pyplot as plt
import csv
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the normal image file")
ap.add_argument("-c", "--class", help = "class for training data")
# ap.add_argument("-s", "--splitimage", help = "path to the spectrum image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
orig = image.copy()

# for training data
ID = args["class"]

# find pairs of eyes
contours = find_eye(image)
[con_pairs, pair_det] = find_pairs(image, contours)
num_pairs = len(con_pairs)
fname = os.path.basename(args["image"])
print("------- RESULTS -------")
print("SEARCHED " + str(fname))
print("FOUND " + str(num_pairs) + " PAIR/S")

# set up new databases
# interpupillary distance and colour
fields1 = ['file','ID','distance','hue','r','g','b']
f1 = open("distcolour.csv", 'w')
writer = csv.writer(f1)
writer.writerow(fields1)
f1.close()
# spectrum
fields2 = ['file','ID','L/R']
fields2 = fields2 + list(range(400, 721))
f2 = open("spec.csv", 'w')
writer = csv.writer(f2)
writer.writerow(fields2)
f2.close()

# For each pair
for i in range(0, num_pairs):
	# get eye details for the pair
	con1, con2 = con_pairs[i][0], con_pairs[i][1]
	pair = pair_det[i]
	eye1, eye2 = pair[0], pair[1]

	# interpupillary distance (relative to pupil width)
	w1, w2 = eye1[3][0]-eye1[2][0], eye2[3][0]-eye2[2][0]
	ave_w = (w1+w2) / 2
	dist = math.sqrt((eye2[0]-eye1[0])**2 + (eye2[1]-eye1[1])**2) / ave_w

	# get colour
	col1 = get_colour(orig, eye1[0:2], ave_w/2)
	col2 = get_colour(orig, eye2[0:2], ave_w/2)
	ave_col = ave_eye_colours(col1, col2)
	r,g,b = ave_col
	hue = get_hue(ave_col)
	
	# print results
	print("---------")
	print("NAE Pair " + str(i+1))
	print("Interpupillary distance: " + str(dist))
	print("Colour (hue): " + str(hue))
	print("Colour (RGB): " + str(ave_col))
	
	# add interpupillary distance and colour to database
	f1 = open("distcolour.csv", 'a')
	writer = csv.writer(f1)
	writer.writerow([fname,ID, dist, hue, r, g, b])
	f1.close()

	# get intensity

	# get label

	# get spectrum
	[spec1, spec2] = get_spectrum(pair, orig)

	# graph spectrum
	x1, y1 = zip(*spec1)
	plt.scatter(x1,y1)

	x2, y2 = zip(*spec2)
	plt.figure()
	plt.scatter(x2,y2)
	plt.show()
	print(list(y1))
	# add spectrum to spec database
	f2 = open("spec.csv", 'a')
	writer = csv.writer(f2)
	writer.writerow([fname,ID,'L']+list(y1))
	writer.writerow([fname,ID,'R']+list(y2))
	f2.close()
	#print("Left eye spectrum")
	#print(spec1)
	#print("Right eye spectrum")
	#print(spec2)



"""
for each pair:
	eye1, eye2 = pair[0], pair[1]
	# interpupillary distance (relative to pupil width)
		width = ave(w1, w2)
		dist = euclidean dist (eye1, eye2) / width

	# get colour
		circle around the eye with radius of 1.5 x radius of contour 
		remove pixels that are too white/black
		average RGB of all remaining pixels
		normalise
"""