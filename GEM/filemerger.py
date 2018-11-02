from pathlib import Path
 
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
	p = Path(path)
	list( p.glob('**/*.txt'))

if (__name__ == "__main__"):

	list_files('.','txt')

	fdest = open("circles_merge.txt", 'w')

	fdest.write('[')

	fdest.write(load_data_and_format("Circles_0_0.txt"))

	fdest.write(load_data_and_format("Circles_1701_0.txt"))

	fdest.write(load_data_and_format("Circles_3376_11.txt"))

	fdest.write(load_data_and_format("Circles_5077_64.txt"))

	fdest.write(load_data_and_format("Circles_6779_121.txt"))

	fdest.write(load_data_and_format("Circles_8480_167.txt")[:-2])

	fdest.write(']')

	fdest.close()

