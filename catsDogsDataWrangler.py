import glob, os, cv2, lmdb, pickle, time
from matplotlib import pyplot
from scipy.misc import toimage
import numpy as np
import shutil

#IMAGE_WIDTH = 227
#IMAGE_HEIGHT = 227
IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100


def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):
    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])
    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)
    return img

files_path = "/home/rudebeans/Desktop/Downloads/train/trainTest/"
#files_path = "/home/rudebeans/Desktop/Downloads/train/"
#files_path = "/home/rudebeans/Downloads/test1"

os.chdir(files_path)

#os.mkdir("trainTrain")
#os.mkdir('trainTest')

allFiles = glob.glob("*.jpg")
print "There are this many files:", len(allFiles)

"""
c = int(len(allFiles)*0.9)
train = allFiles[0:c]
test = allFiles[c:len(allFiles)]
print "there are this many training and testing images: ", len(train), " ", len(test)

for img in test:
	print "moving ", img
	shutil.move(files_path+img, files_path+"trainTest/"+img)
for img in train:
	print "moving ", img
	shutil.move(files_path+img, files_path+"trainTrain/"+img)
"""

f = files_path

chunk = 500
numChunks = len(allFiles) / chunk

def makeDfs():
	for c in range(numChunks):
	#for c in range(5):
		X = []
		Y = []

		currentChunk = allFiles[(c*chunk):(c*chunk+chunk)]

		for i in range(len(currentChunk)):
		#for i in range(700, 1000):

			img_file = currentChunk[i]
			print "got file ", img_file + str(i)
			
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
			else: y = [int(img_file[0:-4])]

			print "appending..."
			X += [x]
			Y += [y]

			print "\n\n"

		X = np.array(X)
		Y = np.array(Y)

		df = [X, Y]

		F = open("df"+str(c)+".txt", 'w')
		pickle.dump(df, F)
		F.close()

def consolidateDfs():
	X = []
	Y = []

	allDfs = glob.glob("df"+"*.txt")

	for g in allDfs:
		f = open(g, 'r')
		df = pickle.load(f)
		x = list(df[0])
		y = list(df[1])

		X += x
		Y += y

		print g

	X = np.array(X)
	Y = np.array(Y)

	df = [X, Y]

	F = open("masterDf.txt", 'w')
	pickle.dump(df, F)
	F.close()


makeDfs()
#consolidateDfs()


"""
for df in glob.glob("df"+"*.txt"):
	print df
	df = pickle.load(open(df, 'r'))
	print len(df[0][0][0])

f = open("masterDf.txt", 'r')
df = pickle.load(f)
X = df[0]
Y = df[1]


print len(X)


for i in range(len(X)):
	print Y[i], "\n\n"
	pyplot.subplot(330 + 1)
	pyplot.imshow(toimage(X[i]))
	# show the plot
	pyplot.show()


# sudo pip install lmdb
# sudo apt-get install libopencv-dev python-opencv
"""