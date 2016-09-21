import glob, os, cv2, lmdb, pickle, time
from matplotlib import pyplot
from scipy.misc import toimage
import numpy as np
import shutil

#IMAGE_WIDTH = 227
#IMAGE_HEIGHT = 227
IMAGE_WIDTH = 20
IMAGE_HEIGHT = 20

owd = os.getcwd()

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):
    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)
    return img

for f in ["train/trainTrain/", "train/trainTest/", "test1/"]:

	print f
	
	os.chdir(f)

	allFiles = glob.glob("*.jpg")

	dfs = glob.glob("*.txt")

	for df in dfs:
		print df
		os.remove(df)


	"""

	print "%d dfs were removed" % len(dfs)
	print "There are %d image files" % len(allFiles)

	X = []
	Y = []

	for img_file in allFiles:
		print "got file ", img_file
		
		print "reading and transforming..."
		img = cv2.imread(img_file, cv2.IMREAD_COLOR)
		img = transform_img(img)

		R = []
		G = []
		B = []

		print "reorganizing arrays..."
		for h in range(len(img)):
			r = [z[0] for z in img[h]]
			R += [r]

			g = [z[1] for z in img[h]]
			G += [g]

			b = [z[2] for z in img[h]]
			B += [b]

		x = [R, G, B]

		if 'cat' in img_file: y = [0]
		elif 'dog' in img_file: y = [1]
		else: y = [int(img_file[0:-4])] # for use when wrangling test data

		print "appending..."
		X += [x]
		Y += [y]

		print "\n\n"

	X = np.array(X)
	Y = np.array(Y)

	df = [X, Y]

	F = open("masterDf.txt", 'w')
	pickle.dump(df, F)
	F.close()
	"""

	os.chdir(owd)