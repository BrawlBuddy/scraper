#!/bin/bash

# Pull changes from the remote repository
git pull origin main

# update the regional battles
python scraper.py
wait

#create combined.csv
python merge.py
wait

#calculate results
python calc.py
wait

# Add changes to the staging area
git add .

# Commit changes
git commit -m "Update files"

# Push changes to the remote repository
git push origin main
