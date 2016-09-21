from matplotlib import pyplot
from scipy.misc import toimage
import pickle
import numpy, glob
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

# Testing git editing

files_path = "/home/rudebeans/Desktop/Downloads/train/trainTrain/"
#files_path = "/home/rudebeans/Downloads/test1"

seed = 7
numpy.random.seed(seed)

IMAGE_SIZE = 100

allFiles = glob.glob(files_path+"df"+"*.txt")

for img in allFiles:
	print img

for d in range(1,len(allFiles)):

	print "working on %d" %d

	df = pickle.load(open(allFiles[d], 'r'))

	X = df[0]
	y = df[1]

	X_train = X
	y_train = y

	#train = pickle.load(open(files_path+"df1.txt", 'r'))
	#test = pickle.load(open(files_path+"df2.txt", 'r'))

	#X_train, y_train, X_test, y_test = X[0:c], y[0:c], X[c:len(X)], y[c:len(X)]


	def showPics():
		for i in range(0, len(X_train), 50):
			print y_train[i], "\n\n"
			pyplot.subplot(330 + 1)
			pyplot.imshow(toimage(X_train[i]))
			# show the plot
			pyplot.show()
	#showPics()

	# normalize inputs from 0-255 to 0.0-1.0
	X_train = X_train.astype('float32')
	#X_test = X_test.astype('float32')
	X_train = X_train / 255.0
	#X_test = X_test / 255.0


	# one hot encode outputs
	y_train = np_utils.to_categorical(y_train)
	#y_test = np_utils.to_categorical(y_test)
	num_classes = y_train.shape[1]

	epochs = 25
	lrate = 0.01
	decay = lrate/epochs

	if d == 0:
		print "creating model..."
		# Create the model
		model = Sequential()
		model.add(Convolution2D(IMAGE_SIZE, 3, 3, input_shape=(3, IMAGE_SIZE, IMAGE_SIZE), border_mode='same', activation='relu', W_constraint=maxnorm(3)))
		model.add(Dropout(0.2))
		model.add(Convolution2D(IMAGE_SIZE, 3, 3, activation='relu', border_mode='same', W_constraint=maxnorm(3)))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Flatten())
		model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
		model.add(Dropout(0.5))
		model.add(Dense(num_classes, activation='softmax'))
		# Compile model
		
		
		sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
		model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
		print(model.summary())

	else: 
		print "loading model..."
		model = load_model('my_model.h5')

	# Fit the model
	model.fit(X_train, y_train, nb_epoch=epochs, batch_size=30)

	model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
	del model  # deletes the existing model


"""
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))


model = load_model('my_model.h5')
# Fit the model
pred = model.predict_classes(X_test[0:50])
print pred

print y_test[0:50]

sub = pd.DataFrame({"pred":pred, 'actVal':y_test[0:50]})
print sub
"""



