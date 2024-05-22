#!/bin/bash

## Used to create fresh environment ##

# Can freeze the reqirements of the environment
# pip freeze > requirements.txt

# Remove the virtual environment
rm -rf venvl

# List the packages installed
pip list

# Create virtual environemnt
virtualenv -v venv

# Create the bin for the environment
source venv/bin/activate

# Install the reqirements in the txt file
pip install -r requirements.txt

# List the packages installed
pip list