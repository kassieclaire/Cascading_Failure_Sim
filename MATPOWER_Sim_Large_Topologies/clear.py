import os
import sys
from os import listdir
from os.path import isfile, join
os.chdir(os.path.dirname(sys.argv[0])) #change current directory to the directory of this script
onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))] #get only the files in this directory into a list
#print(onlyfiles)
files_to_delete = [x for x in onlyfiles if x.startswith('temp_')]
print(files_to_delete)
for file in files_to_delete:
    os.remove(file)