from find_eye import *
from find_pairs import *
import argparse


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

contours = find_eye(image)

[con_pairs, pair_det] = find_pairs(image, contours)

print("Found " + str(len(con_pairs)) + " pair/s")