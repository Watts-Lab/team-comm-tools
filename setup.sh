#!/bin/bash

# Step 1: Install required packages
echo "Installing required packages from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install packages from requirements.txt."
    exit 1
fi

# Step 2: Install the spaCy model
echo "Installing SpaCy model..."
python -m spacy download en_core_web_sm
if [ $? -ne 0 ]; then
    echo "Failed to install spaCy model."
    exit 1
fi

# Step 3: Run the import_nltk.py script
echo "Running import_nltk.py..."
python src/team_comm_tools/utils/import_nltk.py
if [ $? -ne 0 ]; then
    echo "Failed to run import_nltk.py."
    exit 1
fi

echo "Installation and requirements check completed successfully."