
import os  
def load_data_and_format(file):
	str = ""
	f = open(file, 'r')
	line = f.readline()
	while line:
		str = str + '[' + line[:-1] + '],' + '\n'
		line = f.readline()
	f.close
	return str
	
def list_files (path,extension):
	files = [path + f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
	print ('listfiles() found ' + str(len(files)) + ' ".' + extension + '" files in folder ' + path)
	print (files[0])
	print ('.........')
	print (files[-1])
	return files

if (__name__ == "__main__"):
	
	path = 'Y:/GEM0/'
	
	files = list_files(path,'txt')

	fdest = open(path + "circles.mrg", 'w')

	fdest.write('[')

	for file in files[:-1]:
		fdest.write( load_data_and_format(file) )

	fdest.write(load_data_and_format(files[-1])[:-2] )

	fdest.write(']')

	fdest.close()

