Welcome to imagemover.py!

This a utility to help classify and sort training image datasets for use in Machine Learning applications. It is currently only capable of processing image/data files that can be opened
using the Hyperspy library. This program relies on several packages that are not included in 
the Python Standard library. We have included links to installation instructions for each of
these librarys below.

The utility will locate all images of chosen types and open them sequentially show to the user
and allow them to move them a target folder with minimal keystrokes. Images will appear on
screen one at a time and the user will be prompted on which folder to send the image to.

Dependencies:
	Hyperspy
		http://hyperspy.org/hyperspy-doc/dev/user_guide/install.html
	Getch
		https://github.com/joeyespo/py-getch 
		https://pypi.python.org/pypi/py-getch/
	Matplotlib
		https://matplotlib.org/users/installing.html		



All arguments are passed in via command line with the following format

--OPTION ARG ARG*...etc

Some options take a single input and some can handle multiple inputs(like file types). Detailed explanations of each option are listed after common examples.


Common examples:

	python imagemover.py --type jpg --input /Unsorted_Data --output /Sorted_Data 

	python imagemover.py --type png emi dm3 --load PreviousBatch.txt --output /Sorted_Data


Options

--type
	
	The types of files that will be searched for.
	
	Takes an unlimited number of arguments, has no default and is required.

	Examples:

		--type jpg
		--type jpg dm3 emi

--input

	The path for the file tree to pull data from. The format of the path is OS specific
	
	Takes a single argument, defaults to the current directory.

	Examples:

		--input /home/usr/Data
		--input C:\user\Data

--output

	The path for the directory to move the data to. The format of the path is OS specific.
	It is recommended to put your output directory in a different location than your input. Otherwise files may be duplicated.

	Takes a single argument, defaults to the current directory. 

	Examples:

		--input /home/usr/Data --output hom/usr/Organized_Data
		--input C:\user\Data --output C:\user\Organized_Data


--mode

	The method to control how files are moved. There are two supported options: Move and Copy.
	Copy creates a duplicate of the file at the chosen destination and leaves the original file in place. Move places the original file in the chosen output folder and removes the original.

	Takes a single argument, defaults to copy.

	Examples:

		--mode copy
		--mode move


--subfolders
	
	Choose which subfolders to create and store data in. 

	Takes up to 9 arguments, defaults to 'Dispersoid', 'Interface', 'Polycrystal', 'Single Phase', 'Atomic-Images'.

	Examples:

		--subfolders dog cat rabbit
		--subfolders Brightfield Darkfield


--load
	
	Load a list of file names from a path instead of searching a directory.

	Takes up to one argument, defaults to None.

	Examples:

		--load ImageNames.txt
		--load /home/usr/FileMove/batch2.txt

--save_output

	Save a list of file names to a chosen file. This happens automatically when a session is ends early.

	Takes up to one argument, defaults to ImageNames.txt

	Examples:

		--save_output processing_batch_5
		--save_output /home/usr/Data/ImageNames.txt


