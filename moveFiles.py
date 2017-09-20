"""
A small script to move all text files to a new folder :p
"""
import shutil
import os

source = './'
destination = './corpus'

files = os.listdir(source)

for f in files:
    if f.endswith('.txt'):
        shutil.move(f, destination)