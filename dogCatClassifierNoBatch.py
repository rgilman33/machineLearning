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


trainTest_files_path = "train/trainTest/"
trainTrain_files_path = "train/trainTrain/"

seed = 7
numpy.random.seed(seed)

df_test = pickle.load(open(trainTest_files_path+"masterDf.txt", 'r'))
df_train = pickle.load(open(trainTrain_files_path+"masterDf.txt", 'r'))

IMAGE_SIZE = len(df_test[0][0][0])

X_train= df_train[0]
y_train = df_train[1]

X_test= df_test[0]
y_test = df_test[1]

print len(X_train)
print len (X_test)

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
y_test = np_utils.to_categorical(y_test)
num_classes = y_train.shape[1]

epochs = 2
lrate = 0.01
decay = lrate/epochs

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
epochs = 2
lrate = 0.02
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())

# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=epochs, batch_size=IMAGE_SIZE)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))


model.save('my_model_catsDogs.h5')  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model





"""
model = load_model('my_model.h5')
# Fit the model
pred = model.predict_classes(X_test[0:50])
print pred

print y_test[0:50]

sub = pd.DataFrame({"pred":pred, 'actVal':y_test[0:50]})
print sub
"""



