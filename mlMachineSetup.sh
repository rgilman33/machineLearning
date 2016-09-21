# before this file is run, become root user, cd into directory, following command must be entered:

# to run:
# ./droplet_setup.sh

# Update sudo apt-get
sudo apt-get update

###########################################################

# postgres
#See http://tecadmin.net/install-postgresql-server-on-ubuntu/#
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -

sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

sudo apt-get install python-pip python-dev libpq-dev nginx

# Installing scientific Python
sudo apt-get -y install --fix-missing build-essential python-dev python-numpy python-setuptools python-scipy libatlas-dev
sudo apt-get -y install --fix-missing build-essential python-sklearn
#sudo apt-get -y install --fix-missing build-essential ipython
sudo apt-get -y install python-pip
sudo apt-get -y install libxml2-dev libxslt1-dev  # lxml useful for parsing and python uses its

# django (use pip, apt-get finds older version)
pip install django

#other
pip install psycopg2

pip install numpy

# finally got this working! RAM on droplet wasn't enough to compile before. now upgraded.
pip install pandas

# pandas
#sudo apt-get install python-pandas

#pip install beautifulsoup4 html5lib lxml requests, requests_cache urllib2 

# strava
pip install stravalib

pip install geopy

pip install supervisor

pip install upstart

# Installing other Python packages.
pip install virtualenv

apt-get install gunicorn

apt-get install nginx




