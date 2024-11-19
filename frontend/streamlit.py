#-------------------------------------------------------------------------------------#
# Project Setup & Development Guidelines: Program_and_Chill
#-------------------------------------------------------------------------------------#
# 
# INITIAL SETUP:
# 1. Create virtual environment:    python -m venv venv
# 2. Activate virtual environment:
#    - Windows:                    .\venv\Scripts\activate
#    - Unix/MacOS:                 source venv/bin/activate
# 3. Install requirements:         pip install -r requirements.txt
# 4. Create .env file:            cp .env.example .env
# 5. Update dependencies:          pip freeze > requirements.txt
#
# PYTHON DEVELOPMENT COMMANDS:
# Package Management:
# 1. List outdated packages:      pip list --outdated
# 2. Show package info:           pip show package_name
# 3. Uninstall package:          pip uninstall package_name
# 4. Install dev dependencies:    pip install -r requirements-dev.txt
# 5. Upgrade pip:                python -m pip install --upgrade pip
# 6. Install package:            pip install package_name==version
#
# Virtual Environment:
# 1. List installed packages:     pip list
# 2. Export dependencies:         pip freeze > requirements.txt
# 3. Deactivate venv:            deactivate
# 4. Remove venv:                rm -rf venv
#
# STREAMLIT COMMANDS:
# Development:
# 1. Run app:                     streamlit run app.py
# 2. Run with custom port:        streamlit run app.py --server.port 8502
# 3. Enable debug mode:           streamlit run app.py --logger.level=debug
# 4. Clear cache:                 streamlit cache clear
# 5. Show all config options:     streamlit config show
# 6. Create new component:        streamlit create my_component
#
# GIT COMMANDS:
# Basic Operations:
# 1. Initialize repository:        git init
# 2. Add files to staging:        git add .
# 3. Commit changes:              git commit -m "your message"
# 4. Push to remote:              git push -u origin branch-name
# 5. Pull latest changes:         git pull origin branch-name
# 
# Branching:
# 1. Create & switch branch:      git checkout -b branch-name
# 2. Switch branches:             git checkout branch-name
# 3. List branches:               git branch
# 4. Delete branch:               git branch -d branch-name
# 5. Merge branch:                git merge branch-name
#
# Advanced Operations:
# 1. Fetch updates:               git fetch origin
# 2. Rebase branch:               git rebase main
# 3. Cherry-pick commit:          git cherry-pick commit-hash
# 4. Reset to commit:             git reset --hard commit-hash
# 5. Clean untracked files:       git clean -fd
#
#-------------------------------------------------------------------------------------#
#----------# IMPORTS  #----------#
import os
import sys
import logging
import datetime
import streamlit as st
import requests
import json
import pandas as pd
import numpy as np

from dotenv import load_dotenv

#-------------------------------------------------------------------------------------#
#----------# CONFIG  #----------#
load_dotenv()
API_KEY = os.getenv("API_KEY")

#-------------------------------------------------------------------------------------#