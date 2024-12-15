#!/bin/bash
cd "$(dirname "$0")"

#check if the virtual environment exists and, if not, creates one
if [ ! -d "/.venv" ]; then    
    python3 -m venv .venv    
fi

#Activate virtual environment
source .venv/bin/activate

#Install dependencies from requirements.txt
pip install -r requirements.txt

# Create generated folder if it doesn't exist 
mkdir -p generated

#Run Scraper
python3 ex1.py generated > generated/report_$(date +%Y-%m-%d).txt

# Return to the original directory
cd -

deactivate
