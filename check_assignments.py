import os
name='Assignment-'+raw_input('Enter Assignment Number: ')
for x in os.listdir('uploads/'):
	path='uploads/'+x+'/'
	print os.listdir(path+name),x
