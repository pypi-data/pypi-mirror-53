# dnazip

Compress all your DNA (multi-FASTA) files in my project! It's very easy to use :)

It uses 2 bits per base, couldn't get any more effecient than that!

This algoritm is not enirely lossless, it converts lowercase actg to uppercase ACTG, and also adds newlines in decompression

## Installation
To install it from source:

    git clone https://github.com/Bartvelp/dnazip
    cd dnazip
    pip install .
   