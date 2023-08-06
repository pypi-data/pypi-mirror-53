
# dnazip

Compress all your DNA (multi-FASTA) files in my project! It's very easy to use :)

It uses 2 bits per base, couldn't get any more efficient than that!

This algorithm is not entirely lossless, it converts lowercase actg to uppercase ACTG, and also adds newlines in decompression.

## Installation

Install it using pip

	$ pip install dnazip
	$ dnazip -h
	usage: dnazip [-h] [-l LINELENGTH] [-d] [-c] [--debug] [FILE]

	Compress FASTA files, using 2 bits per base. If no input file is given, standard input is used

	positional arguments:
	  FILE                  Input file name

	optional arguments:
	  -h, --help            show this help message and exit
	  -l LINELENGTH, --linelength LINELENGTH
	                        Characters per line
	  -d, --decompress      Decompress file
	  -c, --stdout          Write to standard output
	  --debug               Show debugging statements
Or to install it from source:

	$ git clone https://github.com/Bartvelp/dnazip
	$ cd dnazip
	$ pip install .

## Testing

To run the tests run:

	$ cd dnazip
	$ python tests.py
