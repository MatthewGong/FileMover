import getch
import shutil
import os
import argparse
import hyperspy.api as hs
from matplotlib import pyplot as plt
from collections import OrderedDict

VALID_CHAR = ['1','2','3','4','5','6','7','8','9','q', ' ','0']
INPUT_MAP  = [ 1,2,3,4,5,6,7,8,9]
VALID_MODE = ['load', 'Load', 'copy', 'Copy', 'move', 'Move']
DEFAULT_SUBFOLDERS = ['Dispersoid', 'Interface', 'Polycrystal', 'Single Phase', 'Atomic-Images',]
VERBOSITY = 5
NOIMAGE = plt.imread("No_image_available.png")


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str,
            dest='type', help='file type/s',
            metavar='TYPE', required=True, nargs="+")
    parser.add_argument('--input',type=str,
	    	dest='input', help='input path (default %(default)s',
	    	metavar='INPUT', default=os.getcwd())
    parser.add_argument('--output',type=str,
            dest='output', help='output path (default %(default)s',
            metavar='OUTPUT', default=os.getcwd())
    parser.add_argument('--mode', type=str,
    		dest='mode', help='copy, or move (default %(default)s)',
    		metavar= 'MODE', default="copy")
    parser.add_argument('--subfolders', type=str,
    		dest='folders', help='The subfolders you want to sort to',
    		metavar= 'FOLDERS', nargs="*")
    parser.add_argument('--load', type=str,
    		dest='load', help='file to load list of files from (default %(default)s)',
    		metavar= 'LOAD', default=None)
    parser.add_argument('--save_output', type=str,
    		dest='save_output', help=' (default %(default)s)',
    		metavar= 'SAVE', default="ImageNames.txt")
    parser.set_defaults()
    return parser
    
def ODprint(OrdDict):
	"""
	Creates a nice output for printing ordered dictionaries
	"""
	string = "{"
	for key in OrdDict:
		string += "({} : {}".format(key, OrdDict[key])
		string += "), "
	string = string[:-2] + "}"
	return string

def transfer(destination, subfolder, origin, name, mode):
	"""
	Move or copy the data files to desired destination folder/subfolders
	"""

	# If it's an EMI file we have to move the .SER files as well
	# Find the associated SER files and move them as well
	if name.endswith("emi"):
		#print origin, name
		directory = origin[:-len(name)]
		#print directory, "directory"
		arr = os.listdir(directory)
		#print arr
		ser_files = [x for x in arr if name[:-4] in x and x != name]
		#print ser_files
		for file in ser_files:
			transfer(destination, subfolder, directory+file, file, mode)
			#print "I was going to try and transer", directory+file,   file


	dest = os.path.join(destination, subfolder, name)
	try:
		if mode=='copy':
			shutil.copy(origin, dest)
		elif mode=='move':
			shutil.move(origin, dest)
	except:
		print "An error occured while moving your file. Check your output folder"


def openproperly(image):
	"""
	Determines how best to open and display the immage
	"""
	print image
	s = hs.load(image)

	if image.endswith('dm3'):
		
		try:
			plt.imshow(s.data)
		except:
			plt.imshow(NOIMAGE)
			print "No image to display, check that this file contains an image file"

	elif image.endswith('emi'):
		if type(s) == list:
			for item in s:
				item.plot()
		else:
			s.plot()

	elif image.endswith('ser'):
		s.plot() 
	elif image.endswith('EMSA'):
		s.plot()

	else:
		s.plot()

	plt.show(block=False)
	raw_input("press Enter")
	plt.close('all')


def save_files(dest, images):
	"""
	Save the unprocessed images for later processing
	"""
	file = open(dest, 'w')

	for image in images:
		line = images[image] + ', ' + image + '\n'
		file.write(line)

	file.close()

def create_subfolders(dest, SUBFOLDERS):
	"""
	Create destination subfolders for the images to be moved into
	"""
	if not os.path.isdir(dest):
		os.makedirs(dest)
		print "WARNING: The chosen output directory did not exist."

	for folder in SUBFOLDERS:
		path = os.path.join(dest,folder)
		try:
			os.mkdir(path)
		except:
			pass

def main():
	parser = build_parser()
	options = parser.parse_args()
	
	COUNTER = 0
	MODE = options.mode
	DATA_PATH = options.input
	TARGET_PATH = options.output
	SUBFOLDERS = DEFAULT_SUBFOLDERS if options.folders == None else options.folders
	#print SUBFOLDERS, "SUBFOLDERS"

	# Create and 
	KEY_MAP = SUBFOLDERS + SUBFOLDERS[:9-len(SUBFOLDERS)]
	I_MAP = [key%len(SUBFOLDERS) if key%len(SUBFOLDERS) != 0 else len(SUBFOLDERS)  for key in INPUT_MAP]
	#print I_MAP
	INPUTS = OrderedDict(zip(KEY_MAP, I_MAP))
	
	INPUTS["pass"] = "0, ' '" 
	INPUTS["Save/Quit"] = "q" 

	# Check for Valid inputs
	if MODE not in VALID_MODE:
		raise ValueError("You have chosen an invalid mode ({}). Please choose move or copy.".format(MODE))

	# Set up image dictionaries
	images = {}

	if options.load is not None:
		"""
		Loads up a list of files to be moved
		"""
		LOAD_PATH = options.load

		# construct the dictionaries from the chosen file at LOAD_PATH
		with open(LOAD_PATH, 'r') as f:
			for line in f:
				splitLine = line.strip('\n').split(", ")
				images[splitLine[1]] = splitLine[0]
				
	else:
		"""
		Builds the list of files with the specified file type
		from a chosen directory
		"""
		for root, directories, filenames in os.walk(DATA_PATH):
			for f in filenames:
				for ftype in options.type:
					if f.endswith(ftype):
						string = os.path.join(root, f)
						images[string] = f

					
	
	create_subfolders(TARGET_PATH,SUBFOLDERS)
	
	for image in images.keys():
		
		# print the key options only every so often
		if COUNTER%VERBOSITY == 0:
			print ODprint(INPUTS)
		COUNTER += 1

		#determines the best way to load and display the image
		openproperly(image)

		char = getch.getch()
		while char not in VALID_CHAR:
			char = getch.getch()
		
		print char

		if char=='1':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[0]-1],image, images[image], MODE)
		elif char=='2':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[1]-1],image, images[image], MODE)
		elif char=='3':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[2]-1],image, images[image], MODE)
		elif char=='4':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[3]-1],image, images[image], MODE)
		elif char=='5':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[4]-1],image, images[image], MODE)
		elif char=='6':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[5]-1],image, images[image], MODE)
		elif char=='7':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[6]-1],image, images[image], MODE)
		elif char=='8':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[7]-1],image, images[image], MODE)
		elif char=='9':
			transfer(TARGET_PATH,SUBFOLDERS[I_MAP[8]-1],image, images[image], MODE)
		elif char=='q':
			save_files(options.save_output,images)
			break
		elif char == ' ' or '0':
			pass

		images.pop(image, None)

		save_files(options.save_output, images)


if __name__ == '__main__':
	main()