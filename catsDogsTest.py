from matplotlib import pyplot
from scipy.misc import toimage
import pickle
import numpy as np, glob
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
# load data


files_path = "/home/rudebeans/Desktop/Downloads/train/trainTrain/"
#files_path = "/home/rudebeans/Downloads/test1"

seed = 7
np.random.seed(seed)

IMAGE_SIZE = 100

print "loading model..."
model = load_model('my_model.h5')

allFiles = glob.glob(files_path+"df"+"*.txt")

for img in allFiles:
	print img

for d in range(20, len(allFiles)):

	print "working on ", allFiles[d]

	df = pickle.load(open(allFiles[d], 'r'))

	X = df[0]
	y = df[1]

	X_test = X
	y_test = y


	def showPics():
		for i in range(0, len(X_test), 50):
			print y_test[i], "\n\n"
			pyplot.subplot(330 + 1)
			pyplot.imshow(toimage(X_test[i]))
			# show the plot
			pyplot.show()
	#showPics()

	# normalize inputs from 0-255 to 0.0-1.0
	X_test = X_test.astype('float32')
	#X_test = X_test.astype('float32')
	X_test = X_test / 255.0
	#X_test = X_test / 255.0

	# one hot encode outputs
	y_test = np_utils.to_categorical(y_test)

	print "evaluating model..."
	# Final evaluation of the model
	scores = model.evaluate(X_test, y_test, verbose=0)
	print("Accuracy: %.2f%%" % (scores[1]*100))
	
	"""
	pred = model.predict_classes(X_test[0:50])
	sub = pd.DataFrame({"pred":pred, 'actVal': [p[0] for p in y[0:50]]})
	print sub 

	acc = 1.0 - float(np.sum(np.absolute(sub.pred - sub.actVal))) / float(len(sub))
	print "measured acc at ", acc
	"""




