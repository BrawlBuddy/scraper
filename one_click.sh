#!/bin/bash

# Pull changes from the remote repository
git pull origin main

# Run the first Python file
python first_file.py

# Wait until the first Python file finishes
wait

# Run the second Python file
python second_file.py

# Wait until the second Python file finishes
wait

# Add changes to the staging area
git add .

# Commit changes
git commit -m "Update files"

# Push changes to the remote repository
git push origin main
