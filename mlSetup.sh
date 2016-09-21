#!/bin/bash

#before this file is run, become root user, cd into directory, following command must be entered:

# to run:
# ./mlSetup.sh

# Update sudo apt-get
sudo apt-get update

###########################################################


# Installing scientific Python
sudo apt-get -y install --fix-missing build-essential python-dev python-numpy python-setuptools python-scipy libatlas-dev
sudo apt-get -y install --fix-missing build-essential python-sklearn
#sudo apt-get -y install --fix-missing build-essential ipython
sudo apt-get -y install python-pip
sudo apt-get -y install libxml2-dev libxslt1-dev  # lxml useful for parsing and python uses its

pip install numpy

# finally got this working! RAM on droplet wasn't enough to compile before. now upgraded.
pip install pandas

# pandas
#sudo apt-get install python-pandas

#pip install beautifulsoup4 html5lib lxml requests, requests_cache urllib2 

sudo apt-get install python-numpy python-scipy python-dev python-pip python-nose g++ libopenblas-dev git
sudo pip install Theano

sudo pip install keras

sudo pip install cython
sudo apt-get install libhdf5-dev
sudo pip install h5py

sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

sudo pip install lmdb
sudo apt-get install libopencv-dev python-opencv




