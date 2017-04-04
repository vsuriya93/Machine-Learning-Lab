import os
from prog import load_details

names,assignments=load_details("names","assignments")

for x in names:
	os.mkdir('uploads/'+x)
	for key in assignments:
		path='uploads/'+x+'/'+key
		os.mkdir(path)
