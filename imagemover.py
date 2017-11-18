import getch
import shutil
import os
import argparse
import hyperspy.api as hs
from matplotlib import pyplot as plt


VALID_CHAR = ['1','2','3','4','5','6','7','8','9','q', ' ','0']
VALID_MODE = ['load', 'Load', 'copy', 'Copy', 'move', 'Move']
SUBFOLDERS = ['Dispersoid', 'Interface', 'Polycrystal', 'Single Phase', 'Atomic-Images',]


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str,
            dest='type', help='file type',
            metavar='TYPE', required=True)
    parser.add_argument('--input',type=str,
	    	dest='input', help='input path (default %(default)s',
	    	metavar='INPUT', default=os.getcwd())
    parser.add_argument('--output',type=str,
            dest='output', help='output path (default %(default)s',
            metavar='OUTPUT', default=os.getcwd())
    parser.add_argument('--mode', type=str,
    		dest='mode', help='copy, or move (default %(default)s)',
    		metavar= 'MODE', default="copy")
    parser.add_argument('--load', type=str,
    		dest='load', help='file to load list of files from (default %(default)s)',
    		metavar= 'LOAD', default=None)
    parser.add_argument('--save_output', type=str,
    		dest='save_output', help=' (default %(default)s)',
    		metavar= 'SAVE', default="ImageNames.txt")
    parser.set_defaults()
    return parser
    

def transfer(destination, subfolder, origin, name, mode):
	"""
	Move or copy the data files to desired destination folder/subfolders
	"""
	dest = os.path.join(destination, subfolder, name)
	try:
		if mode=='copy':
			shutil.copy(origin, dest)
		elif mode=='move':
			shutil.move(origin, dest)
	except:
		print "A file with the same name already exists at the destination"



def save_files(dest, images):
	"""
	Save the unprocessed images for later processing
	"""
	file = open(dest, 'w')

	for image in images:
		line = images[image] + ' ' + image + '\n'
		file.write(line)

	file.close()

def create_subfolders(dest):
	for folder in SUBFOLDERS:
		path = os.path.join(dest,folder)
		try:
			os.mkdir(path)
		except:
			pass

def main():
	parser = build_parser()
	options = parser.parse_args()
	

	MODE = options.mode
	DATA_PATH = options.input
	TARGET_PATH = options.output

	if MODE not in VALID_MODE:
		raise ValueError("You have chosen an invalid mode ({}). Please choose move or copy.".format(MODE))

	images = {}

	if options.load is not None:
		"""
		Loads up a list of files to be moved
		"""
		LOAD_PATH = options.load

		with open(LOAD_PATH, 'r') as f:
			for line in f:
				splitLine = line.split()
				images[splitLine[1]] = splitLine[0]
		
	else:
		"""
		Builds the list of files with the chosen file types
		from a chosen directory
		"""
		for root, directories, filenames in os.walk(DATA_PATH):
			for f in filenames:
				if f.endswith(options.type):
					print f
					string = os.path.join(root, f)
					images[string] = f
					
	
	create_subfolders(TARGET_PATH)
	
	for image in images.keys():

		if options.type == "dm3" or options.type == ".dm3":
			
			s = hs.load(image)
			s.metadata
			plt.imshow(s.data)
			plt.show()
			
		else:
			temp = plt.imread(image)
			plt.imshow(temp)
			plt.show()
		
		char = getch.getche()
		while char not in VALID_CHAR:
			char = getch.getche()
		
		print char
		if char=='1':
			transfer(TARGET_PATH,SUBFOLDERS[0%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='2':
			transfer(TARGET_PATH,SUBFOLDERS[1%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='3':
			transfer(TARGET_PATH,SUBFOLDERS[2%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='4':
			transfer(TARGET_PATH,SUBFOLDERS[3%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='5':
			transfer(TARGET_PATH,SUBFOLDERS[4%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='6':
			transfer(TARGET_PATH,SUBFOLDERS[5%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='7':
			transfer(TARGET_PATH,SUBFOLDERS[6%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='8':
			transfer(TARGET_PATH,SUBFOLDERS[7%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='9':
			transfer(TARGET_PATH,SUBFOLDERS[8%len(SUBFOLDERS)],image, images[image], MODE)
		elif char=='q':
			save_files(options.save_output,images)
			break
		elif char == ' ' or '0':
			pass

		images.pop(image, None)

	save_files(options.save_output, images)


if __name__ == '__main__':
	main()