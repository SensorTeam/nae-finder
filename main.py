from find_eye import *
from find_pairs import *
from get_colour import *
import argparse


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
orig = image.copy()
contours = find_eye(image)

[con_pairs, pair_det] = find_pairs(image, contours)
num_pairs = len(con_pairs)
print("Found " + str(num_pairs) + " pair/s")

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

	print("---------")
	print("NAE Pair " + str(i+1))
	print("Interpupillary distance: " + str(dist))
	print("Colour (RGB): " + str(ave_col))



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