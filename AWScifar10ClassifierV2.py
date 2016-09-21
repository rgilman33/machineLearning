
"""
sudo apt-get install python-numpy python-scipy python-dev python-pip python-nose g++ libopenblas-dev git
sudo pip install Theano

sudo pip install keras

sudo pip install cython
sudo apt-get install libhdf5-dev
sudo pip install h5py

"""
# Plot ad hoc CIFAR10 instances
from keras.datasets import cifar10
from matplotlib import pyplot
from scipy.misc import toimage
import pickle
import numpy
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

df = cifar10.load_data()

seed = 7
numpy.random.seed(seed)
#df.to_pickle("cifar10.txt")

(X_train, y_train), (X_test, y_test) = df


# normalize inputs from 0-255 to 0.0-1.0
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, 32, 32), activation='relu', border_mode='same'))
#model.add(Dropout(0.2))
model.add(Convolution2D(96, 3, 3, activation='relu', border_mode='same'))
model.add(Convolution2D(96, 3, 3, activation='relu', border_mode='same'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Convolution2D(192, 3, 3, activation='relu', border_mode='same'))
model.add(Convolution2D(192, 3, 3, activation='relu', border_mode='same'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Convolution2D(192, 3, 3, activation='relu', border_mode='same'))
model.add(Convolution2D(192, 1, 1, activation='relu', border_mode='same'))
model.add(Convolution2D(10, 1, 1, activation='relu', border_mode='same'))
"""
model.add(Convolution2D(64, 3, 3, activation='relu', border_mode='same'))
model.add(Dropout(0.2))
model.add(Convolution2D(64, 3, 3, activation='relu', border_mode='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(128, 3, 3, activation='relu', border_mode='same'))
model.add(Dropout(0.2))
model.add(Convolution2D(128, 3, 3, activation='relu', border_mode='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu', W_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
model.add(Dropout(0.2))
"""
model.add(Dense(num_classes, activation='softmax'))
# Compile model
epochs = 250
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())

# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=epochs, batch_size=64)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

model.save('cifar10_modelV2.h5')  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model

# returns a compiled model
# identical to the previous one
"""
model = load_model('my_model.h5')
print model

"""
