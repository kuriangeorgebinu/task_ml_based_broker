#!/bin/bash

# Set the name of your Python file (without the .py extension)
filename="ml_test.py"
output_file="ml_test.exe"
# Install pyinstaller
pip install pyinstaller
# Create the executable using pyinstaller
pip install scikit-learn
pip install pandas
pip install numpy

pyinstaller "$filename" --noconsole --onefile --distpath distribution --hidden-import "pandas" --hidden-import "numpy" --hidden-import 'sklearn' --hidden-import 'sklearn.metrics.*' --hidden-import 'sklearn.metrics._pairwise_distances_reduction._middle_term_computer' --hidden-import 'sklearn.metrics._pairwise_distances_reduction._datasets_pair'

# Copy the executable to the project directory
cp distribution/"$output_file" "$(dirname "$0")"
