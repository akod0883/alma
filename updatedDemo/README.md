# Alma Munchers - Find the Best Restaurant For You!

## Getting Started

1. Python 3.5 or above
2. pip3
3. Internet Connection

## Description of Files 

`requirements.txt` - This file conatins ALL the python dependencies needed to run the files presented in this repository

`main.py` - starting file ran by 

`app/database.py` - defines functions related to our database. Also codes all the features for our website.

`app/forms.py` - defines all of our flask web forms  

`app/templates/` - this directory contains all the .html files that are used to frontend the pages on our website



## Setup, Install, Run

### Setup

First you must clone a copy of this repository in order to deploy our website
```bash
git clone https://github.com/akod0883/alma.git
cd alma/updatedDemo
```
It is advised that you create a python virtual environment and installing the packages in requirements.txt 


To create a virutal evnironment using venv run the following command in the ***updatedDemo*** directory
```bash
python3 -m venv name_of_virtual_environment
```

To activate the virtual enviornemnt

```bash
source name_of_virtual_environment/bin/activate
```

If this process is done correctly, there should be a (name_of_virtual_environment) next to your username is terminal


### Setting Up GCP
It should be noted that the database should be running on a mySQL server to observe and use all the features created in this repo. For the purposes of CS411 we used a mySQL server hosted on Google Cloud Platform (GCP). If this is something that you are interested in viewing, please contact any of the contributers to this repo, we would be delighted to spin up the server!

Create a `app.yaml` file in the **updatedDemo** with the following content:
```bash
touch app.yaml
```

Within `app.yaml` copy and paste the following information
```yaml
runtime: python38 # or another supported version

instance_class: F1

env_variables:
  MYSQL_USER: <user_name> # please put in your credentials
  MYSQL_PASSWORD: <user_pw> # please put in your credentials
  MYSQL_DB: <database_name> # please put in your credentials
  MYSQL_HOST: <database_ip> # please put in your credentials

handlers:
# Matches requests to /images/... to files in static/images/...
- url: /img
  static_dir: static/img

- url: /script
  static_dir: static/script

- url: /styles
  static_dir: static/styles
```

### Install 

To install all the dependencies for this proejct run the following command in the virtual evironement crated in the Setup step

```bash
python3 -m pip install -r requirements.txt
```

### Run 

To deploy a development server of our website, run the following command in the **updatedDemo** directory

```bash
export FLASK_APP = app
flask run
```

To deploy our website hosted on GCP run the following commands in terminal
Setting up the deployment
```bash
curl https://sdk.cloud.google.com | bash
gcloud components install app-engine-python
gcloud config set project cs411-sp21
gcloud auth login
gcloud app deploy
```


## Authors
**Akhil Kodumuri** - [akod0883](https://github.com/akod0883) 
**Lukas Adomaviciute** - [lukasa3](https://github.com/lukas-adoma) 

